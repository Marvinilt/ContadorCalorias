# 🗄️ Esquema de Base de Datos - Contador de Calorías

**Fecha**: 14 de Septiembre, 2025  
**Versión**: 1.0  
**Motor**: PostgreSQL 15+

## 📋 Resumen

Diseño de base de datos optimizado para el sistema de análisis nutricional por imágenes. Esquema normalizado con índices estratégicos para alta performance.

## 🏗️ Diagrama ERD

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     users       │    │ food_analyses   │    │  detected_foods │
│                 │    │                 │    │                 │
│ • id (PK)       │◄──┤ • id (PK)       │───►│ • id (PK)       │
│ • email         │    │ • user_id (FK)  │    │ • analysis_id   │
│ • password_hash │    │ • image_hash    │    │ • food_name     │
│ • profile       │    │ • total_calories│    │ • portion_grams │
│ • created_at    │    │ • confidence    │    │ • calories      │
│ • updated_at    │    │ • created_at    │    │ • protein       │
└─────────────────┘    └─────────────────┘    │ • carbs         │
                                              │ • fat           │
                                              │ • confidence    │
                                              └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   food_cache    │
                       │                 │
                       │ • id (PK)       │
                       │ • food_name     │
                       │ • nutrition_data│
                       │ • source        │
                       │ • last_updated  │
                       └─────────────────┘
```

## 📊 Tablas Principales

### 1. Tabla `users`
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = true;
CREATE INDEX idx_users_created_at ON users(created_at);

-- Triggers para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

**Campos del perfil (JSONB)**:
```json
{
  "first_name": "string",
  "last_name": "string",
  "date_of_birth": "YYYY-MM-DD",
  "gender": "male|female|other",
  "height_cm": 175,
  "weight_kg": 70,
  "activity_level": "sedentary|light|moderate|active|very_active",
  "dietary_restrictions": ["vegetarian", "gluten_free"],
  "daily_calorie_goal": 2000,
  "preferences": {
    "units": "metric|imperial",
    "language": "es|en",
    "notifications": true
  }
}
```

### 2. Tabla `food_analyses`
```sql
CREATE TABLE food_analyses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    image_hash VARCHAR(64) NOT NULL,
    image_url VARCHAR(500),
    total_calories DECIMAL(8,2) NOT NULL DEFAULT 0,
    total_protein DECIMAL(8,2) NOT NULL DEFAULT 0,
    total_carbs DECIMAL(8,2) NOT NULL DEFAULT 0,
    total_fat DECIMAL(8,2) NOT NULL DEFAULT 0,
    total_fiber DECIMAL(8,2) NOT NULL DEFAULT 0,
    confidence_score INTEGER CHECK (confidence_score >= 1 AND confidence_score <= 10),
    processing_time_ms INTEGER,
    ml_model_version VARCHAR(50) DEFAULT 'gpt-4-vision-preview',
    status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('processing', 'completed', 'failed')),
    error_message TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_food_analyses_user_id ON food_analyses(user_id);
CREATE INDEX idx_food_analyses_created_at ON food_analyses(created_at);
CREATE INDEX idx_food_analyses_status ON food_analyses(status);
CREATE INDEX idx_food_analyses_image_hash ON food_analyses(image_hash);
CREATE INDEX idx_food_analyses_user_date ON food_analyses(user_id, created_at);

-- Índice compuesto para consultas de dashboard
CREATE INDEX idx_food_analyses_user_status_date 
    ON food_analyses(user_id, status, created_at) 
    WHERE status = 'completed';
