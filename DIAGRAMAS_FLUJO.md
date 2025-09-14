# 🔄 Diagramas de Flujo - Contador de Calorías

**Fecha**: 14 de Septiembre, 2025  
**Versión**: 1.0  
**Herramientas**: Mermaid, PlantUML

## 📋 Resumen

Diagramas detallados de flujo de datos y secuencias para todos los procesos críticos del sistema de análisis nutricional por imágenes.

## 🖼️ Flujo Principal: Análisis de Imagen

### Diagrama de Secuencia Completo
```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend (React)
    participant G as API Gateway (FastAPI)
    participant A as Auth Service
    participant M as ML Service (OpenAI)
    participant N as Nutrition Service
    participant C as Cache (Redis)
    participant D as Database (PostgreSQL)
    participant S as Storage (S3)

    U->>F: 1. Captura/sube imagen
    F->>F: 2. Validar imagen (tamaño, formato)
    F->>G: 3. POST /analyze/image
    
    G->>A: 4. Validar JWT token
    A-->>G: 5. Usuario autenticado
    
    G->>G: 6. Generar analysis_id
    G->>D: 7. Crear registro inicial (status: processing)
    G->>S: 8. Subir imagen a storage
    G-->>F: 9. 202 Accepted + analysis_id
    F-->>U: 10. "Análisis en progreso..."
    
    Note over G,M: Procesamiento Asíncrono
    G->>M: 11. Analizar imagen
    M->>M: 12. Llamada a OpenAI Vision API
    M->>M: 13. Parsear respuesta JSON
    M-->>G: 14. Lista de alimentos detectados
    
    loop Para cada alimento detectado
        G->>N: 15. Obtener datos nutricionales
        N->>C: 16. Buscar en cache Redis
        
        alt Cache Hit
            C-->>N: 17. Datos nutricionales cached
        else Cache Miss
            N->>N: 18. Buscar en USDA API
            alt USDA encontrado
                N->>C: 19. Guardar en cache
                N-->>G: 20. Datos USDA
            else USDA no encontrado
                N->>N: 21. Fallback a Nutritionix API
                N->>C: 22. Guardar en cache
                N-->>G: 23. Datos Nutritionix
            end
        end
    end
    
    G->>G: 24. Calcular totales nutricionales
    G->>D: 25. Actualizar análisis (status: completed)
    G->>D: 26. Guardar alimentos detectados
    G->>D: 27. Actualizar resumen diario del usuario
    
    Note over F,U: Polling o WebSocket para actualizaciones
    F->>G: 28. GET /analyze/{analysis_id}
    G->>D: 29. Obtener resultado completo
    G-->>F: 30. Resultado con datos nutricionales
    F-->>U: 31. Mostrar resultados finales
```

### Flujo de Estados del Análisis
```mermaid
stateDiagram-v2
    [*] --> Validating: Usuario sube imagen
    Validating --> Processing: Imagen válida
    Validating --> Failed: Imagen inválida
    
    Processing --> MLAnalysis: Iniciar análisis ML
    MLAnalysis --> NutritionLookup: Alimentos detectados
    MLAnalysis --> Failed: Error en ML
    
    NutritionLookup --> Calculating: Datos nutricionales obtenidos
    NutritionLookup --> PartialData: Algunos alimentos no encontrados
    NutritionLookup --> Failed: Error crítico
    
    PartialData --> Calculating: Continuar con datos parciales
    Calculating --> Completed: Cálculos finalizados
    Calculating --> Failed: Error en cálculos
    
    Completed --> [*]
    Failed --> [*]
    
    note right of Processing
        Timeout: 30 segundos
        Reintentos: 3 veces
    end note
    
    note right of Completed
        Resultado guardado
        Usuario notificado
    end note
```

## 🔍 Flujo de Búsqueda de Alimentos

### Diagrama de Secuencia
```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend
    participant G as API Gateway
    participant C as Cache (Redis)
    participant D as Database
    participant E1 as USDA API
    participant E2 as Nutritionix API

    U->>F: 1. Escribir término de búsqueda
    F->>F: 2. Debounce (300ms)
    F->>G: 3. GET /foods/search?q=manzana
    
    G->>C: 4. Buscar resultados cached
    alt Cache Hit (resultados recientes)
        C-->>G: 5. Resultados cached
        G-->>F: 6. Respuesta rápida
    else Cache Miss
        G->>D: 7. Buscar en food_cache local
        
        alt Datos locales encontrados
            D-->>G: 8. Resultados de DB local
            G->>C: 9. Actualizar cache
            G-->>F: 10. Respuesta con datos locales
        else Búsqueda externa necesaria
            par Búsqueda paralela en APIs
                G->>E1: 11a. Buscar en USDA
                G->>E2: 11b. Buscar en Nutritionix
            end
            
            E1-->>G: 12a. Resultados USDA
            E2-->>G: 12b. Resultados Nutritionix
            
            G->>G: 13. Combinar y rankear resultados
            G->>D: 14. Guardar nuevos alimentos en food_cache
            G->>C: 15. Cachear resultados
            G-->>F: 16. Respuesta completa
        end
    end
    
    F-->>U: 17. Mostrar sugerencias
    
    U->>F: 18. Seleccionar alimento
    F->>G: 19. GET /foods/{food_id}
    G->>D: 20. Obtener detalles completos
    G-->>F: 21. Información nutricional detallada
    F-->>U: 22. Mostrar información completa
```

