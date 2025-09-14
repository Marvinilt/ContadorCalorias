"""
Router para análisis de imágenes
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import asyncio
from datetime import datetime

from database import get_db
from services.ml_service import MLService
from services.nutrition_service import NutritionService
from models.requests import ImageAnalysisRequest
from models.responses import AnalysisResponse, AnalysisStatusResponse
from middleware.auth import get_current_user

router = APIRouter()

@router.post("/image", response_model=AnalysisStatusResponse, status_code=202)
async def analyze_image(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    meal_type: Optional[str] = None,
    notes: Optional[str] = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analizar imagen de alimentos y calcular información nutricional
    """
    
    # Validar archivo
    if not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser una imagen"
        )
    
    # Generar ID único para el análisis
    analysis_id = str(uuid.uuid4())
    
    # Crear registro inicial en base de datos
    analysis_record = {
        "id": analysis_id,
        "user_id": current_user.id,
        "status": "processing",
        "created_at": datetime.utcnow()
    }
    
    # Guardar en DB (implementar con SQLAlchemy)
    # db.add(analysis_record)
    # db.commit()
    
    # Procesar imagen en background
    background_tasks.add_task(
        process_image_analysis,
        analysis_id,
        image,
        current_user.id,
        meal_type,
        notes
    )
    
    return AnalysisStatusResponse(
        analysis_id=analysis_id,
        status="processing",
        estimated_completion=datetime.utcnow().isoformat() + "Z",
        message="Análisis en progreso. Use GET /analyze/{analysis_id} para verificar estado."
    )

@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_result(
    analysis_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener resultado del análisis de imagen
    """
    
    # Buscar análisis en base de datos
    # analysis = db.query(FoodAnalysis).filter(
    #     FoodAnalysis.id == analysis_id,
    #     FoodAnalysis.user_id == current_user.id
    # ).first()
    
    # Simulación de respuesta para MVP
    analysis = {
        "id": analysis_id,
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
            }
        ],
        "created_at": datetime.utcnow().isoformat() + "Z",
        "completed_at": datetime.utcnow().isoformat() + "Z"
    }
    
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Análisis no encontrado"
        )
    
    return analysis

async def process_image_analysis(
    analysis_id: str,
    image: UploadFile,
    user_id: int,
    meal_type: Optional[str],
    notes: Optional[str]
):
    """
    Procesar análisis de imagen en background
    """
    try:
        # 1. Inicializar servicios
        ml_service = MLService()
        nutrition_service = NutritionService()
        
        # 2. Leer imagen
        image_data = await image.read()
        
        # 3. Analizar con OpenAI Vision
        detected_foods = await ml_service.analyze_food_image(image_data)
        
        # 4. Obtener información nutricional
        enriched_foods = []
        for food in detected_foods:
            nutrition_data = await nutrition_service.get_nutrition_data(
                food["name"], 
                food["portion_grams"]
            )
            enriched_foods.append({**food, **nutrition_data})
        
        # 5. Calcular totales
        total_nutrition = calculate_total_nutrition(enriched_foods)
        
        # 6. Actualizar base de datos
        # update_analysis_record(analysis_id, "completed", enriched_foods, total_nutrition)
        
        print(f"✅ Análisis {analysis_id} completado exitosamente")
        
    except Exception as e:
        print(f"❌ Error en análisis {analysis_id}: {e}")
        # update_analysis_record(analysis_id, "failed", error=str(e))

def calculate_total_nutrition(foods):
    """Calcular totales nutricionales"""
    totals = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "fiber": 0,
        "sugar": 0,
        "sodium": 0
    }
    
    for food in foods:
        nutrition = food.get("nutrition", {})
        for key in totals:
            totals[key] += nutrition.get(key, 0)
    
    return totals