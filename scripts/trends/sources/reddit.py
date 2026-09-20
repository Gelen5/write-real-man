"""Reddit search through the user's existing, read-only OpenCLI adapter."""
from __future__ import annotations

from typing import Any

from opencli_adapter import search


def collect(query: str = "AI everyday use", window: str = "72h", limit: int = 20) -> list[dict[str, Any]]:
    raw = search("reddit", query, window, limit)
    return [{
        "platform": "reddit",
        "source_type": "community",
        "trend_type": "pain_point" if "?" in str(row.get("title") or "") or "求助" in str(row.get("title") or "") else "use_case" if row.get("selftext") else "news",
        "title": row.get("title"),
        "summary": row.get("selftext") or "",
        "url": row.get("url"),
        "author": row.get("author"),
        "published_at": row.get("created_utc") or row.get("created_at"),
        "engagement": {"likes": row.get("score") if row.get("score") is not None else None, "comments": row.get("comments") if row.get("comments") is not None else None},
        "keywords": [str(row.get("subreddit") or "")],
        "raw_topic": row.get("title"),
    } for row in raw]
