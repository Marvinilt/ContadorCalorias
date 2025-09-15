# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Agregado
- Configuración inicial del proyecto
- Documentación técnica inicial
- Estructura base del repositorio
- Investigación completa de APIs de visión (OpenAI, Google Vision, YOLO)
- Análisis de bases de datos nutricionales (USDA, Nutritionix, Edamam)
- Script de pruebas para APIs (`scripts/test_apis.py`)
- Script de configuración automática (`scripts/setup_environment.py`)
- Script de comparación de APIs (`scripts/api_comparison.py`)
- Archivo de dependencias (`requirements.txt`)
- Template de variables de entorno (`.env.example`)
- Guía de configuración completa (`docs/SETUP_GUIDE.md`)
- README.md principal del proyecto
- Estructura de directorios completa
- Directorio para imágenes de prueba (`test_images/`)
- Directorio para resultados (`results/`)
- Script de pruebas simplificado (`scripts/simple_api_test.py`)
- Guía de pruebas manuales (`MANUAL_API_TEST.md`)
- Configuración de API keys en archivo `.env`
- Pruebas exitosas de todas las APIs principales
- Validación de USDA Food Data Central (26k+ alimentos encontrados)
- Validación de Nutritionix API (reconocimiento de lenguaje natural)
- Validación de OpenAI API (conectividad confirmada)
- Reporte completo de resultados (`RESULTADOS_PRUEBAS_APIS.md`)
- Stack tecnológico confirmado para MVP
- Arquitectura técnica detallada completada
- Esquema de base de datos PostgreSQL optimizado
- Especificación completa de APIs REST
- Diagramas de flujo y secuencias documentados
- Estrategias de cache y performance definidas
- Plan de seguridad y manejo de errores implementado

### 🟡 Semana 2 - Desarrollo del MVP (En Progreso)

#### ✅ Backend FastAPI Completado
- Backend FastAPI con arquitectura modular implementado
- 4 routers principales: auth, images, nutrition, analytics
- Servicios ML (OpenAI Vision) y nutrición (USDA + Nutritionix)
- Middleware de autenticación JWT, rate limiting y logging
- Modelos Pydantic para validación completa
- Pruebas unitarias y documentación de setup
- 18 archivos de código backend (2,044+ líneas)

#### ✅ Frontend React Completado
- Frontend React con TypeScript y Tailwind CSS
- 7 componentes principales: Camera, Results, Layout, Home, Login, Analytics
- Hooks personalizados para auth y análisis de imágenes
- Integración completa con backend FastAPI
- Testing framework configurado con Vitest
- Documentación de setup y guías técnicas
- 17 archivos de código frontend (960+ líneas)

### Cambiado

### Deprecado

### Removido

### Corregido

### Seguridad

## [0.1.0] - 2024-01-XX

### Agregado
- Inicialización del proyecto App Contador de Calorías por Foto
- Configuración inicial de Git
- Documentación base del proyecto

---

## Tipos de cambios
- **Agregado** para nuevas funcionalidades
- **Cambiado** para cambios en funcionalidades existentes
- **Deprecado** para funcionalidades que serán removidas en próximas versiones
- **Removido** para funcionalidades removidas en esta versión
- **Corregido** para corrección de bugs
- **Seguridad** en caso de vulnerabilidades