"""Public Hacker News search through the Algolia HN API."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from urllib.parse import quote
from typing import Any

from common import fetch_json


def collect(query: str = "AI assistant", window: str = "72h", limit: int = 20) -> list[dict[str, Any]]:
    hours = {"24h": 24, "72h": 72, "7d": 168, "30d": 720}.get(window, 72)
    after = int((datetime.now(timezone.utc) - timedelta(hours=hours)).timestamp())
    url = f"https://hn.algolia.com/api/v1/search_by_date?query={quote(query)}&tags=story&numericFilters=created_at_i>{after}&hitsPerPage={min(max(limit, 1), 50)}"
    data = fetch_json(url)
    records = []
    for hit in data.get("hits", []):
        records.append({
            "platform": "hackernews",
            "source_type": "community",
            "title": hit.get("title") or hit.get("story_title") or "",
            "summary": hit.get("story_text") or "",
            "url": hit.get("url") or (f"https://news.ycombinator.com/item?id={hit.get('objectID')}" if hit.get("objectID") else ""),
            "author": hit.get("author"),
            "published_at": hit.get("created_at"),
            "engagement": {"likes": hit.get("points"), "comments": hit.get("num_comments")},
            "raw_topic": hit.get("title") or "",
        })
    return records