```

**Campos de metadata (JSONB)**:
```json
{
  "image_dimensions": {"width": 1920, "height": 1080},
  "image_size_bytes": 2048576,
  "device_info": "iPhone 14 Pro",
  "location": {"lat": 40.7128, "lng": -74.0060},
  "meal_type": "breakfast|lunch|dinner|snack",
  "notes": "Usuario agregó notas adicionales"
}
```

### 3. Tabla `detected_foods`
```sql
CREATE TABLE detected_foods (
    id SERIAL PRIMARY KEY,
    analysis_id INTEGER NOT NULL REFERENCES food_analyses(id) ON DELETE CASCADE,
    food_name VARCHAR(255) NOT NULL,
    food_name_normalized VARCHAR(255) NOT NULL,
    portion_grams DECIMAL(8,2) NOT NULL,
    portion_description VARCHAR(100),
    calories DECIMAL(8,2) NOT NULL DEFAULT 0,
    protein DECIMAL(8,2) NOT NULL DEFAULT 0,
    carbs DECIMAL(8,2) NOT NULL DEFAULT 0,
    fat DECIMAL(8,2) NOT NULL DEFAULT 0,
    fiber DECIMAL(8,2) NOT NULL DEFAULT 0,
    sugar DECIMAL(8,2) NOT NULL DEFAULT 0,
    sodium DECIMAL(8,2) NOT NULL DEFAULT 0,
    confidence INTEGER CHECK (confidence >= 1 AND confidence <= 10),
    nutrition_source VARCHAR(50) NOT NULL, -- 'usda', 'nutritionix', 'manual'
    food_category VARCHAR(100),
    brand_name VARCHAR(255),
    barcode VARCHAR(50),
    additional_nutrients JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_detected_foods_analysis_id ON detected_foods(analysis_id);
CREATE INDEX idx_detected_foods_name ON detected_foods(food_name_normalized);
CREATE INDEX idx_detected_foods_category ON detected_foods(food_category);
CREATE INDEX idx_detected_foods_source ON detected_foods(nutrition_source);

-- Índice para búsquedas de alimentos populares
CREATE INDEX idx_detected_foods_popular 
    ON detected_foods(food_name_normalized, created_at) 
    WHERE confidence >= 7;
```

### 4. Tabla `food_cache`
```sql
CREATE TABLE food_cache (
    id SERIAL PRIMARY KEY,
    food_name VARCHAR(255) UNIQUE NOT NULL,
    food_name_normalized VARCHAR(255) NOT NULL,
    nutrition_data JSONB NOT NULL,
    source VARCHAR(50) NOT NULL CHECK (source IN ('usda', 'nutritionix')),
    external_id VARCHAR(100),
    confidence_score INTEGER DEFAULT 10,
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE UNIQUE INDEX idx_food_cache_name ON food_cache(food_name);
CREATE INDEX idx_food_cache_normalized ON food_cache(food_name_normalized);
CREATE INDEX idx_food_cache_source ON food_cache(source);
CREATE INDEX idx_food_cache_usage ON food_cache(usage_count DESC);
CREATE INDEX idx_food_cache_last_used ON food_cache(last_used);

-- Trigger para actualizar usage_count y last_used
CREATE OR REPLACE FUNCTION update_food_cache_usage()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE food_cache 
    SET usage_count = usage_count + 1, 
        last_used = NOW()
    WHERE food_name_normalized = NEW.food_name_normalized;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_food_cache_on_detection
    AFTER INSERT ON detected_foods
    FOR EACH ROW EXECUTE FUNCTION update_food_cache_usage();
```

**Estructura de nutrition_data (JSONB)**:
```json
{
  "per_100g": {
    "calories": 52,
    "protein": 0.26,
    "carbs": 13.81,
    "fat": 0.17,
    "fiber": 2.4,
    "sugar": 10.39,
    "sodium": 1,
    "vitamins": {
      "vitamin_c": 4.6,
      "vitamin_a": 54
    },
    "minerals": {
      "calcium": 6,
      "iron": 0.12,
      "potassium": 107
    }
  },
  "serving_sizes": [
    {"description": "1 medium apple", "grams": 182},
    {"description": "1 cup sliced", "grams": 109}
  ],
  "allergens": [],
  "categories": ["fruits", "fresh_fruits"]
}
```

## 📈 Tablas de Analytics

### 5. Tabla `user_daily_summaries`
```sql
CREATE TABLE user_daily_summaries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    total_calories DECIMAL(8,2) NOT NULL DEFAULT 0,
    total_protein DECIMAL(8,2) NOT NULL DEFAULT 0,
    total_carbs DECIMAL(8,2) NOT NULL DEFAULT 0,
    total_fat DECIMAL(8,2) NOT NULL DEFAULT 0,
    total_fiber DECIMAL(8,2) NOT NULL DEFAULT 0,
    analyses_count INTEGER NOT NULL DEFAULT 0,
    foods_count INTEGER NOT NULL DEFAULT 0,
    avg_confidence DECIMAL(4,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, date)
);

-- Índices
CREATE UNIQUE INDEX idx_user_daily_summaries_user_date ON user_daily_summaries(user_id, date);
CREATE INDEX idx_user_daily_summaries_date ON user_daily_summaries(date);

-- Trigger para actualizar resúmenes diarios
CREATE OR REPLACE FUNCTION update_daily_summary()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_daily_summaries (
        user_id, date, total_calories, total_protein, 
        total_carbs, total_fat, total_fiber, analyses_count, foods_count
    )
    SELECT 
        NEW.user_id,
        DATE(NEW.created_at),
        COALESCE(SUM(fa.total_calories), 0),
        COALESCE(SUM(fa.total_protein), 0),
        COALESCE(SUM(fa.total_carbs), 0),
        COALESCE(SUM(fa.total_fat), 0),
        COALESCE(SUM(fa.total_fiber), 0),
        COUNT(fa.id),
        COALESCE(SUM((
            SELECT COUNT(*) FROM detected_foods df 
            WHERE df.analysis_id = fa.id
        )), 0)
    FROM food_analyses fa
    WHERE fa.user_id = NEW.user_id 
      AND DATE(fa.created_at) = DATE(NEW.created_at)
      AND fa.status = 'completed'
    ON CONFLICT (user_id, date) 
    DO UPDATE SET
        total_calories = EXCLUDED.total_calories,
        total_protein = EXCLUDED.total_protein,
        total_carbs = EXCLUDED.total_carbs,
        total_fat = EXCLUDED.total_fat,
        total_fiber = EXCLUDED.total_fiber,
        analyses_count = EXCLUDED.analyses_count,
        foods_count = EXCLUDED.foods_count,
        updated_at = NOW();
    
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_daily_summary_on_analysis
    AFTER INSERT OR UPDATE ON food_analyses
    FOR EACH ROW 
    WHEN (NEW.status = 'completed')
    EXECUTE FUNCTION update_daily_summary();
```

## 🔍 Consultas Optimizadas

### Consultas Frecuentes
```sql
-- 1. Obtener análisis recientes del usuario
SELECT 
    fa.id,
    fa.total_calories,
    fa.confidence_score,
    fa.created_at,
    COUNT(df.id) as foods_count
FROM food_analyses fa
LEFT JOIN detected_foods df ON fa.id = df.analysis_id
WHERE fa.user_id = $1 
  AND fa.status = 'completed'
  AND fa.created_at >= NOW() - INTERVAL '7 days'
GROUP BY fa.id
ORDER BY fa.created_at DESC
LIMIT 20;

-- 2. Buscar alimentos en cache
SELECT 
    food_name,
    nutrition_data,
    source,
    confidence_score
FROM food_cache
WHERE food_name_normalized ILIKE $1 || '%'
ORDER BY usage_count DESC, confidence_score DESC
LIMIT 10;

-- 3. Resumen nutricional diario
SELECT 
    date,
    total_calories,
    total_protein,
    total_carbs,
    total_fat,
    analyses_count
FROM user_daily_summaries
WHERE user_id = $1
  AND date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY date DESC;

-- 4. Alimentos más detectados (trending)
SELECT 
    df.food_name_normalized,
    COUNT(*) as detection_count,
    AVG(df.confidence) as avg_confidence,
    AVG(df.calories) as avg_calories
FROM detected_foods df
JOIN food_analyses fa ON df.analysis_id = fa.id
WHERE fa.created_at >= NOW() - INTERVAL '7 days'
  AND fa.status = 'completed'
  AND df.confidence >= 7
GROUP BY df.food_name_normalized
HAVING COUNT(*) >= 5
ORDER BY detection_count DESC
LIMIT 20;
```

## 🚀 Optimizaciones de Performance

### Particionamiento
```sql
-- Particionamiento por fecha para food_analyses
CREATE TABLE food_analyses_2025_q1 PARTITION OF food_analyses
    FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');

CREATE TABLE food_analyses_2025_q2 PARTITION OF food_analyses
    FOR VALUES FROM ('2025-04-01') TO ('2025-07-01');

-- Índices en particiones
CREATE INDEX idx_food_analyses_2025_q1_user_id 
    ON food_analyses_2025_q1(user_id);
```

### Configuración de PostgreSQL
```sql
-- Configuraciones recomendadas
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
```

## 🔒 Seguridad y Permisos

### Row Level Security
```sql
-- Habilitar RLS en tablas sensibles
ALTER TABLE food_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE detected_foods ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_daily_summaries ENABLE ROW LEVEL SECURITY;

-- Políticas de acceso
CREATE POLICY user_own_analyses ON food_analyses
    FOR ALL TO app_user
    USING (user_id = current_setting('app.current_user_id')::INTEGER);

CREATE POLICY user_own_summaries ON user_daily_summaries
    FOR ALL TO app_user
    USING (user_id = current_setting('app.current_user_id')::INTEGER);
```

### Roles y Permisos
```sql
-- Rol para la aplicación
CREATE ROLE app_user;
GRANT SELECT, INSERT, UPDATE ON users TO app_user;
GRANT SELECT, INSERT, UPDATE ON food_analyses TO app_user;
GRANT SELECT, INSERT, UPDATE ON detected_foods TO app_user;
GRANT SELECT, INSERT, UPDATE ON food_cache TO app_user;
GRANT SELECT, INSERT, UPDATE ON user_daily_summaries TO app_user;

-- Rol de solo lectura para analytics
CREATE ROLE analytics_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_reader;
```

## 📊 Métricas y Monitoreo

### Vistas para Analytics
```sql
-- Vista de estadísticas generales
CREATE VIEW analytics_overview AS
SELECT 
    COUNT(DISTINCT u.id) as total_users,
    COUNT(fa.id) as total_analyses,
    COUNT(df.id) as total_foods_detected,
    AVG(fa.confidence_score) as avg_confidence,
    AVG(fa.processing_time_ms) as avg_processing_time
FROM users u
LEFT JOIN food_analyses fa ON u.id = fa.user_id
LEFT JOIN detected_foods df ON fa.id = df.analysis_id
WHERE fa.status = 'completed';

-- Vista de alimentos populares
CREATE VIEW popular_foods AS
SELECT 
    df.food_name_normalized,
    COUNT(*) as detection_count,
    AVG(df.confidence) as avg_confidence,
    COUNT(DISTINCT fa.user_id) as unique_users
FROM detected_foods df
JOIN food_analyses fa ON df.analysis_id = fa.id
WHERE fa.created_at >= NOW() - INTERVAL '30 days'
  AND fa.status = 'completed'
GROUP BY df.food_name_normalized
ORDER BY detection_count DESC;
```

---

**Estado**: ✅ Esquema completo definido  
**Siguiente**: Definición de APIs internas  
**Estimación**: Base de datos lista para implementación