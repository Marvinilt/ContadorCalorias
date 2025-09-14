# 🚀 Configuración del Backend - Contador de Calorías

**Fecha**: 14 de Septiembre, 2025  
**Versión**: MVP 1.0

## 📋 Resumen

Guía completa para configurar y ejecutar el backend FastAPI del sistema de análisis nutricional por imágenes.

## 🔧 Prerrequisitos

### Software Requerido
- **Python 3.9+**
- **PostgreSQL 13+**
- **Redis 6+**
- **Git**

### APIs Externas
- **OpenAI API Key** (para Vision API)
- **USDA API Key** (gratuito)
- **Nutritionix API Key** (plan gratuito disponible)

## ⚙️ Instalación

### 1. Clonar Repositorio
```bash
git clone https://github.com/Marvinilt/ContadorCalorias.git
cd ContadorCalorias
```

### 2. Configurar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
# Instalar dependencias del backend
pip install -r requirements-backend.txt
```

### 4. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus API keys
```

**Contenido del archivo `.env`:**
```env
# API Keys
OPENAI_API_KEY=tu-openai-api-key-aqui
USDA_API_KEY=tu-usda-api-key-aqui
NUTRITIONIX_APP_ID=tu-nutritionix-app-id-aqui
NUTRITIONIX_APP_KEY=tu-nutritionix-app-key-aqui

# JWT
JWT_SECRET_KEY=tu-jwt-secret-key-super-seguro

# Database
DATABASE_URL=postgresql://user:password@localhost/contador_calorias

# Redis
REDIS_URL=redis://localhost:6379/0

# Environment
ENVIRONMENT=development
DEBUG=True
```

### 5. Configurar Base de Datos

#### PostgreSQL
```sql
-- Crear base de datos
CREATE DATABASE contador_calorias;
CREATE USER contador_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE contador_calorias TO contador_user;
```

#### Redis
```bash
# Instalar Redis (Windows con Chocolatey)
choco install redis-64

# Instalar Redis (Ubuntu)
sudo apt install redis-server

# Iniciar Redis
redis-server
```

## 🚀 Ejecución

### Desarrollo
```bash
# Navegar al directorio del backend
cd src/backend

# Ejecutar servidor de desarrollo
python run.py
```

### Producción
```bash
# Con Uvicorn directamente
uvicorn main:app --host 0.0.0.0 --port 8000

# Con Gunicorn (recomendado para producción)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📊 Verificación

### Health Check
```bash
curl http://localhost:8000/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-14T12:00:00Z",
  "services": {
    "database": "connected",
    "cache": "connected",
    "ml_service": "available"
  }
}
```

### Documentación API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Ejecutar Pruebas
```bash
# Todas las pruebas
pytest tests/ -v

# Pruebas específicas
pytest tests/test_backend.py -v

# Con cobertura
pytest tests/ --cov=src/backend --cov-report=html
```

### Pruebas Manuales

#### Autenticación
```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"
```

#### Análisis de Imagen
```bash
# Subir imagen para análisis
curl -X POST "http://localhost:8000/api/v1/analyze/image" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "image=@test_image.jpg"
```

## 📁 Estructura del Proyecto

```
src/backend/
├── main.py                 # Aplicación principal FastAPI
├── config.py              # Configuración
├── database.py            # Conexión a base de datos
├── run.py                 # Script de ejecución
├── routers/               # Endpoints REST
│   ├── auth.py           # Autenticación
│   ├── images.py         # Análisis de imágenes
│   ├── nutrition.py      # Datos nutricionales
│   └── analytics.py      # Estadísticas
├── services/             # Lógica de negocio
│   ├── ml_service.py     # Servicio ML
│   └── nutrition_service.py # Servicio nutrición
├── middleware/           # Middleware personalizado
│   ├── auth.py          # Autenticación JWT
│   ├── rate_limit.py    # Rate limiting
│   └── logging.py       # Logging
└── models/              # Modelos Pydantic
    ├── requests.py      # Modelos de request
    └── responses.py     # Modelos de response
```

## 🔒 Seguridad

### Configuración de Producción
```env
# Cambiar en producción
JWT_SECRET_KEY=clave-super-segura-de-256-bits
DEBUG=False
ENVIRONMENT=production

# HTTPS obligatorio
CORS_ORIGINS=["https://tu-dominio.com"]
ALLOWED_HOSTS=["tu-dominio.com"]
```

### Rate Limiting
- **Análisis de imágenes**: 10 requests/minuto
- **Búsqueda de alimentos**: 100 requests/minuto
- **Login**: 5 requests/minuto
- **Registro**: 3 requests/minuto

## 📈 Monitoreo

### Logs
```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Logs de análisis específicos
grep "Analysis Request" logs/app.log
```

### Métricas
- **Tiempo de respuesta**: Header `X-Process-Time`
- **Rate limiting**: Headers `X-RateLimit-*`
- **Health checks**: `/health` endpoint

## 🐛 Troubleshooting

### Problemas Comunes

#### Error de conexión a PostgreSQL
```bash
# Verificar que PostgreSQL esté ejecutándose
pg_isready -h localhost -p 5432

# Verificar credenciales en .env
```

#### Error de conexión a Redis
```bash
# Verificar que Redis esté ejecutándose
redis-cli ping

# Debería responder: PONG
```

#### Error de API Keys
```bash
# Verificar que las API keys estén configuradas
python -c "from config import settings; print(settings.OPENAI_API_KEY[:10])"
```

### Logs de Debug
```python
# Habilitar logs detallados
import logging
logging.getLogger("contador_calorias").setLevel(logging.DEBUG)
```

## 🔄 Actualizaciones

### Actualizar Dependencias
```bash
pip install -r requirements-backend.txt --upgrade
```

### Migraciones de Base de Datos
```bash
# Cuando se implementen con Alembic
alembic upgrade head
```

---

**Estado**: ✅ Backend MVP funcional  
**Siguiente**: Implementación del frontend React  
**Soporte**: Ver documentación en `/docs` o crear issue en GitHub