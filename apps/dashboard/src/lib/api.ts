import { supabase } from './supabase'

const apiUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

export type Website = {
  id: string
  name: string
  normalized_origin: string
  verification_status: 'UNVERIFIED' | 'PENDING' | 'VERIFIED' | 'FAILED'
  last_score: number | null
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const { data } = await supabase.auth.getSession()
  if (!data.session?.access_token) {
    throw new Error('Your session has expired. Please sign in again.')
  }
  const response = await fetch(`${apiUrl}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${data.session.access_token}`,
      'Content-Type': 'application/json',
      ...init?.headers,
    },
  })
  if (!response.ok) {
    const body = await response.json().catch(() => null)
    throw new Error(body?.detail || 'The request could not be completed.')
  }
  return response.json() as Promise<T>
}

export function listWebsites(): Promise<Website[]> {
  return request<Website[]>('/api/websites')
}

export function createWebsite(input: { name: string; url: string }): Promise<Website & { verification_token: string }> {
  return request<Website & { verification_token: string }>('/api/websites', {
    method: 'POST',
    body: JSON.stringify(input),
  })
}

export function verifyWebsite(websiteId: string): Promise<Website> {
  return request<Website>(`/api/websites/${websiteId}/verify`, { method: 'POST' })
}
