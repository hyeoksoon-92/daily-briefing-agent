# tools/github.py
import httpx
from datetime import date, timedelta


def get_github_trending(limit: int = 5) -> str:
    since = (date.today() - timedelta(days=1)).isoformat()
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"created:>{since}",
        "sort": "stars",
        "order": "desc",
        "per_page": limit,
    }
    headers = {"Accept": "application/vnd.github+json"}
    response = httpx.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    items = response.json().get("items", [])[:limit]

    lines = []
    for i, repo in enumerate(items, 1):
        name = repo["full_name"]
        desc = repo.get("description") or "설명 없음"
        stars = repo["stargazers_count"]
        lang = repo.get("language") or "N/A"
        lines.append(f"{i}. {name} ({lang}) - {stars}★\n   {desc}")
    return "\n".join(lines)
