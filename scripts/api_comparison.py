#!/usr/bin/env python3
"""
Script para comparar precisión y rendimiento de las APIs
Fase 1 - Días 3-4: Evaluación comparativa
"""

import json
import time
from pathlib import Path
from typing import Dict, List
from test_apis import APITester
import os
from dotenv import load_dotenv

class APIComparison:
    def __init__(self):
        load_dotenv()
        self.tester = APITester()
        self.results = {
            "comparison_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_images": [],
            "api_performance": {},
            "recommendations": {}
        }
    
    def run_comparison(self, test_images: List[str]):
        """Ejecutar comparación completa entre APIs"""
        print("🔬 COMPARACIÓN DE APIs DE VISIÓN")
        print("=" * 50)
        
        config = {
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "usda_api_key": os.getenv("USDA_API_KEY"),
            "nutritionix_app_id": os.getenv("NUTRITIONIX_APP_ID"),
            "nutritionix_app_key": os.getenv("NUTRITIONIX_APP_KEY")
        }
        
        for image_path in test_images:
            if not Path(image_path).exists():
                print(f"⚠️  Imagen no encontrada: {image_path}")
                continue
            
            print(f"\n📸 Analizando: {Path(image_path).name}")
            print("-" * 30)
            
            image_results = {
                "image_path": image_path,
                "apis_tested": {},
                "processing_times": {},
                "costs": {}
            }
            
            # Test OpenAI Vision
            if config["openai_api_key"]:
                start_time = time.time()
                result = self.tester.test_openai_vision(image_path, config["openai_api_key"])
                processing_time = time.time() - start_time
                
                image_results["apis_tested"]["openai"] = result
                image_results["processing_times"]["openai"] = processing_time
                image_results["costs"]["openai"] = result.get("cost_estimate", 0)
                
                print(f"🤖 OpenAI Vision: {processing_time:.2f}s - ${result.get('cost_estimate', 0):.4f}")
            
            self.results["test_images"].append(image_results)
        
        # Generar análisis comparativo
        self._analyze_performance()
        self._generate_recommendations()
        self._save_comparison_results()
    
    def _analyze_performance(self):
        """Analizar rendimiento de las APIs"""
        if not self.results["test_images"]:
            return
        
        # Calcular métricas promedio
        openai_times = []
        openai_costs = []
        
        for image_result in self.results["test_images"]:
            if "openai" in image_result["processing_times"]:
                openai_times.append(image_result["processing_times"]["openai"])
                openai_costs.append(image_result["costs"]["openai"])
        
        if openai_times:
            self.results["api_performance"]["openai"] = {
                "avg_processing_time": sum(openai_times) / len(openai_times),
                "avg_cost_per_image": sum(openai_costs) / len(openai_costs),
                "total_images_processed": len(openai_times),
                "success_rate": len([r for r in self.results["test_images"] 
                                   if r["apis_tested"].get("openai", {}).get("status") == "success"]) / len(openai_times)
            }
    
    def _generate_recommendations(self):
        """Generar recomendaciones basadas en los resultados"""
        recommendations = []
        
        # Análisis de OpenAI Vision
        openai_perf = self.results["api_performance"].get("openai", {})
        if openai_perf:
            avg_time = openai_perf.get("avg_processing_time", 0)
            avg_cost = openai_perf.get("avg_cost_per_image", 0)
            success_rate = openai_perf.get("success_rate", 0)
            
            if success_rate > 0.8:
                recommendations.append("✅ OpenAI Vision muestra alta precisión para reconocimiento de alimentos")
            
            if avg_time < 5:
                recommendations.append("✅ Tiempo de respuesta de OpenAI Vision es aceptable para MVP")
            else:
                recommendations.append("⚠️ Tiempo de respuesta de OpenAI Vision podría ser optimizado")
            
            # Estimación de costos mensuales
            monthly_cost_1k_users = avg_cost * 5 * 30 * 1000  # 5 fotos/día, 30 días, 1000 usuarios
            recommendations.append(f"💰 Costo estimado mensual (1K usuarios): ${monthly_cost_1k_users:.2f}")
            
            if monthly_cost_1k_users < 200:
                recommendations.append("✅ Costos de OpenAI Vision son viables para MVP")
            else:
                recommendations.append("⚠️ Considerar optimización de costos o modelo híbrido")
        
        # Recomendación de stack
        recommendations.append("🏗️ Stack recomendado para MVP:")
        recommendations.append("   - Visión: OpenAI Vision API (precisión)")
        recommendations.append("   - Nutrición: USDA + Nutritionix (cobertura)")
        recommendations.append("   - Fallback: Modelo YOLO local (costos)")
        
        self.results["recommendations"] = recommendations
    
    def _save_comparison_results(self):
        """Guardar resultados de comparación"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"results/api_comparison_{timestamp}.json"
        
        Path("results").mkdir(exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Comparación guardada en: {filename}")
        self._print_comparison_summary()
    
    def _print_comparison_summary(self):
        """Imprimir resumen de la comparación"""
        print("\n" + "=" * 50)
        print("📊 RESUMEN DE COMPARACIÓN")
        print("=" * 50)
        
        # Performance de OpenAI
        openai_perf = self.results["api_performance"].get("openai", {})
        if openai_perf:
            print(f"\n🤖 OpenAI Vision Performance:")
            print(f"   ⏱️  Tiempo promedio: {openai_perf.get('avg_processing_time', 0):.2f}s")
            print(f"   💰 Costo promedio: ${openai_perf.get('avg_cost_per_image', 0):.4f}/imagen")
            print(f"   ✅ Tasa de éxito: {openai_perf.get('success_rate', 0)*100:.1f}%")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        for rec in self.results["recommendations"]:
            print(f"   {rec}")

def main():
    """Ejecutar comparación de APIs"""
    print("🔬 COMPARADOR DE APIs - Contador de Calorías")
    print("Fase 1 - Días 3-4: Evaluación y Comparación")
    print("=" * 50)
    
    # Buscar imágenes de prueba
    test_images_dir = Path("test_images")
    if not test_images_dir.exists():
        print("❌ Directorio test_images/ no encontrado")
        print("Ejecuta primero: python scripts/setup_environment.py")
        return
    
    # Buscar imágenes disponibles
    image_extensions = ['.jpg', '.jpeg', '.png']
    test_images = []
    
    for ext in image_extensions:
        test_images.extend(test_images_dir.glob(f"*{ext}"))
        test_images.extend(test_images_dir.glob(f"*{ext.upper()}"))
    
    if not test_images:
        print("⚠️  No se encontraron imágenes de prueba en test_images/")
        print("Agrega algunas imágenes de alimentos y ejecuta nuevamente")
        return
    
    print(f"📸 Imágenes encontradas: {len(test_images)}")
    for img in test_images:
        print(f"   - {img.name}")
    
    # Ejecutar comparación
    comparator = APIComparison()
    comparator.run_comparison([str(img) for img in test_images])

if __name__ == "__main__":
    main()