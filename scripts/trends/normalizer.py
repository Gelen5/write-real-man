#!/usr/bin/env python3
"""Normalize public-source records into the TrendItem schema."""
from __future__ import annotations

import hashlib
import re
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ENGAGEMENT_KEYS = ("likes", "comments", "shares", "views", "stars")


def _date(value: Any) -> str | None:
    if value is None or value == "":
        return None
    try:
        if isinstance(value, (int, float)) or str(value).isdigit():
            dt = datetime.fromtimestamp(float(value), tz=timezone.utc)
        else:
            raw = str(value).replace("Z", "+00:00")
            relative = re.fullmatch(r"\s*(刚刚|\d+\s*(?:分钟前|小时前|天前))\s*", str(value))
            if relative:
                label = relative.group(1)
                now = datetime.now(timezone.utc)
                if label == "刚刚":
                    dt = now
                else:
                    amount = int(re.search(r"\d+", label).group())
                    unit = "minutes" if "分钟" in label else "hours" if "小时" in label else "days"
                    dt = now - timedelta(**{unit: amount})
            elif re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", raw):
                year, month, day = map(int, raw.split("-"))
                dt = datetime(year, month, day, tzinfo=timezone.utc)
            else:
                try:
                    dt = datetime.fromisoformat(raw)
                except ValueError:
                    dt = parsedate_to_datetime(str(value))
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            dt = dt.astimezone(timezone.utc)
        return dt.isoformat().replace("+00:00", "Z")
    except (ValueError, TypeError, OverflowError, OSError):
        return None


def _url(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    parts = urlsplit(raw)
    params = parse_qsl(parts.query, keep_blank_values=True)
    if parts.netloc.casefold() == "weixin.sogou.com" and parts.path.rstrip("/") == "/link":
        params = [(k, v) for k, v in params if k in {"url", "type"}]
    elif parts.netloc.casefold().endswith("xiaohongshu.com"):
        params = []
    query = [(k, v) for k, v in params if not k.casefold().startswith("utm_") and k.casefold() not in {"fbclid", "gclid", "spm_id", "xsec_token", "xsec_source"}]
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), urlencode(query, doseq=True), ""))


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value) if value is not None and value != "" else None
    except (ValueError, TypeError, OverflowError):
        return None


def normalize_item(raw: dict[str, Any], platform: str | None = None) -> dict[str, Any] | None:
    title = re.sub(r"\s+", " ", str(raw.get("title") or "")).strip()
    if not title:
        return None
    source_platform = str(platform or raw.get("platform") or "unknown").lower()
    url = _url(raw.get("url") or raw.get("link"))
    raw_key = url or f"{source_platform}:{title.casefold()}:{raw.get('published_at') or raw.get('created_at') or ''}"
    item_id = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()[:16]
    engagement_raw = raw.get("engagement") if isinstance(raw.get("engagement"), dict) else {}
    engagement = {key: _int_or_none(engagement_raw.get(key, raw.get(key))) for key in ENGAGEMENT_KEYS}
    keywords = raw.get("keywords") if isinstance(raw.get("keywords"), list) else []
    return {
        "id": item_id,
        "platform": source_platform,
        "source_name": str(raw.get("source_name") or platform or source_platform).strip(),
        "source_type": str(raw.get("source_type") or "community"),
        "title": title,
        "summary": str(raw.get("summary") or raw.get("selftext") or raw.get("description") or "").strip(),
        "url": url,
        "author": str(raw.get("author") or "").strip() or None,
        "published_at": _date(raw.get("published_at") or raw.get("created_at") or raw.get("created_utc")),
        "engagement": engagement,
        "keywords": list(dict.fromkeys(str(k).strip() for k in keywords if str(k).strip())),
        "product": str(raw.get("product") or "").strip() or None,
        "raw_topic": str(raw.get("raw_topic") or title),
        "trend_type": str(raw.get("trend_type") or "news"),
        "rank_inputs": raw.get("rank_inputs") if isinstance(raw.get("rank_inputs"), dict) else {},
    }


def normalize_items(records: list[dict[str, Any]], platform: str | None = None) -> list[dict[str, Any]]:
    result = []
    for record in records:
        item = normalize_item(record, platform)
        if item:
            result.append(item)
    return result
