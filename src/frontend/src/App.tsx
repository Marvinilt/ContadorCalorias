import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './hooks/useAuth'
import Layout from './components/Layout'
import Home from './components/Home'
import Camera from './components/Camera'
import Results from './components/Results'
import Analytics from './components/Analytics'
import Login from './components/Login'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="camera" element={<Camera />} />
          <Route path="results/:analysisId" element={<Results />} />
          <Route path="analytics" element={<Analytics />} />
        </Route>
      </Routes>
    </AuthProvider>
  )
}

export default App