import pytest

from backend.api.deps.auth import AuthenticationError, extract_bearer_token


def test_extract_bearer_token_accepts_a_bearer_header() -> None:
    assert extract_bearer_token("Bearer signed.jwt.token") == "signed.jwt.token"


@pytest.mark.parametrize("header", [None, "", "Basic abc", "Bearer "])
def test_extract_bearer_token_rejects_missing_or_malformed_headers(header: str | None) -> None:
    with pytest.raises(AuthenticationError):
        extract_bearer_token(header)
