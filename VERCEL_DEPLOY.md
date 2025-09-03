# 🚀 Deploy en Vercel - Smart Chatbot

## ⚠️ **IMPORTANTE: Limitaciones de Vercel**

Vercel es una plataforma **serverless** que tiene algunas limitaciones importantes para este chatbot:

### ❌ **No compatible con:**
- **WebSockets** (necesarios para chat en tiempo real)
- **Ollama local** (no puedes ejecutar servicios locales)
- **Conexiones persistentes** (cada request es independiente)

### ✅ **Alternativas recomendadas:**
1. **Railway** - Soporta WebSockets y servicios persistentes
2. **Render** - Soporta aplicaciones Python completas
3. **Heroku** - Plataforma tradicional para Python
4. **DigitalOcean App Platform** - Soporte completo para Python

## 🔧 **Configuración para Vercel (versión limitada)**

Si aún quieres probar en Vercel, el chatbot funcionará como una **API REST** básica (sin chat en tiempo real):

### 1. **Variables de Entorno en Vercel Dashboard:**
```bash
GITHUB_TOKEN=your_github_token_here
OLLAMA_BASE_URL=https://tu-servicio-ollama.com
```

### 2. **Servicios externos necesarios:**
- **Ollama en la nube** (RunPod, Modal, etc.)
- **Base de datos** para almacenar conversaciones
- **WebSocket service** separado (Pusher, Ably, etc.)

## 🚀 **Deploy en Vercel:**

```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Login en Vercel
vercel login

# 3. Deploy
vercel

# 4. Para producción
vercel --prod
```

## 📱 **Funcionalidades disponibles en Vercel:**
- ✅ API endpoints básicos
- ✅ Conexión con GitHub
- ✅ Análisis de repositorios
- ❌ Chat en tiempo real
- ❌ WebSockets
- ❌ Streaming de respuestas

## 🔄 **Migración a plataforma compatible:**

Para mantener **todas las funcionalidades**, considera migrar a:

### **Railway (Recomendado):**
```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### **Render:**
- Conecta tu repositorio de GitHub
- Selecciona "Web Service"
- Build Command: `pip install -r requirements.txt`
- Start Command: `python main.py`

## 📊 **Comparación de plataformas:**

| Plataforma | WebSockets | Python | Precio | Facilidad |
|------------|------------|---------|---------|-----------|
| **Vercel** | ❌ | ⚠️ | $0-20/mes | ⭐⭐⭐⭐⭐ |
| **Railway** | ✅ | ✅ | $5/mes | ⭐⭐⭐⭐ |
| **Render** | ✅ | ✅ | $7/mes | ⭐⭐⭐⭐ |
| **Heroku** | ✅ | ✅ | $7/mes | ⭐⭐⭐ |

## 🎯 **Recomendación final:**

**Para este chatbot específico, usa Railway o Render** para mantener todas las funcionalidades de chat en tiempo real.
