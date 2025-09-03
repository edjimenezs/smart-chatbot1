@echo off
chcp 65001 >nul
echo 🚀 Configurando Smart Chatbot para GitHub...
echo ==================================================

REM Paso 1: Verificar ubicación
echo 📍 Verificando ubicación...
if not exist "main.py" (
    echo ❌ Error: No estás en la carpeta del proyecto
    echo    Ejecuta este script desde: C:\Users\Eduardo Saavedra\smart-chatbot
    pause
    exit /b 1
)
echo ✅ Ubicación correcta

REM Paso 2: Crear .gitignore
echo 🔐 Creando .gitignore para proteger secretos...
(
echo # Archivos de configuración con secretos
echo .env
echo .env.local
echo .env.production
echo.
echo # Archivos de Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo build/
echo develop-eggs/
echo dist/
echo downloads/
echo eggs/
echo .eggs/
echo lib/
echo lib64/
echo parts/
echo sdist/
echo var/
echo wheels/
echo *.egg-info/
echo .installed.cfg
echo *.egg
echo.
echo # Entornos virtuales
echo .venv/
echo venv/
echo ENV/
echo env/
echo.
echo # IDEs
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo.
echo # Logs
echo *.log
echo logs/
echo.
echo # Archivos temporales
echo temp_timeout.txt
echo temp_*
) > .gitignore
echo ✅ .gitignore creado

REM Paso 3: Inicializar Git
echo 📦 Inicializando Git...
if exist ".git" (
    echo 🗑️  Eliminando Git anterior...
    rmdir /s /q .git
)
git init
echo ✅ Git inicializado

REM Paso 4: Agregar archivos
echo 📁 Agregando archivos al repositorio...
git add .
echo ✅ Archivos agregados

REM Paso 5: Hacer commit
echo 💾 Haciendo commit inicial...
git commit -m "Initial commit: Smart Chatbot with Ollama and GitHub integration"
echo ✅ Commit realizado

REM Paso 6: Cambiar a rama main
echo 🌿 Cambiando a rama main...
git branch -M main
echo ✅ Rama main configurada

REM Paso 7: Conectar con GitHub
echo 🔗 Conectando con GitHub...
git remote add origin https://github.com/edjimenezs/smart-chatbot1.git
echo ✅ Repositorio remoto configurado

REM Paso 8: Subir a GitHub
echo 🚀 Subiendo código a GitHub...
echo    Esto puede tomar unos segundos...
git push -u origin main

REM Paso 9: Verificar estado
echo 🔍 Verificando estado final...
git status
git remote -v

echo ==================================================
echo 🎉 ¡Configuración completada!
echo 📍 Tu código está en: https://github.com/edjimenezs/smart-chatbot1.git
echo 🔐 Tu archivo .env está protegido y NO se subió a GitHub
echo 💬 Ahora puedes usar el chatbot con funcionalidad completa de GitHub
pause
