import { useMutation, useQuery } from 'react-query'
import { api } from '../services/api'

interface AnalyzeImageRequest {
  image: File
  meal_type?: string
  notes?: string
}

interface AnalysisResult {
  analysis_id: string
  status: string
  message: string
}

interface FoodAnalysis {
  id: string
  status: 'processing' | 'completed' | 'failed'
  confidence_score?: number
  total_nutrition?: {
    calories: number
    protein: number
    carbs: number
    fat: number
    fiber: number
  }
  detected_foods?: Array<{
    name: string
    portion: { grams: number; description: string }
    nutrition: {
      calories: number
      protein: number
      carbs: number
      fat: number
    }
    confidence: number
  }>
}

export function useAnalyzeImage() {
  return useMutation<AnalysisResult, Error, AnalyzeImageRequest>(
    async ({ image, meal_type, notes }) => {
      const formData = new FormData()
      formData.append('image', image)
      if (meal_type) formData.append('meal_type', meal_type)
      if (notes) formData.append('notes', notes)
      
      const response = await api.post('/analyze/image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      return response.data
    }
  )
}

export function useAnalysisResult(analysisId: string) {
  return useQuery<FoodAnalysis, Error>(
    ['analysis', analysisId],
    async () => {
      const response = await api.get(`/analyze/${analysisId}`)
      return response.data
    },
    {
      enabled: !!analysisId,
      refetchInterval: (data) => {
        return data?.status === 'processing' ? 2000 : false
      }
    }
  )
}