## 👤 Flujo de Autenticación

### Registro de Usuario
```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend
    participant G as API Gateway
    participant A as Auth Service
    participant D as Database
    participant E as Email Service

    U->>F: 1. Completar formulario registro
    F->>F: 2. Validación frontend
    F->>G: 3. POST /auth/register
    
    G->>G: 4. Validar datos (email único, password fuerte)
    G->>G: 5. Hash password (bcrypt)
    G->>D: 6. Crear usuario en DB
    
    G->>A: 7. Generar tokens JWT
    A-->>G: 8. Access + Refresh tokens
    
    G->>E: 9. Enviar email de verificación
    G-->>F: 10. Usuario creado + tokens
    F->>F: 11. Guardar tokens en localStorage
    F-->>U: 12. Bienvenida + verificar email
    
    Note over E,U: Proceso de verificación
    U->>E: 13. Click en link de verificación
    E->>G: 14. GET /auth/verify-email?token=...
    G->>D: 15. Marcar email como verificado
    G-->>E: 16. Confirmación
    E-->>U: 17. Email verificado exitosamente
```

### Login y Renovación de Token
```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend
    participant G as API Gateway
    participant A as Auth Service
    participant D as Database

    U->>F: 1. Ingresar credenciales
    F->>G: 2. POST /auth/login
    
    G->>D: 3. Buscar usuario por email
    G->>G: 4. Verificar password (bcrypt)
    
    alt Credenciales válidas
        G->>A: 5. Generar nuevos tokens
        A-->>G: 6. Access + Refresh tokens
        G->>D: 7. Actualizar last_login
        G-->>F: 8. Login exitoso + tokens
        F->>F: 9. Guardar tokens
        F-->>U: 10. Redirigir a dashboard
    else Credenciales inválidas
        G-->>F: 11. Error 401
        F-->>U: 12. Mostrar error
    end
    
    Note over F,A: Renovación automática de token
    F->>F: 13. Detectar token próximo a expirar
    F->>G: 14. POST /auth/refresh
    G->>A: 15. Validar refresh token
    A-->>G: 16. Nuevo access token
    G-->>F: 17. Token renovado
    F->>F: 18. Actualizar token guardado
```

## 📊 Flujo de Analytics

### Generación de Resumen Diario
```mermaid
sequenceDiagram
    participant S as Scheduler (Cron)
    participant A as Analytics Service
    participant D as Database
    participant C as Cache
    participant N as Notification Service

    S->>A: 1. Trigger diario (00:00 UTC)
    
    loop Para cada usuario activo
        A->>D: 2. Obtener análisis del día anterior
        A->>A: 3. Calcular totales nutricionales
        A->>A: 4. Comparar con metas del usuario
        A->>A: 5. Generar insights y tendencias
        
        A->>D: 6. Guardar/actualizar user_daily_summaries
        A->>C: 7. Invalidar cache de analytics del usuario
        
        alt Usuario tiene notificaciones habilitadas
            A->>N: 8. Enviar resumen diario
        end
    end
    
    A->>A: 9. Generar estadísticas globales
    A->>D: 10. Actualizar métricas de sistema
    A->>C: 11. Cachear estadísticas populares
```

### Consulta de Tendencias
```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend
    participant G as API Gateway
    participant A as Analytics Service
    participant C as Cache
    participant D as Database

    U->>F: 1. Solicitar tendencias (30 días)
    F->>G: 2. GET /analytics/trends?period=30d
    
    G->>C: 3. Buscar tendencias cached
    alt Cache Hit
        C-->>G: 4. Datos cached
        G-->>F: 5. Respuesta rápida
    else Cache Miss
        G->>A: 6. Calcular tendencias
        A->>D: 7. Query datos históricos
        A->>A: 8. Calcular promedios, medianas
        A->>A: 9. Detectar patrones y tendencias
        A->>A: 10. Generar insights personalizados
        A-->>G: 11. Tendencias calculadas
        G->>C: 12. Cachear resultados (TTL: 1h)
        G-->>F: 13. Respuesta con tendencias
    end
    
    F->>F: 14. Renderizar gráficos
    F-->>U: 15. Mostrar visualizaciones
```

