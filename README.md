# 🤖 Smart Chatbot - Tu Asistente de Programación

Un chatbot inteligente y funcional al 100% que utiliza **Ollama** para modelos de IA locales y se conecta a tu **repositorio de GitHub** para proporcionar asistencia contextual de programación.

## ✨ Características Principales

- 🚀 **Chat en tiempo real** con WebSockets
- 🧠 **Integración con Ollama** para modelos de IA locales
- 🔗 **Conexión directa con GitHub** para análisis de repositorios
- 💬 **Interfaz web moderna y responsive** 
- 📱 **Diseño adaptativo** para móviles y escritorio
- 🔄 **Estado del sistema en tiempo real**
- 📊 **Análisis de repositorios** con información detallada
- ⚡ **Respuestas rápidas** y contextuales

## 🛠️ Tecnologías Utilizadas

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **IA**: Ollama (modelos locales)
- **GitHub**: PyGithub API
- **Comunicación**: WebSockets
- **Estilo**: CSS Grid, Flexbox, Gradientes

## 📋 Requisitos Previos

1. **Python 3.8+** instalado
2. **Ollama** instalado y ejecutándose
3. **Token de GitHub** (opcional, para funcionalidad completa)

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone <tu-repositorio>
cd smart-chatbot
```

## 🌐 **Deploy en la Nube**

### **⚠️ IMPORTANTE: Limitaciones de Vercel**
Este chatbot usa **WebSockets** y **conexiones persistentes**, que **NO son compatibles** con Vercel (plataforma serverless).

**Plataformas recomendadas:**
- 🚂 **Railway** - Soporta WebSockets (Recomendado)
- 🌊 **Render** - Soporta aplicaciones Python completas
- 🎯 **Heroku** - Plataforma tradicional para Python

**Ver archivo `VERCEL_DEPLOY.md` para más detalles.**

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Copia el archivo de ejemplo y configúralo:

```bash
copy env.example .env
```

Edita el archivo `.env` con tus configuraciones:

```env
# Configuración de Ollama
OLLAMA_BASE_URL=http://localhost:11434

# Configuración de GitHub (opcional)
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=username/repository
```

### 4. Instalar y Configurar Ollama

#### Windows:
```bash
# Descargar desde: https://ollama.ai/download
# O usar winget:
winget install Ollama.Ollama
```

#### macOS:
```bash
brew install ollama
```

#### Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 5. Descargar un Modelo

```bash
# Iniciar Ollama
ollama serve

# En otra terminal, descargar un modelo
ollama pull llama2
# o
ollama pull codellama
# o
ollama pull mistral
```

### 6. Ejecutar el Chatbot

```bash
python main.py
```

El chatbot estará disponible en: **http://localhost:8000**

## 🔧 Configuración de GitHub (Opcional)

Para conectar tu repositorio de GitHub:

1. Ve a [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Genera un nuevo token con permisos de `repo`
3. Copia el token en tu archivo `.env`
4. Reinicia el chatbot

## 📱 Uso del Chatbot

### Chat Básico
- Escribe tu pregunta en el campo de texto
- Presiona Enter o haz clic en el botón de enviar
- El chatbot responderá usando el modelo de Ollama

### Conexión con GitHub
1. Ingresa la URL de tu repositorio en el sidebar
2. Haz clic en "Conectar"
3. El chatbot analizará tu repositorio
4. Podrás hacer preguntas específicas sobre tu código

### Ejemplos de Preguntas
- "¿Cómo optimizar este código Python?"
- "Explica esta función de JavaScript"
- "¿Cuáles son las mejores prácticas para este patrón?"
- "Ayúdame a debuggear este error"

## 🏗️ Estructura del Proyecto

```
smart-chatbot/
├── main.py              # Aplicación principal FastAPI
├── requirements.txt     # Dependencias de Python
├── env.example         # Variables de entorno de ejemplo
├── README.md           # Este archivo
├── templates/          # Plantillas HTML
│   └── index.html     # Interfaz principal
└── static/            # Archivos estáticos (si los hay)
```

## 🔍 Endpoints de la API

- `GET /` - Interfaz principal del chatbot
- `GET /api/health` - Estado del sistema
- `WS /ws` - WebSocket para chat en tiempo real

## 🐛 Solución de Problemas

### Ollama no está ejecutándose
```bash
# Verificar si Ollama está corriendo
ollama list

# Si no está corriendo, iniciarlo
ollama serve
```

### Error de conexión con GitHub
- Verifica que tu token sea válido
- Asegúrate de que tenga permisos de `repo`
- Revisa que la URL del repositorio sea correcta

### Problemas de puertos
- El chatbot usa el puerto 8000 por defecto
- Ollama usa el puerto 11434
- Asegúrate de que estos puertos estén disponibles

## 🚀 Personalización

### Cambiar el Modelo de Ollama
Edita la función `process_chat_message` en `main.py`:

```python
# Cambiar el modelo por defecto
model_name = "tu-modelo-preferido"
```

### Modificar la Interfaz
Edita `templates/index.html` para personalizar:
- Colores y estilos
- Layout y componentes
- Funcionalidades adicionales

### Agregar Nuevas Funcionalidades
- Nuevos endpoints en `main.py`
- Nuevos tipos de mensajes WebSocket
- Integraciones adicionales

## 📊 Monitoreo y Logs

El chatbot incluye:
- Indicadores de estado en tiempo real
- Logs de conexión WebSocket
- Verificación de salud del sistema
- Manejo de errores robusto

## 🔒 Seguridad

- Las variables sensibles se manejan a través de archivos `.env`
- No se almacenan tokens en el código
- Validación de entrada en todos los endpoints
- Manejo seguro de conexiones WebSocket

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas:

1. Revisa la sección de solución de problemas
2. Verifica que Ollama esté ejecutándose
3. Revisa los logs de la consola
4. Abre un issue en el repositorio

## 🎯 Roadmap

- [ ] Soporte para múltiples modelos de Ollama
- [ ] Historial de conversaciones persistente
- [ ] Análisis de código más profundo
- [ ] Integración con más plataformas de código
- [ ] API REST completa
- [ ] Dockerización
- [ ] Tests automatizados

---

**¡Disfruta usando tu Smart Chatbot personal! 🚀**

Si te gusta el proyecto, ¡dale una estrella! ⭐

