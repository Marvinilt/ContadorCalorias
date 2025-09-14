# Guía de Configuración - Contador de Calorías por Foto

## 🚀 Configuración Rápida

### 1. Prerrequisitos
- Python 3.9+
- Git configurado
- Conexión a internet

### 2. Instalación Automática
```bash
# Ejecutar script de configuración
python scripts/setup_environment.py
```

### 3. Configuración Manual (Alternativa)

#### Instalar dependencias:
```bash
pip install -r requirements.txt
```

#### Configurar variables de entorno:
```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus API keys
```

## 🔑 Obtener API Keys

### OpenAI Vision API
1. Ir a https://platform.openai.com/
2. Crear cuenta o iniciar sesión
3. Ir a API Keys
4. Crear nueva API key
5. Copiar key que empieza con `sk-`

**Costo**: ~$0.01 por imagen

### USDA Food Data Central (Gratuito)
1. Ir a https://fdc.nal.usda.gov/api-guide.html
2. Registrarse para obtener API key
3. Verificar email
4. Copiar API key

**Costo**: Gratuito

### Nutritionix API
1. Ir a https://www.nutritionix.com/business/api
2. Crear cuenta desarrollador
3. Obtener App ID y App Key
4. Plan gratuito: 500 requests/día

**Costo**: Gratuito hasta 500/día

## 📸 Imágenes de Prueba

### Agregar imágenes en `test_images/`:
- `apple.jpg` - Una manzana
- `banana.jpg` - Un plátano  
- `chicken.jpg` - Pechuga de pollo
- `mixed_meal.jpg` - Plato con varios alimentos
- `pizza_slice.jpg` - Porción de pizza

### Especificaciones:
- **Formatos**: JPG, PNG
- **Tamaño**: 1024x1024 o menor
- **Calidad**: Buena iluminación, enfoque claro

## 🧪 Ejecutar Pruebas

### Prueba básica de APIs:
```bash
python scripts/test_apis.py
```

### Comparación completa:
```bash
python scripts/api_comparison.py
```

### Verificar configuración:
```bash
python scripts/setup_environment.py
```

## 📊 Interpretar Resultados

### Archivos generados:
- `api_test_results_YYYYMMDD_HHMMSS.json` - Resultados detallados
- `results/api_comparison_YYYYMMDD_HHMMSS.json` - Análisis comparativo

### Métricas clave:
- **Tasa de éxito**: % de imágenes procesadas correctamente
- **Tiempo de procesamiento**: Segundos por imagen
- **Costo por imagen**: USD por análisis
- **Precisión**: Calidad del reconocimiento

## 🔧 Solución de Problemas

### Error: "API key not found"
- Verificar que `.env` existe
- Confirmar que las keys están correctas
- No incluir espacios extra

### Error: "Image not found"
- Verificar que las imágenes están en `test_images/`
- Confirmar formato (JPG, PNG)
- Verificar permisos de archivo

### Error: "Connection timeout"
- Verificar conexión a internet
- Intentar nuevamente (APIs pueden tener latencia)
- Verificar límites de rate limiting

### Error: "Invalid API response"
- Verificar que la API key es válida
- Confirmar que tienes créditos/requests disponibles
- Revisar documentación de la API

## 📈 Próximos Pasos

Después de completar las pruebas:

1. **Analizar resultados** de precisión y costos
2. **Seleccionar stack** definitivo para MVP
3. **Continuar con Fase 1 - Semana 2**: Prototipado
4. **Documentar decisiones** en ADR (Architecture Decision Records)

## 📞 Soporte

Si encuentras problemas:
1. Revisar logs en consola
2. Verificar archivos de resultados
3. Consultar documentación de APIs
4. Revisar issues en el repositorio