#!/usr/bin/env python3
"""Collect public AI trend signals with isolated adapters and an hourly cache."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
SOURCES_DIR = HERE / "sources"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SOURCES_DIR))
from normalizer import normalize_item  # noqa: E402

WINDOW_HOURS = {"24h": 24, "72h": 72, "7d": 168, "30d": 720}
ADAPTERS = {
    "official": "official", "xiaohongshu": "xiaohongshu", "zhihu": "zhihu", "weibo": "weibo",
    "douyin": "douyin", "bilibili": "bilibili", "wechat": "wechat", "toutiao": "toutiao", "juejin": "juejin", "36kr": "social",
    "reddit": "reddit", "x": "x", "github": "github", "hackernews": "hackernews", "producthunt": "producthunt",
}
DOMESTIC_PLATFORMS = ["xiaohongshu", "zhihu", "weibo", "douyin", "bilibili", "wechat", "toutiao", "juejin", "36kr"]
GLOBAL_PLATFORMS = ["reddit", "x", "github", "hackernews", "producthunt"]
DEFAULT_PLATFORMS = ["official", *DOMESTIC_PLATFORMS, *GLOBAL_PLATFORMS]
SOURCE_LABELS = {
    "official": "官方产品与更新源", "xiaohongshu": "小红书公开搜索", "zhihu": "知乎公开搜索", "weibo": "微博公开搜索",
    "douyin": "抖音公开搜索", "bilibili": "B站公开搜索", "wechat": "微信公众号文章搜索（搜狗）",
    "toutiao": "今日头条公开热榜", "juejin": "掘金 AI 热榜", "36kr": "36氪公开搜索",
    "reddit": "Reddit 公开搜索", "x": "X 最新搜索", "github": "GitHub 公共 API", "hackernews": "Hacker News 公共 API", "producthunt": "Product Hunt API",
}


def _parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if result.tzinfo is None:
            result = result.replace(tzinfo=timezone.utc)
        return result.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _run_one(name: str, query: str, window: str, limit: int, now: datetime, loader: Callable[[str], Any] = importlib.import_module) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    started = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        module = loader(f"{ADAPTERS[name]}")
        if query.strip().casefold() in {"ai", "ai 日常"}:
            adapter_query = "AI" if name == "official" else "AI 日常" if name in DOMESTIC_PLATFORMS else "AI everyday"
        else:
            adapter_query = query
        if name == "36kr":
            result = module.collect("36kr", adapter_query, window, limit)
        else:
            result = module.collect(query=adapter_query, window=window, limit=limit)
        source_status = []
        if isinstance(result, dict):
            rows = result.get("items", [])
            source_status = result.get("sources", [])
            status = result.get("status", "ok")
        else:
            rows, status = result, "ok"
        normalized = []
        older_than = now - timedelta(hours=WINDOW_HOURS[window])
        for raw in rows:
            if not isinstance(raw, dict):
                continue
            record = dict(raw)
            record.setdefault("source_name", SOURCE_LABELS.get(name, name))
            item = normalize_item(record, name)
            if not item:
                continue
            item["source_name"] = record.get("source_name") or name
            item["source_id"] = record.get("source_id") or name
            item["platform_group"] = "official" if name == "official" else "domestic" if name in DOMESTIC_PLATFORMS else "global"
            item["window_hours"] = WINDOW_HOURS[window]
            published = _parse_time(item.get("published_at"))
            if published and published < older_than:
                continue
            item["date_confidence"] = "dated" if published else "unknown"
            normalized.append(item)
        region = "official" if name == "official" else "domestic" if name in DOMESTIC_PLATFORMS else "global"
        return ({"name": name, "label": SOURCE_LABELS.get(name, name), "region": region, "status": status, "items": len(normalized), "collected_at": started, "sources": source_status}, normalized)
    except Exception as exc:
        region = "official" if name == "official" else "domestic" if name in DOMESTIC_PLATFORMS else "global"
        return ({"name": name, "label": SOURCE_LABELS.get(name, name), "region": region, "status": "unavailable", "items": 0, "collected_at": started, "reason": f"{type(exc).__name__}: {str(exc)[:240]}"}, [])


def collect_trends(query: str, window: str = "72h", platforms: list[str] | None = None, limit: int = 20, loader: Callable[[str], Any] = importlib.import_module, now: datetime | None = None) -> dict[str, Any]:
    if window not in WINDOW_HOURS:
        raise ValueError(f"unsupported window: {window}")
    names = platforms or DEFAULT_PLATFORMS
    invalid = sorted(set(names) - set(ADAPTERS))
    if invalid:
        raise ValueError(f"unknown platforms: {invalid}")
    now = now or datetime.now(timezone.utc)
    results = []
    all_items = []
    with ThreadPoolExecutor(max_workers=min(5, max(1, len(names)))) as pool:
        futures = [pool.submit(_run_one, name, query, window, limit, now, loader) for name in names]
        for future in as_completed(futures):
            status, rows = future.result()
            results.append(status)
            all_items.extend(rows)
    results.sort(key=lambda r: names.index(r["name"]))
    return {"schema_version": "0.3.0", "collected_at": now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"), "query": query, "window": window, "window_hours": WINDOW_HOURS[window], "source_results": results, "items": all_items, "partial": any(row["status"] != "ok" for row in results)}


def _cache_path(cache_dir: Path, query: str, window: str, platforms: list[str]) -> Path:
    key = hashlib.sha256((query + "\0" + window + "\0" + ",".join(platforms)).encode()).hexdigest()[:16]
    return cache_dir / f"{window}-{key}.json"


def collect_cached(query: str, window: str, platforms: list[str], limit: int, cache_dir: Path, cache_minutes: int = 60, refresh: bool = False) -> dict[str, Any]:
    cache_file = _cache_path(cache_dir, query, window, platforms)
    if cache_file.exists() and not refresh:
        age = datetime.now(timezone.utc).timestamp() - cache_file.stat().st_mtime
        if age < max(0, cache_minutes) * 60:
            payload = json.loads(cache_file.read_text(encoding="utf-8"))
            payload["cache"] = "hit"
            return payload
    payload = collect_trends(query, window, platforms, limit)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    payload["cache"] = "miss"
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="AI 日常")
    parser.add_argument("--window", choices=WINDOW_HOURS, default="72h")
    parser.add_argument("--platforms", default=",".join(DEFAULT_PLATFORMS), help="comma-separated adapters")
    parser.add_argument("--limit", type=int, default=20, help="maximum records per adapter")
    parser.add_argument("--cache-minutes", type=int, default=60)
    parser.add_argument("--cache-dir", default=str(HERE.parents[1] / ".cache" / "trends"))
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()
    platforms = [name.strip().lower() for name in args.platforms.split(",") if name.strip()]
    cache_dir = Path(args.cache_dir)
    payload = collect_cached(args.query, args.window, platforms, args.limit, cache_dir, args.cache_minutes, args.refresh)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        output_path = Path(args.out)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
