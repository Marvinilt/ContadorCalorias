import { Link } from 'react-router-dom'
import { Camera, BarChart3, Zap } from 'lucide-react'

export default function Home() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Hero Section */}
      <div className="text-center py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Analiza tus alimentos con IA
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Toma una foto de tu comida y obtén información nutricional detallada 
          al instante usando inteligencia artificial avanzada.
        </p>
        <Link
          to="/camera"
          className="btn-primary inline-flex items-center gap-2 text-lg px-8 py-3"
        >
          <Camera className="h-5 w-5" />
          Comenzar Análisis
        </Link>
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-3 gap-8 py-12">
        <div className="text-center">
          <div className="bg-blue-100 rounded-full p-3 w-12 h-12 mx-auto mb-4 flex items-center justify-center">
            <Camera className="h-6 w-6 text-blue-600" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Análisis Instantáneo</h3>
          <p className="text-gray-600">
            Sube una foto y obtén resultados nutricionales en segundos
          </p>
        </div>

        <div className="text-center">
          <div className="bg-green-100 rounded-full p-3 w-12 h-12 mx-auto mb-4 flex items-center justify-center">
            <Zap className="h-6 w-6 text-green-600" />
          </div>
          <h3 className="text-lg font-semibold mb-2">IA Avanzada</h3>
          <p className="text-gray-600">
            Tecnología de visión artificial para reconocimiento preciso
          </p>
        </div>

        <div className="text-center">
          <div className="bg-purple-100 rounded-full p-3 w-12 h-12 mx-auto mb-4 flex items-center justify-center">
            <BarChart3 className="h-6 w-6 text-purple-600" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Seguimiento</h3>
          <p className="text-gray-600">
            Monitorea tu progreso nutricional con analytics detallados
          </p>
        </div>
      </div>

      {/* Stats */}
      <div className="bg-white rounded-lg shadow-md p-8 mb-12">
        <h2 className="text-2xl font-bold text-center mb-8">
          Información Nutricional Precisa
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div>
            <div className="text-3xl font-bold text-blue-600 mb-1">300k+</div>
            <div className="text-sm text-gray-600">Alimentos en base de datos</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-green-600 mb-1">95%</div>
            <div className="text-sm text-gray-600">Precisión en detección</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-purple-600 mb-1">&lt;5s</div>
            <div className="text-sm text-gray-600">Tiempo de análisis</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-orange-600 mb-1">24/7</div>
            <div className="text-sm text-gray-600">Disponibilidad</div>
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="text-center py-8">
        <h2 className="text-2xl font-bold mb-4">¿Listo para comenzar?</h2>
        <p className="text-gray-600 mb-6">
          Toma tu primera foto y descubre la información nutricional de tus alimentos
        </p>
        <Link
          to="/camera"
          className="btn-primary inline-flex items-center gap-2"
        >
          <Camera className="h-4 w-4" />
          Analizar Ahora
        </Link>
      </div>
    </div>
  )
}