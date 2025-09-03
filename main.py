from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles  # Not needed
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import asyncio
import requests
import os
from dotenv import load_dotenv
from github import Github
import aiofiles
from pathlib import Path

# Import configuration
from config import config

app = FastAPI(title="Smart Chatbot", version="1.0.0")

# Mount static files (commented out - not needed for this chatbot)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# GitHub client
github_client = None
if config.is_github_enabled():
    github_client = Github(config.GITHUB_TOKEN)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "chat":
                response = await process_chat_message(message_data["message"])
                await manager.send_personal_message(
                    json.dumps({
                        "type": "response",
                        "content": response,
                        "timestamp": message_data.get("timestamp")
                    }), 
                    websocket
                )
            elif message_data["type"] == "github_connect":
                response = await connect_github_repo(message_data["repo_url"])
                await manager.send_personal_message(
                    json.dumps({
                        "type": "github_status",
                        "content": response
                    }), 
                    websocket
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def process_chat_message(message: str) -> str:
    """Process chat message using Ollama"""
    try:
        # Check if Ollama is running
        response = requests.get(f"{config.get_ollama_url('api/tags')}", timeout=5)
        if response.status_code != 200:
            return "❌ Error: Ollama no está ejecutándose. Por favor, inicia Ollama primero."
        
        # Get available models
        models_response = requests.get(f"{config.get_ollama_url('api/tags')}")
        if models_response.status_code == 200:
            models = models_response.json().get("models", [])
            if not models:
                return "❌ Error: No hay modelos disponibles en Ollama. Por favor, descarga un modelo primero."
            
            # Use phi3 if available, otherwise first available model
            phi3_model = None
            for model in models:
                if "phi3" in model["name"]:
                    phi3_model = model["name"]
                    break
            
            if phi3_model:
                model_name = phi3_model
            else:
                model_name = models[0]["name"]
        else:
            return "❌ Error: No se pudieron obtener los modelos de Ollama."
        
        # Send message to Ollama
        ollama_data = {
            "model": model_name,
            "prompt": f"{config.get_model_selection_prompt()}\n\nUsuario: {message}",
            "stream": False
        }
        
        ollama_response = requests.post(
            f"{config.get_ollama_url('api/generate')}",
            json=ollama_data,
            timeout=config.OLLAMA_TIMEOUT
        )
        
        if ollama_response.status_code == 200:
            response_data = ollama_response.json()
            return response_data.get("response", "No se pudo generar una respuesta.")
        else:
            return f"❌ Error al comunicarse con Ollama: {ollama_response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"❌ Error de conexión con Ollama: {str(e)}"
    except Exception as e:
        return f"❌ Error inesperado: {str(e)}"

async def connect_github_repo(repo_url: str) -> str:
    """Connect to GitHub repository and analyze code"""
    try:
        if not github_client:
            return "❌ Error: Token de GitHub no configurado. Por favor, configura GITHUB_TOKEN en el archivo .env"
        
        # Extract username and repository from URL
        if "github.com" in repo_url:
            parts = repo_url.split("github.com/")[-1].split("/")
            if len(parts) >= 2:
                username = parts[0]
                repo_name = parts[1].replace(".git", "")
            else:
                return "❌ Error: URL de GitHub inválida"
        else:
            return "❌ Error: URL de GitHub inválida"
        
        # Get repository
        repo = github_client.get_repo(f"{username}/{repo_name}")
        
        # Get repository information
        repo_info = {
            "name": repo.name,
            "description": repo.description or "Sin descripción",
            "language": repo.language or "No especificado",
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "size": repo.size,
            "default_branch": repo.default_branch
        }
        
        # Get main files
        contents = repo.get_contents("")
        files = []
        for content in contents[:10]:  # Limit to first 10 files
            if content.type == "file":
                files.append({
                    "name": content.name,
                    "path": content.path,
                    "size": content.size
                })
        
        response = f"✅ Conectado exitosamente al repositorio: {repo.name}\n\n"
        response += f"📊 Información del repositorio:\n"
        response += f"• Descripción: {repo_info['description']}\n"
        response += f"• Lenguaje principal: {repo_info['language']}\n"
        response += f"• Estrellas: {repo_info['stars']}\n"
        response += f"• Forks: {repo_info['forks']}\n"
        response += f"• Rama principal: {repo_info['default_branch']}\n\n"
        response += f"📁 Archivos principales:\n"
        for file in files:
            response += f"• {file['name']} ({file['size']} bytes)\n"
        
        return response
        
    except Exception as e:
        return f"❌ Error al conectar con GitHub: {str(e)}"

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check Ollama
        ollama_status = "✅ Conectado" if requests.get(f"{config.get_ollama_url('api/tags')}", timeout=5).status_code == 200 else "❌ Desconectado"
        
        # Check GitHub
        github_status = "✅ Conectado" if config.is_github_enabled() else "❌ No configurado"
        
        return {
            "status": "healthy",
            "ollama": ollama_status,
            "github": github_status,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    # Validate configuration
    errors = config.validate()
    if errors:
        print("❌ Errores de configuración:")
        for error in errors:
            print(f"  - {error}")
        exit(1)
    
    print("🚀 Iniciando Smart Chatbot...")
    print(f"📍 Servidor: http://{config.HOST}:{config.PORT}")
    print(f"🧠 Ollama: {config.OLLAMA_BASE_URL}")
    print(f"🔗 GitHub: {'✅ Habilitado' if config.is_github_enabled() else '❌ Deshabilitado'}")
    print("=" * 50)
    
    uvicorn.run(app, host=config.HOST, port=config.PORT)
