#!/usr/bin/env python3
"""Remove exact URL and near-identical repost duplicates."""
from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any


def _key(item: dict[str, Any]) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", str(item.get("title", "")).casefold())


def deduplicate(items: list[dict[str, Any]], similarity: float = 0.92) -> list[dict[str, Any]]:
    """Keep one representative while retaining every observation as evidence."""
    result: list[dict[str, Any]] = []
    by_url: dict[str, dict[str, Any]] = {}
    for original in items:
        item = dict(original)
        url = str(item.get("url") or "").rstrip("/").casefold()
        duplicate = by_url.get(url) if url else None
        if duplicate is None:
            key = _key(item)
            duplicate = next((candidate for candidate in result if key and SequenceMatcher(None, key, _key(candidate)).ratio() >= similarity), None)
        observation = {k: item.get(k) for k in ("id", "platform", "source_name", "source_type", "trend_type", "url", "author", "published_at", "engagement", "summary")}
        if duplicate is not None:
            previous = duplicate.setdefault("evidence", [observation])
            already_seen = any(
                (observation.get("id") and e.get("id") == observation.get("id"))
                or (url and e.get("url", "").rstrip("/").casefold() == url)
                for e in previous
            )
            if not already_seen:
                previous.append(observation)
            continue
        item["evidence"] = [observation]
        result.append(item)
        if url:
            by_url[url] = item
    return result
