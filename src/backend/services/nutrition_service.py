"""
Servicio de información nutricional
"""

import aiohttp
import asyncio
from typing import Dict, Optional
import json
from config import settings
from database import get_redis

class NutritionService:
    """Servicio para obtener información nutricional de alimentos"""
    
    def __init__(self):
        self.usda_base_url = "https://api.nal.usda.gov/fdc/v1"
        self.nutritionix_base_url = "https://trackapi.nutritionix.com/v2"
        
    async def get_nutrition_data(self, food_name: str, portion_grams: float) -> Dict:
        """
        Obtener datos nutricionales con estrategia de cache y fallback
        """
        # 1. Buscar en cache Redis
        cache_key = f"nutrition:{food_name.lower()}"
        redis_client = await get_redis()
        
        try:
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                data = json.loads(cached_data)
                return self._calculate_portion_nutrition(data, portion_grams)
        except Exception as e:
            print(f"⚠️ Error accediendo cache: {e}")
        
        # 2. Buscar en USDA (fuente primaria)
        usda_data = await self._search_usda(food_name)
        if usda_data:
            # Guardar en cache
            try:
                await redis_client.setex(cache_key, 604800, json.dumps(usda_data))  # 7 días
            except Exception as e:
                print(f"⚠️ Error guardando en cache: {e}")
            
            return self._calculate_portion_nutrition(usda_data, portion_grams)
        
        # 3. Fallback a Nutritionix
        nutritionix_data = await self._search_nutritionix(food_name, portion_grams)
        if nutritionix_data:
            return nutritionix_data
        
        # 4. Fallback final: datos estimados
        return self._get_estimated_nutrition(food_name, portion_grams)
    
    async def _search_usda(self, food_name: str) -> Optional[Dict]:
        """Buscar alimento en USDA Food Data Central"""
        try:
            url = f"{self.usda_base_url}/foods/search"
            params = {
                "query": food_name,
                "api_key": settings.USDA_API_KEY,
                "pageSize": 5,
                "dataType": ["Foundation", "SR Legacy"]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        foods = data.get("foods", [])
                        
                        if foods:
                            # Tomar el primer resultado más relevante
                            food = foods[0]
                            return self._parse_usda_food(food)
            
        except Exception as e:
            print(f"❌ Error buscando en USDA: {e}")
        
        return None
    
    async def _search_nutritionix(self, food_name: str, portion_grams: float) -> Optional[Dict]:
        """Buscar alimento en Nutritionix API"""
        try:
            url = f"{self.nutritionix_base_url}/natural/nutrients"
            headers = {
                "x-app-id": settings.NUTRITIONIX_APP_ID,
                "x-app-key": settings.NUTRITIONIX_APP_KEY,
                "Content-Type": "application/json"
            }
            
            # Convertir gramos a descripción natural
            query = f"{portion_grams}g {food_name}"
            
            payload = {"query": query}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload, timeout=8) as response:
                    if response.status == 200:
                        data = await response.json()
                        foods = data.get("foods", [])
                        
                        if foods:
                            return self._parse_nutritionix_food(foods[0])
            
        except Exception as e:
            print(f"❌ Error buscando en Nutritionix: {e}")
        
        return None
    
    def _parse_usda_food(self, food_data: Dict) -> Dict:
        """Parsear datos de USDA a formato estándar"""
        nutrients = {}
        
        # Mapear nutrientes de USDA
        nutrient_map = {
            "Energy": "calories",
            "Protein": "protein", 
            "Carbohydrate, by difference": "carbs",
            "Total lipid (fat)": "fat",
            "Fiber, total dietary": "fiber",
            "Sugars, total including NLEA": "sugar",
            "Sodium, Na": "sodium"
        }
        
        for nutrient in food_data.get("foodNutrients", []):
            nutrient_name = nutrient.get("nutrientName", "")
            if nutrient_name in nutrient_map:
                key = nutrient_map[nutrient_name]
                value = nutrient.get("value", 0)
                
                # Convertir unidades si es necesario
                if key == "calories":
                    nutrients[key] = value
                elif key == "sodium":
                    nutrients[key] = value / 1000  # mg a g
                else:
                    nutrients[key] = value
        
        return {
            "nutrition_per_100g": nutrients,
            "source": "usda",
            "food_name": food_data.get("description", "")
        }
    
    def _parse_nutritionix_food(self, food_data: Dict) -> Dict:
        """Parsear datos de Nutritionix a formato estándar"""
        return {
            "nutrition": {
                "calories": food_data.get("nf_calories", 0),
                "protein": food_data.get("nf_protein", 0),
                "carbs": food_data.get("nf_total_carbohydrate", 0),
                "fat": food_data.get("nf_total_fat", 0),
                "fiber": food_data.get("nf_dietary_fiber", 0),
                "sugar": food_data.get("nf_sugars", 0),
                "sodium": food_data.get("nf_sodium", 0) / 1000  # mg a g
            },
            "source": "nutritionix",
            "food_name": food_data.get("food_name", "")
        }
    
    def _calculate_portion_nutrition(self, base_data: Dict, portion_grams: float) -> Dict:
        """Calcular nutrición para porción específica"""
        base_nutrition = base_data.get("nutrition_per_100g", {})
        factor = portion_grams / 100.0
        
        calculated_nutrition = {}
        for key, value in base_nutrition.items():
            calculated_nutrition[key] = round(value * factor, 2)
        
        return {
            "nutrition": calculated_nutrition,
            "source": base_data.get("source", "calculated"),
            "food_name": base_data.get("food_name", "")
        }
    
    def _get_estimated_nutrition(self, food_name: str, portion_grams: float) -> Dict:
        """Datos nutricionales estimados como último recurso"""
        # Estimaciones muy básicas por categoría
        estimates_per_100g = {
            "fruta": {"calories": 50, "protein": 1, "carbs": 12, "fat": 0.2},
            "verdura": {"calories": 25, "protein": 2, "carbs": 5, "fat": 0.1},
            "carne": {"calories": 200, "protein": 20, "carbs": 0, "fat": 15},
            "pan": {"calories": 250, "protein": 8, "carbs": 50, "fat": 3},
            "default": {"calories": 100, "protein": 5, "carbs": 15, "fat": 5}
        }
        
        # Detectar categoría básica (muy simplificado)
        category = "default"
        food_lower = food_name.lower()
        
        if any(word in food_lower for word in ["manzana", "naranja", "plátano", "fruta"]):
            category = "fruta"
        elif any(word in food_lower for word in ["lechuga", "tomate", "verdura", "vegetal"]):
            category = "verdura"
        elif any(word in food_lower for word in ["pollo", "carne", "pescado"]):
            category = "carne"
        elif any(word in food_lower for word in ["pan", "bread"]):
            category = "pan"
        
        base_nutrition = estimates_per_100g[category]
        factor = portion_grams / 100.0
        
        calculated_nutrition = {}
        for key, value in base_nutrition.items():
            calculated_nutrition[key] = round(value * factor, 2)
        
        return {
            "nutrition": calculated_nutrition,
            "source": "estimated",
            "food_name": food_name
        }