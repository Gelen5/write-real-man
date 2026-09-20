"""Official AI product/news RSS feeds used for fact discovery, not heat alone."""
from __future__ import annotations

import json
import os
from typing import Any

from common import read_feed

DEFAULT_FEEDS = [
    {"name": "OpenAI News", "url": "https://openai.com/news/rss.xml"},
    {"name": "Google DeepMind", "url": "https://deepmind.google/blog/feed/basic/"},
    {"name": "Google AI Blog", "url": "https://blog.google/technology/ai/rss/"},
]


def collect(query: str = "AI", window: str = "72h", limit: int = 20) -> dict[str, Any]:
    configured = os.environ.get("WRITE_REAL_MAN_OFFICIAL_FEEDS")
    feeds = json.loads(configured) if configured else DEFAULT_FEEDS
    if not isinstance(feeds, list):
        raise RuntimeError("WRITE_REAL_MAN_OFFICIAL_FEEDS must be a JSON array of {name,url}")
    items = []
    statuses = []
    query_terms = [word.casefold() for word in query.split() if len(word) > 2]
    for feed in feeds:
        name = str(feed.get("name") or feed.get("url") or "official")
        try:
            records = read_feed(str(feed["url"]), platform="official", source_type="news")
            matched = []
            for item in records:
                text = (item.get("title", "") + " " + item.get("summary", "")).casefold()
                if not query_terms or any(term in text for term in query_terms) or query.casefold() in {"ai", "artificial intelligence"}:
                    item["source_name"] = name
                    item["source_id"] = name.casefold().replace(" ", "-")
                    matched.append(item)
            items.extend(matched[:limit])
            statuses.append({"name": name, "status": "ok", "items": min(limit, len(matched))})
        except Exception as exc:  # each feed fails independently
            statuses.append({"name": name, "status": "unavailable", "reason": str(exc)[:240]})
    good = [row for row in statuses if row["status"] == "ok"]
    if not good:
        raise RuntimeError("all configured official feeds are unavailable")
    status = "partial" if any(row["status"] != "ok" for row in statuses) else "ok"
    return {"items": items, "status": status, "sources": statuses}
