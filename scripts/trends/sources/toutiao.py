"""Read public Toutiao hot-list items and keep only AI-related records."""
from __future__ import annotations

from opencli_adapter import run_json, _records


def collect(query="AI", window="72h", limit=20):
    del window  # endpoint exposes a daily list and no historical filter
    terms = [term.casefold() for term in query.split() if len(term) > 1]
    raw = _records(run_json("toutiao", ["hot", "--limit", str(min(limit, 50))]))
    selected = []
    for row in raw:
        title = str(row.get("title") or row.get("query") or "")
        if terms and not any(term in title.casefold() for term in terms):
            continue
        selected.append({"platform": "toutiao", "source_type": "community", "title": title, "url": row.get("url"), "published_at": row.get("published_at"), "engagement": {"likes": row.get("hot_value")}, "raw_topic": title})
    return selected
