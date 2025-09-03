from http.server import BaseHTTPRequestHandler
import json
import requests
import os
from urllib.parse import parse_qs, urlparse

class ChatHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Maneja las peticiones POST para el chat"""
        try:
            # Obtener el contenido del request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            # Extraer el mensaje del usuario
            user_message = request_data.get('message', '')
            
            if not user_message:
                self.send_error_response('Mensaje requerido')
                return
            
            # Procesar el mensaje (versión simplificada)
            response = self.process_message(user_message)
            
            # Enviar respuesta exitosa
            self.send_success_response(response)
            
        except Exception as e:
            self.send_error_response(f'Error interno: {str(e)}')
    
    def do_GET(self):
        """Maneja las peticiones GET para información del sistema"""
        if self.path == '/api/health':
            self.send_success_response({
                'status': 'healthy',
                'platform': 'Vercel',
                'features': [
                    'API REST funcional',
                    'Chat simplificado',
                    'Análisis de GitHub',
                    'Sin WebSockets'
                ]
            })
        else:
            self.send_error_response('Endpoint no encontrado', 404)
    
    def process_message(self, message: str) -> str:
        """Procesa el mensaje del usuario y genera una respuesta"""
        
        # Respuestas predefinidas para diferentes tipos de preguntas
        message_lower = message.lower()
        
        # Preguntas sobre programación
        if any(word in message_lower for word in ['python', 'código', 'code', 'programación']):
            return "¡Excelente pregunta sobre programación! 🐍\n\nEn Vercel, este chatbot funciona como una API REST. Puedes hacer preguntas sobre:\n• Conceptos de programación\n• Mejores prácticas\n• Patrones de diseño\n• Debugging\n\n¿En qué lenguaje específico te gustaría que te ayude?"
        
        # Preguntas sobre el chatbot
        elif any(word in message_lower for word in ['chatbot', 'bot', 'ayuda', 'help']):
            return "🤖 **Smart Chatbot en Vercel**\n\nEste es tu asistente de programación funcionando en la nube. Aunque no tengo acceso a Ollama aquí, puedo ayudarte con:\n\n✅ **Conceptos de programación**\n✅ **Mejores prácticas**\n✅ **Análisis de código**\n✅ **Solución de problemas**\n\n¿Qué te gustaría aprender hoy?"
        
        # Preguntas sobre GitHub
        elif any(word in message_lower for word in ['github', 'repo', 'repositorio']):
            return "🔗 **GitHub Integration**\n\nPara conectar tu repositorio de GitHub, necesitarás:\n\n1. **Token de GitHub** con permisos `repo`\n2. **Configurar variables de entorno** en Vercel\n3. **URL de tu repositorio**\n\n¿Te gustaría que te explique cómo configurar esto paso a paso?"
        
        # Preguntas sobre Ollama
        elif any(word in message_lower for word in ['ollama', 'modelo', 'ia', 'ai']):
            return "🧠 **Ollama en Vercel**\n\nEn Vercel no puedo ejecutar Ollama directamente, pero puedo:\n\n✅ **Explicar conceptos de IA**\n✅ **Ayudarte con prompts**\n✅ **Recomendar modelos**\n✅ **Explicar cómo funciona**\n\n¿Te gustaría que te explique cómo configurar Ollama en tu PC local o en la nube?"
        
        # Preguntas sobre Vercel
        elif any(word in message_lower for word in ['vercel', 'deploy', 'nube', 'cloud']):
            return "☁️ **Vercel Deployment**\n\n¡Excelente! Tu chatbot está funcionando en Vercel. Aquí tienes:\n\n✅ **API REST funcional**\n✅ **Deploy automático**\n✅ **HTTPS gratuito**\n✅ **CDN global**\n\nPara funcionalidades completas (WebSockets, Ollama), considera Railway o Render."
        
        # Respuesta por defecto
        else:
            return f"¡Hola! 👋\n\nRecibí tu mensaje: '{message}'\n\nSoy tu asistente de programación funcionando en Vercel. Aunque no tengo acceso a Ollama aquí, puedo ayudarte con:\n\n• 📚 **Conceptos de programación**\n• 🔧 **Mejores prácticas**\n• 🐛 **Debugging**\n• 📖 **Recursos de aprendizaje**\n\n¿En qué puedo ayudarte específicamente?"
    
    def send_success_response(self, data):
        """Envía una respuesta exitosa"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = {
            'success': True,
            'data': data,
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def send_error_response(self, message, status_code=400):
        """Envía una respuesta de error"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'success': False,
            'error': message,
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Maneja las peticiones OPTIONS para CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

# Función principal para Vercel
def handler(request, context):
    """Función principal para Vercel"""
    if request.method == 'POST':
        # Procesar chat
        try:
            body = request.get_json()
            user_message = body.get('message', '')
            
            if not user_message:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'success': False,
                        'error': 'Mensaje requerido'
                    })
                }
            
            # Procesar mensaje
            response = process_message(user_message)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'success': True,
                    'data': response
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'success': False,
                    'error': f'Error interno: {str(e)}'
                })
            }
    
    elif request.method == 'GET':
        # Endpoint de salud
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'data': {
                    'status': 'healthy',
                    'platform': 'Vercel',
                    'features': [
                        'API REST funcional',
                        'Chat simplificado',
                        'Análisis de GitHub',
                        'Sin WebSockets'
                    ]
                }
            })
        }
    
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({
                'success': False,
                'error': 'Método no permitido'
            })
        }

def process_message(message: str) -> str:
    """Procesa el mensaje del usuario y genera una respuesta"""
    
    # Respuestas predefinidas para diferentes tipos de preguntas
    message_lower = message.lower()
    
    # Preguntas sobre programación
    if any(word in message_lower for word in ['python', 'código', 'code', 'programación']):
        return "¡Excelente pregunta sobre programación! 🐍\n\nEn Vercel, este chatbot funciona como una API REST. Puedes hacer preguntas sobre:\n• Conceptos de programación\n• Mejores prácticas\n• Patrones de diseño\n• Debugging\n\n¿En qué lenguaje específico te gustaría que te ayude?"
    
    # Preguntas sobre el chatbot
    elif any(word in message_lower for word in ['chatbot', 'bot', 'ayuda', 'help']):
        return "🤖 **Smart Chatbot en Vercel**\n\nEste es tu asistente de programación funcionando en la nube. Aunque no tengo acceso a Ollama aquí, puedo ayudarte con:\n\n✅ **Conceptos de programación**\n✅ **Mejores prácticas**\n✅ **Análisis de código**\n✅ **Solución de problemas**\n\n¿Qué te gustaría aprender hoy?"
    
    # Preguntas sobre GitHub
    elif any(word in message_lower for word in ['github', 'repo', 'repositorio']):
        return "🔗 **GitHub Integration**\n\nPara conectar tu repositorio de GitHub, necesitarás:\n\n1. **Token de GitHub** con permisos `repo`\n2. **Configurar variables de entorno** en Vercel\n3. **URL de tu repositorio**\n\n¿Te gustaría que te explique cómo configurar esto paso a paso?"
    
    # Preguntas sobre Ollama
    elif any(word in message_lower for word in ['ollama', 'modelo', 'ia', 'ai']):
        return "🧠 **Ollama en Vercel**\n\nEn Vercel no puedo ejecutar Ollama directamente, pero puedo:\n\n✅ **Explicar conceptos de IA**\n✅ **Ayudarte con prompts**\n✅ **Recomendar modelos**\n✅ **Explicar cómo funciona**\n\n¿Te gustaría que te explique cómo configurar Ollama en tu PC local o en la nube?"
    
    # Preguntas sobre Vercel
    elif any(word in message_lower for word in ['vercel', 'deploy', 'nube', 'cloud']):
        return "☁️ **Vercel Deployment**\n\n¡Excelente! Tu chatbot está funcionando en Vercel. Aquí tienes:\n\n✅ **API REST funcional**\n✅ **Deploy automático**\n✅ **HTTPS gratuito**\n✅ **CDN global**\n\nPara funcionalidades completas (WebSockets, Ollama), considera Railway o Render."
    
    # Respuesta por defecto
    else:
        return f"¡Hola! 👋\n\nRecibí tu mensaje: '{message}'\n\nSoy tu asistente de programación funcionando en Vercel. Aunque no tengo acceso a Ollama aquí, puedo ayudarte con:\n\n• 📚 **Conceptos de programación**\n• 🔧 **Mejores prácticas**\n• 🐛 **Debugging**\n• 📖 **Recursos de aprendizaje**\n\n¿En qué puedo ayudarte específicamente?"
