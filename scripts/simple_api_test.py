#!/usr/bin/env python3
"""
Script simplificado para probar APIs sin dependencias externas
Solo usa librerías estándar de Python
"""

import json
import urllib.request
import urllib.parse
import base64
import os
import time
from datetime import datetime

def load_env_file():
    """Cargar variables de entorno desde archivo .env"""
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print("❌ Archivo .env no encontrado")
        return {}
    return env_vars

def test_usda_api(food_name, api_key):
    """Probar USDA Food Data Central API"""
    print(f"🥗 Probando USDA API para: {food_name}")
    
    try:
        # Construir URL de búsqueda
        base_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
        params = {
            'query': food_name,
            'api_key': api_key,
            'pageSize': '5'
        }
        
        url = base_url + '?' + urllib.parse.urlencode(params)
        
        # Hacer request
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        foods = data.get('foods', [])
        if foods:
            food = foods[0]
            return {
                "status": "success",
                "food_name": food.get('description', ''),
                "fdc_id": food.get('fdcId', ''),
                "total_results": len(foods)
            }
        else:
            return {
                "status": "not_found",
                "message": f"No se encontró información para: {food_name}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def test_nutritionix_api(food_query, app_id, app_key):
    """Probar Nutritionix API"""
    print(f"🍎 Probando Nutritionix API para: {food_query}")
    
    try:
        url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
        
        # Preparar datos
        data = json.dumps({"query": food_query}).encode('utf-8')
        
        # Preparar headers
        req = urllib.request.Request(url, data=data)
        req.add_header('Content-Type', 'application/json')
        req.add_header('x-app-id', app_id)
        req.add_header('x-app-key', app_key)
        
        # Hacer request
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
        
        foods = result.get('foods', [])
        if foods:
            food = foods[0]
            return {
                "status": "success",
                "food_name": food.get('food_name', ''),
                "calories": food.get('nf_calories', 0),
                "protein": food.get('nf_protein', 0),
                "carbs": food.get('nf_total_carbohydrate', 0),
                "fat": food.get('nf_total_fat', 0)
            }
        else:
            return {
                "status": "not_found",
                "message": f"No se encontró información para: {food_query}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def test_openai_vision_simple(api_key):
    """Probar OpenAI Vision API con texto simple"""
    print("🤖 Probando OpenAI Vision API (sin imagen)")
    
    try:
        url = "https://api.openai.com/v1/chat/completions"
        
        # Preparar datos para test simple
        data = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "user",
                    "content": "Responde solo 'API funcionando correctamente' si recibes este mensaje"
                }
            ],
            "max_tokens": 10
        }
        
        # Preparar request
        req = urllib.request.Request(url, json.dumps(data).encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', f'Bearer {api_key}')
        
        # Hacer request
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode())
        
        if 'choices' in result and result['choices']:
            return {
                "status": "success",
                "response": result['choices'][0]['message']['content'],
                "usage": result.get('usage', {})
            }
        else:
            return {
                "status": "error",
                "error": "Respuesta inesperada de la API"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def run_simple_tests():
    """Ejecutar pruebas simplificadas"""
    print("🧪 PRUEBAS SIMPLIFICADAS DE APIs")
    print("Contador de Calorías - Fase 1")
    print("=" * 50)
    
    # Cargar configuración
    env_vars = load_env_file()
    
    if not env_vars:
        print("❌ No se pudieron cargar las variables de entorno")
        return
    
    results = {
        "test_date": datetime.now().isoformat(),
        "results": {}
    }
    
    # Test USDA API
    usda_key = env_vars.get('USDA_API_KEY')
    if usda_key:
        print("\n" + "-" * 30)
        test_foods = ['apple', 'banana', 'chicken breast']
        usda_results = {}
        
        for food in test_foods:
            result = test_usda_api(food, usda_key)
            usda_results[food] = result
            
            if result['status'] == 'success':
                print(f"✅ {food}: {result['food_name']}")
            else:
                print(f"❌ {food}: {result.get('error', 'Error')}")
        
        results['results']['usda'] = usda_results
    else:
        print("⚠️  USDA API key no encontrada")
    
    # Test Nutritionix API
    nutritionix_id = env_vars.get('NUTRITIONIX_APP_ID')
    nutritionix_key = env_vars.get('NUTRITIONIX_APP_KEY')
    
    if nutritionix_id and nutritionix_key:
        print("\n" + "-" * 30)
        test_queries = ['1 medium apple', '100g chicken breast']
        nutritionix_results = {}
        
        for query in test_queries:
            result = test_nutritionix_api(query, nutritionix_id, nutritionix_key)
            nutritionix_results[query] = result
            
            if result['status'] == 'success':
                print(f"✅ {query}: {result['calories']} cal")
            else:
                print(f"❌ {query}: {result.get('error', 'Error')}")
        
        results['results']['nutritionix'] = nutritionix_results
    else:
        print("⚠️  Nutritionix API keys no encontradas")
    
    # Test OpenAI API (simple)
    openai_key = env_vars.get('OPENAI_API_KEY')
    if openai_key:
        print("\n" + "-" * 30)
        result = test_openai_vision_simple(openai_key)
        results['results']['openai'] = result
        
        if result['status'] == 'success':
            print(f"✅ OpenAI API: Conectado correctamente")
        else:
            print(f"❌ OpenAI API: {result.get('error', 'Error')}")
    else:
        print("⚠️  OpenAI API key no encontrada")
    
    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"simple_test_results_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Resultados guardados en: {filename}")
    except Exception as e:
        print(f"⚠️  No se pudieron guardar resultados: {e}")
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    total_apis = 0
    working_apis = 0
    
    for api_name, api_result in results['results'].items():
        total_apis += 1
        if isinstance(api_result, dict):
            if api_result.get('status') == 'success':
                working_apis += 1
                print(f"✅ {api_name.upper()}: Funcionando")
            else:
                print(f"❌ {api_name.upper()}: Error")
        else:
            # Para casos como USDA que tiene múltiples tests
            success_count = 0
            total_count = 0
            for test_name, test_result in api_result.items():
                total_count += 1
                if test_result.get('status') == 'success':
                    success_count += 1
            
            if success_count > 0:
                working_apis += 1
                print(f"✅ {api_name.upper()}: {success_count}/{total_count} tests exitosos")
            else:
                print(f"❌ {api_name.upper()}: {success_count}/{total_count} tests exitosos")
    
    print(f"\n🎯 APIs funcionando: {working_apis}/{total_apis}")
    
    if working_apis >= 2:
        print("🎉 ¡Suficientes APIs funcionando para continuar con el MVP!")
    else:
        print("⚠️  Se necesitan al menos 2 APIs funcionando para el MVP")

if __name__ == "__main__":
    run_simple_tests()