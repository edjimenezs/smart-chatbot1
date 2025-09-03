"""
Configuración centralizada para Smart Chatbot
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración centralizada del chatbot"""
    
    # Configuración del servidor
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Configuración de Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", 30))
    OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "auto")
    
    # Configuración de GitHub
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_REPO = os.getenv("GITHUB_REPO", "username/repository")
    GITHUB_TIMEOUT = int(os.getenv("GITHUB_TIMEOUT", 10))
    
    # Configuración del chat
    MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", 1000))
    CHAT_HISTORY_LIMIT = int(os.getenv("CHAT_HISTORY_LIMIT", 100))
    
    # Configuración de seguridad
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    RATE_LIMIT = os.getenv("RATE_LIMIT", "100/minute")
    
    # Configuración de logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "smart-chatbot.log")
    
    @classmethod
    def validate(cls):
        """Validar configuración requerida"""
        errors = []
        
        if not cls.OLLAMA_BASE_URL:
            errors.append("OLLAMA_BASE_URL no está configurado")
        
        if cls.GITHUB_TOKEN and not (cls.GITHUB_TOKEN.startswith("ghp_") or cls.GITHUB_TOKEN.startswith("github_pat_")):
            errors.append("GITHUB_TOKEN parece ser inválido")
        
        if cls.PORT < 1 or cls.PORT > 65535:
            errors.append("PORT debe estar entre 1 y 65535")
        
        return errors
    
    @classmethod
    def get_ollama_url(cls, endpoint: str = "") -> str:
        """Obtener URL completa de Ollama"""
        base = cls.OLLAMA_BASE_URL.rstrip("/")
        endpoint = endpoint.lstrip("/")
        return f"{base}/{endpoint}" if endpoint else base
    
    @classmethod
    def is_github_enabled(cls) -> bool:
        """Verificar si GitHub está habilitado"""
        return bool(cls.GITHUB_TOKEN)
    
    @classmethod
    def get_model_selection_prompt(cls) -> str:
        """Obtener prompt para selección de modelo"""
        return """Eres un asistente de programación experto y preciso. 

INSTRUCCIONES IMPORTANTES:
- Responde SOLO en español natural y claro
- NO generes código de programación en tus respuestas
- NO uses funciones como Composer BotResponse() o similares
- Sé específico y directo en tus respuestas
- Si te piden una línea específica, muestra EXACTAMENTE esa línea
- Si no estás seguro, di "No estoy seguro" en lugar de inventar

Tu objetivo es ayudar con:
- Análisis y explicación de código
- Debugging y solución de problemas  
- Mejores prácticas de programación
- Optimización de código
- Explicación de conceptos técnicos

Responde de manera clara, concisa y útil. Si es código, incluye comentarios explicativos.
Si no estás seguro de algo, sé honesto al respecto."""
    
    @classmethod
    def get_system_info(cls) -> dict:
        """Obtener información del sistema"""
        return {
            "host": cls.HOST,
            "port": cls.PORT,
            "debug": cls.DEBUG,
            "ollama_url": cls.OLLAMA_BASE_URL,
            "github_enabled": cls.is_github_enabled(),
            "max_message_length": cls.MAX_MESSAGE_LENGTH,
            "chat_history_limit": cls.CHAT_HISTORY_LIMIT
        }

# Instancia global de configuración
config = Config()