## 🔄 Flujo de Sincronización de Cache

### Estrategia de Cache Multi-Nivel
```mermaid
flowchart TD
    A[Request] --> B{Cache L1<br/>Redis}
    B -->|Hit| C[Respuesta Rápida]
    B -->|Miss| D{Cache L2<br/>Database}
    D -->|Hit| E[Actualizar L1]
    E --> C
    D -->|Miss| F{API Externa<br/>USDA/Nutritionix}
    F -->|Success| G[Guardar en DB]
    G --> H[Actualizar L1]
    H --> C
    F -->|Error| I[Respuesta de Error]
    
    style B fill:#e1f5fe
    style D fill:#f3e5f5
    style F fill:#fff3e0
```

### Invalidación de Cache
```mermaid
sequenceDiagram
    participant U as Usuario
    participant G as API Gateway
    participant C as Cache (Redis)
    participant D as Database
    participant B as Background Job

    Note over G,B: Evento: Nuevo análisis completado
    G->>C: 1. Invalidar cache de usuario
    G->>C: 2. Invalidar analytics del usuario
    G->>B: 3. Queue job: actualizar estadísticas
    
    B->>D: 4. Recalcular food popularity
    B->>C: 5. Actualizar cache de trending foods
    B->>C: 6. Actualizar cache de búsquedas populares
    
    Note over G,B: Evento: Usuario actualiza perfil
    G->>C: 7. Invalidar cache de perfil
    G->>C: 8. Invalidar metas nutricionales
    G->>B: 9. Queue job: recalcular recomendaciones
```

## 🚨 Flujo de Manejo de Errores

### Estrategia de Retry y Fallback
```mermaid
flowchart TD
    A[API Request] --> B{Rate Limit OK?}
    B -->|No| C[429 Too Many Requests]
    B -->|Yes| D[Procesar Request]
    
    D --> E{OpenAI API Call}
    E -->|Success| F[Continuar Flujo]
    E -->|Error| G{Retry Count < 3?}
    
    G -->|Yes| H[Exponential Backoff]
    H --> I[Wait: 2^retry seconds]
    I --> E
    
    G -->|No| J{Fallback Available?}
    J -->|Yes| K[Usar Modelo Local]
    K --> L[Respuesta Degradada]
    J -->|No| M[Error 503]
    
    F --> N{Nutrition API Call}
    N -->|USDA Success| O[Respuesta Completa]
    N -->|USDA Error| P[Try Nutritionix]
    P -->|Success| Q[Respuesta Parcial]
    P -->|Error| R[Respuesta Mínima]
    
    style C fill:#ffcdd2
    style M fill:#ffcdd2
    style L fill:#fff3e0
    style Q fill:#fff3e0
    style R fill:#fff3e0
```

## 📱 Flujo de Experiencia de Usuario

### Flujo Completo de Análisis (UX)
```mermaid
journey
    title Experiencia de Usuario: Análisis de Imagen
    section Captura
      Abrir cámara: 5: Usuario
      Enfocar alimento: 4: Usuario
      Capturar foto: 5: Usuario
      Previsualizar: 4: Usuario
    section Análisis
      Subir imagen: 3: Usuario, Sistema
      Mostrar progreso: 4: Sistema
      Esperar resultado: 2: Usuario
      Recibir notificación: 5: Sistema
    section Resultados
      Ver alimentos detectados: 5: Usuario
      Revisar calorías: 5: Usuario
      Ajustar porciones: 4: Usuario
      Guardar análisis: 5: Usuario
    section Seguimiento
      Ver en historial: 4: Usuario
      Comparar con metas: 5: Usuario
      Compartir resultado: 3: Usuario
```

## 🔧 Configuración de Timeouts

### Timeouts por Servicio
```yaml
timeouts:
  api_gateway:
    request_timeout: 30s
    keepalive_timeout: 65s
  
  ml_service:
    openai_timeout: 25s
    analysis_timeout: 30s
    retry_delay: 2s
  
  nutrition_service:
    usda_timeout: 5s
    nutritionix_timeout: 8s
    cache_timeout: 1s
  
  database:
    connection_timeout: 5s
    query_timeout: 10s
    transaction_timeout: 15s
  
  cache:
    redis_timeout: 1s
    connection_pool_timeout: 2s
```

---

**Estado**: ✅ Diagramas completos  
**Herramientas**: Mermaid para visualización  
**Siguiente**: Plan de testing y validación