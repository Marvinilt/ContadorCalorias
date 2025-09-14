"""
Servicio de Machine Learning para análisis de imágenes
"""

import openai
import base64
import json
import asyncio
from typing import List, Dict
from config import settings

class MLService:
    """Servicio para análisis de imágenes con OpenAI Vision"""
    
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4-vision-preview"
        
    async def analyze_food_image(self, image_data: bytes) -> List[Dict]:
        """
        Analizar imagen y extraer información de alimentos
        """
        try:
            # Convertir imagen a base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{image_base64}"
            
            # Llamada a OpenAI Vision API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self._get_analysis_prompt()},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }],
                max_tokens=500,
                temperature=0.1
            )
            
            # Parsear respuesta
            content = response.choices[0].message.content
            return self._parse_analysis_response(content)
            
        except Exception as e:
            print(f"❌ Error en análisis ML: {e}")
            # Fallback: devolver datos de ejemplo
            return self._get_fallback_response()
    
    def _get_analysis_prompt(self) -> str:
        """Prompt optimizado para análisis de alimentos"""
        return """
        Analiza esta imagen de alimentos y proporciona información detallada.
        
        Responde ÚNICAMENTE con un JSON válido en este formato:
        {
          "foods": [
            {
              "name": "nombre_del_alimento",
              "portion_grams": 150,
              "confidence": 8,
              "notes": "descripción adicional"
            }
          ],
          "overall_confidence": 7,
          "image_quality": "good"
        }
        
        Instrucciones:
        1. Identifica TODOS los alimentos visibles
        2. Estima porciones en gramos de forma realista
        3. Asigna confianza del 1-10 (10 = muy seguro)
        4. Usa nombres comunes en español
        5. Si no hay alimentos, devuelve array vacío
        
        Responde SOLO con el JSON, sin texto adicional.
        """
    
    def _parse_analysis_response(self, content: str) -> List[Dict]:
        """Parsear respuesta de OpenAI"""
        try:
            # Limpiar respuesta y extraer JSON
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            data = json.loads(content)
            return data.get("foods", [])
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parseando JSON: {e}")
            print(f"Contenido recibido: {content}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> List[Dict]:
        """Respuesta de fallback en caso de error"""
        return [
            {
                "name": "Alimento no identificado",
                "portion_grams": 100,
                "confidence": 3,
                "notes": "Error en el análisis, valores estimados"
            }
        ]
    
    async def validate_image(self, image_data: bytes) -> bool:
        """Validar que la imagen contiene alimentos"""
        # Implementar validación básica
        return len(image_data) > 1000  # Mínimo 1KB
    
    async def get_image_quality_score(self, image_data: bytes) -> int:
        """Evaluar calidad de la imagen (1-10)"""
        # Implementación básica - en producción usar análisis más sofisticado
        size_score = min(10, len(image_data) // 100000)  # Basado en tamaño
        return max(1, size_score)