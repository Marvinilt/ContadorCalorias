import { render, screen, fireEvent } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from 'react-query'
import { BrowserRouter } from 'react-router-dom'
import { vi } from 'vitest'
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
    mutateAsync: mockMutateAsync
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
  test('renders camera interface', () => {
    renderWithProviders(<Camera />)
    expect(screen.getByText('Analizar Alimentos')).toBeInTheDocument()
  })

  test('handles file selection', () => {
    renderWithProviders(<Camera />)
    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' })
    const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement
    fireEvent.change(fileInput, { target: { files: [file] } })
    expect(screen.getByText('Analizar Imagen')).toBeInTheDocument()
  })
})