import { render, screen } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from 'react-query'
import { MemoryRouter } from 'react-router-dom'
import { vi, describe, test, expect } from 'vitest'
import App from '../App'

// Mock useAuth hook
vi.mock('../hooks/useAuth', () => ({
  useAuth: () => ({
    user: { id: 1, email: 'test@example.com' },
    login: vi.fn(),
    logout: vi.fn(),
    isLoading: false
  }),
  AuthProvider: ({ children }: { children: React.ReactNode }) => <div>{children}</div>
}))

// Mock components
vi.mock('../components/Layout', () => ({
  default: () => <div>Layout Component</div>
}))

vi.mock('../components/Home', () => ({
  default: () => <div>Home Component</div>
}))

vi.mock('../components/Login', () => ({
  default: () => <div>Login Component</div>
}))

const renderWithProviders = (component: React.ReactElement, initialEntries = ['/']) => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  })
  
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={initialEntries}>
        {component}
      </MemoryRouter>
    </QueryClientProvider>
  )
}

describe('App Component', () => {
  test('renders without crashing', () => {
    renderWithProviders(<App />)
    expect(screen.getByText('Layout Component')).toBeInTheDocument()
  })

  test('renders login page on /login route', () => {
    renderWithProviders(<App />, ['/login'])
    expect(screen.getByText('Login Component')).toBeInTheDocument()
  })
})