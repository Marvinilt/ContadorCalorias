# 🚀 Guía de Ejecución - Contador de Calorías MVP

## 📋 Prerrequisitos

### Software Necesario
- **Node.js 16+** (para frontend)
- **Python 3.9+** (para backend) 
- **PostgreSQL 13+** (base de datos)
- **Redis 6+** (cache)

### API Keys Requeridas
- **OpenAI API Key** (para análisis de imágenes)
- **USDA API Key** (gratuito)
- **Nutritionix API Keys** (gratuito)

## 🔧 Configuración Inicial

### 1. Clonar y Configurar Proyecto
```bash
git clone https://github.com/Marvinilt/ContadorCalorias.git
cd ContadorCalorias
```

### 2. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus API keys
```

**Contenido del archivo `.env`:**
```env
# API Keys (REQUERIDAS)
OPENAI_API_KEY=tu-openai-api-key-aqui
USDA_API_KEY=tu-usda-api-key-aqui
NUTRITIONIX_APP_ID=tu-nutritionix-app-id
NUTRITIONIX_APP_KEY=tu-nutritionix-app-key

# JWT
JWT_SECRET_KEY=mi-clave-secreta-super-segura

# Database (opcional para demo)
DATABASE_URL=postgresql://user:password@localhost/contador_calorias

# Redis (opcional para demo)
REDIS_URL=redis://localhost:6379/0
```

## 🎯 Ejecución Rápida (Demo Mode)

### Opción 1: Solo Frontend (Modo Demo)
```bash
# 1. Ir al frontend
cd src/frontend

# 2. Instalar dependencias
npm install

# 3. Ejecutar en modo desarrollo
npm run dev
```

**URL**: http://localhost:3000

### Opción 2: Full Stack Completo

#### Terminal 1 - Backend
```bash
# 1. Ir al backend
cd src/backend

# 2. Instalar dependencias
pip install -r requirements-backend.txt

# 3. Ejecutar servidor
python run.py
```

#### Terminal 2 - Frontend
```bash
# 1. Ir al frontend
cd src/frontend

# 2. Instalar dependencias (si no se hizo antes)
npm install

# 3. Ejecutar frontend
npm run dev
```

## 🌐 URLs de la Aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎮 Cómo Usar la Aplicación

### 1. Acceso Inicial
- Abrir http://localhost:3000
- Hacer clic en "Iniciar Sesión"
- **Credenciales de prueba**:
  - Email: `test@example.com`
  - Password: `password123`

### 2. Analizar Alimentos
1. Ir a la sección "Cámara"
2. Subir una imagen de comida (JPG, PNG, WEBP)
3. Hacer clic en "Analizar Imagen"
4. Ver resultados nutricionales

### 3. Ver Analytics
- Ir a la sección "Analytics"
- Ver resumen nutricional diario
- Revisar análisis recientes

## 🔧 Configuración Avanzada

### Base de Datos PostgreSQL
```sql
-- Crear base de datos
CREATE DATABASE contador_calorias;
CREATE USER contador_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE contador_calorias TO contador_user;
```

### Redis (Cache)
```bash
# Windows (con Chocolatey)
choco install redis-64
redis-server

# Ubuntu/Linux
sudo apt install redis-server
redis-server
```

## 🐛 Solución de Problemas

### Error: "No se encontró Python"
```bash
# Instalar Python desde python.org
# O usar Microsoft Store
# Verificar instalación:
python --version
```

### Error: "Module not found"
```bash
# Backend
cd src/backend
pip install -r requirements-backend.txt

# Frontend
cd src/frontend
npm install
```

### Error de CORS
- Verificar que el backend esté ejecutándose en puerto 8000
- Verificar configuración CORS en `src/backend/main.py`

### Error de API Keys
- Verificar que las API keys estén en el archivo `.env`
- Verificar que el archivo `.env` esté en la raíz del proyecto

## 📱 Funcionalidades Disponibles

### ✅ Implementadas
- **Login/Logout**: Autenticación JWT
- **Análisis de Imágenes**: Subir foto y obtener análisis
- **Resultados Nutricionales**: Calorías, proteínas, carbohidratos, grasas
- **Dashboard**: Resumen de análisis recientes
- **Navegación**: Entre todas las secciones

### 🔄 Simuladas (MVP)
- **Análisis ML**: Usa datos de ejemplo (requiere OpenAI API Key real)
- **Base de Datos**: Funciona en memoria (requiere PostgreSQL para persistencia)
- **Cache**: Funciona sin Redis (requiere Redis para performance)

## 🎯 Flujo de Usuario Típico

1. **Acceder**: http://localhost:3000
2. **Login**: test@example.com / password123
3. **Ir a Cámara**: Subir imagen de comida
4. **Analizar**: Hacer clic en "Analizar Imagen"
5. **Ver Resultados**: Información nutricional detallada
6. **Analytics**: Ver resumen en dashboard

## 📊 Datos de Prueba

### Imágenes de Ejemplo
- Usar imágenes de la carpeta `test_images/`
- O subir cualquier imagen de comida (JPG, PNG, WEBP)

### Usuarios de Prueba
- **Email**: test@example.com
- **Password**: password123

## 🚀 Deployment

### Desarrollo Local
```bash
# Backend
cd src/backend && python run.py

# Frontend  
cd src/frontend && npm run dev
```

### Producción
```bash
# Backend
cd src/backend && uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend
cd src/frontend && npm run build && npm run preview
```

---

**Estado**: ✅ MVP Funcional  
**Modo Demo**: Disponible sin configuración completa  
**Modo Full**: Requiere API keys y servicios externos