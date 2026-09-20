#!/usr/bin/env python3
"""Group close title/topic matches; keep source-level observations visible."""
from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any

STOP = {"the", "and", "for", "with", "from", "that", "this", "how", "what", "can", "new", "using", "use", "ai", "的", "了", "和", "在", "怎么", "如何", "一个", "这个"}


def _tokens(item: dict[str, Any]) -> set[str]:
    text = " ".join(str(item.get(k) or "") for k in ("title", "raw_topic", "keywords")).casefold()
    words = re.findall(r"[a-z0-9+#.-]{2,}|[\u4e00-\u9fff]{2,}", text)
    return {word for word in words if word not in STOP}


def _related(left: dict[str, Any], right: dict[str, Any], threshold: float) -> bool:
    product_left = str(left.get("product") or "").casefold()
    product_right = str(right.get("product") or "").casefold()
    if product_left and product_left == product_right:
        a, b = _tokens(left), _tokens(right)
        jaccard = len(a & b) / max(1, len(a | b))
        title_ratio = SequenceMatcher(None, str(left.get("title", "")).casefold(), str(right.get("title", "")).casefold()).ratio()
        return jaccard >= threshold or title_ratio >= 0.62
    a, b = _tokens(left), _tokens(right)
    jaccard = len(a & b) / max(1, len(a | b))
    title_ratio = SequenceMatcher(None, str(left.get("title", "")).casefold(), str(right.get("title", "")).casefold()).ratio()
    return jaccard >= threshold or title_ratio >= max(0.82, threshold + 0.25)


def cluster(items: list[dict[str, Any]], threshold: float = 0.30) -> list[dict[str, Any]]:
    parents = list(range(len(items)))

    def find(idx: int) -> int:
        while parents[idx] != idx:
            parents[idx] = parents[parents[idx]]
            idx = parents[idx]
        return idx

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if _related(items[i], items[j], threshold):
                parents[find(j)] = find(i)
    groups: dict[int, list[dict[str, Any]]] = {}
    for i, item in enumerate(items):
        groups.setdefault(find(i), []).append(item)
    result = []
    for group in groups.values():
        representative = max(group, key=lambda row: (bool(row.get("published_at")), len(str(row.get("summary") or ""))))
        observations = [e for item in group for e in item.get("evidence", [{k: item.get(k) for k in ("id", "platform", "source_name", "source_type", "trend_type", "url", "author", "published_at", "engagement", "summary")}])]
        platforms = sorted({str(e.get("platform") or "unknown") for e in observations})
        sources = sorted({str(e.get("source_name") or e.get("platform") or "unknown") for e in observations})
        result.append({
            "topic": representative.get("raw_topic") or representative.get("title"),
            "representative": representative,
            "items": group,
            "evidence": observations,
            "sources": sources,
            "source_count": len(observations),
            "platforms": platforms,
            "platform_count": len(platforms),
            "trend_types": sorted({str(e.get("trend_type") or "news") for e in observations}),
        })
    return result
