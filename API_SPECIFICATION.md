# 🔌 Especificación de APIs - Contador de Calorías

**Fecha**: 14 de Septiembre, 2025  
**Versión**: v1.0  
**Base URL**: `https://api.contador-calorias.com/v1`

## 📋 Resumen

Especificación completa de las APIs REST para el sistema de análisis nutricional por imágenes. Diseño RESTful con autenticación JWT y documentación OpenAPI.

## 🔐 Autenticación

### JWT Bearer Token
```http
Authorization: Bearer <jwt_token>
```

### Endpoints de Autenticación

#### `POST /auth/register`
Registro de nuevo usuario.

**Request Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "password123",
  "profile": {
    "first_name": "Juan",
    "last_name": "Pérez",
    "date_of_birth": "1990-05-15",
    "height_cm": 175,
    "weight_kg": 70,
    "activity_level": "moderate"
  }
}
```

**Response (201):**
```json
{
  "user": {
    "id": 123,
    "email": "usuario@ejemplo.com",
    "profile": { ... },
    "created_at": "2025-09-14T10:30:00Z"
  },
  "tokens": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires_in": 1800
  }
}
```

#### `POST /auth/login`
Inicio de sesión.

**Request Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "user": {
    "id": 123,
    "email": "usuario@ejemplo.com",
    "profile": { ... }
  },
  "tokens": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires_in": 1800
  }
}
```

#### `POST /auth/refresh`
Renovar token de acceso.

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 🖼️ Análisis de Imágenes

### `POST /analyze/image`
Analizar imagen de alimentos y calcular información nutricional.

**Headers:**
```http
Content-Type: multipart/form-data
Authorization: Bearer <jwt_token>
```

**Request Body (multipart/form-data):**
```
image: <file> (required) - Imagen en formato JPG, PNG, WEBP (max 5MB)
meal_type: string (optional) - "breakfast", "lunch", "dinner", "snack"
notes: string (optional) - Notas adicionales del usuario
```

**Response (202 - Accepted):**
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "estimated_completion": "2025-09-14T10:35:00Z",
  "message": "Análisis en progreso. Use GET /analyze/{analysis_id} para verificar estado."
}
```

### `GET /analyze/{analysis_id}`
Obtener resultado del análisis.

**Response (200 - Completed):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "confidence_score": 8,
  "processing_time_ms": 3450,
  "total_nutrition": {
    "calories": 245.5,
    "protein": 12.3,
    "carbs": 35.7,
    "fat": 8.9,
    "fiber": 4.2,
    "sugar": 18.5,
    "sodium": 125.0
  },
  "detected_foods": [
    {
      "id": 1,
      "name": "Manzana roja",
      "name_normalized": "apple_red",
      "portion": {
        "grams": 182,
        "description": "1 manzana mediana"
      },
      "nutrition": {
        "calories": 94.6,
        "protein": 0.5,
        "carbs": 25.1,
        "fat": 0.3,
        "fiber": 4.4,
        "sugar": 18.9
      },
      "confidence": 9,
      "category": "fruits",
      "source": "usda"
    },
    {
      "id": 2,
      "name": "Pan integral",
      "name_normalized": "whole_wheat_bread",
      "portion": {
        "grams": 60,
        "description": "2 rebanadas"
      },
      "nutrition": {
        "calories": 150.9,
        "protein": 11.8,
        "carbs": 10.6,
        "fat": 8.6,
        "fiber": -0.2,
        "sugar": -0.4
      },
      "confidence": 7,
      "category": "grains",
      "source": "nutritionix"
    }
  ],
  "image": {
    "hash": "a1b2c3d4e5f6...",
    "url": "https://storage.contador-calorias.com/images/550e8400...",
    "dimensions": {
      "width": 1920,
      "height": 1080
    },
    "size_bytes": 2048576
  },
  "metadata": {
    "meal_type": "breakfast",
    "notes": "Desayuno saludable",
    "device_info": "iPhone 14 Pro",
    "location": {
      "lat": 40.7128,
      "lng": -74.0060
    }
  },
  "created_at": "2025-09-14T10:30:00Z",
  "completed_at": "2025-09-14T10:33:45Z"
}
```

**Response (202 - Processing):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 65,
  "current_step": "Analizando información nutricional",
  "estimated_completion": "2025-09-14T10:35:00Z"
}
```

**Response (422 - Failed):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "error": {
    "code": "ANALYSIS_FAILED",
    "message": "No se pudieron detectar alimentos en la imagen",
    "details": "La imagen no contiene alimentos reconocibles o la calidad es insuficiente"
  },
  "created_at": "2025-09-14T10:30:00Z",
  "failed_at": "2025-09-14T10:32:15Z"
}
```

## 🍎 Búsqueda de Alimentos

### `GET /foods/search`
Buscar alimentos en la base de datos.

