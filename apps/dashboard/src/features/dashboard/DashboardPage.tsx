import { useEffect, useState } from 'react'
import { Shield, PlusCircle, ArrowRight, Cpu, Globe } from 'lucide-react'

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

  const verifiedCount = websites.filter((w) => w.verification_status === 'VERIFIED').length
  const scoredSites = websites.filter((w) => w.last_score !== null)
  const avgScore = scoredSites.length
    ? Math.round(scoredSites.reduce((acc, curr) => acc + (curr.last_score || 0), 0) / scoredSites.length)
    : null

  const getScoreColor = (score: number | null) => {
    if (score === null) return 'text-slate-500'
    if (score >= 90) return 'text-emerald-400'
    if (score >= 80) return 'text-cyan-400'
    if (score >= 70) return 'text-yellow-400'
    return 'text-rose-400'
  }

  return (
    <main className="app-container min-h-screen">
      {/* Console Header */}
      <header className="console-header border-b border-[#1c2b42] pb-6 mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <p className="eyebrow">AUTHORIZED WEB SECURITY SCANNER</p>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white mt-1">
            ThreatSentry
          </h1>
          <p className="subtitle text-sm text-slate-400 mt-1">
            Verified target inventory and continuous posture assessment.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <a
            href="/model"
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-[#111e33] hover:bg-[#1c2b42] text-cyan-400 text-xs font-semibold border border-[#2a3f5f] transition-all no-underline"
          >
            <Cpu className="w-3.5 h-3.5" />
            <span>ML Intelligence</span>
          </a>
          <button
            type="button"
            onClick={() => void signOut()}
            className="px-3.5 py-2 rounded-lg bg-[#111e33] hover:bg-rose-950/40 text-slate-300 hover:text-rose-400 text-xs font-semibold border border-[#2a3f5f] hover:border-rose-900/50 transition-all cursor-pointer"
          >
            Sign out
          </button>
        </div>
      </header>

      {/* Quick Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="glass-card p-4 sm:p-5">
          <span className="text-xs font-semibold uppercase text-slate-400">Total Assets</span>
          <div className="text-2xl sm:text-3xl font-bold text-white mt-1">{websites.length}</div>
          <span className="text-xs text-slate-500">Monitored domains</span>
        </div>

        <div className="glass-card p-4 sm:p-5">
          <span className="text-xs font-semibold uppercase text-slate-400">Verified Ownership</span>
          <div className="text-2xl sm:text-3xl font-bold text-emerald-400 mt-1">{verifiedCount}</div>
          <span className="text-xs text-slate-500">Eligible for Deep Scan</span>
        </div>

        <div className="glass-card p-4 sm:p-5">
          <span className="text-xs font-semibold uppercase text-slate-400">Average Posture Score</span>
          <div className={`text-2xl sm:text-3xl font-bold mt-1 ${getScoreColor(avgScore)}`}>
            {avgScore !== null ? `${avgScore}` : '—'}
            {avgScore !== null && <span className="text-xs text-slate-500 font-normal"> / 100</span>}
          </div>
          <span className="text-xs text-slate-500">Across scanned targets</span>
        </div>

        <div className="glass-card p-4 sm:p-5">
          <span className="text-xs font-semibold uppercase text-slate-400">ML Engine</span>
          <div className="text-2xl sm:text-3xl font-bold text-cyan-400 mt-1">Active</div>
          <span className="text-xs text-slate-500">Hybrid detection ready</span>
        </div>
      </div>

      {/* Websites Grid */}
      <section aria-labelledby="websites-title">
        <div className="section-header flex items-center justify-between mb-4">
          <div>
            <h2 id="websites-title" className="text-xl font-bold text-white">
              Websites
            </h2>
            <p className="subtitle text-xs text-slate-400">
              Verified assets and security posture.
            </p>
          </div>
          <a
            href="/websites/new"
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow-lg shadow-cyan-500/20 transition-all no-underline"
          >
            <PlusCircle className="w-4 h-4" />
            <span>Add website</span>
          </a>
        </div>

        {message ? (
          <div className="glass-card p-8 text-center text-slate-400 text-sm" role="status">
            <p>{message}</p>
          </div>
        ) : null}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 website-grid">
          {websites.map((website) => {
            const isVerified = website.verification_status === 'VERIFIED'
            return (
              <a
                href={`/websites/${website.id}`}
                className="glass-card p-6 flex flex-col justify-between group hover:border-cyan-500/50 transition-all no-underline text-inherit website-card block"
                key={website.id}
                style={{ textDecoration: 'none', color: 'inherit', display: 'block' }}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <p
                      className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider eyebrow ${
                        isVerified
                          ? 'bg-emerald-950/60 text-emerald-400 border border-emerald-800/60'
                          : 'bg-amber-950/60 text-amber-400 border border-amber-800/60'
                      }`}
                    >
                      {website.verification_status}
                    </p>
                    {website.last_score !== null && (
                      <span className={`text-xs font-bold font-mono ${getScoreColor(website.last_score)}`}>
                        Grade {website.last_score >= 90 ? 'A' : website.last_score >= 80 ? 'B' : website.last_score >= 70 ? 'C' : 'D'}
                      </span>
                    )}
                  </div>

                  <h3 className="text-lg font-bold text-white group-hover:text-cyan-300 transition-colors">
                    {website.name}
                  </h3>
                  <p className="text-xs font-mono text-slate-400 truncate mt-1">
                    {website.normalized_origin}
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-[#1c2b42] flex items-center justify-between">
                  <div>
                    <span className="text-[10px] uppercase font-semibold text-slate-500 block">
                      Security Posture
                    </span>
                    <strong className={`text-sm font-bold ${getScoreColor(website.last_score)}`}>
                      {website.last_score === null ? 'Not scanned' : `${website.last_score} / 100`}
                    </strong>
                  </div>

                  <div className="flex items-center gap-1 text-xs font-medium text-cyan-400 group-hover:translate-x-0.5 transition-transform">
                    <span>Posture details</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </a>
            )
          })}
        </div>
      </section>
    </main>
  )
}
