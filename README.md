# 📸 Contador de Calorías por Fotografía

Aplicación que utiliza inteligencia artificial para analizar fotografías de alimentos y calcular automáticamente las calorías contenidas en los mismos.

## 🚀 Estado del Proyecto

**Fase Actual:** Investigación y Análisis (Semana 1)
**Progreso:** 🟡 En desarrollo

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   ML Service    │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (PostgreSQL)  │
                       └─────────────────┘
```

## 🛠️ Stack Tecnológico

- **Frontend**: React.js, Tailwind CSS
- **Backend**: Python, FastAPI, Uvicorn
- **ML/AI**: OpenAI Vision API, OpenCV, YOLO
- **Base de Datos**: PostgreSQL, Redis
- **APIs**: USDA Food Data Central, Nutritionix API

## 📁 Estructura del Proyecto

```
ContadorCalorias/
├── docs/                   # Documentación
├── src/                    # Código fuente
│   ├── frontend/          # Aplicación React
│   ├── backend/           # API FastAPI
│   └── ml/                # Modelos ML
├── tests/                 # Pruebas
├── config/                # Configuraciones
├── scripts/               # Scripts utilidad
├── CHANGELOG.md           # Cambios
├── PLANIFICACION_PROYECTO.md
├── TECHNICAL_DOCS.md
├── FLUJO_TRABAJO_IA.md
└── INVESTIGACION_APIS.md
```

## 🎯 Funcionalidades MVP

- [x] Configuración inicial del proyecto
- [ ] Captura de fotografías de alimentos
- [ ] Reconocimiento automático de alimentos
- [ ] Estimación de porciones
- [ ] Cálculo de calorías y macronutrientes
- [ ] Visualización de resultados

## 📋 Instalación y Desarrollo

### Prerrequisitos
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+

### Configuración
```bash
# Clonar repositorio
git clone https://github.com/Marvinilt/ContadorCalorias.git
cd ContadorCalorias

# Backend
cd src/backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

## 🧪 Testing

```bash
# Backend tests
pytest tests/

# Frontend tests
npm test
```

## 📖 Documentación

- [Planificación del Proyecto](PLANIFICACION_PROYECTO.md)
- [Documentación Técnica](TECHNICAL_DOCS.md)
- [Flujo de Trabajo IA](FLUJO_TRABAJO_IA.md)
- [Investigación APIs](INVESTIGACION_APIS.md)

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

## 📞 Contacto

**Desarrollador**: Marvinilt
**Repositorio**: https://github.com/Marvinilt/ContadorCalorias