import { render, screen } from '@testing-library/react'

import { LoginPage } from './LoginPage'

it('renders email-password login controls', () => {
  render(<LoginPage />)

  expect(screen.getByRole('heading', { name: 'Sign in to ThreatSentry' })).toBeInTheDocument()
  expect(screen.getByLabelText('Email')).toBeInTheDocument()
  expect(screen.getByLabelText('Password')).toBeInTheDocument()
})