**Query Parameters:**
```
q: string (required) - Término de búsqueda
limit: integer (optional, default: 10, max: 50) - Número de resultados
source: string (optional) - "usda", "nutritionix", "all" (default)
category: string (optional) - Filtrar por categoría
```

**Example Request:**
```http
GET /foods/search?q=manzana&limit=5&source=usda
```

**Response (200):**
```json
{
  "query": "manzana",
  "total_results": 156,
  "results": [
    {
      "id": "usda_169905",
      "name": "Manzana, cruda, con cáscara",
      "name_normalized": "apple_raw_with_skin",
      "source": "usda",
      "category": "fruits",
      "nutrition_per_100g": {
        "calories": 52,
        "protein": 0.26,
        "carbs": 13.81,
        "fat": 0.17,
        "fiber": 2.4,
        "sugar": 10.39
      },
      "serving_sizes": [
        {
          "description": "1 manzana mediana",
          "grams": 182
        },
        {
          "description": "1 taza en rodajas",
          "grams": 109
        }
      ],
      "confidence": 10,
      "usage_count": 1247
    }
  ],
  "suggestions": [
    "manzana verde",
    "manzana roja",
    "jugo de manzana"
  ]
}
```

### `GET /foods/{food_id}`
Obtener información detallada de un alimento específico.

**Response (200):**
```json
{
  "id": "usda_169905",
  "name": "Manzana, cruda, con cáscara",
  "name_normalized": "apple_raw_with_skin",
  "source": "usda",
  "external_id": "169905",
  "category": "fruits",
  "brand": null,
  "barcode": null,
  "nutrition_per_100g": {
    "calories": 52,
    "protein": 0.26,
    "carbs": 13.81,
    "fat": 0.17,
    "fiber": 2.4,
    "sugar": 10.39,
    "sodium": 1,
    "vitamins": {
      "vitamin_c": 4.6,
      "vitamin_a": 54,
      "folate": 3
    },
    "minerals": {
      "calcium": 6,
      "iron": 0.12,
      "potassium": 107,
      "magnesium": 5
    }
  },
  "serving_sizes": [
    {
      "description": "1 manzana mediana (7.5 cm diámetro)",
      "grams": 182,
      "nutrition": {
        "calories": 94.6,
        "protein": 0.47,
        "carbs": 25.1,
        "fat": 0.31
      }
    }
  ],
  "allergens": [],
  "dietary_flags": [
    "vegan",
    "vegetarian",
    "gluten_free",
    "dairy_free"
  ],
  "usage_count": 1247,
  "last_updated": "2025-09-14T08:00:00Z"
}
```

## 👤 Gestión de Usuario

### `GET /users/profile`
Obtener perfil del usuario autenticado.

**Response (200):**
```json
{
  "id": 123,
  "email": "usuario@ejemplo.com",
  "profile": {
    "first_name": "Juan",
    "last_name": "Pérez",
    "date_of_birth": "1990-05-15",
    "gender": "male",
    "height_cm": 175,
    "weight_kg": 70,
    "activity_level": "moderate",
    "dietary_restrictions": ["vegetarian"],
    "daily_calorie_goal": 2200,
    "preferences": {
      "units": "metric",
      "language": "es",
      "notifications": true
    }
  },
  "stats": {
    "total_analyses": 45,
    "total_foods_detected": 127,
    "avg_daily_calories": 1850,
    "streak_days": 12
  },
  "created_at": "2025-08-01T10:00:00Z",
  "updated_at": "2025-09-14T09:15:00Z"
}
```

### `PUT /users/profile`
Actualizar perfil del usuario.

**Request Body:**
```json
{
  "profile": {
    "weight_kg": 68,
    "daily_calorie_goal": 2000,
    "dietary_restrictions": ["vegetarian", "gluten_free"],
    "preferences": {
      "notifications": false
    }
  }
}
```

### `GET /users/history`
Obtener historial de análisis del usuario.

**Query Parameters:**
```
page: integer (optional, default: 1)
limit: integer (optional, default: 20, max: 100)
from_date: string (optional) - ISO 8601 date
to_date: string (optional) - ISO 8601 date
meal_type: string (optional) - "breakfast", "lunch", "dinner", "snack"
```

**Response (200):**
```json
{
  "page": 1,
  "limit": 20,
  "total_pages": 3,
  "total_results": 45,
  "analyses": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "total_calories": 245.5,
      "foods_count": 2,
      "confidence_score": 8,
      "meal_type": "breakfast",
      "created_at": "2025-09-14T10:30:00Z",
      "foods_summary": [
        "Manzana roja (94.6 cal)",
        "Pan integral (150.9 cal)"
      ]
    }
  ]
}
```

## 📊 Analytics y Estadísticas

### `GET /analytics/daily-summary`
Obtener resumen nutricional diario.

