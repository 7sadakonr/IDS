import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'

import { LoginPage } from './LoginPage'

const { signInWithPassword } = vi.hoisted(() => ({ signInWithPassword: vi.fn() }))

vi.mock('../../lib/supabase', () => ({
  supabase: {
    auth: { signInWithPassword },
  },
}))

it('renders email-password login controls', () => {
  render(<LoginPage />)

  expect(screen.getByRole('heading', { name: 'Sign in to ThreatSentry' })).toBeInTheDocument()
  expect(screen.getByLabelText('Email')).toBeInTheDocument()
  expect(screen.getByLabelText('Password')).toBeInTheDocument()
})

it('signs in with the submitted credentials', async () => {
  signInWithPassword.mockResolvedValue({ data: { session: null }, error: null })
  const user = userEvent.setup()
  render(<LoginPage />)

  await user.type(screen.getByLabelText('Email'), 'analyst@example.com')
  await user.type(screen.getByLabelText('Password'), 'secure-password')
  await user.click(screen.getByRole('button', { name: 'Sign in' }))

  expect(signInWithPassword).toHaveBeenCalledWith({
    email: 'analyst@example.com',
    password: 'secure-password',
  })
})
