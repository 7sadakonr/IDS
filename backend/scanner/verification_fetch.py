from collections.abc import Awaitable, Callable, Sequence

import httpx

from backend.scanner.ssrf import ensure_public_host
from backend.scanner.target_validation import normalize_target
from backend.scanner.verification import matches_verification_file

Resolver = Callable[[str], Awaitable[Sequence[str]]]
MAX_VERIFICATION_BYTES = 64 * 1024


async def verify_ownership_document(origin: str, token: str, *, resolver: Resolver | None = None) -> bool:
    """Fetch the fixed ownership challenge path after DNS safety validation.

    Redirects are deliberately not followed here; a future redirect handler must
    validate every next location before any network request is made.
    """
    target = normalize_target(origin)
    await ensure_public_host(target.host, resolver=resolver)
    challenge_url = f"{target.origin}/.well-known/threatsentry.txt"
    timeout = httpx.Timeout(connect=5, read=8, write=5, pool=5)
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
        async with client.stream("GET", challenge_url, headers={"Accept": "text/plain"}) as response:
            if response.status_code != 200:
                return False
            body = bytearray()
            async for chunk in response.aiter_bytes():
                body.extend(chunk)
                if len(body) > MAX_VERIFICATION_BYTES:
                    return False
    return matches_verification_file(body.decode("utf-8", errors="replace"), token)
