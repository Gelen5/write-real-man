"""Read the public AI-tagged Juejin hot list; technical bias is penalized later."""
from __future__ import annotations

from opencli_adapter import run_json, _records


def collect(query="AI 日常 使用", window="72h", limit=20):
    del window  # this endpoint is a current hot list, not a date-filtered search
    query_terms = [term.casefold() for term in query.split() if len(term) > 1]
    raw = _records(run_json("juejin", ["hot", "--category", "ai", "--limit", str(min(limit, 50))]))
    return [{
        "platform": "juejin", "source_type": "community", "title": row.get("title"),
        "summary": row.get("brief"), "url": row.get("url"), "author": row.get("author"),
        "published_at": row.get("published_at") or row.get("date"),
        "engagement": {"likes": row.get("likes"), "comments": row.get("comments"), "views": row.get("views")},
        "raw_topic": row.get("title"),
    } for row in raw if row.get("title") and (query in {"AI", "AI 日常", "AI everyday"} or any(term in (str(row.get("title", "")) + " " + str(row.get("brief", ""))).casefold() for term in query_terms))]
