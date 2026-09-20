"""Unauthenticated GitHub repository discovery; rate limits fail locally."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from urllib.parse import quote
from typing import Any

from common import fetch_json


def collect(query: str = "AI assistant agent", window: str = "72h", limit: int = 20) -> list[dict[str, Any]]:
    days = {"24h": 1, "72h": 3, "7d": 7, "30d": 30}.get(window, 3)
    since = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()
    search = f'{query} created:>={since}'
    url = f"https://api.github.com/search/repositories?q={quote(search)}&sort=updated&order=desc&per_page={min(max(limit, 1), 50)}"
    data = fetch_json(url, headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
    return [{
        "platform": "github",
        "source_type": "tool",
        "title": repo.get("full_name") or repo.get("name") or "",
        "summary": repo.get("description") or "",
        "url": repo.get("html_url") or "",
        "author": (repo.get("owner") or {}).get("login"),
        "published_at": repo.get("created_at"),
        "engagement": {"stars": repo.get("stargazers_count")},
        "keywords": [topic for topic in (repo.get("topics") or [])],
        "raw_topic": repo.get("description") or repo.get("full_name") or "",
    } for repo in data.get("items", [])]
