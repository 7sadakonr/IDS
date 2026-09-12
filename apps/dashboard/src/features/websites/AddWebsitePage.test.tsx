import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'

import { AddWebsitePage } from './AddWebsitePage'

const { createWebsite } = vi.hoisted(() => ({ createWebsite: vi.fn() }))

vi.mock('../../lib/api', () => ({ createWebsite }))

it('creates a website from its display name and URL', async () => {
  createWebsite.mockResolvedValue({ id: 'site-1', verification_token: 'token-value' })
  const user = userEvent.setup()
  render(<AddWebsitePage />)

  await user.type(screen.getByLabelText('Website name'), 'Example Store')
  await user.type(screen.getByLabelText('Website URL'), 'https://example.com')
  await user.click(screen.getByRole('button', { name: 'Add website' }))

  expect(createWebsite).toHaveBeenCalledWith({ name: 'Example Store', url: 'https://example.com' })
  expect(await screen.findByText('threatsentry-verification=token-value')).toBeInTheDocument()
})
