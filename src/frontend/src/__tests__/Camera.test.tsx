import { render, screen, fireEvent } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from 'react-query'
import { BrowserRouter } from 'react-router-dom'
import { vi, describe, test, expect, beforeEach } from 'vitest'
import Camera from '../components/Camera'

const mockNavigate = vi.fn()
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => mockNavigate
  }
})

const mockMutateAsync = vi.fn()
vi.mock('../hooks/useAnalysis', () => ({
  useAnalyzeImage: () => ({
    mutateAsync: mockMutateAsync,
    isLoading: false
  })
}))

vi.mock('../hooks/useAuth', () => ({
  useAuth: () => ({
    user: { id: 1, email: 'test@example.com' },
    login: vi.fn(),
    logout: vi.fn(),
    isLoading: false
  })
}))

const renderWithProviders = (component: React.ReactElement) => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  })
  
  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {component}
      </BrowserRouter>
    </QueryClientProvider>
  )
}

describe('Camera Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  test('renders camera interface', () => {
    renderWithProviders(<Camera />)
    expect(screen.getByText('Analizar Alimentos')).toBeInTheDocument()
    expect(screen.getByText('Subir Imagen')).toBeInTheDocument()
  })

  test('handles file selection', () => {
    renderWithProviders(<Camera />)
    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' })
    const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement
    
    Object.defineProperty(fileInput, 'files', {
      value: [file],
      writable: false,
    })
    
    fireEvent.change(fileInput)
    expect(screen.getByText('Analizar Imagen')).toBeInTheDocument()
  })
})