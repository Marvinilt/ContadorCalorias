import { useParams } from 'react-router-dom'
import { Loader2, AlertCircle, CheckCircle } from 'lucide-react'
import { useAnalysisResult } from '../hooks/useAnalysis'

export default function Results() {
  const { analysisId } = useParams<{ analysisId: string }>()
  const { data: analysis, isLoading, error } = useAnalysisResult(analysisId!)

  if (isLoading) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="card text-center">
          <Loader2 className="mx-auto h-8 w-8 animate-spin text-blue-600 mb-4" />
          <h2 className="text-xl font-semibold mb-2">Analizando imagen...</h2>
          <p className="text-gray-600">Esto puede tomar unos segundos</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="card text-center">
          <AlertCircle className="mx-auto h-8 w-8 text-red-600 mb-4" />
          <h2 className="text-xl font-semibold mb-2">Error en el análisis</h2>
          <p className="text-gray-600">No se pudo procesar la imagen</p>
        </div>
      </div>
    )
  }

  if (analysis?.status === 'processing') {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="card text-center">
          <Loader2 className="mx-auto h-8 w-8 animate-spin text-blue-600 mb-4" />
          <h2 className="text-xl font-semibold mb-2">Procesando...</h2>
          <p className="text-gray-600">Analizando los alimentos detectados</p>
        </div>
      </div>
    )
  }

  if (analysis?.status === 'failed') {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="card text-center">
          <AlertCircle className="mx-auto h-8 w-8 text-red-600 mb-4" />
          <h2 className="text-xl font-semibold mb-2">Análisis fallido</h2>
          <p className="text-gray-600">No se pudieron detectar alimentos en la imagen</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-2">
          <CheckCircle className="h-6 w-6 text-green-600" />
          <h1 className="text-2xl font-bold">Análisis Completado</h1>
        </div>
        <p className="text-gray-600">
          Confianza: {analysis?.confidence_score}/10
        </p>
      </div>

      {/* Resumen Nutricional */}
      <div className="card mb-6">
        <h2 className="text-xl font-semibold mb-4">Resumen Nutricional</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {Math.round(analysis?.total_nutrition?.calories || 0)}
            </div>
            <div className="text-sm text-gray-600">Calorías</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {Math.round(analysis?.total_nutrition?.protein || 0)}g
            </div>
            <div className="text-sm text-gray-600">Proteína</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-600">
              {Math.round(analysis?.total_nutrition?.carbs || 0)}g
            </div>
            <div className="text-sm text-gray-600">Carbohidratos</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-red-600">
              {Math.round(analysis?.total_nutrition?.fat || 0)}g
            </div>
            <div className="text-sm text-gray-600">Grasas</div>
          </div>
        </div>
      </div>

      {/* Alimentos Detectados */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Alimentos Detectados</h2>
        <div className="space-y-4">
          {analysis?.detected_foods?.map((food, index) => (
            <div key={index} className="border rounded-lg p-4">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-medium">{food.name}</h3>
                <span className="text-sm text-gray-500">
                  Confianza: {food.confidence}/10
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-3">
                {food.portion.description} ({food.portion.grams}g)
              </p>
              <div className="grid grid-cols-4 gap-2 text-sm">
                <div>
                  <span className="font-medium">{Math.round(food.nutrition.calories)}</span>
                  <span className="text-gray-500 ml-1">cal</span>
                </div>
                <div>
                  <span className="font-medium">{Math.round(food.nutrition.protein)}g</span>
                  <span className="text-gray-500 ml-1">prot</span>
                </div>
                <div>
                  <span className="font-medium">{Math.round(food.nutrition.carbs)}g</span>
                  <span className="text-gray-500 ml-1">carb</span>
                </div>
                <div>
                  <span className="font-medium">{Math.round(food.nutrition.fat)}g</span>
                  <span className="text-gray-500 ml-1">grasa</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}