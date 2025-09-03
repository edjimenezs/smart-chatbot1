#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración del Smart Chatbot
Ejecuta este script antes de iniciar el chatbot principal
"""

import sys
import requests
import os
from pathlib import Path

def print_header(title):
    """Imprimir encabezado con formato"""
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_status(message, status="INFO"):
    """Imprimir mensaje con estado"""
    if status == "SUCCESS":
        print(f"✅ {message}")
    elif status == "ERROR":
        print(f"❌ {message}")
    elif status == "WARNING":
        print(f"⚠️  {message}")
    else:
        print(f"ℹ️  {message}")

def test_python():
    """Verificar versión de Python"""
    print_header("Verificando Python")
    
    version = sys.version_info
    print_status(f"Versión de Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_status("Se requiere Python 3.8 o superior", "ERROR")
        return False
    
    print_status("Python cumple con los requisitos", "SUCCESS")
    return True

def test_dependencies():
    """Verificar dependencias instaladas"""
    print_header("Verificando Dependencias")
    
    required_packages = [
        "fastapi", "uvicorn", "requests", "python-dotenv", 
        "PyGithub", "aiofiles", "jinja2", "websockets"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print_status(f"{package}: Instalado", "SUCCESS")
        except ImportError:
            print_status(f"{package}: No instalado", "ERROR")
            missing_packages.append(package)
    
    if missing_packages:
        print_status(f"Instala las dependencias faltantes: pip install {' '.join(missing_packages)}", "ERROR")
        return False
    
    return True

def test_ollama():
    """Verificar conexión con Ollama"""
    print_header("Verificando Ollama")
    
    try:
        # Intentar conectar a Ollama
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            print_status("Ollama está ejecutándose", "SUCCESS")
            
            # Verificar modelos disponibles
            data = response.json()
            models = data.get("models", [])
            
            if models:
                print_status(f"Modelos disponibles: {len(models)}", "SUCCESS")
                for model in models[:3]:  # Mostrar solo los primeros 3
                    print_status(f"  - {model['name']} ({model.get('size', 'N/A')})", "INFO")
            else:
                print_status("No hay modelos descargados", "WARNING")
                print_status("Ejecuta: ollama pull codellama", "INFO")
            
            return True
        else:
            print_status(f"Ollama respondió con código: {response.status_code}", "ERROR")
            return False
            
    except requests.exceptions.ConnectionError:
        print_status("No se puede conectar a Ollama", "ERROR")
        print_status("Asegúrate de que Ollama esté ejecutándose: ollama serve", "INFO")
        return False
    except Exception as e:
        print_status(f"Error al verificar Ollama: {str(e)}", "ERROR")
        return False

def test_github_config():
    """Verificar configuración de GitHub"""
    print_header("Verificando Configuración de GitHub")
    
    # Verificar archivo .env
    env_file = Path(".env")
    if not env_file.exists():
        print_status("Archivo .env no encontrado", "WARNING")
        print_status("Copia env.example a .env y configúralo", "INFO")
        return False
    
    # Verificar token de GitHub
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token and github_token != "tu_token_de_github_aqui":
            print_status("Token de GitHub configurado", "SUCCESS")
            
            # Verificar que el token sea válido
            if github_token.startswith("ghp_") or github_token.startswith("github_pat_"):
                print_status("Formato de token válido", "SUCCESS")
                return True
            else:
                print_status("Formato de token inválido", "ERROR")
                return False
        else:
            print_status("Token de GitHub no configurado", "WARNING")
            print_status("GitHub estará deshabilitado", "INFO")
            return True
            
    except Exception as e:
        print_status(f"Error al verificar configuración: {str(e)}", "ERROR")
        return False

def test_files():
    """Verificar archivos del proyecto"""
    print_header("Verificando Archivos del Proyecto")
    
    required_files = [
        "main.py",
        "config.py", 
        "requirements.txt",
        "templates/index.html",
        "README.md"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print_status(f"{file_path}: Encontrado", "SUCCESS")
        else:
            print_status(f"{file_path}: No encontrado", "ERROR")
            missing_files.append(file_path)
    
    if missing_files:
        print_status("Algunos archivos están faltando", "ERROR")
        return False
    
    return True

def test_config():
    """Verificar configuración del sistema"""
    print_header("Verificando Configuración del Sistema")
    
    try:
        from config import config
        
        # Validar configuración
        errors = config.validate()
        
        if errors:
            print_status("Errores de configuración encontrados:", "ERROR")
            for error in errors:
                print_status(f"  - {error}", "ERROR")
            return False
        
        print_status("Configuración válida", "SUCCESS")
        
        # Mostrar información del sistema
        system_info = config.get_system_info()
        print_status(f"Host: {system_info['host']}", "INFO")
        print_status(f"Puerto: {system_info['port']}", "INFO")
        print_status(f"Ollama: {system_info['ollama_url']}", "INFO")
        print_status(f"GitHub: {'Habilitado' if system_info['github_enabled'] else 'Deshabilitado'}", "INFO")
        
        return True
        
    except Exception as e:
        print_status(f"Error al verificar configuración: {str(e)}", "ERROR")
        return False

def main():
    """Función principal de pruebas"""
    print_header("Smart Chatbot - Verificación del Sistema")
    print()
    
    tests = [
        ("Python", test_python),
        ("Dependencias", test_dependencies),
        ("Archivos", test_files),
        ("Configuración", test_config),
        ("Ollama", test_ollama),
        ("GitHub", test_github_config)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_status(f"Error en {test_name}: {str(e)}", "ERROR")
            results.append((test_name, False))
        
        print()
    
    # Resumen de resultados
    print_header("Resumen de Verificación")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
    
    print()
    print_status(f"Pruebas pasadas: {passed}/{total}", "INFO")
    
    if passed == total:
        print_status("¡Sistema listo para usar!", "SUCCESS")
        print_status("Ejecuta: python main.py", "INFO")
        return True
    else:
        print_status("Hay problemas que resolver antes de continuar", "ERROR")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
