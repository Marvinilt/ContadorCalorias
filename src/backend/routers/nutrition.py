"""
Router para búsqueda y datos nutricionales
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from services.nutrition_service import NutritionService
from models.responses import FoodSearchResponse, FoodDetailResponse
from middleware.auth import get_current_user

router = APIRouter()

@router.get("/search", response_model=FoodSearchResponse)
async def search_foods(
    q: str = Query(..., min_length=2, max_length=100, description="Término de búsqueda"),
    limit: int = Query(10, ge=1, le=50, description="Número de resultados"),
    source: str = Query("all", regex="^(usda|nutritionix|all)$", description="Fuente de datos"),
    category: Optional[str] = Query(None, max_length=50, description="Filtrar por categoría"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buscar alimentos en la base de datos
    """
    
    nutrition_service = NutritionService()
    
    # Simulación de búsqueda para MVP
    results = [
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
                "sugar": 10.39,
                "sodium": 0.001
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
    ]
    
    # Filtrar por término de búsqueda
    filtered_results = [
        result for result in results 
        if q.lower() in result["name"].lower()
    ]
    
    return {
        "query": q,
        "total_results": len(filtered_results),
        "results": filtered_results[:limit],
        "suggestions": [
            "manzana verde",
            "manzana roja", 
            "jugo de manzana"
        ]
    }

@router.get("/{food_id}", response_model=FoodDetailResponse)
async def get_food_details(
    food_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener información detallada de un alimento específico
    """
    
    # Simulación para MVP
    if food_id == "usda_169905":
        return {
            "id": "usda_169905",
            "name": "Manzana, cruda, con cáscara",
            "name_normalized": "apple_raw_with_skin",
            "source": "usda",
            "external_id": "169905",
            "category": "fruits",
            "brand": None,
            "barcode": None,
            "nutrition_per_100g": {
                "calories": 52,
                "protein": 0.26,
                "carbs": 13.81,
                "fat": 0.17,
                "fiber": 2.4,
                "sugar": 10.39,
                "sodium": 0.001
            },
            "serving_sizes": [
                {
                    "description": "1 manzana mediana (7.5 cm diámetro)",
                    "grams": 182
                },
                {
                    "description": "1 taza en rodajas",
                    "grams": 109
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
    
    raise HTTPException(
        status_code=404,
        detail="Alimento no encontrado"
    )

@router.post("/calculate-nutrition")
async def calculate_nutrition(
    food_id: str,
    portion_grams: float = Query(..., ge=1, le=2000),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Calcular información nutricional para una porción específica
    """
    
    # Obtener datos del alimento
    # food_data = get_food_by_id(food_id)
    
    # Simulación para MVP
    if food_id == "usda_169905":
        base_nutrition = {
            "calories": 52,
            "protein": 0.26,
            "carbs": 13.81,
            "fat": 0.17,
            "fiber": 2.4,
            "sugar": 10.39,
            "sodium": 0.001
        }
        
        factor = portion_grams / 100.0
        calculated_nutrition = {}
        
        for key, value in base_nutrition.items():
            calculated_nutrition[key] = round(value * factor, 2)
        
        return {
            "food_id": food_id,
            "portion_grams": portion_grams,
            "nutrition": calculated_nutrition,
            "source": "usda"
        }
    
    raise HTTPException(
        status_code=404,
        detail="Alimento no encontrado"
    )