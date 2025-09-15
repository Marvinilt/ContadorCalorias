export default function Analytics() {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">Analytics</h1>
      
      <div className="grid md:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Resumen Diario</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span>Calorías consumidas</span>
              <span className="font-medium">1,850 / 2,200</span>
            </div>
            <div className="flex justify-between">
              <span>Proteínas</span>
              <span className="font-medium">85g / 110g</span>
            </div>
            <div className="flex justify-between">
              <span>Carbohidratos</span>
              <span className="font-medium">220g / 275g</span>
            </div>
            <div className="flex justify-between">
              <span>Grasas</span>
              <span className="font-medium">68g / 73g</span>
            </div>
          </div>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Análisis Recientes</h2>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span>Manzana roja</span>
              <span className="text-sm text-gray-500">95 cal</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Pan integral</span>
              <span className="text-sm text-gray-500">151 cal</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Pollo a la plancha</span>
              <span className="text-sm text-gray-500">165 cal</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}