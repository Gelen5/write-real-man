#!/usr/bin/env python3
"""Transparent heuristic scoring for ordinary-reader topic opportunities."""
from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WEIGHTS = {"ordinary_people_relevance": 30, "usefulness": 20, "actionability": 15, "freshness": 10, "cross_platform_heat": 10, "novelty": 10, "evidence_quality": 5}
EVERYDAY = ("周报", "简历", "旅行", "行程", "家长", "孩子", "学校", "做饭", "备餐", "照片", "封面", "小红书", "公众号", "邮件", "文件", "pdf", "会议", "日程", "租房", "报销", "客服", "作业", "购物", "预算", "求职", "普通人", "上班族", "家庭", "日常", "短视频", "视频", "分镜", "自媒体", "创作者", "vlog", "chatgpt", "gemini", "claude", "family", "school", "calendar", "meal", "grocery", "recipe", "household", "email", "schedule", "travel", "resume", "job seeker", "office", "photo", "file", "meeting", "shopping list")
TECH = ("transformer", "attention", "inference engine", "throughput", "cuda kernel", "benchmark", "training run", "模型训练", "推理吞吐", "架构优化", "参数量", "sdk", "api", "mcp server")
MARKETING = ("best ever", "game changing", "革命性", "颠覆", "领先全球", "改变一切")
PURE_NEWS = ("raises $", "融资", "估值", "发布会", "季度营收", "参数达", "benchmark result")


def _age_hours(value: str | None, now: datetime) -> float | None:
    if not value:
        return None


def _count(value: Any) -> float:
    try:
        return max(0.0, float(value)) if value is not None else 0.0
    except (TypeError, ValueError, OverflowError):
        return 0.0
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return max(0.0, (now - dt.astimezone(timezone.utc)).total_seconds() / 3600)
    except (TypeError, ValueError):
        return None


def _dimensions(cluster: dict[str, Any], now: datetime) -> tuple[dict[str, float], list[dict[str, Any]]]:
    item = cluster.get("representative") or cluster
    text = " ".join(str(item.get(key) or "") for key in ("title", "summary", "raw_topic", "product")).casefold()
    explicit = item.get("rank_inputs") or {}
    everyday_hits = sum(term in text for term in EVERYDAY)
    technical_hits = sum(term in text for term in TECH)
    evidence = cluster.get("evidence") or item.get("evidence") or []
    platforms = cluster.get("platforms") or [e.get("platform") for e in evidence]
    unique_platforms = len({p for p in platforms if p})
    engagement_rows = [e.get("engagement") or {} for e in evidence]
    max_comments = max((_count(row.get("comments")) for row in engagement_rows), default=0)
    max_likes = max((_count(row.get("likes")) for row in engagement_rows), default=0)
    engagement_heat = min(0.25, math.log1p(max_comments) / math.log1p(300) * 0.18 + math.log1p(max_likes) / math.log1p(1000) * 0.07)
    computed_heat = min(1, max(0.18, (unique_platforms - 1) * 0.38 + min(0.24, len(evidence) * 0.04) + engagement_heat))
    age = _age_hours(item.get("published_at"), now)
    dims = {
        "ordinary_people_relevance": min(1, float(explicit.get("ordinary_people_relevance", 0.30 + 0.24 * everyday_hits - 0.25 * technical_hits))),
        "usefulness": min(1, float(explicit.get("usefulness", 0.25 + 0.16 * everyday_hits - 0.18 * technical_hits))),
        "actionability": min(1, float(explicit.get("actionability", 0.25 + 0.12 * everyday_hits - 0.18 * technical_hits))),
        "freshness": float(explicit.get("freshness", max(0, 1 - age / max(1, float(item.get("window_hours", 144)))) if age is not None else 0.25)),
        "cross_platform_heat": float(explicit.get("cross_platform_heat", computed_heat)),
        "novelty": float(explicit.get("novelty", 0.60 if everyday_hits and not technical_hits else 0.32)),
        "evidence_quality": float(explicit.get("evidence_quality", min(1, (0.25 if evidence else 0.1) + (0.55 if any(e.get("source_type") == "official" for e in evidence) else 0) + (0.18 if any(e.get("url") for e in evidence) else 0)))),
    }
    dims = {key: max(0.0, min(1.0, val)) for key, val in dims.items()}
    penalties = []
    if technical_hits >= 2:
        penalties.append({"code": "too_technical", "points": 20})
    if any(term in text for term in PURE_NEWS) and not everyday_hits:
        penalties.append({"code": "pure_news", "points": 15})
    if any(term in text for term in MARKETING):
        penalties.append({"code": "pure_marketing", "points": 20})
    if len(evidence) < 2:
        penalties.append({"code": "weak_evidence", "points": 15})
    selected_hours = max(1, float(item.get("window_hours", 72)))
    if age is not None and age > selected_hours:
        penalties.append({"code": "stale", "points": min(20, 10 + int((age - selected_hours) / selected_hours) * 5)})
    return dims, penalties


def score_topic(cluster: dict[str, Any], now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    dimensions, penalties = _dimensions(cluster, now)
    raw = sum(dimensions[name] * weight for name, weight in WEIGHTS.items())
    total = max(0, round(raw - sum(p["points"] for p in penalties), 1))
    item = cluster.get("representative") or cluster
    text = " ".join(str(item.get(key) or "") for key in ("title", "summary", "raw_topic")).casefold()
    current_evidence = bool(item.get("published_at")) and item.get("date_confidence", "dated") != "unknown"
    return {**cluster, "score": total, "dimensions": {k: round(v, 3) for k, v in dimensions.items()}, "penalties": penalties, "classification": "hybrid" if cluster.get("trend_types") and any(x in ("use_case", "pain_point", "behaviour") for x in cluster["trend_types"]) else "trend", "too_technical": any(p["code"] == "too_technical" for p in penalties), "current_evidence": current_evidence, "eligible": current_evidence and total >= 55 and dimensions["ordinary_people_relevance"] >= 0.45 and dimensions["usefulness"] >= 0.40 and not any(p["code"] == "too_technical" for p in penalties), "debug_terms": {"everyday_hits": sum(t in text for t in EVERYDAY), "technical_hits": sum(t in text for t in TECH)}}


def rank_topics(clusters: list[dict[str, Any]], now: datetime | None = None) -> list[dict[str, Any]]:
    return sorted((score_topic(row, now) for row in clusters), key=lambda x: (x["eligible"], x["score"], x.get("platform_count", 0)), reverse=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON with an items array or clusters array")
    parser.add_argument("--out")
    args = parser.parse_args()
    from deduplicator import deduplicate
    from cluster import cluster
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        items = payload
    else:
        items = payload.get("items", [])
    clusters = payload.get("clusters") if isinstance(payload, dict) else None
    ranked = rank_topics(clusters if clusters is not None else cluster(deduplicate(items)))
    output = json.dumps({"topics": ranked}, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
