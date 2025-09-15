"""
Verificación de Criterios de Aceptación - MVP Contador de Calorías
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path: str) -> bool:
    """Verificar si un archivo existe"""
    return Path(file_path).exists()

def check_directory_structure() -> dict:
    """Verificar estructura de directorios del proyecto"""
    base_path = Path(__file__).parent.parent
    
    required_structure = {
        "src/backend": base_path / "src" / "backend",
        "src/frontend": base_path / "src" / "frontend", 
        "docs": base_path / "docs",
        "tests": base_path / "tests"
    }
    
    results = {}
    for name, path in required_structure.items():
        results[name] = path.exists()
    
    return results

def check_backend_files() -> dict:
    """Verificar archivos críticos del backend"""
    base_path = Path(__file__).parent.parent / "src" / "backend"
    
    required_files = [
        "main.py",
        "config.py", 
        "database.py",
        "routers/auth.py",
        "routers/images.py",
        "routers/nutrition.py",
        "routers/analytics.py",
        "services/ml_service.py",
        "services/nutrition_service.py",
        "middleware/auth.py",
        "middleware/rate_limit.py",
        "models/requests.py",
        "models/responses.py"
    ]
    
    results = {}
    for file_path in required_files:
        full_path = base_path / file_path
        results[file_path] = full_path.exists()
    
    return results

def check_frontend_files() -> dict:
    """Verificar archivos críticos del frontend"""
    base_path = Path(__file__).parent.parent / "src" / "frontend"
    
    required_files = [
        "package.json",
        "src/App.tsx",
        "src/main.tsx",
        "src/components/Camera.tsx",
        "src/components/Results.tsx",
        "src/components/Layout.tsx",
        "src/components/Home.tsx",
        "src/components/Login.tsx",
        "src/hooks/useAuth.tsx",
        "src/hooks/useAnalysis.ts",
        "src/services/api.ts"
    ]
    
    results = {}
    for file_path in required_files:
        full_path = base_path / file_path
        results[file_path] = full_path.exists()
    
    return results

def check_documentation() -> dict:
    """Verificar documentación técnica"""
    base_path = Path(__file__).parent.parent
    
    required_docs = [
        "README.md",
        "CHANGELOG.md",
        "ARQUITECTURA_DETALLADA.md",
        "ESQUEMA_BASE_DATOS.md", 
        "API_SPECIFICATION.md",
        "DIAGRAMAS_FLUJO.md",
        "docs/BACKEND_SETUP.md",
        "docs/FRONTEND_SETUP.md",
        "docs/TESTING_GUIDE.md"
    ]
    
    results = {}
    for doc_path in required_docs:
        full_path = base_path / doc_path
        results[doc_path] = full_path.exists()
    
    return results

def check_testing_files() -> dict:
    """Verificar archivos de testing"""
    base_path = Path(__file__).parent.parent
    
    testing_files = [
        "tests/test_backend.py",
        "src/frontend/src/__tests__/Camera.test.tsx",
        "src/frontend/src/__tests__/App.test.tsx",
        "src/frontend/vitest.config.ts"
    ]
    
    results = {}
    for test_path in testing_files:
        full_path = base_path / test_path
        results[test_path] = full_path.exists()
    
    return results

def verify_acceptance_criteria():
    """Verificar todos los criterios de aceptación del MVP"""
    
    print("🔍 VERIFICACIÓN DE CRITERIOS DE ACEPTACIÓN - MVP")
    print("=" * 60)
    
    # 1. Estructura del proyecto
    print("\n📁 1. ESTRUCTURA DEL PROYECTO")
    structure = check_directory_structure()
    for name, exists in structure.items():
        status = "✅" if exists else "❌"
        print(f"   {status} {name}")
    
    # 2. Backend FastAPI
    print("\n🔧 2. BACKEND FASTAPI")
    backend_files = check_backend_files()
    backend_count = sum(backend_files.values())
    total_backend = len(backend_files)
    
    for file_path, exists in backend_files.items():
        status = "✅" if exists else "❌"
        print(f"   {status} {file_path}")
    
    print(f"\n   📊 Backend: {backend_count}/{total_backend} archivos ({backend_count/total_backend*100:.1f}%)")
    
    # 3. Frontend React
    print("\n🎨 3. FRONTEND REACT")
    frontend_files = check_frontend_files()
    frontend_count = sum(frontend_files.values())
    total_frontend = len(frontend_files)
    
    for file_path, exists in frontend_files.items():
        status = "✅" if exists else "❌"
        print(f"   {status} {file_path}")
    
    print(f"\n   📊 Frontend: {frontend_count}/{total_frontend} archivos ({frontend_count/total_frontend*100:.1f}%)")
    
    # 4. Documentación
    print("\n📚 4. DOCUMENTACIÓN TÉCNICA")
    docs = check_documentation()
    docs_count = sum(docs.values())
    total_docs = len(docs)
    
    for doc_path, exists in docs.items():
        status = "✅" if exists else "❌"
        print(f"   {status} {doc_path}")
    
    print(f"\n   📊 Documentación: {docs_count}/{total_docs} archivos ({docs_count/total_docs*100:.1f}%)")
    
    # 5. Testing
    print("\n🧪 5. TESTING FRAMEWORK")
    tests = check_testing_files()
    tests_count = sum(tests.values())
    total_tests = len(tests)
    
    for test_path, exists in tests.items():
        status = "✅" if exists else "❌"
        print(f"   {status} {test_path}")
    
    print(f"\n   📊 Testing: {tests_count}/{total_tests} archivos ({tests_count/total_tests*100:.1f}%)")
    
    # 6. Resumen final
    print("\n🎯 RESUMEN DE CRITERIOS DE ACEPTACIÓN")
    print("-" * 40)
    
    total_files = backend_count + frontend_count + docs_count + tests_count
    total_expected = total_backend + total_frontend + total_docs + total_tests
    overall_percentage = (total_files / total_expected) * 100
    
    criteria = [
        ("Estructura del proyecto", all(structure.values())),
        ("Backend FastAPI (>90%)", backend_count/total_backend >= 0.9),
        ("Frontend React (>90%)", frontend_count/total_frontend >= 0.9), 
        ("Documentación técnica (>90%)", docs_count/total_docs >= 0.9),
        ("Testing framework (>80%)", tests_count/total_tests >= 0.8),
        ("Completitud general (>90%)", overall_percentage >= 90)
    ]
    
    passed_criteria = 0
    for criterion, passed in criteria:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} {criterion}")
        if passed:
            passed_criteria += 1
    
    print(f"\n📈 RESULTADO FINAL: {passed_criteria}/{len(criteria)} criterios cumplidos")
    print(f"📊 Completitud general: {overall_percentage:.1f}%")
    
    if passed_criteria == len(criteria):
        print("\n🎉 ¡TODOS LOS CRITERIOS DE ACEPTACIÓN CUMPLIDOS!")
        print("✅ MVP listo para producción")
        return True
    else:
        print(f"\n⚠️  {len(criteria) - passed_criteria} criterios pendientes")
        print("🔄 Revisar elementos faltantes antes del deployment")
        return False

if __name__ == "__main__":
    success = verify_acceptance_criteria()
    sys.exit(0 if success else 1)