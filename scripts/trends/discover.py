#!/usr/bin/env python3
"""Run collection → dedup → cluster → rank → human-centered transformation."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from collector import DEFAULT_PLATFORMS, WINDOW_HOURS, collect_cached
from deduplicator import deduplicate
from cluster import cluster
from topic_ranker import rank_topics
from topic_transformer import transform_topics

EVERGREEN = [
    {"title": "手头有几条工作记录，怎么让 AI 帮忙整理周报", "audience": "普通上班族", "classification": "evergreen"},
    {"title": "收到几十页 PDF，怎样让 AI 按问题找重点", "audience": "需要处理长文件的人", "classification": "evergreen"},
    {"title": "简历没思路时，先让 AI 对照经历和岗位要求", "audience": "普通求职者", "classification": "evergreen"},
    {"title": "旅行计划别排太满，让 AI 按真实限制做减法", "audience": "正在安排出行的人", "classification": "evergreen"},
    {"title": "没选题时，先给 AI 一段真实素材", "audience": "自媒体创作者", "classification": "evergreen"},
    {"title": "家长群通知太长，让 AI 先列日期、物品和待确认项", "audience": "家长", "classification": "evergreen"},
    {"title": "会议记录很零散，让 AI 先整理决定和待办", "audience": "经常参加会议的上班族", "classification": "evergreen"},
    {"title": "冰箱里食材有限时，让 AI 按现有东西列几种晚饭思路", "audience": "需要安排家常饭菜的人", "classification": "evergreen"},
    {"title": "收到退换货说明时，让 AI 把期限和需要准备的材料列出来", "audience": "经常网购的普通消费者", "classification": "evergreen"},
    {"title": "家电说明书太长时，让 AI 按你的问题找相关步骤", "audience": "需要查操作说明的人", "classification": "evergreen"},
]


def evergreen_for_query(query: str) -> list[dict[str, str]]:
    q = query.casefold()
    if "workbuddy" in q:
        return [
            {"title": "WorkBuddy 刚打开，先让它整理一小段工作记录", "audience": "刚接触 WorkBuddy 的上班族", "classification": "evergreen"},
            {"title": "周报只有几条零散记录时，怎么让 WorkBuddy 整理又不夸大进度", "audience": "需要交周报的上班族", "classification": "evergreen"},
            {"title": "WorkBuddy 里已有资料太多，怎样选一份作为当前任务的参考", "audience": "需要处理工作文档的人", "classification": "evergreen"},
            {"title": "客户的问题还没解决，怎么让 WorkBuddy 先整理成待确认清单", "audience": "客服、销售和项目协作人员", "classification": "evergreen"},
            {"title": "不会做海报时，怎样用 WorkBuddy 起一版可修改的草稿", "audience": "小店主和普通创作者", "classification": "evergreen"},
            {"title": "会议记录太乱时，怎样让 WorkBuddy 分开列决定和待办", "audience": "经常参加会议的上班族", "classification": "evergreen"},
            {"title": "让 WorkBuddy 处理文件前，先检查它有没有把待确认写成已完成", "audience": "需要提交工作材料的人", "classification": "evergreen"},
        ]
    if "chatgpt" in q:
        return [
            {"title": "收到几十页 PDF，怎样让 ChatGPT 按问题找重点", "audience": "需要处理长文件的人", "classification": "evergreen"},
            {"title": "简历没思路时，先让 ChatGPT 对照经历和岗位要求", "audience": "普通求职者", "classification": "evergreen"},
            {"title": "家庭通知太多时，怎样让 ChatGPT 列出日期和待确认项", "audience": "家长和家庭成员", "classification": "evergreen"},
            {"title": "旅行计划别排太满，让 ChatGPT 按真实限制做减法", "audience": "正在安排出行的人", "classification": "evergreen"},
            {"title": "每周都要重复整理的事，先试着让 ChatGPT 汇总成清单", "audience": "经常处理重复事务的人", "classification": "evergreen"},
            {"title": "没选题时，先给 ChatGPT 一段真实素材", "audience": "自媒体创作者", "classification": "evergreen"},
            {"title": "ChatGPT 给错日期时，怎么按原文逐项校正", "audience": "日常使用 AI 的普通人", "classification": "evergreen"},
        ]
    return EVERGREEN


def discover(query: str, audience: str, window: str = "72h", fallback_window: str = "7d", platforms: list[str] | None = None, top_n: int = 10, limit_per_source: int = 20, cache_dir: Path | None = None, cache_minutes: int = 60, refresh: bool = False, auto_expand: bool = True) -> dict[str, Any]:
    platforms = platforms or DEFAULT_PLATFORMS
    cache_dir = cache_dir or HERE.parents[1] / ".cache" / "trends"
    first = collect_cached(query, window, platforms, limit_per_source, cache_dir, cache_minutes, refresh)
    collections = [first]
    item_rows = list(first["items"])
    deduped = deduplicate(item_rows)
    ranked = rank_topics(cluster(deduped))
    topics = transform_topics(ranked, audience, top_n)
    used_window = window
    if auto_expand and len(topics) < top_n and window == "72h" and fallback_window == "7d":
        wider = collect_cached(query, fallback_window, platforms, limit_per_source, cache_dir, cache_minutes, refresh)
        collections.append(wider)
        item_rows.extend(wider["items"])
        for row in item_rows:
            row["window_hours"] = WINDOW_HOURS[fallback_window]
        ranked = rank_topics(cluster(deduplicate(item_rows)))
        topics = transform_topics(ranked, audience, top_n)
        used_window = fallback_window
    current_count = len(topics)
    return {
        "schema_version": "0.3.0",
        "collected_at": collections[-1].get("collected_at"),
        "query": query,
        "audience": audience,
        "requested_window": window,
        "window": used_window,
        "fallback_used": used_window != window,
        "top_n": top_n,
        "eligible_count": current_count,
        "topics": topics,
        "evergreen_opportunities": evergreen_for_query(query) if current_count < top_n else [],
        "source_results": [{**row, "window": collection["window"]} for collection in collections for row in collection["source_results"]],
        "items_collected": len(item_rows),
        "partial": any(collection.get("partial") for collection in collections),
        "cache": [collection.get("cache", "direct") for collection in collections],
        "note": "Scores are transparent heuristics. Undated records are not eligible as current trends; evergreen opportunities are not counted in the live top list.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="AI 日常")
    parser.add_argument("--audience", default="普通上班族和普通 AI 用户")
    parser.add_argument("--window", choices=WINDOW_HOURS, default="72h")
    parser.add_argument("--fallback-window", choices=WINDOW_HOURS, default="7d")
    parser.add_argument("--platforms", default=",".join(DEFAULT_PLATFORMS))
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--cache-minutes", type=int, default=60)
    parser.add_argument("--cache-dir", default=str(HERE.parents[1] / ".cache" / "trends"))
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--no-fallback", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()
    result = discover(args.query, args.audience, args.window, args.fallback_window, [p.strip() for p in args.platforms.split(",") if p.strip()], args.top, args.limit, Path(args.cache_dir), args.cache_minutes, args.refresh, not args.no_fallback)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
