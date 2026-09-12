import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import App from './App'
import { AuthProvider } from './features/auth/authState'
import './styles.css'

const rootElement = document.getElementById('root')

if (!rootElement) {
  throw new Error('ThreatSentry root element is missing')
}

createRoot(rootElement).render(
  <StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </StrictMode>,
)
