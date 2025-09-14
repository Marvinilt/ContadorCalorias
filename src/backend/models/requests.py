"""
Modelos de request (Pydantic)
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any, List
from datetime import date

class UserRegisterRequest(BaseModel):
    """Modelo para registro de usuario"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    profile: Optional[Dict[str, Any]] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe tener al menos una mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('La contraseña debe tener al menos una minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe tener al menos un número')
        return v

class UserLoginRequest(BaseModel):
    """Modelo para login de usuario"""
    email: EmailStr
    password: str

class UserProfileUpdate(BaseModel):
    """Modelo para actualización de perfil"""
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, regex="^(male|female|other)$")
    height_cm: Optional[int] = Field(None, ge=100, le=250)
    weight_kg: Optional[float] = Field(None, ge=30, le=300)
    activity_level: Optional[str] = Field(
        None, 
        regex="^(sedentary|light|moderate|active|very_active)$"
    )
    dietary_restrictions: Optional[List[str]] = None
    daily_calorie_goal: Optional[int] = Field(None, ge=1000, le=5000)
    preferences: Optional[Dict[str, Any]] = None

class ImageAnalysisRequest(BaseModel):
    """Modelo para análisis de imagen"""
    meal_type: Optional[str] = Field(
        None, 
        regex="^(breakfast|lunch|dinner|snack)$"
    )
    notes: Optional[str] = Field(None, max_length=500)
    
class FoodSearchRequest(BaseModel):
    """Modelo para búsqueda de alimentos"""
    query: str = Field(..., min_length=2, max_length=100)
    limit: Optional[int] = Field(10, ge=1, le=50)
    source: Optional[str] = Field("all", regex="^(usda|nutritionix|all)$")
    category: Optional[str] = Field(None, max_length=50)

class NutritionCalculationRequest(BaseModel):
    """Modelo para cálculo nutricional manual"""
    food_id: str
    portion_grams: float = Field(..., ge=1, le=2000)
    
class AnalyticsRequest(BaseModel):
    """Modelo para consultas de analytics"""
    period: Optional[str] = Field("30d", regex="^(7d|30d|90d|1y)$")
    metric: Optional[str] = Field(
        "calories", 
        regex="^(calories|protein|carbs|fat|fiber)$"
    )
    
class FeedbackRequest(BaseModel):
    """Modelo para feedback del usuario"""
    analysis_id: str
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = Field(None, max_length=1000)
    issues: Optional[List[str]] = None