import { useState, useRef } from 'react'
import { Camera as CameraIcon, Upload, RotateCcw } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useAnalyzeImage } from '../hooks/useAnalysis'

export default function Camera() {
  const [image, setImage] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [isCapturing, setIsCapturing] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()
  
  const analyzeImageMutation = useAnalyzeImage()

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setImage(file)
      const reader = new FileReader()
      reader.onload = (e) => setPreview(e.target?.result as string)
      reader.readAsDataURL(file)
    }
  }

  const handleAnalyze = async () => {
    if (!image) return
    
    setIsCapturing(true)
    try {
      const result = await analyzeImageMutation.mutateAsync({
        image,
        meal_type: 'lunch',
        notes: ''
      })
      navigate(`/results/${result.analysis_id}`)
    } catch (error) {
      console.error('Error analyzing image:', error)
    } finally {
      setIsCapturing(false)
    }
  }

  const resetImage = () => {
    setImage(null)
    setPreview(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Analizar Alimentos
        </h1>
        <p className="text-gray-600">
          Toma una foto o sube una imagen de tu comida para obtener información nutricional
        </p>
      </div>

      <div className="card">
        {!preview ? (
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
            <CameraIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <p className="text-gray-600 mb-4">
              Selecciona una imagen de tu comida
            </p>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              className="btn-primary inline-flex items-center gap-2"
            >
              <Upload className="h-4 w-4" />
              Subir Imagen
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="relative">
              <img
                src={preview}
                alt="Preview"
                className="w-full h-64 object-cover rounded-lg"
              />
              <button
                onClick={resetImage}
                className="absolute top-2 right-2 p-2 bg-white rounded-full shadow-md hover:bg-gray-50"
              >
                <RotateCcw className="h-4 w-4" />
              </button>
            </div>
            
            <div className="flex gap-3">
              <button
                onClick={handleAnalyze}
                disabled={isCapturing}
                className="btn-primary flex-1 disabled:opacity-50"
              >
                {isCapturing ? 'Analizando...' : 'Analizar Imagen'}
              </button>
              <button
                onClick={resetImage}
                className="btn-secondary"
              >
                Cambiar
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="mt-8 text-sm text-gray-500 text-center">
        <p>Formatos soportados: JPG, PNG, WEBP (máx. 5MB)</p>
      </div>
    </div>
  )
}