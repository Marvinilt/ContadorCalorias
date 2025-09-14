# 🧪 Guía de Testing - Contador de Calorías

**Fecha**: 14 de Septiembre, 2025  
**Versión**: MVP 1.0

## 📋 Resumen

Guía completa para ejecutar y mantener las pruebas del sistema de análisis nutricional por imágenes.

## 🎯 Estrategia de Testing

### Niveles de Testing
1. **Unit Tests** - Funciones individuales
2. **Integration Tests** - Servicios y APIs
3. **End-to-End Tests** - Flujo completo de usuario
4. **Performance Tests** - Carga y rendimiento

### Cobertura Objetivo
- **Backend**: >90% cobertura de código
- **Frontend**: >85% cobertura de componentes
- **APIs**: 100% endpoints críticos

## 🔧 Configuración de Testing

### Backend (FastAPI)
```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio pytest-cov httpx

# Ejecutar todas las pruebas
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=src/backend --cov-report=html

# Pruebas específicas
pytest tests/test_backend.py::TestAuthEndpoints -v
```

### Variables de Entorno para Testing
```env
# .env.test
ENVIRONMENT=testing
DATABASE_URL=postgresql://test_user:test_pass@localhost/test_contador_calorias
REDIS_URL=redis://localhost:6379/1
OPENAI_API_KEY=test_key
USDA_API_KEY=test_key
NUTRITIONIX_APP_ID=test_id
NUTRITIONIX_APP_KEY=test_key
```

## 📊 Pruebas del Backend

### Estructura de Pruebas
```
tests/
├── test_backend.py         # Pruebas principales
├── test_ml_service.py      # Servicio ML
├── test_nutrition_service.py # Servicio nutrición
├── test_auth.py           # Autenticación
├── test_rate_limiting.py  # Rate limiting
└── fixtures/              # Datos de prueba
    ├── test_images/       # Imágenes de prueba
    └── mock_responses/    # Respuestas simuladas
```

### Casos de Prueba Críticos

#### 1. Autenticación
```python
def test_login_success():
    """Verificar login exitoso"""
    response = client.post("/api/v1/auth/login", data={
        "username": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()["tokens"]

def test_protected_endpoint_without_token():
    """Verificar protección de endpoints"""
    response = client.get("/api/v1/analytics/daily-summary")
    assert response.status_code == 401
```

#### 2. Análisis de Imágenes
```python
@pytest.mark.asyncio
async def test_image_analysis_flow():
    """Probar flujo completo de análisis"""
    # 1. Subir imagen
    with open("tests/fixtures/test_images/apple.jpg", "rb") as f:
        response = client.post(
            "/api/v1/analyze/image",
            files={"image": f},
            headers={"Authorization": "Bearer test_token"}
        )
    
    assert response.status_code == 202
    analysis_id = response.json()["analysis_id"]
    
    # 2. Verificar resultado
    response = client.get(
        f"/api/v1/analyze/{analysis_id}",
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert "detected_foods" in response.json()
```

#### 3. Rate Limiting
```python
def test_rate_limiting():
    """Verificar límites de requests"""
    # Hacer múltiples requests
    for i in range(12):  # Más del límite de 10
        response = client.post("/api/v1/analyze/image", 
                             files={"image": ("test.jpg", b"fake", "image/jpeg")})
    
    # Verificar que se aplique rate limiting
    assert any(r.status_code == 429 for r in responses)
```

### Mocks y Fixtures

#### Mock de OpenAI API
```python
@patch('services.ml_service.openai.AsyncOpenAI')
async def test_ml_service_mock(mock_openai):
    mock_response = AsyncMock()
    mock_response.choices[0].message.content = '''
    {
      "foods": [{"name": "manzana", "portion_grams": 150, "confidence": 8}]
    }
    '''
    mock_openai.return_value.chat.completions.create.return_value = mock_response
    
    ml_service = MLService()
    result = await ml_service.analyze_food_image(b"fake_image")
    assert len(result) == 1
```

## 🚀 Pruebas de Performance

