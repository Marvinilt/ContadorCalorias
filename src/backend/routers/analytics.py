"""
Router para analytics y estadísticas
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from database import get_db
from models.responses import AnalyticsResponse, TrendsResponse, PopularFoodsResponse
from middleware.auth import get_current_user

router = APIRouter()

@router.get("/daily-summary", response_model=AnalyticsResponse)
async def get_daily_summary(
    date: Optional[str] = Query(None, description="Fecha específica (YYYY-MM-DD)"),
    days: int = Query(7, ge=1, le=90, description="Número de días"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener resumen nutricional diario
    """
    
    # Calcular rango de fechas
    end_date = datetime.now().date()
    if date:
        end_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    start_date = end_date - timedelta(days=days-1)
    
    # Simulación de datos para MVP
    daily_summaries = []
    
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        
        # Datos simulados
        daily_summaries.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "nutrition": {
                "calories": 1850 + (i * 50),
                "protein": 85.2,
                "carbs": 220.5,
                "fat": 65.8,
                "fiber": 28.3,
                "sugar": 45.2,
                "sodium": 2.1
            },
            "goals": {
                "calories": 2200,
                "protein": 110,
                "carbs": 275,
                "fat": 73,
                "fiber": 30,
                "sugar": 50,
                "sodium": 2.3
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
        })
    
    return {
        "period": {
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "days": days
        },
        "daily_summaries": daily_summaries,
        "averages": {
            "calories": 1923,
            "protein": 89.1,
            "carbs": 235.7,
            "fat": 68.2,
            "fiber": 28.5,
            "sugar": 44.8,
            "sodium": 2.0
        }
    }

@router.get("/trends", response_model=TrendsResponse)
async def get_trends(
    period: str = Query("30d", regex="^(7d|30d|90d|1y)$"),
    metric: str = Query("calories", regex="^(calories|protein|carbs|fat|fiber)$"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener tendencias nutricionales
    """
    
    # Mapear período a días
    period_days = {
        "7d": 7,
        "30d": 30,
        "90d": 90,
        "1y": 365
    }
    
    days = period_days[period]
    
    # Generar datos de tendencia simulados
    data_points = []
    base_values = {
        "calories": 1900,
        "protein": 85,
        "carbs": 230,
        "fat": 70,
        "fiber": 25
    }
    
    base_value = base_values[metric]
    goal_value = base_value * 1.15  # Meta 15% más alta
    
    for i in range(days):
        date = (datetime.now().date() - timedelta(days=days-1-i))
        value = base_value + (i * 2) + ((-1)**i * 10)  # Variación simulada
        
        data_points.append({
            "date": date.strftime("%Y-%m-%d"),
            "value": round(value, 1),
            "goal": goal_value,
            "percentage": round((value / goal_value) * 100, 1)
        })
    
    # Generar insights
    insights = [
        {
            "type": "trend",
            "message": f"Tu {metric} promedio ha aumentado 5% en las últimas 2 semanas",
            "impact": "positive"
        },
        {
            "type": "goal",
            "message": f"Has alcanzado tu meta de {metric} 23 de los últimos {days} días",
            "impact": "positive"
        }
    ]
    
    # Calcular estadísticas
    values = [dp["value"] for dp in data_points]
    statistics = {
        "average": round(sum(values) / len(values), 1),
        "median": round(sorted(values)[len(values)//2], 1),
        "min": min(values),
        "max": max(values),
        "std_deviation": 15.7,  # Simulado
        "goal_achievement_rate": 76.7  # Simulado
    }
    
    return {
        "period": period,
        "metric": metric,
        "data_points": data_points,
        "insights": insights,
        "statistics": statistics
    }

@router.get("/popular-foods", response_model=PopularFoodsResponse)
async def get_popular_foods(
    period: str = Query("30d", regex="^(7d|30d|90d)$"),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener alimentos más consumidos por el usuario
    """
    
    # Datos simulados de alimentos populares
    popular_foods = [
        {
            "name": "Manzana roja",
            "category": "fruits",
            "consumption_count": 18,
            "total_calories": 1702.8,
            "avg_portion_grams": 175,
            "frequency_per_week": 4.2
        },
        {
            "name": "Pan integral",
            "category": "grains",
            "consumption_count": 12,
            "total_calories": 1800.0,
            "avg_portion_grams": 60,
            "frequency_per_week": 2.8
        },
        {
            "name": "Pollo a la plancha",
            "category": "protein",
            "consumption_count": 8,
            "total_calories": 1600.0,
            "avg_portion_grams": 150,
            "frequency_per_week": 1.9
        }
    ]
    
    return {
        "period": period,
        "foods": popular_foods
    }

@router.get("/goals-progress")
async def get_goals_progress(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener progreso hacia metas nutricionales
    """
    
    # Datos simulados de progreso
    return {
        "daily_goals": {
            "calories": 2200,
            "protein": 110,
            "carbs": 275,
            "fat": 73
        },
        "current_progress": {
            "calories": 1850,
            "protein": 95,
            "carbs": 220,
            "fat": 68
        },
        "percentage_complete": {
            "calories": 84.1,
            "protein": 86.4,
            "carbs": 80.0,
            "fat": 93.2
        },
        "streak": {
            "current_days": 12,
            "best_streak": 28,
            "goals_met_this_week": 5
        },
        "recommendations": [
            "Necesitas 350 calorías más para alcanzar tu meta diaria",
            "Excelente progreso en proteínas, sigue así",
            "Considera agregar más carbohidratos complejos"
        ]
    }