# Smart Chatbot - PowerShell Startup Script
# Ejecutar como: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Smart Chatbot - Iniciando..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Por favor, instala Python 3.8+ desde https://python.org" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar dependencias
Write-Host "Verificando dependencias..." -ForegroundColor Yellow
if (-not (Test-Path "requirements.txt")) {
    Write-Host "✗ ERROR: No se encontró requirements.txt" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Instalar dependencias
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "✓ Dependencias instaladas correctamente" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: No se pudieron instalar las dependencias" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Configuración del Sistema" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "IMPORTANTE: Asegúrate de que Ollama esté ejecutándose" -ForegroundColor Yellow
Write-Host "Si no tienes Ollama instalado:" -ForegroundColor Yellow
Write-Host "1. Descarga desde: https://ollama.ai/download" -ForegroundColor White
Write-Host "2. Instala y ejecuta: ollama serve" -ForegroundColor White
Write-Host "3. Descarga un modelo: ollama pull llama2" -ForegroundColor White
Write-Host ""

# Verificar archivo .env
Write-Host "Verificando archivo .env..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "Creando archivo .env desde env.example..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
    Write-Host ""
    Write-Host "IMPORTANTE: Edita el archivo .env con tu configuración" -ForegroundColor Yellow
    Write-Host "- GITHUB_TOKEN: Tu token de GitHub (opcional)" -ForegroundColor White
    Write-Host "- OLLAMA_BASE_URL: URL de Ollama (por defecto: http://localhost:11434)" -ForegroundColor White
    Write-Host ""
    Read-Host "Presiona Enter para continuar"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Iniciando Smart Chatbot..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "El chatbot estará disponible en: http://localhost:8000" -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

# Iniciar el chatbot
python main.py

Read-Host "Presiona Enter para salir"
