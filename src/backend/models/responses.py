"""
Modelos de response (Pydantic)
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class NutritionData(BaseModel):
    """Modelo para datos nutricionales"""
    calories: float = Field(..., ge=0)
    protein: float = Field(..., ge=0)
    carbs: float = Field(..., ge=0)
    fat: float = Field(..., ge=0)
    fiber: Optional[float] = Field(0, ge=0)
    sugar: Optional[float] = Field(0, ge=0)
    sodium: Optional[float] = Field(0, ge=0)

class PortionInfo(BaseModel):
    """Información de porción"""
    grams: float = Field(..., ge=0)
    description: str

class DetectedFood(BaseModel):
    """Alimento detectado en análisis"""
    id: int
    name: str
    name_normalized: str
    portion: PortionInfo
    nutrition: NutritionData
    confidence: int = Field(..., ge=1, le=10)
    category: Optional[str] = None
    source: str

class ImageInfo(BaseModel):
    """Información de la imagen analizada"""
    hash: str
    url: Optional[str] = None
    dimensions: Optional[Dict[str, int]] = None
    size_bytes: Optional[int] = None

class AnalysisMetadata(BaseModel):
    """Metadatos del análisis"""
    meal_type: Optional[str] = None
    notes: Optional[str] = None
    device_info: Optional[str] = None
    location: Optional[Dict[str, float]] = None

class AnalysisResponse(BaseModel):
    """Respuesta completa de análisis"""
    id: str
    status: str
    confidence_score: int = Field(..., ge=1, le=10)
    processing_time_ms: int
    total_nutrition: NutritionData
    detected_foods: List[DetectedFood]
    image: Optional[ImageInfo] = None
    metadata: Optional[AnalysisMetadata] = None
    created_at: str
    completed_at: Optional[str] = None

class AnalysisStatusResponse(BaseModel):
    """Respuesta de estado de análisis"""
    analysis_id: str
    status: str
    progress: Optional[int] = Field(None, ge=0, le=100)
    current_step: Optional[str] = None
    estimated_completion: Optional[str] = None
    message: str

class UserProfile(BaseModel):
    """Perfil de usuario"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None
    dietary_restrictions: Optional[List[str]] = None
    daily_calorie_goal: Optional[int] = None
    preferences: Optional[Dict[str, Any]] = None

class UserStats(BaseModel):
    """Estadísticas del usuario"""
    total_analyses: int = 0
    total_foods_detected: int = 0
    avg_daily_calories: float = 0
    streak_days: int = 0

class UserResponse(BaseModel):
    """Respuesta de usuario"""
    user: Dict[str, Any]
    tokens: Optional[Dict[str, Any]] = None

class TokenResponse(BaseModel):
    """Respuesta de tokens"""
    user: Dict[str, Any]
    tokens: Dict[str, Any]

class FoodItem(BaseModel):
    """Item de alimento en búsqueda"""
    id: str
    name: str
    name_normalized: str
    source: str
    category: Optional[str] = None
    brand: Optional[str] = None
    nutrition_per_100g: NutritionData
    serving_sizes: Optional[List[PortionInfo]] = None
    confidence: int = Field(..., ge=1, le=10)
    usage_count: int = 0

class FoodSearchResponse(BaseModel):
    """Respuesta de búsqueda de alimentos"""
    query: str
    total_results: int
    results: List[FoodItem]
    suggestions: Optional[List[str]] = None

class FoodDetailResponse(BaseModel):
    """Respuesta detallada de alimento"""
    id: str
    name: str
    name_normalized: str
    source: str
    external_id: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    barcode: Optional[str] = None
    nutrition_per_100g: NutritionData
    serving_sizes: List[PortionInfo]
    allergens: List[str] = []
    dietary_flags: List[str] = []
    usage_count: int = 0
    last_updated: str

class DailySummary(BaseModel):
    """Resumen diario nutricional"""
    date: str
    nutrition: NutritionData
    goals: Optional[NutritionData] = None
    progress: Optional[Dict[str, float]] = None
    analyses_count: int = 0
    foods_count: int = 0
    meal_distribution: Optional[Dict[str, float]] = None

class AnalyticsResponse(BaseModel):
    """Respuesta de analytics"""
    period: Dict[str, str]
    daily_summaries: List[DailySummary]
    averages: Optional[NutritionData] = None

class TrendDataPoint(BaseModel):
    """Punto de datos para tendencias"""
    date: str
    value: float
    goal: Optional[float] = None
    percentage: Optional[float] = None

class Insight(BaseModel):
    """Insight de analytics"""
    type: str
    message: str
    impact: str  # positive, negative, neutral

class TrendsResponse(BaseModel):
    """Respuesta de tendencias"""
    period: str
    metric: str
    data_points: List[TrendDataPoint]
    insights: List[Insight]
    statistics: Dict[str, float]

class PopularFood(BaseModel):
    """Alimento popular del usuario"""
    name: str
    category: str
    consumption_count: int
    total_calories: float
    avg_portion_grams: float
    frequency_per_week: float

class PopularFoodsResponse(BaseModel):
    """Respuesta de alimentos populares"""
    period: str
    foods: List[PopularFood]

class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""
    error: Dict[str, Any]