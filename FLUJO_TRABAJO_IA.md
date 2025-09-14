# Flujo de Trabajo de IA para Desarrollo Profesional de Software

## 🤖 Contexto de IA y Metodología de Desarrollo

### Principios Fundamentales
- **Desarrollo Incremental**: Cada feature se desarrolla completamente antes de pasar a la siguiente
- **Documentaci��n Continua**: Todo cambio debe ser documentado inmediatamente
- **Calidad Primero**: Testing y validación son obligatorios en cada iteración
- **Contexto Actualizado**: La IA mantiene contexto actualizado del estado del proyecto
- **Control de Versiones**: Uso de Git con MCP GitHub para gestión profesional de código
- **Branching Strategy**: GitFlow con branches específicos por tipo de trabajo

## 🔄 Control de Versiones con MCP GitHub

### Estrategia de Branching
```
main (producción)
├── develop (desarrollo)
�?  ├── feature/nombre-funcionalidad
�?  ├── feature/deteccion-alimentos
�?  ├── feature/calculo-calorias
�?  └── feature/interfaz-usuario
├── hotfix/correccion-critica
└── release/v1.0.0
```

### Nomenclatura de Branches
- **Features**: `feature/nombre-funcionalidad`
- **Fixes**: `fix/correccion-funcionalidad-x`
- **Hotfixes**: `hotfix/descripcion-correccion`
- **Releases**: `release/v1.0.0`

### Comandos MCP GitHub Integrados
```bash
# Crear nueva feature branch
git checkout -b feature/deteccion-alimentos

# Commits estructurados
git commit -m "feat(vision): implementar detección básica de alimentos

- Agregar modelo YOLO para detección
- Implementar preprocesamiento de imágenes
- Crear endpoint /detect-food
- Tests unitarios con 90% cobertura

Closes #123"
```

### Convención de Commits
```
<tipo>(<scope>): <descripción>

<cuerpo opcional>

<footer opcional>
```

#### Tipos de Commit
- **feat**: Nueva funcionalidad
- **fix**: Corrección de bug
- **docs**: Cambios en documentación
- **style**: Cambios de formato (no afectan lógica)
- **refactor**: Refactorización de código
- **test**: Agregar o modificar tests
- **chore**: Tareas de mantenimiento

## 📋 Proceso de Desarrollo por Feature

### 1. Análisis y Planificación de Feature
```
ENTRADA: Requerimiento de feature
PROCESO:
├── Análisis de requerimientos
├── Definición de criterios de aceptación
├── Estimación de esfuerzo
├── Identificación de dependencias
├── Creación de issue en GitHub
├── Creación de branch específico
└── Actualización de contexto IA
SALIDA: Feature specification document + Branch activo
```

#### Comandos MCP GitHub para Inicialización
```bash
# Crear issue
gh issue create --title "Feature: Detección de alimentos" --body "Descripción detallada"

# Crear y cambiar a branch
git checkout -b feature/deteccion-alimentos

# Primer commit inicial
git commit -m "feat(setup): inicializar feature detección de alimentos

- Crear estructura base de archivos
- Definir criterios de aceptación
- Configurar tests iniciales

Refs #123"
```

#### Criterios de Aceptación Template
```markdown
## Feature: [NOMBRE_FEATURE]
### Criterios de Aceptación:
- [ ] Funcionalidad principal implementada
- [ ] Tests unitarios con cobertura >85%
- [ ] Tests de integración funcionando
- [ ] Documentación técnica actualizada
- [ ] Documentación de API actualizada
- [ ] UI/UX implementado según diseño
- [ ] Performance dentro de parámetros
- [ ] Seguridad validada
- [ ] Código revisado y aprobado
```

### 2. Diseño de Interfaz y Arquitectura
```
PROCESO DE DISEÑO:
├── Wireframes de UI/UX
├── Definición de componentes
├── Arquitectura de datos
├── Definición de APIs
├── Patrones de diseño aplicables
└── Validación con stakeholders
```

### 3. Implementación de Feature
```
FLUJO DE IMPLEMENTACIÓN:
├── Creación de estructura base
├── Implementación de lógica core
├── Desarrollo de interfaz
├── Integración con servicios
├── Implementación de validaciones
└── Optimización de performance
```

