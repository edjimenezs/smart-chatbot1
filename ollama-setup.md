# 🚀 Configuración de Ollama para Smart Chatbot

Esta guía te ayudará a configurar Ollama correctamente para usar con tu Smart Chatbot.

## 📥 Instalación de Ollama

### Windows
1. **Descarga directa**: Ve a [https://ollama.ai/download](https://ollama.ai/download)
2. **Usando winget** (recomendado):
   ```cmd
   winget install Ollama.Ollama
   ```
3. **Reinicia tu terminal** después de la instalación

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## 🔧 Configuración Inicial

### 1. Iniciar Ollama
```bash
ollama serve
```

**Nota**: En Windows, Ollama se ejecuta como servicio automáticamente.

### 2. Verificar la Instalación
```bash
ollama list
```

Si es la primera vez, la lista estará vacía.

## 📚 Descargar Modelos

### Modelos Recomendados para Programación

#### Code Llama (Recomendado para código)
```bash
ollama pull codellama
```
- **Tamaño**: ~4GB
- **Especialidad**: Generación y análisis de código
- **Idiomas**: Python, JavaScript, Java, C++, etc.

#### Llama 2 (Balanceado)
```bash
ollama pull llama2
```
- **Tamaño**: ~4GB
- **Especialidad**: Conversación general + programación
- **Idiomas**: Múltiples idiomas

#### Mistral (Rápido)
```bash
ollama pull mistral
```
- **Tamaño**: ~4GB
- **Especialidad**: Respuestas rápidas y precisas
- **Idiomas**: Inglés, programación

#### Phi-2 (Ligero)
```bash
ollama pull phi
```
- **Tamaño**: ~1.5GB
- **Especialidad**: Eficiente para tareas simples
- **Idiomas**: Inglés, programación básica

### 3. Verificar Modelos Descargados
```bash
ollama list
```

Deberías ver algo como:
```
NAME        ID          SIZE   MODIFIED
codellama   a1b2c3d4   4.2GB  2 hours ago
llama2      e5f6g7h8   4.1GB  1 day ago
```

## 🧪 Probar Ollama

### Test Básico
```bash
ollama run codellama "Escribe una función en Python que calcule el factorial"
```

### Test de Programación
```bash
ollama run codellama "Explica qué hace este código: def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"
```

## 🔗 Integración con Smart Chatbot

### 1. Verificar que Ollama esté ejecutándose
```bash
ollama list
```

### 2. Verificar el puerto
Ollama usa el puerto **11434** por defecto. Asegúrate de que esté disponible.

### 3. Configurar en .env
```env
OLLAMA_BASE_URL=http://localhost:11434
```

## 🐛 Solución de Problemas

### Error: "Ollama no está ejecutándose"
```bash
# Verificar si Ollama está corriendo
ollama list

# Si no responde, iniciarlo
ollama serve
```

### Error: "No hay modelos disponibles"
```bash
# Descargar un modelo
ollama pull codellama

# Verificar que se descargó
ollama list
```

### Error de Conexión
```bash
# Verificar que el puerto esté libre
netstat -an | findstr 11434

# Reiniciar Ollama
ollama serve
```

### Problemas de Memoria
Si tienes poca RAM:
1. Usa modelos más pequeños (phi, mistral)
2. Cierra otras aplicaciones
3. Aumenta la memoria virtual en Windows

## ⚡ Optimización

### Para Mejor Rendimiento
1. **Usa SSD**: Los modelos se cargan más rápido
2. **RAM**: Mínimo 8GB, recomendado 16GB+
3. **GPU**: Ollama soporta GPU para aceleración (opcional)

### Configuración de GPU (Opcional)
```bash
# Verificar soporte de GPU
ollama run codellama "¿Estás usando GPU?"

# Si tienes NVIDIA GPU, instala CUDA
# Si tienes AMD GPU, instala ROCm
```

## 📊 Monitoreo

### Ver Uso de Recursos
```bash
# Ver modelos en memoria
ollama list

# Ver logs
ollama serve --verbose
```

### Limpiar Memoria
```bash
# Remover modelo de memoria
ollama rm codellama

# Limpiar cache
ollama prune
```

## 🔄 Actualizaciones

### Actualizar Ollama
```bash
# Windows: Descargar nueva versión desde el sitio web
# macOS/Linux:
brew upgrade ollama
# o
curl -fsSL https://ollama.ai/install.sh | sh
```

### Actualizar Modelos
```bash
ollama pull codellama:latest
```

## 📱 Comandos Útiles

```bash
# Ver información del sistema
ollama show codellama

# Ejecutar modelo interactivo
ollama run codellama

# Ejecutar con parámetros específicos
ollama run codellama --temperature 0.7

# Ayuda
ollama --help
```

## 🎯 Próximos Pasos

1. ✅ Instalar Ollama
2. ✅ Descargar al menos un modelo
3. ✅ Verificar que funcione con `ollama run`
4. ✅ Configurar Smart Chatbot
5. 🚀 ¡Disfrutar de tu asistente de IA!

---

**¿Necesitas ayuda?** Revisa la documentación oficial en [ollama.ai](https://ollama.ai) o abre un issue en el repositorio del Smart Chatbot.
