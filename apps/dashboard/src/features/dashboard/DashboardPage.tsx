import { useEffect, useState } from 'react'

import { listWebsites, Website } from '../../lib/api'
import { useAuth } from '../auth/authState'

export function DashboardPage() {
  const { signOut } = useAuth()
  const [websites, setWebsites] = useState<Website[]>([])
  const [message, setMessage] = useState('Loading websites...')

  useEffect(() => {
    void listWebsites()
      .then((items) => {
        setWebsites(items)
        setMessage(items.length ? '' : 'No websites yet. Add a website to begin verification.')
      })
      .catch((error: unknown) => setMessage(error instanceof Error ? error.message : 'Unable to load websites.'))
  }, [])

  return (
    <main className="app-shell">
      <header className="console-header">
        <div><p className="eyebrow">AUTHORIZED WEB SECURITY SCANNER</p><h1>ThreatSentry</h1></div>
        <button type="button" onClick={() => void signOut()}>Sign out</button>
      </header>
      <section aria-labelledby="websites-title">
        <div className="section-header"><div><h2 id="websites-title">Websites</h2><p className="subtitle">Verified assets and security posture.</p></div><a href="/websites/new">Add website</a></div>
        {message ? <p role="status">{message}</p> : null}
        <div className="website-grid">
          {websites.map((website) => (
            <article className="website-card" key={website.id}>
              <p className="eyebrow">{website.verification_status}</p>
              <h3>{website.name}</h3>
              <p>{website.normalized_origin}</p>
              <strong>{website.last_score === null ? 'Not scanned' : `${website.last_score} / 100`}</strong>
            </article>
          ))}
        </div>
      </section>
    </main>
  )
}
