@echo off
echo ========================================
echo    Smart Chatbot - Iniciando...
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo Verificando dependencias...
if not exist "requirements.txt" (
    echo ERROR: No se encontró requirements.txt
    pause
    exit /b 1
)

echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Configuración del Sistema
echo ========================================
echo.

echo IMPORTANTE: Asegúrate de que Ollama esté ejecutándose
echo Si no tienes Ollama instalado:
echo 1. Descarga desde: https://ollama.ai/download
echo 2. Instala y ejecuta: ollama serve
echo 3. Descarga un modelo: ollama pull llama2
echo.

echo Verificando archivo .env...
if not exist ".env" (
    echo Creando archivo .env desde env.example...
    copy env.example .env
    echo.
    echo IMPORTANTE: Edita el archivo .env con tu configuración
    echo - GITHUB_TOKEN: Tu token de GitHub (opcional)
    echo - OLLAMA_BASE_URL: URL de Ollama (por defecto: http://localhost:11434)
    echo.
    pause
)

echo.
echo ========================================
echo    Iniciando Smart Chatbot...
echo ========================================
echo.
echo El chatbot estará disponible en: http://localhost:8000
echo Presiona Ctrl+C para detener
echo.

python main.py

pause
