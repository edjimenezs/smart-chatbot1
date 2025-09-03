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

# GitHub client and active repository
github_client = None
active_repo = None
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
                # Send initial response to indicate processing
                await manager.send_personal_message(
                    json.dumps({
                        "type": "response_start",
                        "content": "🤔 Procesando tu mensaje..."
                    }), 
                    websocket
                )
                
                # Process message with streaming
                await process_chat_message_streaming(message_data["message"], websocket)
                
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
    """Process chat message using Ollama with GitHub context"""
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
        
        # Check if user is asking about specific files or code
        github_context = ""
        keywords = [
            "archivo", "file", "código", "code", "función", "function", 
            "main.py", "config.py", "requirements.txt", "index.html",
            "analiza", "analyze", "revisa", "review", "explica", "explain",
            "qué hace", "what does", "cómo funciona", "how does", "error", "bug"
        ]
        
        print(f"🔍 DEBUG: Mensaje del usuario: '{message}'")
        print(f"🔍 DEBUG: Palabras clave detectadas: {[k for k in keywords if k in message.lower()]}")
        
        if any(keyword in message.lower() for keyword in keywords):
            print("🔍 DEBUG: Palabras clave detectadas, obteniendo contexto de GitHub...")
            github_context = await get_github_context(message)
            print(f"🔍 DEBUG: Contexto obtenido: {'SÍ' if github_context else 'NO'}")
        else:
            print("🔍 DEBUG: No se detectaron palabras clave, usando chat normal")
        
        # Prepare prompt with GitHub context if available
        if github_context:
            prompt = f"{config.get_model_selection_prompt()}\n\nContexto del repositorio:\n{github_context}\n\nUsuario: {message}"
            print(f"🔍 DEBUG: Prompt con contexto de GitHub, longitud: {len(prompt)} caracteres")
        else:
            prompt = f"{config.get_model_selection_prompt()}\n\nUsuario: {message}"
            print(f"🔍 DEBUG: Prompt sin contexto, longitud: {len(prompt)} caracteres")
        
        # Send message to Ollama
        ollama_data = {
            "model": model_name,
            "prompt": prompt,
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

async def get_github_context(message: str) -> str:
    """Get relevant GitHub context based on user message"""
    try:
        print(f"🔍 DEBUG: get_github_context llamado con mensaje: {message}")
        
        if not github_client:
            print("❌ DEBUG: No hay github_client")
            return ""
        
        # Try to get the connected repository
        global active_repo
        print(f"🔍 DEBUG: active_repo actual: {active_repo}")
        
        if not active_repo:
            print("🔍 DEBUG: No hay active_repo, intentando obtener el primero...")
            try:
                # Get the first repository from the user's account
                user = github_client.get_user()
                repos = user.get_repos()
                if not repos:
                    print("❌ DEBUG: No se encontraron repositorios")
                    return ""
                
                # Use the first repository (usually the main one)
                active_repo = repos[0]
                print(f"✅ DEBUG: Repositorio activo establecido: {active_repo.name}")
            except Exception as e:
                print(f"❌ DEBUG: Error obteniendo repositorio: {str(e)}")
                return ""
        
        repo = active_repo
        print(f"🔍 DEBUG: Usando repositorio: {repo.name}")
        
        # Extract file names from the message
        files_to_read = []
        message_lower = message.lower()
        
        # Check for specific file mentions
        if "main.py" in message_lower:
            files_to_read.append("main.py")
        if "config.py" in message_lower:
            files_to_read.append("config.py")
        if "requirements.txt" in message_lower:
            files_to_read.append("requirements.txt")
        if "index.html" in message_lower:
            files_to_read.append("templates/index.html")
        
        # If no specific files mentioned, read main.py by default
        if not files_to_read:
            files_to_read.append("main.py")
        
        # Read file contents
        context = f"Repositorio: {repo.name}\n"
        context += f"Archivos relevantes:\n\n"
        
        print(f"🔍 DEBUG: Intentando leer archivos: {files_to_read}")
        
        for file_path in files_to_read:
            try:
                print(f"🔍 DEBUG: Leyendo archivo: {file_path}")
                contents = repo.get_contents(file_path)
                if contents.type == "file":
                    # Decode content (GitHub returns base64)
                    import base64
                    file_content = base64.b64decode(contents.content).decode('utf-8')
                    print(f"✅ DEBUG: Archivo {file_path} leído exitosamente, tamaño: {len(file_content)} caracteres")
                    context += f"--- {file_path} ---\n{file_content}\n\n"
                else:
                    print(f"❌ DEBUG: {file_path} no es un archivo, es: {contents.type}")
            except Exception as e:
                print(f"❌ DEBUG: Error leyendo {file_path}: {str(e)}")
                context += f"--- {file_path} ---\nNo se pudo leer el archivo: {str(e)}\n\n"
        
        print(f"🔍 DEBUG: Contexto generado, longitud: {len(context)} caracteres")
        return context
        
    except Exception as e:
        return f"Error obteniendo contexto de GitHub: {str(e)}"

async def process_chat_message_streaming(message: str, websocket: WebSocket):
    """Process chat message using Ollama with streaming and GitHub context"""
    try:
        # Check if Ollama is running
        response = requests.get(f"{config.get_ollama_url('api/tags')}", timeout=5)
        if response.status_code != 200:
            await manager.send_personal_message(
                json.dumps({
                    "type": "response_end",
                    "content": "❌ Error: Ollama no está ejecutándose. Por favor, inicia Ollama primero."
                }), 
                websocket
            )
            return
        
        # Get available models
        models_response = requests.get(f"{config.get_ollama_url('api/tags')}")
        if models_response.status_code == 200:
            models = models_response.json().get("models", [])
            if not models:
                await manager.send_personal_message(
                    json.dumps({
                        "type": "response_end",
                        "content": "❌ Error: No hay modelos disponibles en Ollama. Por favor, descarga un modelo primero."
                    }), 
                    websocket
                )
                return
            
            # Use phi3:mini if available, otherwise first available model
            phi3_mini_model = None
            for model in models:
                if "phi3:mini" in model["name"]:
                    phi3_mini_model = model["name"]
                    break
            
            if phi3_mini_model:
                model_name = phi3_mini_model
            else:
                model_name = models[0]["name"]
        else:
            await manager.send_personal_message(
                json.dumps({
                    "type": "response_end",
                    "content": "❌ Error: No se pudieron obtener los modelos de Ollama."
                }), 
                websocket
            )
            return
        
        # Check if user is asking about specific files or code
        github_context = ""
        keywords = [
            "archivo", "file", "código", "code", "función", "function", 
            "main.py", "config.py", "requirements.txt", "index.html",
            "analiza", "analyze", "revisa", "review", "explica", "explain",
            "qué hace", "what does", "cómo funciona", "how does", "error", "bug"
        ]
        
        print(f"🔍 DEBUG: Mensaje del usuario: '{message}'")
        print(f"🔍 DEBUG: Palabras clave detectadas: {[k for k in keywords if k in message.lower()]}")
        
        if any(keyword in message.lower() for keyword in keywords):
            print("🔍 DEBUG: Palabras clave detectadas, obteniendo contexto de GitHub...")
            github_context = await get_github_context(message)
            print(f"🔍 DEBUG: Contexto obtenido: {'SÍ' if github_context else 'NO'}")
        else:
            print("🔍 DEBUG: No se detectaron palabras clave, usando chat normal")
        
        # Prepare prompt with GitHub context if available
        if github_context:
            prompt = f"{config.get_model_selection_prompt()}\n\nContexto del repositorio:\n{github_context}\n\nUsuario: {message}"
            print(f"🔍 DEBUG: Prompt con contexto de GitHub, longitud: {len(prompt)} caracteres")
        else:
            prompt = f"{config.get_model_selection_prompt()}\n\nUsuario: {message}"
            print(f"🔍 DEBUG: Prompt sin contexto, longitud: {len(prompt)} caracteres")
        
        # Send message to Ollama with streaming
        ollama_data = {
            "model": model_name,
            "prompt": prompt,
            "stream": True
        }
        
        print(f"🚀 Enviando a Ollama con modelo: {model_name}")
        
        # Stream response from Ollama
        ollama_response = requests.post(
            f"{config.get_ollama_url('api/generate')}",
            json=ollama_data,
            timeout=config.OLLAMA_TIMEOUT,
            stream=True
        )
        
        if ollama_response.status_code == 200:
            full_response = ""
            for line in ollama_response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'response' in data:
                            chunk = data['response']
                            full_response += chunk
                            
                            # Send chunk to frontend
                            await manager.send_personal_message(
                                json.dumps({
                                    "type": "response_chunk",
                                    "content": chunk
                                }), 
                                websocket
                            )
                            
                        if data.get('done', False):
                            break
                            
                    except json.JSONDecodeError:
                        continue
            
            # Send end marker
            await manager.send_personal_message(
                json.dumps({
                    "type": "response_end",
                    "content": ""
                }), 
                websocket
            )
            
            print(f"✅ Respuesta completa enviada, longitud: {len(full_response)} caracteres")
            
        else:
            await manager.send_personal_message(
                json.dumps({
                    "type": "response_end",
                    "content": f"❌ Error al comunicarse con Ollama: {ollama_response.status_code}"
                }), 
                websocket
            )
            
    except requests.exceptions.RequestException as e:
        await manager.send_personal_message(
            json.dumps({
                "type": "response_end",
                "content": f"❌ Error de conexión con Ollama: {str(e)}"
            }), 
            websocket
        )
    except Exception as e:
        await manager.send_personal_message(
            json.dumps({
                "type": "response_end",
                "content": f"❌ Error inesperado: {str(e)}"
            }), 
            websocket
        )

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
        
        # Store active repository globally
        global active_repo
        active_repo = repo
        
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
