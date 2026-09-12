# ThreatSentry — Agent Handoff

Last updated: 2026-09-12

## Goal

Implement `ThreatSentry_COMPLETE_MASTER_PLAN_REACT_TYPESCRIPT.md` as a React/TypeScript dashboard with a FastAPI scanner backend and Supabase auth/data store. The user expects implementation to continue autonomously; do not stop to restate the plan unless a material product decision or external credential/action is required.

## Run locally

From the repository root:

```powershell
npm run dev
```

This starts:

- Dashboard: `http://localhost:3000`
- API: `http://localhost:8000`
- API health: `http://localhost:8000/health`

The root `package.json` uses `concurrently` and the root virtual environment at `.venv`.

## Environment and Supabase

- `backend/.env` exists locally and is gitignored. Required secrets were populated by the user.
- `apps/dashboard/.env` exists locally and is gitignored. It includes the Supabase URL/anon key and `VITE_API_URL`.
- Do not print, commit, or overwrite secret values.
- Supabase project was linked previously. Migration `supabase/migrations/0001_initial_schema.sql` was reconciled/applied using Supabase migration repair; local and remote migration history matched at that time.

## Completed implementation

### Foundation

- React/Vite dashboard and FastAPI API scaffold.
- Root `npm run dev` starts frontend and backend together.
- Development CORS permits localhost plus private LAN Vite origins on port 3000; production stays restricted to configured origins.
- Supabase schema/migration with RLS for profiles, websites, scan jobs, findings, input authorizations, and model versions.

### Authentication

- Supabase email/password sign-in: `/login`.
- Supabase registration: `/register`.
- Session restoration via `AuthProvider`.
- Protected routes redirect anonymous users to `/login` without rendering private content first.
- Successful sign-in redirects to `/dashboard`.
- Backend validates Bearer tokens with Supabase before user-owned API access.

### Website management and ownership verification

- Backend website API: list, create, get, update name, delete, all owner-scoped server-side.
- Website creation normalizes HTTP(S) URLs and issues an ownership token.
- Dashboard lists websites using the authenticated access token.
- `/websites/new` adds a website, shows `/.well-known/threatsentry.txt` contents, and has a Verify ownership button.
- Backend verification fetch has DNS public-address validation, strict timeout, 64 KiB response cap, and refuses redirects rather than following unvalidated destinations.
- `POST /api/websites/{website_id}/verify` persists `VERIFIED` or `FAILED`.

### Security primitives already present

- Target normalization and literal private-address rejection.
- DNS resolution protection that rejects non-public resolved addresses.
- Header finding checks, stable fingerprints, score/grade calculation, and in-memory scan job state transitions.
- `backend/api/scan_policy.py` and its test are currently uncommitted but implemented: it blocks scan start unless verification status is `VERIFIED`.

## Verification last run

- Backend: `38 passed` (`.venv\Scripts\python.exe -m pytest backend/tests -q`), with two upstream TestClient deprecation warnings.
- Frontend: latest full run before the last backend-only CORS adjustment was `9 passed`.
- Frontend production build passed after the login redirect fix.

Run before claiming completion:

```powershell
.\.venv\Scripts\python.exe -m pytest backend\tests -q
npm --prefix apps/dashboard run test:run
npm --prefix apps/dashboard run build
```

## Current uncommitted work

- `backend/api/scan_policy.py`
- `backend/tests/test_scan_policy.py`

These tests pass and should be committed before building the scan router.

## Immediate next task — scan job system

Implement in this order:

1. Commit `scan_policy.py` and its test.
2. Add a scan router:
   - `POST /api/websites/{website_id}/scans`
   - `GET /api/scans/{scan_id}`
   - `POST /api/scans/{scan_id}/cancel`
   - `GET /api/websites/{website_id}/scans`
3. Enforce authentication, server-side ownership, `VERIFIED` status, one active scan per website, and SSRF revalidation at scan start.
4. Create and persist `scan_jobs` rows with safe public error messages.
5. Implement a small in-process/background runner with cancellation checks and persisted progress/stage updates. Keep the scanner boundary separable for a later worker migration.
6. Connect dashboard polling and a Website detail/scan-progress page.

Use test-first development for each production behavior. Do not create an active SQLi/XSS probe before ownership verification, SSRF validation, scope control, and user authorization are enforced.

## Remaining plan areas after scan jobs

1. Bounded same-origin crawler and passive checks: TLS, headers, cookies, DNS, technology, and exposure.
2. Findings persistence, deduplication, score/result pages, history/compare.
3. Controlled active SQLi/XSS checks only for verified assets; POST requires persistent explicit allowlist.
4. Auth polish: logout UI, forgot password, redirect authenticated users from auth pages.
5. ML dataset/training/evaluation/artifact checksum/inference.
6. Controlled labs, scanner benchmark, Docker/CI/deployment documentation and hardening.

## Safety requirements — do not weaken

- Never trust a client-supplied `user_id`; derive it from the validated Supabase token.
- Never scan targets that are not ownership-verified.
- Block localhost, private/reserved/link-local/metadata destinations and revalidate every redirect before requesting it.
- Do not log passwords, tokens, cookies, secrets, or raw sensitive form data.
- Keep production CORS explicit; the private-LAN regex is development-only.
- Do not commit `.env` files or ML raw datasets.

## Useful files

- Master specification: `ThreatSentry_COMPLETE_MASTER_PLAN_REACT_TYPESCRIPT.md`
- Backend app: `backend/main.py`
- Auth dependency: `backend/api/deps/auth.py`
- Website API: `backend/api/routers/websites.py`
- Verification fetch: `backend/scanner/verification_fetch.py`
- Frontend routes: `apps/dashboard/src/App.tsx`
- Auth session: `apps/dashboard/src/features/auth/authState.tsx`
- Dashboard: `apps/dashboard/src/features/dashboard/DashboardPage.tsx`
- Website onboarding: `apps/dashboard/src/features/websites/AddWebsitePage.tsx`
