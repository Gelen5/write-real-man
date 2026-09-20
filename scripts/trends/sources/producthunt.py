"""Product Hunt GraphQL discovery (requires a user-provided developer token)."""
from __future__ import annotations

import json
import os
import urllib.request
from typing import Any

from common import USER_AGENT


def collect(query: str = "AI", window: str = "72h", limit: int = 20) -> list[dict[str, Any]]:
    token = os.environ.get("PRODUCTHUNT_API_TOKEN")
    if not token:
        raise RuntimeError("Product Hunt API token is not configured; source unavailable")
    gql = "query($n:Int!){posts(first:$n,order:NEWEST){edges{node{name tagline url votesCount createdAt}}}}"
    body = json.dumps({"query": gql, "variables": {"n": min(max(limit, 1), 20)}}).encode()
    req = urllib.request.Request("https://api.producthunt.com/v2/api/graphql", data=body, method="POST", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as response:
        payload = json.loads(response.read().decode("utf-8"))
    nodes = [edge["node"] for edge in payload.get("data", {}).get("posts", {}).get("edges", [])]
    query_terms = [term.casefold() for term in query.split() if len(term) > 1]
    rows = []
    for row in nodes:
        text = f"{row.get('name') or ''} {row.get('tagline') or ''}".casefold()
        if query_terms and not any(term in text for term in query_terms):
            continue
        rows.append({"platform": "producthunt", "source_type": "tool", "title": row.get("name"), "summary": row.get("tagline"), "url": row.get("url"), "published_at": row.get("createdAt"), "engagement": {"likes": row.get("votesCount")}, "raw_topic": row.get("tagline")})
    return rows
