# tests/test_github.py
import respx
import httpx
from tools.github import get_github_trending


@respx.mock
def test_get_github_trending_returns_repos():
    respx.get("https://api.github.com/search/repositories").mock(
        return_value=httpx.Response(200, json={
            "items": [
                {
                    "full_name": "owner/repo",
                    "description": "A cool project",
                    "stargazers_count": 1234,
                    "language": "Python",
                }
            ]
        })
    )
    result = get_github_trending()
    assert "owner/repo" in result
    assert "1234" in result
    assert "Python" in result
    assert isinstance(result, str)
    assert respx.calls.call_count == 1


@respx.mock
def test_get_github_trending_handles_missing_fields():
    respx.get("https://api.github.com/search/repositories").mock(
        return_value=httpx.Response(200, json={
            "items": [
                {
                    "full_name": "owner/minimal",
                    "description": None,
                    "stargazers_count": 0,
                    "language": None,
                }
            ]
        })
    )
    result = get_github_trending()
    assert "owner/minimal" in result
    assert "설명 없음" in result
    assert isinstance(result, str)
