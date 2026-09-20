"""X/Twitter search through the user's existing OpenCLI read adapter."""
from __future__ import annotations

from typing import Any

from opencli_adapter import search


def collect(query: str = "AI assistant everyday", window: str = "72h", limit: int = 20) -> list[dict[str, Any]]:
    raw = search("twitter", query, window, limit)
    return [{
        "platform": "x",
        "source_type": "community",
        "trend_type": "use_case" if any(word in str(row.get("text") or "").casefold() for word in ("using", "i use", "made with", "教程", "我用")) else "news",
        "title": row.get("title") or str(row.get("text") or "").splitlines()[0][:180],
        "summary": row.get("text") or row.get("summary") or "",
        "url": row.get("url") or row.get("link"),
        "author": row.get("author") or row.get("username"),
        "published_at": row.get("created_at") or row.get("published_at"),
        "engagement": {"likes": _first(row, "likes", "like_count"), "comments": _first(row, "replies", "reply_count"), "shares": _first(row, "retweets", "repost_count"), "views": row.get("views")},
        "raw_topic": row.get("text") or row.get("title") or "",
    } for row in raw if row.get("text") or row.get("title")]


def _first(row: dict[str, Any], *keys: str) -> Any:
    return next((row[key] for key in keys if row.get(key) is not None), None)
