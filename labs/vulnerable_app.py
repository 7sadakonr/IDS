import html
import os
from pathlib import Path
import sqlite3
from typing import Any
from fastapi import FastAPI, Form, Query, Request, Response
from fastapi.responses import HTMLResponse, PlainTextResponse

app = FastAPI(title="ThreatSentry Controlled Lab", version="1.2.0")

# Security Mode: Default to True (Secure / Hardened)
SECURE_MODE: bool = True

# In-memory SQLite database
def get_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE products (id TEXT, name TEXT, price REAL, description TEXT)")
    cursor.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)",
        [
            ("1", "Secure Laptop Stand", 39.99, "Ergonomic aluminum stand for high productivity"),
            ("2", "Mechanical Keyboard", 129.50, "Tactile wireless keyboard with RGB lighting"),
            ("3", "Privacy Screen Protector", 24.00, "Anti-glare security filter for laptop displays"),
        ],
    )
    conn.commit()
    return conn

DB_CONN = get_db()

import re

# State for verification token
TOKEN_FILE = Path("labs/threatsentry.txt")
_in_memory_token = "ts_lab_token_demo"

if TOKEN_FILE.exists():
    try:
        _in_memory_token = TOKEN_FILE.read_text("utf-8").strip().replace("threatsentry-verification=", "")
    except Exception:
        pass


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """Dynamically applies full OWASP security headers or vulnerable oversights."""
    response: Response = await call_next(request)

    if SECURE_MODE:
        # --- ALL 8 OWASP DEFENSIVE SECURITY HEADERS ---
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        # Hardened cookie with HttpOnly, Secure, and SameSite protection
        response.headers.append("Set-Cookie", "lab_session=guest_abc12345; Path=/; HttpOnly; SameSite=Lax; Secure")

        # Suppress all technology and version banners
        if "server" in response.headers:
            del response.headers["server"]
        if "Server" in response.headers:
            del response.headers["Server"]
        if "X-Powered-By" in response.headers:
            del response.headers["X-Powered-By"]
        if "x-powered-by" in response.headers:
            del response.headers["x-powered-by"]
    else:
        # --- VULNERABLE PROFILE ---
        response.headers["Server"] = "VulnerableLab/1.0 (Ubuntu 22.04)"
        response.headers["X-Powered-By"] = "PHP/8.1.0-Simulated"
        response.headers.append("Set-Cookie", "lab_session=guest_abc12345; Path=/")

    return response


@app.get("/.well-known/threatsentry.txt", response_class=PlainTextResponse)
def get_verification_challenge(request: Request, token: str | None = None):
    """Serves the ownership challenge token for ThreatSentry verification."""
    global _in_memory_token
    if TOKEN_FILE.exists():
        try:
            _in_memory_token = TOKEN_FILE.read_text("utf-8").strip().replace("threatsentry-verification=", "")
        except Exception:
            pass
    effective_token = (
        request.headers.get("X-ThreatSentry-Token")
        or request.query_params.get("token")
        or token
        or _in_memory_token
    )
    return "threatsentry-verification=" + effective_token + "\n"


