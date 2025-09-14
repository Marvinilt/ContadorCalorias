"""
FastAPI Main Application - Contador de Calorías
Aplicación principal del API Gateway
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from contextlib import asynccontextmanager

from routers import auth, images, nutrition, analytics
from middleware.rate_limit import RateLimitMiddleware
from middleware.logging import LoggingMiddleware
from database import init_db
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    print("🚀 Iniciando Contador de Calorías API...")
    await init_db()
    print("✅ Base de datos inicializada")
    
    yield
    
    # Shutdown
    print("🔄 Cerrando aplicación...")

# Crear aplicación FastAPI
app = FastAPI(
    title="Contador de Calorías API",
    description="API para análisis nutricional por imágenes de alimentos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Middleware de seguridad
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Middleware personalizado
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(images.router, prefix="/api/v1/analyze", tags=["Image Analysis"])
app.include_router(nutrition.router, prefix="/api/v1/foods", tags=["Nutrition"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Contador de Calorías API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": "2025-09-14T12:00:00Z",
        "services": {
            "database": "connected",
            "cache": "connected",
            "ml_service": "available"
        }
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Manejo personalizado de excepciones HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "timestamp": "2025-09-14T12:00:00Z"
            }
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )