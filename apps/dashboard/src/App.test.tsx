import { render, screen } from '@testing-library/react'

import App from './App'

describe('App', () => {
  it('renders the ThreatSentry application shell', () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: 'ThreatSentry' })).toBeInTheDocument()
    expect(screen.getByText('Security operations console')).toBeInTheDocument()
  })
})
