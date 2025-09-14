#!/usr/bin/env python3
"""
Script para probar las APIs de visión y bases de datos nutricionales
Fase 1 - Semana 1: Investigación y Análisis
"""

import os
import requests
import base64
from typing import Dict, List, Optional
import json
from datetime import datetime

class APITester:
    def __init__(self):
        self.results = {
            "test_date": datetime.now().isoformat(),
            "apis_tested": [],
            "results": {}
        }
    
    def test_openai_vision(self, image_path: str, api_key: str) -> Dict:
        """Probar OpenAI Vision API para reconocimiento de alimentos"""
        print("🔍 Probando OpenAI Vision API...")
        
        try:
            # Codificar imagen en base64
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Identifica todos los alimentos en esta imagen. Para cada alimento, proporciona: nombre, cantidad estimada, y si es posible, calorías aproximadas. Responde en formato JSON."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "response": result["choices"][0]["message"]["content"],
                    "usage": result.get("usage", {}),
                    "cost_estimate": self._calculate_openai_cost(result.get("usage", {}))
                }
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def test_usda_api(self, food_name: str, api_key: str) -> Dict:
        """Probar USDA Food Data Central API"""
        print(f"🥗 Probando USDA API para: {food_name}")
        
        try:
            # Buscar alimento
            search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
            search_params = {
                "query": food_name,
                "api_key": api_key,
                "pageSize": 5
            }
            
            response = requests.get(search_url, params=search_params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                foods = data.get("foods", [])
                
                if foods:
                    # Obtener detalles del primer resultado
                    food_id = foods[0]["fdcId"]
                    detail_url = f"https://api.nal.usda.gov/fdc/v1/food/{food_id}"
                    detail_params = {"api_key": api_key}
                    
                    detail_response = requests.get(detail_url, params=detail_params, timeout=10)
                    
                    if detail_response.status_code == 200:
                        food_detail = detail_response.json()
                        nutrients = self._extract_key_nutrients(food_detail.get("foodNutrients", []))
                        
                        return {
                            "status": "success",
                            "food_name": foods[0].get("description", ""),
                            "fdc_id": food_id,
                            "nutrients": nutrients,
                            "total_results": len(foods)
                        }
                
                return {
                    "status": "not_found",
                    "message": f"No se encontró información para: {food_name}"
                }
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def test_nutritionix_api(self, food_query: str, app_id: str, app_key: str) -> Dict:
        """Probar Nutritionix API"""
        print(f"🍎 Probando Nutritionix API para: {food_query}")
        
        try:
            url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
            headers = {
                "x-app-id": app_id,
                "x-app-key": app_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "query": food_query
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                foods = data.get("foods", [])
                
                if foods:
                    food = foods[0]
                    return {
                        "status": "success",
                        "food_name": food.get("food_name", ""),
                        "calories": food.get("nf_calories", 0),
                        "protein": food.get("nf_protein", 0),
                        "carbs": food.get("nf_total_carbohydrate", 0),
                        "fat": food.get("nf_total_fat", 0),
                        "serving_qty": food.get("serving_qty", 1),
                        "serving_unit": food.get("serving_unit", "")
                    }
                
                return {
                    "status": "not_found",
                    "message": f"No se encontró información para: {food_query}"
                }
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _calculate_openai_cost(self, usage: Dict) -> float:
        """Calcular costo estimado de OpenAI Vision"""
        # Precios aproximados (pueden cambiar)
        input_cost_per_token = 0.01 / 1000  # $0.01 per 1K tokens
        output_cost_per_token = 0.03 / 1000  # $0.03 per 1K tokens
        
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        
        return (input_tokens * input_cost_per_token) + (output_tokens * output_cost_per_token)
    
    def _extract_key_nutrients(self, nutrients: List[Dict]) -> Dict:
        """Extraer nutrientes clave de la respuesta USDA"""
        key_nutrients = {
            "Energy": "calories",
            "Protein": "protein",
            "Carbohydrate, by difference": "carbs",
            "Total lipid (fat)": "fat"
        }
        
        result = {}
        for nutrient in nutrients:
            nutrient_name = nutrient.get("nutrient", {}).get("name", "")
            if nutrient_name in key_nutrients:
                result[key_nutrients[nutrient_name]] = {
                    "amount": nutrient.get("amount", 0),
                    "unit": nutrient.get("nutrient", {}).get("unitName", "")
                }
        
        return result
    
    def run_comprehensive_test(self, config: Dict):
        """Ejecutar pruebas completas de todas las APIs"""
        print("🚀 Iniciando pruebas comprehensivas de APIs...")
        print("=" * 50)
        
        # Test OpenAI Vision (si hay imagen de prueba)
        if config.get("openai_api_key") and config.get("test_image_path"):
            if os.path.exists(config["test_image_path"]):
                self.results["apis_tested"].append("OpenAI Vision")
                self.results["results"]["openai_vision"] = self.test_openai_vision(
                    config["test_image_path"], 
                    config["openai_api_key"]
                )
            else:
                print("⚠️  Imagen de prueba no encontrada para OpenAI Vision")
        
        # Test USDA API
        if config.get("usda_api_key"):
            self.results["apis_tested"].append("USDA")
            test_foods = ["apple", "banana", "chicken breast"]
            self.results["results"]["usda"] = {}
            
            for food in test_foods:
                self.results["results"]["usda"][food] = self.test_usda_api(
                    food, 
                    config["usda_api_key"]
                )
        
        # Test Nutritionix API
        if config.get("nutritionix_app_id") and config.get("nutritionix_app_key"):
            self.results["apis_tested"].append("Nutritionix")
            test_queries = ["1 medium apple", "100g chicken breast", "1 cup rice"]
            self.results["results"]["nutritionix"] = {}
            
            for query in test_queries:
                self.results["results"]["nutritionix"][query] = self.test_nutritionix_api(
                    query,
                    config["nutritionix_app_id"],
                    config["nutritionix_app_key"]
                )
        
        # Guardar resultados
        self._save_results()
        self._print_summary()
    
    def _save_results(self):
        """Guardar resultados en archivo JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"api_test_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Resultados guardados en: {filename}")
    
    def _print_summary(self):
        """Imprimir resumen de resultados"""
        print("\n" + "=" * 50)
        print("📊 RESUMEN DE PRUEBAS")
        print("=" * 50)
        
        for api in self.results["apis_tested"]:
            print(f"\n🔸 {api}:")
            api_results = self.results["results"].get(api.lower().replace(" ", "_"), {})
            
            if isinstance(api_results, dict):
                success_count = 0
                total_count = 0
                
                for key, result in api_results.items():
                    total_count += 1
                    if isinstance(result, dict) and result.get("status") == "success":
                        success_count += 1
                        print(f"  ✅ {key}: OK")
                    else:
                        print(f"  ❌ {key}: Error")
                
                if total_count > 0:
                    success_rate = (success_count / total_count) * 100
                    print(f"  📈 Tasa de éxito: {success_rate:.1f}%")

def main():
    """Función principal para ejecutar las pruebas"""
    print("🧪 PROBADOR DE APIs - Contador de Calorías")
    print("Fase 1 - Semana 1: Investigación y Análisis")
    print("=" * 50)
    
    # Configuración (reemplazar con tus API keys)
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "usda_api_key": os.getenv("USDA_API_KEY", ""),
        "nutritionix_app_id": os.getenv("NUTRITIONIX_APP_ID", ""),
        "nutritionix_app_key": os.getenv("NUTRITIONIX_APP_KEY", ""),
        "test_image_path": "test_images/sample_food.jpg"
    }
    
    # Verificar configuración
    missing_keys = []
    if not config["openai_api_key"]:
        missing_keys.append("OPENAI_API_KEY")
    if not config["usda_api_key"]:
        missing_keys.append("USDA_API_KEY")
    if not config["nutritionix_app_id"] or not config["nutritionix_app_key"]:
        missing_keys.append("NUTRITIONIX_APP_ID/KEY")
    
    if missing_keys:
        print("⚠️  Variables de entorno faltantes:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\nConfigura las variables de entorno o edita el script directamente.")
        return
    
    # Ejecutar pruebas
    tester = APITester()
    tester.run_comprehensive_test(config)

if __name__ == "__main__":
    main()