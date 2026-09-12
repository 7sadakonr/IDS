import { FormEvent, useState } from 'react'

import { createWebsite, verifyWebsite } from '../../lib/api'

export function AddWebsitePage() {
  const [token, setToken] = useState<string | null>(null)
  const [websiteId, setWebsiteId] = useState<string | null>(null)
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
      setWebsiteId(website.id)
      setMessage(null)
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Unable to add website.')
    }
  }

  async function verify() {
    if (!websiteId) return
    try {
      const website = await verifyWebsite(websiteId)
      setMessage(website.verification_status === 'VERIFIED'
        ? 'Ownership verified. You can now start a scan.'
        : 'Verification failed. Check the file path and content, then try again.')
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Unable to verify ownership.')
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
      {token ? <section className="auth-panel"><h2>Verify ownership</h2><p>Create this file on your website:</p><code>/.well-known/threatsentry.txt</code><p>With exactly this content:</p><code>{`threatsentry-verification=${token}`}</code><button type="button" onClick={() => void verify()}>Verify ownership</button></section> : null}
      {message ? <p role="alert">{message}</p> : null}
    </main>
  )
}
