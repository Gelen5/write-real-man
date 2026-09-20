"""Generic read-only OpenCLI adapter for optional public social sources."""
from __future__ import annotations

from typing import Any

from opencli_adapter import search


def collect(platform: str, query: str, window: str = "72h", limit: int = 20) -> list[dict[str, Any]]:
    cli_name = "weixin" if platform in {"wechat", "weixin"} else platform
    raw = search(cli_name, query, window, limit)
    rows = []
    for row in raw:
        text = row.get("text") or row.get("summary") or row.get("selftext") or row.get("description") or row.get("brief") or row.get("desc") or ""
        title = row.get("title") or (str(text).splitlines()[0][:180] if text else "")
        if not title:
            continue
        lowered = (str(title) + " " + str(text)).casefold()
        trend_type = "pain_point" if any(word in lowered for word in ("求助", "不会", "卡住", "怎么办", "不工作", "失败", "bug", "问题")) else "use_case" if any(word in lowered for word in ("教程", "入门", "怎么用", "怎么做", "分享", "体验", "日常", "整理", "做法", "工作流")) else "news"
        rows.append({
            "platform": platform,
            "source_type": "community",
            "trend_type": trend_type,
            "title": title,
            "summary": text,
            "url": row.get("url") or row.get("link"),
            "author": row.get("author") or row.get("username"),
            "published_at": row.get("published_at") or row.get("publish_time") or row.get("date") or row.get("time") or row.get("created_at") or row.get("created_utc"),
            "engagement": {"likes": _first_present(row, "likes", "like_count", "score", "votes", "hot_value"), "comments": _first_present(row, "comments", "replies"), "shares": _first_present(row, "shares"), "views": _first_present(row, "views", "plays", "play_count")},
            "raw_topic": title,
        })
    return rows


def _first_present(row: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if row.get(key) is not None and row.get(key) != "":
            return row[key]
    return None
