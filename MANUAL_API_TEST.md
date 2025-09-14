# Prueba Manual de APIs - Contador de Calorías

## 🚨 Problema Detectado
Python no está correctamente configurado en el sistema. 

## 🔧 Solución Rápida

### Opción 1: Instalar Python desde Microsoft Store
1. Abrir Microsoft Store
2. Buscar "Python 3.11" o "Python 3.12"
3. Instalar la versión más reciente
4. Reiniciar terminal

### Opción 2: Instalar desde python.org
1. Ir a https://www.python.org/downloads/
2. Descargar Python 3.9+ para Windows
3. **IMPORTANTE**: Marcar "Add Python to PATH" durante instalación
4. Reiniciar terminal

## 🧪 Pruebas Manuales de APIs

Mientras tanto, puedes probar las APIs manualmente:

### 1. USDA Food Data Central API

**URL de prueba:**
```
https://api.nal.usda.gov/fdc/v1/foods/search?query=apple&api_key=YOUR_USDA_API_KEY&pageSize=5
```

**Resultado esperado:** JSON con información nutricional de manzanas

### 2. Nutritionix API

**Comando cURL:**
```bash
curl -X POST https://trackapi.nutritionix.com/v2/natural/nutrients \
  -H "Content-Type: application/json" \
  -H "x-app-id: YOUR_NUTRITIONIX_APP_ID" \
  -H "x-app-key: YOUR_NUTRITIONIX_APP_KEY" \
  -d '{"query":"1 medium apple"}'
```

**Resultado esperado:** JSON con calorías y macronutrientes

### 3. OpenAI Vision API

**Comando cURL:**
```bash
curl -X POST https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Responde solo: API funcionando"}],
    "max_tokens": 10
  }'
```

**Resultado esperado:** Respuesta de texto confirmando conexión

## 📊 Evaluación Manual

### Criterios de Éxito:
- ✅ **USDA API**: Devuelve información nutricional
- ✅ **Nutritionix API**: Calcula calorías correctamente  
- ✅ **OpenAI API**: Responde a requests básicos

### Métricas a Evaluar:
1. **Tiempo de respuesta** (< 5 segundos)
2. **Precisión de datos** (información coherente)
3. **Disponibilidad** (APIs responden consistentemente)

## 🎯 Resultados Esperados

Basado en la investigación previa:

### USDA API:
- ✅ **Gratuito** y confiable
- ✅ **300k+ alimentos** en base de datos
- ✅ **Datos oficiales** del gobierno de EE.UU.

### Nutritionix API:
- ✅ **500 requests/día** gratuitos
- ✅ **Reconocimiento natural** ("1 manzana mediana")
- ✅ **Incluye restaurantes** y marcas comerciales

### OpenAI Vision API:
- ✅ **Alta precisión** para reconocimiento de alimentos
- ⚠️  **Costo**: ~$0.01 por imagen
- ✅ **Análisis contextual** avanzado

## 🚀 Próximos Pasos

Una vez que Python esté configurado:

1. **Ejecutar pruebas automatizadas:**
   ```bash
   python scripts/simple_api_test.py
   ```

2. **Ejecutar comparación completa:**
   ```bash
   python scripts/api_comparison.py
   ```

3. **Continuar con Fase 1 - Días 5-7:**
   - Diseño de arquitectura detallada
   - Diagramas de flujo de datos
   - Esquema de base de datos

## 📝 Documentar Resultados

Cuando completes las pruebas, documenta:
- Tiempo de respuesta de cada API
- Precisión de los datos obtenidos
- Cualquier error o limitación encontrada
- Recomendación final de stack tecnológico

---

**Estado actual**: APIs configuradas, esperando pruebas técnicas
**Siguiente fase**: Diseño de arquitectura detallada