### Load Testing con Locust
```python
# locustfile.py
from locust import HttpUser, task, between

class CalorieCounterUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login y obtener token
        response = self.client.post("/api/v1/auth/login", data={
            "username": "test@example.com",
            "password": "password123"
        })
        self.token = response.json()["tokens"]["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def search_foods(self):
        self.client.get("/api/v1/foods/search?q=apple", headers=self.headers)
    
    @task(1)
    def analyze_image(self):
        with open("test_image.jpg", "rb") as f:
            self.client.post("/api/v1/analyze/image", 
                           files={"image": f}, headers=self.headers)
```

### Ejecutar Load Tests
```bash
# Instalar Locust
pip install locust

# Ejecutar pruebas de carga
locust -f locustfile.py --host=http://localhost:8000
```

## 📈 Métricas de Performance

### Objetivos de Performance
| Endpoint | Tiempo Objetivo | Throughput |
|----------|----------------|------------|
| `/health` | <100ms | 1000 req/s |
| `/auth/login` | <500ms | 100 req/s |
| `/foods/search` | <1s | 200 req/s |
| `/analyze/image` | <5s | 10 req/s |

### Monitoreo
```python
# Middleware de métricas
class MetricsMiddleware:
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Registrar métricas
        metrics.record_request_time(request.url.path, process_time)
        metrics.record_status_code(response.status_code)
        
        return response
```

## 🔍 Testing de APIs Externas

### Mock de USDA API
```python
@pytest.fixture
def mock_usda_response():
    return {
        "foods": [{
            "description": "Apple, raw",
            "foodNutrients": [
                {"nutrientName": "Energy", "value": 52},
                {"nutrientName": "Protein", "value": 0.26}
            ]
        }]
    }

@patch('aiohttp.ClientSession.get')
async def test_usda_integration(mock_get, mock_usda_response):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = mock_usda_response
    mock_get.return_value.__aenter__.return_value = mock_response
    
    service = NutritionService()
    result = await service._search_usda("apple")
    assert result is not None
```

## 🛡️ Security Testing

### Pruebas de Seguridad
```python
def test_sql_injection_protection():
    """Verificar protección contra SQL injection"""
    malicious_input = "'; DROP TABLE users; --"
    response = client.get(f"/api/v1/foods/search?q={malicious_input}")
    assert response.status_code != 500

def test_jwt_token_validation():
    """Verificar validación de tokens JWT"""
    invalid_token = "invalid.jwt.token"
    response = client.get("/api/v1/analytics/daily-summary",
                         headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401

def test_rate_limiting_bypass_attempt():
    """Verificar que no se pueda evadir rate limiting"""
    # Intentar con diferentes IPs
    headers = {"X-Forwarded-For": "192.168.1.100"}
    responses = []
    for i in range(15):
        response = client.post("/api/v1/analyze/image", headers=headers)
        responses.append(response.status_code)
    
    assert 429 in responses
```

## 📊 Reportes de Testing

### Cobertura de Código
```bash
# Generar reporte HTML
pytest --cov=src/backend --cov-report=html

# Ver reporte
open htmlcov/index.html
```

### Reporte de Performance
```bash
# Con pytest-benchmark
pytest tests/test_performance.py --benchmark-only --benchmark-html=benchmark.html
```

## 🔄 CI/CD Testing

### GitHub Actions
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:6
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements-backend.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src/backend --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## 🐛 Debugging Tests

### Debugging con pytest
```bash
# Ejecutar con debugging
pytest tests/test_backend.py::test_specific -v -s --pdb

# Ver logs detallados
pytest tests/ -v -s --log-cli-level=DEBUG

# Ejecutar solo tests fallidos
pytest --lf
```

### Debugging Async Tests
```python
import asyncio
import pytest

@pytest.mark.asyncio
async def test_async_function():
    # Usar breakpoint en código async
    import pdb; pdb.set_trace()
    result = await some_async_function()
    assert result is not None
```

---

**Estado**: ✅ Testing framework implementado  
**Cobertura actual**: Backend >85%  
**Siguiente**: Frontend testing + E2E tests