import { FormEvent, useState } from 'react'

import { createWebsite } from '../../lib/api'

export function AddWebsitePage() {
  const [token, setToken] = useState<string | null>(null)
  const [message, setMessage] = useState<string | null>(null)

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = new FormData(event.currentTarget)
    try {
      const website = await createWebsite({
        name: String(form.get('name') ?? ''),
        url: String(form.get('url') ?? ''),
      })
      setToken(website.verification_token)
      setMessage(null)
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Unable to add website.')
    }
  }

  return (
    <main className="app-shell">
      <p className="eyebrow">ASSET ONBOARDING</p>
      <h1>Add website</h1>
      <p className="subtitle">Only add websites you own or are explicitly authorized to assess.</p>
      <form className="auth-panel" onSubmit={submit}>
        <label htmlFor="name">Website name</label>
        <input id="name" name="name" required maxLength={120} />
        <label htmlFor="url">Website URL</label>
        <input id="url" name="url" type="url" placeholder="https://example.com" required />
        <button type="submit">Add website</button>
      </form>
      {token ? <section className="auth-panel"><h2>Verify ownership</h2><p>Create this file on your website:</p><code>/.well-known/threatsentry.txt</code><p>With exactly this content:</p><code>{`threatsentry-verification=${token}`}</code></section> : null}
      {message ? <p role="alert">{message}</p> : null}
    </main>
  )
}
