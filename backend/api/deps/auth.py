class AuthenticationError(ValueError):
    """Raised before a malformed bearer token reaches an authorization boundary."""


def extract_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise AuthenticationError("Authorization header is required")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise AuthenticationError("Authorization header must use a bearer token")
    return token.strip()