#### Estándares de Código
- **Nomenclatura**: Consistente y descriptiva
- **Comentarios**: Explicar el "por qué", no el "qué"
- **Modularidad**: Funciones pequeñas y específicas
- **Reutilización**: DRY (Don't Repeat Yourself)
- **SOLID**: Principios de diseño orientado a objetos

### 4. Testing Obligatorio
```
NIVELES DE TESTING:
├── Tests Unitarios (>85% cobertura)
├── Tests de Integración
├── Tests de API
├── Tests de UI/UX
├── Tests de Performance
└── Tests de Seguridad
```

#### Template de Testing
```python
# tests/test_[feature_name].py
import pytest
from unittest.mock import Mock, patch

class Test[FeatureName]:
    def setup_method(self):
        """Setup para cada test"""
        pass
    
    def test_[functionality]_success(self):
        """Test caso exitoso"""
        pass
    
    def test_[functionality]_error_handling(self):
        """Test manejo de errores"""
        pass
    
    def test_[functionality]_edge_cases(self):
        """Test casos límite"""
        pass
```

### 5. Documentación Técnica
```
DOCUMENTACIÓN REQUERIDA:
├── README.md actualizado
├── API Documentation (OpenAPI/Swagger)
├── Architecture Decision Records (ADR)
├── Deployment Guide
├── Troubleshooting Guide
└── Change Log
```

#### Template ADR (Architecture Decision Record)
```markdown
# ADR-[NUMBER]: [TÍTULO]

## Estado
[Propuesto | Aceptado | Rechazado | Obsoleto]

## Contexto
[Descripción del problema y contexto]

## Decisión
[Decisión tomada y justificación]

## Consecuencias
[Impactos positivos y negativos]

## Alternativas Consideradas
[Otras opciones evaluadas]
```

### 6. Validación de Criterios de Aceptación
```
CHECKLIST DE VALIDACIÓN:
├── �?Funcionalidad cumple requerimientos
├── �?Tests pasan exitosamente
├── �?Performance dentro de SLA
├── �?Seguridad validada
├── �?Documentación completa
├── �?UI/UX aprobado
└── �?Code review completado
```

### 7. Actualización de Contexto
```
CONTEXTO A ACTUALIZAR:
├── Estado actual del proyecto
├── Features completadas
├── Dependencias actualizadas
├── Configuraciones modificadas
├── Lecciones aprendidas
└── Próximos pasos
```

## 🔄 Workflow de IA por Feature

### Fase 1: Inicialización
```
PROMPT INICIAL:
"Desarrollar feature [NOMBRE] siguiendo el flujo de trabajo profesional.
Contexto actual: [ESTADO_PROYECTO]
Criterios de aceptación: [CRITERIOS]
Dependencias: [DEPENDENCIAS]"
```

### Fase 2: Desarrollo Iterativo
```
ITERACIÓN:
1. Implementar componente específico
2. Crear tests correspondientes
3. Documentar cambios
4. Validar funcionamiento
5. Actualizar contexto
6. Continuar con siguiente componente
```

### Fase 3: Validación y Cierre
```
VALIDACIÓN FINAL:
1. Ejecutar suite completa de tests
2. Verificar criterios de aceptación
3. Generar documentación final
4. Actualizar contexto global
5. Preparar para siguiente feature
```

## 📁 Estructura de Archivos por Feature

```
feature-[nombre]/
├── src/
�?  ├── components/
�?  ├── services/
�?  ├── utils/
�?  └── types/
├── tests/
�?  ├── unit/
�?  ├── integration/
�?  └── e2e/
├── docs/
�?  ├── README.md
�?  ├── API.md
�?  └── ADR/
├── assets/
�?  ├── wireframes/
�?  └── mockups/
└── CHANGELOG.md
```

## 🎯 Métricas de Calidad

### Métricas Técnicas
- **Cobertura de Tests**: >85%
- **Complejidad Ciclomática**: <10 por función
- **Duplicación de Código**: <5%
- **Deuda Técnica**: Documentada y priorizada

### Métricas de Proceso
- **Tiempo por Feature**: Tracking y análisis
- **Defectos por Feature**: <2 bugs críticos
- **Criterios de Aceptación**: 100% cumplidos
- **Documentación**: 100% actualizada

## 🚀 Comandos de IA Específicos

### Iniciar Nueva Feature
```
/context add PLANIFICACION_PROYECTO.md
/context add FLUJO_TRABAJO_IA.md
Prompt: "Iniciar desarrollo de feature [NOMBRE] siguiendo el flujo profesional"
```

### Validar Feature Completada
```
Prompt: "Validar que feature [NOMBRE] cumple todos los criterios de aceptación y estándares de calidad"
```

### Actualizar Contexto Post-Feature
```
Prompt: "Actualizar contexto del proyecto tras completar feature [NOMBRE]. Incluir estado actual, dependencias y próximos pasos"
```

## 📋 Templates de Documentación

### CHANGELOG.md Template
```markdown
# Changelog

## [Unreleased]

## [1.0.0] - 2025-09-14
### Added
- Feature [NOMBRE]: [DESCRIPCIÓN]

### Changed
- [CAMBIOS]

### Fixed
- [CORRECCIONES]

### Security
- [MEJORAS DE SEGURIDAD]
```

### README.md Feature Template
```markdown
# Feature: [NOMBRE]

## Descripción
[Descripción detallada de la feature]

## Instalación
[Pasos de instalación específicos]

## Uso
[Ejemplos de uso]

## API
[Documentación de endpoints]

## Testing
[Cómo ejecutar tests]

## Contribución
[Guidelines específicos]
```

## 🔧 Herramientas de Calidad

### Linting y Formatting
- **Python**: black, flake8, mypy
- **JavaScript**: ESLint, Prettier
- **Documentación**: markdownlint

### Testing Tools
- **Python**: pytest, coverage.py
- **JavaScript**: Jest, Cypress
- **API**: Postman, Newman

### CI/CD Pipeline
```yaml
# .github/workflows/feature-validation.yml
name: Feature Validation
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: pytest --cov=src tests/
      - name: Lint Code
        run: flake8 src/
      - name: Check Documentation
        run: markdownlint docs/
```

---

**Nota**: Este flujo debe seguirse estrictamente para mantener la calidad y consistencia del proyecto. Cada feature debe completar todo el ciclo antes de proceder con la siguiente.
