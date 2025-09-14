"""
Pruebas para el backend FastAPI
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import json

# Importar la aplicación
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))

from main import app

client = TestClient(app)

class TestHealthEndpoints:
    """Pruebas de endpoints de salud"""
    
    def test_root_endpoint(self):
        """Probar endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Contador de Calorías API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "active"
    
    def test_health_check(self):
        """Probar health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "services" in data

class TestAuthEndpoints:
    """Pruebas de autenticación"""
    
    def test_login_success(self):
        """Probar login exitoso"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "tokens" in data
        assert data["tokens"]["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self):
        """Probar login con credenciales inválidas"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "invalid@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Credenciales inválidas"

class TestNutritionEndpoints:
    """Pruebas de endpoints de nutrición"""
    
    def setup_method(self):
        """Setup para cada test"""
        # Token de prueba (simulado)
        self.headers = {"Authorization": "Bearer test_token"}
    
    @patch('routers.auth.get_current_user')
    def test_search_foods(self, mock_user):
        """Probar búsqueda de alimentos"""
        mock_user.return_value = {"id": 1, "email": "test@example.com"}
        
        response = client.get(
            "/api/v1/foods/search?q=manzana",
            headers=self.headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "query" in data
        assert "results" in data
        assert data["query"] == "manzana"
    
    @patch('routers.auth.get_current_user')
    def test_get_food_details(self, mock_user):
        """Probar obtener detalles de alimento"""
        mock_user.return_value = {"id": 1, "email": "test@example.com"}
        
        response = client.get(
            "/api/v1/foods/usda_169905",
            headers=self.headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "usda_169905"
        assert "nutrition_per_100g" in data

class TestAnalyticsEndpoints:
    """Pruebas de endpoints de analytics"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.headers = {"Authorization": "Bearer test_token"}
    
    @patch('routers.auth.get_current_user')
    def test_daily_summary(self, mock_user):
        """Probar resumen diario"""
        mock_user.return_value = {"id": 1, "email": "test@example.com"}
        
        response = client.get(
            "/api/v1/analytics/daily-summary",
            headers=self.headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "period" in data
        assert "daily_summaries" in data
        assert "averages" in data
    
    @patch('routers.auth.get_current_user')
    def test_trends(self, mock_user):
        """Probar tendencias"""
        mock_user.return_value = {"id": 1, "email": "test@example.com"}
        
        response = client.get(
            "/api/v1/analytics/trends?period=30d&metric=calories",
            headers=self.headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["period"] == "30d"
        assert data["metric"] == "calories"
        assert "data_points" in data

class TestMLService:
    """Pruebas del servicio ML"""
    
    @pytest.mark.asyncio
    @patch('services.ml_service.openai.AsyncOpenAI')
    async def test_analyze_food_image(self, mock_openai):
        """Probar análisis de imagen"""
        from services.ml_service import MLService
        
        # Mock de respuesta de OpenAI
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = '''
        {
          "foods": [
            {
              "name": "manzana",
              "portion_grams": 150,
              "confidence": 8,
              "notes": "manzana roja mediana"
            }
          ],
          "overall_confidence": 8,
          "image_quality": "good"
        }
        '''
        
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        ml_service = MLService()
        result = await ml_service.analyze_food_image(b"fake_image_data")
        
        assert len(result) == 1
        assert result[0]["name"] == "manzana"
        assert result[0]["portion_grams"] == 150

class TestNutritionService:
    """Pruebas del servicio de nutrición"""
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.get')
    async def test_search_usda(self, mock_get):
        """Probar búsqueda en USDA"""
        from services.nutrition_service import NutritionService
        
        # Mock de respuesta USDA
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "foods": [
                {
                    "description": "Apple, raw",
                    "foodNutrients": [
                        {"nutrientName": "Energy", "value": 52},
                        {"nutrientName": "Protein", "value": 0.26}
                    ]
                }
            ]
        }
        mock_get.return_value.__aenter__.return_value = mock_response
        
        nutrition_service = NutritionService()
        result = await nutrition_service._search_usda("apple")
        
        assert result is not None
        assert "nutrition_per_100g" in result

class TestRateLimiting:
    """Pruebas de rate limiting"""
    
    def test_rate_limit_exceeded(self):
        """Probar que se aplique rate limiting"""
        # Hacer muchos requests rápidamente
        responses = []
        for i in range(15):  # Más del límite de 10/min para análisis
            response = client.post(
                "/api/v1/analyze/image",
                files={"image": ("test.jpg", b"fake_image", "image/jpeg")},
                headers={"Authorization": "Bearer test_token"}
            )
            responses.append(response.status_code)
        
        # Al menos uno debería ser 429 (Too Many Requests)
        assert 429 in responses

if __name__ == "__main__":
    pytest.main([__file__, "-v"])