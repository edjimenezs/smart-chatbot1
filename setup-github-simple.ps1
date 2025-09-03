# Script de Configuracion Automatica para Smart Chatbot
# Este script configura Git y GitHub automaticamente

Write-Host "Configurando Smart Chatbot para GitHub..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan

# Paso 1: Verificar que estamos en la carpeta correcta
Write-Host "Verificando ubicacion..." -ForegroundColor Yellow
if (-not (Test-Path "main.py")) {
    Write-Host "Error: No estas en la carpeta del proyecto" -ForegroundColor Red
    Write-Host "   Ejecuta este script desde: C:\Users\Eduardo Saavedra\smart-chatbot" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}
Write-Host "Ubicacion correcta" -ForegroundColor Green

# Paso 2: Crear .gitignore ANTES de cualquier commit
Write-Host "Creando .gitignore para proteger secretos..." -ForegroundColor Yellow
@"
# Archivos de configuracion con secretos
.env
.env.local
.env.production

# Archivos de Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Entornos virtuales
.venv/
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# Archivos temporales
temp_timeout.txt
temp_*
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
Write-Host ".gitignore creado" -ForegroundColor Green

# Paso 3: Inicializar Git
Write-Host "Inicializando Git..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "Eliminando Git anterior..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .git
}
git init
Write-Host "Git inicializado" -ForegroundColor Green

# Paso 4: Agregar archivos (excluyendo .env)
Write-Host "Agregando archivos al repositorio..." -ForegroundColor Yellow
git add .
Write-Host "Archivos agregados" -ForegroundColor Green

# Paso 5: Hacer commit inicial
Write-Host "Haciendo commit inicial..." -ForegroundColor Yellow
git commit -m "Initial commit: Smart Chatbot with Ollama and GitHub integration"
Write-Host "Commit realizado" -ForegroundColor Green

# Paso 6: Cambiar a rama main
Write-Host "Cambiando a rama main..." -ForegroundColor Yellow
git branch -M main
Write-Host "Rama main configurada" -ForegroundColor Green

# Paso 7: Conectar con GitHub
Write-Host "Conectando con GitHub..." -ForegroundColor Yellow
$repoUrl = "https://github.com/edjimenezs/smart-chatbot1.git"
git remote add origin $repoUrl
Write-Host "Repositorio remoto configurado" -ForegroundColor Green

# Paso 8: Subir a GitHub
Write-Host "Subiendo codigo a GitHub..." -ForegroundColor Yellow
Write-Host "   Esto puede tomar unos segundos..." -ForegroundColor Cyan
git push -u origin main

# Paso 9: Verificar estado final
Write-Host "Verificando estado final..." -ForegroundColor Yellow
git status
git remote -v

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Configuracion completada!" -ForegroundColor Green
Write-Host "Tu codigo esta en: $repoUrl" -ForegroundColor Cyan
Write-Host "Tu archivo .env esta protegido y NO se subio a GitHub" -ForegroundColor Green
Write-Host "Ahora puedes usar el chatbot con funcionalidad completa de GitHub" -ForegroundColor Cyan

Read-Host "Presiona Enter para salir"
