# 🎨 Configuración del Frontend - Contador de Calorías

**Fecha**: 14 de Septiembre, 2025  
**Versión**: MVP 1.0

## 📋 Resumen

Guía completa para configurar y ejecutar el frontend React del sistema de análisis nutricional por imágenes.

## 🔧 Prerrequisitos

### Software Requerido
- **Node.js 16+**
- **npm 8+** o **yarn 1.22+**
- **Git**

## ⚙️ Instalación

### 1. Navegar al Frontend
```bash
cd src/frontend
```

### 2. Instalar Dependencias
```bash
# Con npm
npm install

# Con yarn
yarn install
```

### 3. Configurar Variables de Entorno
```bash
# Crear archivo .env.local
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env.local
```

## 🚀 Ejecución

### Desarrollo
```bash
# Iniciar servidor de desarrollo
npm run dev

# Con yarn
yarn dev
```

**URL**: http://localhost:3000

### Producción
```bash
# Build para producción
npm run build

# Preview del build
npm run preview
```

## 🧪 Testing

### Ejecutar Pruebas
```bash
# Todas las pruebas
npm test

# Con watch mode
npm run test:watch

# Con UI
npm run test:ui

# Con cobertura
npm run test:coverage
```

### Estructura de Pruebas
```
src/
├── __tests__/
│   ├── Camera.test.tsx
│   ├── Results.test.tsx
│   └── Auth.test.tsx
├── components/
└── hooks/
```

## 📁 Estructura del Proyecto

```
src/frontend/
├── public/                 # Assets estáticos
├── src/
│   ├── components/        # Componentes React
│   │   ├── Camera.tsx    # Captura de imágenes
│   │   ├── Results.tsx   # Resultados de análisis
│   │   ├── Layout.tsx    # Layout principal
│   │   ├── Home.tsx      # Página de inicio
│   │   ├── Login.tsx     # Autenticación
│   │   └── Analytics.tsx # Dashboard
│   ├── hooks/            # Hooks personalizados
│   │   ├── useAuth.tsx   # Gestión de autenticación
│   │   └── useAnalysis.ts # Análisis de imágenes
│   ├── services/         # Servicios API
│   │   └── api.ts        # Cliente Axios
│   ├── types/            # Tipos TypeScript
│   ├── utils/            # Utilidades
│   ├── __tests__/        # Pruebas unitarias
│   ├── App.tsx           # Componente principal
│   ├── main.tsx          # Entry point
│   └── index.css         # Estilos globales
├── package.json          # Dependencias
├── vite.config.ts        # Configuración Vite
├── tailwind.config.js    # Configuración Tailwind
└── tsconfig.json         # Configuración TypeScript
```

## 🎨 Stack Tecnológico

### Core
- **React 18** - Framework principal
- **TypeScript** - Tipado estático
- **Vite** - Build tool y dev server

### Routing y Estado
- **React Router** - Navegación SPA
- **React Query** - Estado del servidor
- **Context API** - Estado global

### Estilos
- **Tailwind CSS** - Framework de estilos
- **Lucide React** - Iconos

### Testing
- **Vitest** - Test runner
- **Testing Library** - Utilidades de testing
- **jsdom** - DOM environment

## 🔧 Configuración Detallada

### Vite Configuration
```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true
  }
})
```

### Tailwind Configuration
```javascript
// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### TypeScript Configuration
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true
  }
}
```

## 🔌 Integración con Backend

### API Configuration
```typescript
// src/services/api.ts
import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
})

// Interceptors para JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

### Environment Variables
```bash
# .env.local
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=Contador de Calorías
```

## 🧪 Testing Strategy

### Unit Tests
```typescript
// Camera.test.tsx
import { render, screen } from '@testing-library/react'
import Camera from '../components/Camera'

test('renders camera interface', () => {
  render(<Camera />)
  expect(screen.getByText('Analizar Alimentos')).toBeInTheDocument()
})
```

### Integration Tests
```typescript
// Auth integration test
test('login flow works correctly', async () => {
  render(<App />)
  
  fireEvent.click(screen.getByText('Iniciar Sesión'))
  fireEvent.change(screen.getByLabelText('Email'), {
    target: { value: 'test@example.com' }
  })
  
  // Assert navigation to dashboard
})
```

## 📱 Responsive Design

### Breakpoints
```css
/* Tailwind breakpoints */
sm: 640px   /* Mobile landscape */
md: 768px   /* Tablet */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large desktop */
```

### Mobile-First Approach
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Responsive grid */}
</div>
```

## 🚀 Performance

### Code Splitting
```typescript
// Lazy loading de componentes
const Analytics = lazy(() => import('./components/Analytics'))

<Suspense fallback={<Loading />}>
  <Analytics />
</Suspense>
```

### Bundle Analysis
```bash
# Analizar bundle size
npm run build
npx vite-bundle-analyzer dist
```

## 🔒 Seguridad

### Content Security Policy
```html
<!-- En index.html -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; img-src 'self' data: blob:;">
```

### Input Sanitization
```typescript
// Validación de archivos
const validateFile = (file: File) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']
  const maxSize = 5 * 1024 * 1024 // 5MB
  
  return allowedTypes.includes(file.type) && file.size <= maxSize
}
```

## 🐛 Troubleshooting

### Problemas Comunes

#### Error de CORS
```bash
# Verificar que el backend esté ejecutándose
curl http://localhost:8000/health

# Verificar configuración CORS en backend
```

#### Problemas de Build
```bash
# Limpiar cache
rm -rf node_modules/.vite
npm run dev
```

#### TypeScript Errors
```bash
# Verificar tipos
npx tsc --noEmit
```

## 📊 Métricas de Performance

### Objetivos
| Métrica | Objetivo |
|---------|----------|
| First Contentful Paint | < 1.5s |
| Largest Contentful Paint | < 2.5s |
| Cumulative Layout Shift | < 0.1 |
| Bundle Size | < 500KB |

### Monitoreo
```bash
# Lighthouse audit
npx lighthouse http://localhost:3000 --view

# Bundle analyzer
npm run build && npx vite-bundle-analyzer dist
```

---

**Estado**: ✅ Frontend MVP funcional  
**Testing**: Configurado con Vitest  
**Siguiente**: Integración completa con backend