**Query Parameters:**
```
date: string (optional, default: today) - YYYY-MM-DD format
days: integer (optional, default: 7, max: 90) - Número de días
```

**Response (200):**
```json
{
  "period": {
    "from": "2025-09-08",
    "to": "2025-09-14",
    "days": 7
  },
  "daily_summaries": [
    {
      "date": "2025-09-14",
      "nutrition": {
        "calories": 1850,
        "protein": 85.2,
        "carbs": 220.5,
        "fat": 65.8,
        "fiber": 28.3
      },
      "goals": {
        "calories": 2200,
        "protein": 110,
        "carbs": 275,
        "fat": 73
      },
      "progress": {
        "calories": 84.1,
        "protein": 77.5,
        "carbs": 80.2,
        "fat": 90.1
      },
      "analyses_count": 3,
      "foods_count": 8,
      "meal_distribution": {
        "breakfast": 420,
        "lunch": 680,
        "dinner": 590,
        "snack": 160
      }
    }
  ],
  "averages": {
    "daily_calories": 1923,
    "daily_protein": 89.1,
    "daily_carbs": 235.7,
    "daily_fat": 68.2
  }
}
```

### `GET /analytics/trends`
Obtener tendencias nutricionales.

**Query Parameters:**
```
period: string (optional, default: "30d") - "7d", "30d", "90d", "1y"
metric: string (optional, default: "calories") - "calories", "protein", "carbs", "fat"
```

**Response (200):**
```json
{
  "period": "30d",
  "metric": "calories",
  "data_points": [
    {
      "date": "2025-08-15",
      "value": 1950,
      "goal": 2200,
      "percentage": 88.6
    }
  ],
  "insights": [
    {
      "type": "trend",
      "message": "Tus calorías promedio han aumentado 5% en las últimas 2 semanas",
      "impact": "positive"
    },
    {
      "type": "goal",
      "message": "Has alcanzado tu meta de calorías 23 de los últimos 30 días",
      "impact": "positive"
    }
  ],
  "statistics": {
    "average": 1923,
    "median": 1890,
    "min": 1420,
    "max": 2450,
    "std_deviation": 245.7,
    "goal_achievement_rate": 76.7
  }
}
```

### `GET /analytics/popular-foods`
Obtener alimentos más consumidos por el usuario.

**Response (200):**
```json
{
  "period": "30d",
  "foods": [
    {
      "name": "Manzana roja",
      "category": "fruits",
      "consumption_count": 18,
      "total_calories": 1702.8,
      "avg_portion_grams": 175,
      "frequency_per_week": 4.2
    }
  ]
}
```

## ⚡ Webhooks

### `POST /webhooks/analysis-completed`
Webhook enviado cuando se completa un análisis.

**Payload:**
```json
{
  "event": "analysis.completed",
  "timestamp": "2025-09-14T10:33:45Z",
  "data": {
    "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": 123,
    "total_calories": 245.5,
    "confidence_score": 8,
    "processing_time_ms": 3450
  }
}
```

## 🚨 Códigos de Error

### Códigos HTTP Estándar
- `200` - OK
- `201` - Created
- `202` - Accepted (procesamiento asíncrono)
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Unprocessable Entity
- `429` - Too Many Requests
- `500` - Internal Server Error

### Estructura de Error
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Los datos proporcionados no son válidos",
    "details": {
      "field": "email",
      "issue": "El formato del email no es válido"
    },
    "timestamp": "2025-09-14T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

### Códigos de Error Específicos
```json
{
  "INVALID_IMAGE_FORMAT": "Formato de imagen no soportado",
  "IMAGE_TOO_LARGE": "La imagen excede el tamaño máximo permitido",
  "NO_FOODS_DETECTED": "No se detectaron alimentos en la imagen",
  "ANALYSIS_TIMEOUT": "El análisis tardó demasiado tiempo",
  "INSUFFICIENT_CREDITS": "Créditos insuficientes para realizar el análisis",
  "RATE_LIMIT_EXCEEDED": "Se ha excedido el límite de requests por minuto",
  "USER_NOT_FOUND": "Usuario no encontrado",
  "INVALID_CREDENTIALS": "Credenciales inválidas",
  "TOKEN_EXPIRED": "El token de acceso ha expirado",
  "FOOD_NOT_FOUND": "Alimento no encontrado en la base de datos"
}
```

## 📝 Rate Limiting

### Límites por Endpoint
```json
{
  "/analyze/image": "10 requests/minute",
  "/foods/search": "100 requests/minute",
  "/auth/login": "5 requests/minute",
  "/auth/register": "3 requests/minute",
  "default": "60 requests/minute"
}
```

### Headers de Rate Limiting
```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1694692800
X-RateLimit-Retry-After: 45
```

---

**Estado**: ✅ Especificación completa  
**Siguiente**: Diagramas de secuencia y validación  
**Formato**: OpenAPI 3.0 compatible