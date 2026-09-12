import { BrowserRouter, Navigate, Route, Routes } from 'react-router'

import { LoginPage } from './features/auth/LoginPage'

function DashboardPlaceholder() {
  return (
    <main className="app-shell">
      <p className="eyebrow">AUTHORIZED WEB SECURITY SCANNER</p>
      <h1>ThreatSentry</h1>
      <p className="subtitle">Security operations console</p>
    </main>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/dashboard" element={<DashboardPlaceholder />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
