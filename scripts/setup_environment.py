#!/usr/bin/env python3
"""
Script para configurar el entorno de desarrollo
Fase 1 - Días 3-4: Configuración y pruebas iniciales
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ requerido")
        return False
    print(f"✅ Python {sys.version.split()[0]} OK")
    return True

def install_dependencies():
    """Instalar dependencias del proyecto"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencias instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_env_file():
    """Crear archivo .env si no existe"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        env_file.write_text(env_example.read_text())
        print("✅ Archivo .env creado desde .env.example")
        print("⚠️  Edita .env con tus API keys reales")
        return True
    elif env_file.exists():
        print("✅ Archivo .env ya existe")
        return True
    else:
        print("❌ No se pudo crear .env")
        return False

def check_api_keys():
    """Verificar si las API keys están configuradas"""
    from dotenv import load_dotenv
    load_dotenv()
    
    keys_to_check = [
        ("OPENAI_API_KEY", "OpenAI Vision API"),
        ("USDA_API_KEY", "USDA Food Data"),
        ("NUTRITIONIX_APP_ID", "Nutritionix API"),
        ("NUTRITIONIX_APP_KEY", "Nutritionix API Key")
    ]
    
    configured_keys = []
    missing_keys = []
    
    for key, description in keys_to_check:
        value = os.getenv(key, "")
        if value and not value.startswith("your-") and not value.startswith("sk-your-"):
            configured_keys.append(description)
            print(f"✅ {description}: Configurado")
        else:
            missing_keys.append(description)
            print(f"⚠️  {description}: No configurado")
    
    return len(configured_keys), len(missing_keys)

def create_test_structure():
    """Crear estructura de directorios para testing"""
    dirs_to_create = [
        "test_images",
        "results",
        "logs"
    ]
    
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Directorio {dir_name}/ creado")

def download_sample_images():
    """Crear imágenes de muestra para testing"""
    sample_images_info = """
📸 IMÁGENES DE PRUEBA NECESARIAS

Para probar las APIs, necesitas agregar imágenes en test_images/:

Sugerencias de imágenes:
- test_images/apple.jpg (una manzana)
- test_images/banana.jpg (un plátano) 
- test_images/chicken.jpg (pechuga de pollo)
- test_images/mixed_meal.jpg (plato con varios alimentos)
- test_images/pizza_slice.jpg (porción de pizza)

Puedes:
1. Tomar fotos con tu teléfono
2. Descargar imágenes de stock gratuitas
3. Usar imágenes de ejemplo de internet

Formatos soportados: JPG, PNG
Tamaño recomendado: 1024x1024 o menor
"""
    
    readme_path = Path("test_images/README.md")
    readme_path.write_text(sample_images_info)
    print("✅ Guía de imágenes creada en test_images/README.md")

def main():
    """Configurar entorno completo"""
    print("🚀 CONFIGURACIÓN DEL ENTORNO DE DESARROLLO")
    print("Contador de Calorías por Foto - Fase 1")
    print("=" * 50)
    
    # Verificaciones básicas
    if not check_python_version():
        return False
    
    # Instalar dependencias
    if not install_dependencies():
        return False
    
    # Crear archivo .env
    if not create_env_file():
        return False
    
    # Crear estructura de directorios
    create_test_structure()
    
    # Crear guía de imágenes
    download_sample_images()
    
    # Verificar API keys
    print("\n🔑 VERIFICACIÓN DE API KEYS")
    print("-" * 30)
    configured, missing = check_api_keys()
    
    print(f"\n📊 RESUMEN DE CONFIGURACIÓN")
    print("-" * 30)
    print(f"✅ APIs configuradas: {configured}")
    print(f"⚠️  APIs pendientes: {missing}")
    
    if missing > 0:
        print(f"\n📋 PRÓXIMOS PASOS:")
        print("1. Editar .env con tus API keys")
        print("2. Agregar imágenes de prueba en test_images/")
        print("3. Ejecutar: python scripts/test_apis.py")
    else:
        print(f"\n🎉 ¡Entorno configurado completamente!")
        print("Ejecuta: python scripts/test_apis.py")
    
    return True

if __name__ == "__main__":
    main()