@app.get("/set-token", response_class=HTMLResponse)
@app.post("/set-token", response_class=HTMLResponse)
def set_verification_token(token: str = Query(default="", alias="token")):
    global _in_memory_token
    clean_token = token.strip().replace("threatsentry-verification=", "")
    if clean_token and re.match(r"^[A-Za-z0-9_\-]+$", clean_token):
        _in_memory_token = clean_token
        try:
            TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
            TOKEN_FILE.write_text("threatsentry-verification=" + clean_token + "\n", encoding="utf-8")
        except Exception:
            pass

    safe_token = html.escape(_in_memory_token)
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Token Updated - ThreatSentry Lab</title>
        <style>body {{ font-family: sans-serif; background: #0b1329; color: #e2e8f0; padding: 2rem; }}</style>
    </head>
    <body>
        <h2>Verification Token Updated!</h2>
        <p>Active Token: <code>threatsentry-verification={safe_token}</code></p>
        <p><a href="/" style="color: #38bdf8;">&larr; Back to Lab Home</a></p>
    </body>
    </html>
    """)


@app.post("/toggle-security", response_class=HTMLResponse)
async def toggle_security_post(request: Request):
    """POST-only toggle to prevent web crawlers from accidentally toggling security mode."""
    global SECURE_MODE
    body = (await request.body()).decode("utf-8", errors="ignore")
    if "mode=secure" in body:
        SECURE_MODE = True
    elif "mode=vulnerable" in body:
        SECURE_MODE = False
    else:
        SECURE_MODE = not SECURE_MODE

    status_str = "🛡️ SECURE / HARDENED (Safe)" if SECURE_MODE else "⚠️ VULNERABLE (Testing Mode)"
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="1;url=/" />
        <title>Security Mode Switched</title>
        <style>body {{ font-family: sans-serif; background: #0b1329; color: #e2e8f0; padding: 2rem; }}</style>
    </head>
    <body>
        <h2>Security Mode Switched to: {status_str}</h2>
        <p>Redirecting back to lab home in 1 second... <a href="/" style="color:#38bdf8;">Click here</a></p>
    </body>
    </html>
    """)



@app.get("/toggle-security", response_class=HTMLResponse)
def toggle_security_get(mode: str = Query(default="")):
    """For automated tests only; web crawler will not find a link to this."""
    global SECURE_MODE
    if mode.lower() in ("secure", "safe", "true", "1"):
        SECURE_MODE = True
    elif mode.lower() in ("vulnerable", "vuln", "false", "0"):
        SECURE_MODE = False
    else:
        SECURE_MODE = not SECURE_MODE

    return HTMLResponse(f"<!DOCTYPE html><html><body>Mode: {SECURE_MODE}</body></html>")


@app.get("/", response_class=HTMLResponse)
def home():
    # POST form button ensures crawler will never trigger or follow it
    status_card = f"""
    <div class="card" style="border: 2px solid {'#10b981' if SECURE_MODE else '#e11d48'}; background: {'#064e3b33' if SECURE_MODE else '#88133733'};">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <h2 style="color: {'#34d399' if SECURE_MODE else '#f87171'}; margin: 0 0 0.5rem 0;">
                    {'🛡️ Security Status: HARDENED & SECURE' if SECURE_MODE else '⚠️ Security Status: VULNERABLE'}
                </h2>
                <p style="margin: 0; color: {'#a7f3d0' if SECURE_MODE else '#fecdd3'}; font-size: 0.9rem;">
                    {'[PROTECTED] Parameterized SQL queries, HTML entity escaping (XSS immune), full OWASP security headers (CSP, HSTS, X-Frame-Options, nosniff, permissions, COOP, CORP), and hardened cookies.' if SECURE_MODE else '[VULNERABLE] Raw SQL concatenation, unescaped HTML reflection, banner disclosure, and missing security headers.'}
                </p>
            </div>
            <div>
                <form method="POST" action="/toggle-security">
                    <input type="hidden" name="mode" value="{'vulnerable' if SECURE_MODE else 'secure'}" />
                    <button type="submit" style="background: {'#e11d48' if SECURE_MODE else '#059669'}; color: white; padding: 0.6rem 1.2rem; border-radius: 6px; font-weight: bold; cursor: pointer; border: none;">
                        {'Switch to Vulnerable Mode' if SECURE_MODE else 'Switch to Secure Mode'}
                    </button>
                </form>
            </div>
        </div>
    </div>
    """

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>ThreatSentry Test Target Lab</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #070d18; color: #e2e8f0; margin: 0; padding: 2rem; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .card {{ background: #0e1726; border: 1px solid #1e293b; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; }}
            h1, h2, h3 {{ color: #ffffff; }}
            input[type="text"] {{ background: #1e293b; border: 1px solid #334155; color: white; padding: 0.5rem 0.75rem; border-radius: 4px; width: 60%; }}
            button {{ background: #0284c7; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-weight: bold; }}
            button:hover {{ opacity: 0.9; }}
            a {{ color: #38bdf8; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
            code {{ background: #1e293b; padding: 0.2rem 0.4rem; border-radius: 4px; font-family: monospace; color: #7dd3fc; }}
            .badge {{ display: inline-block; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: bold; }}
            .vuln {{ background: #881337; color: #fda4af; }}
            .safe {{ background: #064e3b; color: #6ee7b7; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ThreatSentry Test Lab Target</h1>
            <p>A controlled testing environment running locally on <code>http://localhost:8080</code> for verifying crawlers, active scanners (SQLi, XSS), passive header detection, and hybrid ML analysis.</p>

            <!-- Mode Switcher Card -->
            {status_card}

            <!-- Verification Card -->
            <div class="card">
                <h2>1. Website Verification Token</h2>
                <p>Current active challenge token: <code>threatsentry-verification={html.escape(_in_memory_token)}</code></p>
                <form action="/set-token" method="GET" style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
                    <input type="text" name="token" placeholder="Paste token from ThreatSentry (e.g. ts_verify_...)" value="{html.escape(_in_memory_token)}" required />
                    <button type="submit">Update Token</button>
                </form>
            </div>

            <!-- Search Service -->
            <div class="card">
                <h2>2. Search Service <span class="badge {'safe' if SECURE_MODE else 'vuln'}">{'Protected (Escaped)' if SECURE_MODE else 'Vulnerable: Reflected XSS'}</span></h2>
                <p>{'Input in parameter <code>q</code> is securely encoded using HTML entity escaping.' if SECURE_MODE else 'Input in parameter <code>q</code> is rendered directly into HTML without context-aware entity encoding.'}</p>
                <form action="/search" method="GET" style="display: flex; gap: 0.5rem;">
                    <input type="text" name="q" value="laptop stand" />
                    <button type="submit">Search Products</button>
                </form>
            </div>

            <!-- Product Catalog -->
            <div class="card">
                <h2>3. Product Catalog <span class="badge {'safe' if SECURE_MODE else 'vuln'}">{'Protected (Parameterized SQL)' if SECURE_MODE else 'Vulnerable: SQL Injection'}</span></h2>
                <p>{'Parameter <code>id</code> is bound securely via prepared statement parameter binding.' if SECURE_MODE else 'Parameter <code>id</code> is interpolated directly into an in-memory SQLite query.'}</p>
                <ul>
                    <li><a href="/products?id=1">Product 1 (Secure Laptop Stand)</a></li>
                    <li><a href="/products?id=2">Product 2 (Mechanical Keyboard)</a></li>
                    <li><a href="/products?id=3">Product 3 (Privacy Screen Protector)</a></li>
                    <li><a href="/products?id=1%27">Probe: Product ID <code>1'</code></a></li>
                </ul>
            </div>

            <!-- Benign Navigation Links -->
            <div class="card">
                <h2>4. Benign Site Navigation <span class="badge safe">Safe Traffic</span></h2>
                <p>Static pages used by the ThreatSentry crawler to discover site map and verify passive headers.</p>
                <p><a href="/about">About Us</a> &bull; <a href="/contact">Contact Page</a> &bull; <a href="/.well-known/threatsentry.txt">View Verification File</a></p>
            </div>
        </div>
    </body>
    </html>
    """)


@app.get("/search", response_class=HTMLResponse)
def search(q: str = "laptop"):
    """Search endpoint: Immune to XSS in SECURE_MODE, vulnerable otherwise."""
    rendered_query = html.escape(q) if SECURE_MODE else q

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search Results - ThreatSentry Lab</title>
        <style>body {{ font-family: sans-serif; background: #070d18; color: #e2e8f0; padding: 2rem; }} a {{ color: #38bdf8; }}</style>
    </head>
    <body>
        <h1>Search Results {'(Protected)' if SECURE_MODE else ''}</h1>
        <p>You searched for: <strong>{rendered_query}</strong></p>

        <div style="margin-top: 1.5rem;">
            <p>Found 3 matching items.</p>
            <ul>
                <li>Laptop Stand (Aluminum)</li>
                <li>Adjustable Desk Riser</li>
                <li>Compact Laptop Sleeve</li>
            </ul>
        </div>
        <p><a href="/">&larr; Back to Home</a></p>
    </body>
    </html>
    """)


@app.get("/products", response_class=HTMLResponse)
def get_product(id: str = "1"):
    """Product details: Protected with parameterized queries in SECURE_MODE, vulnerable otherwise."""
    cursor = DB_CONN.cursor()

    if SECURE_MODE:
        # Parameterized query immune to SQL injection
        cursor.execute("SELECT id, name, price, description FROM products WHERE id = ?", (id,))
        row = cursor.fetchone()
        if not row:
            return HTMLResponse("""
            <!DOCTYPE html>
            <html><body style="background:#070d18; color:white; font-family:sans-serif; padding:2rem;">
            <h2>Product Not Found</h2>
            <p><a href="/" style="color:#38bdf8;">&larr; Back to Catalog</a></p>
            </body></html>
            """, status_code=404)

        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{html.escape(row['name'])} - ThreatSentry Lab</title>
            <style>body {{ font-family: sans-serif; background: #070d18; color: #e2e8f0; padding: 2rem; }} a {{ color: #38bdf8; }}</style>
        </head>
        <body>
            <h1>{html.escape(row['name'])}</h1>
            <p><strong>Price:</strong> ${row['price']:.2f}</p>
            <p><strong>Description:</strong> {html.escape(row['description'])}</p>
            <p><a href="/">&larr; Back to Catalog</a></p>
        </body>
        </html>
        """)
    else:
        # Vulnerable SQL concatenation
        query = f"SELECT id, name, price, description FROM products WHERE id = '{id}'"
        try:
            cursor.execute(query)
            row = cursor.fetchone()
            if not row:
                return HTMLResponse("""
                <!DOCTYPE html>
                <html><body style="background:#070d18; color:white; font-family:sans-serif; padding:2rem;">
                <h2>Product Not Found</h2>
                <p><a href="/" style="color:#38bdf8;">&larr; Back to Catalog</a></p>
                </body></html>
                """, status_code=404)

            return HTMLResponse(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{html.escape(row['name'])} - ThreatSentry Lab</title>
                <style>body {{ font-family: sans-serif; background: #070d18; color: #e2e8f0; padding: 2rem; }} a {{ color: #38bdf8; }}</style>
            </head>
            <body>
                <h1>{html.escape(row['name'])}</h1>
                <p><strong>Price:</strong> ${row['price']:.2f}</p>
                <p><strong>Description:</strong> {html.escape(row['description'])}</p>
                <p><a href="/">&larr; Back to Catalog</a></p>
            </body>
            </html>
            """)
        except sqlite3.OperationalError as exc:
            return HTMLResponse(f"""
            <!DOCTYPE html>
            <html>
            <head><title>500 Internal Server Error</title></head>
            <body style="background:#1a050b; color:#fda4af; font-family:monospace; padding:2rem;">
                <h2>Database Query Execution Error</h2>
                <p><strong>sqlite3.OperationalError:</strong> {html.escape(str(exc))}</p>
                <pre>Query: {html.escape(query)}</pre>
            </body>
            </html>
            """, status_code=500)


@app.get("/about", response_class=HTMLResponse)
def about():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html><body style="background:#070d18; color:#e2e8f0; font-family:sans-serif; padding:2rem;">
        <h1>About ThreatSentry Test Lab</h1>
        <p>This application is designed for vulnerability testing, hybrid ML evaluation, and automated scanning benchmarks.</p>
        <p><a href="/" style="color:#38bdf8;">&larr; Back to Home</a></p>
    </body></html>
    """)


@app.get("/contact", response_class=HTMLResponse)
def contact():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html><body style="background:#070d18; color:#e2e8f0; font-family:sans-serif; padding:2rem;">
        <h1>Contact Support</h1>
        <p>Email: security-lab@threatsentry.local</p>
        <p><a href="/" style="color:#38bdf8;">&larr; Back to Home</a></p>
    </body></html>
    """)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
