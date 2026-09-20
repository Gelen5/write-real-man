#!/usr/bin/env python3
"""Deterministic preflight diagnostics for Chinese AI-tech articles.

This is a writing-quality heuristic, not an AI detector.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？!?；;])\s*")
TRANSITIONS = [
    "首先", "其次", "再次", "最后", "总之", "综上", "总体而言", "值得注意的是",
    "需要注意的是", "与此同时", "此外", "进一步来说", "从这个角度来看", "换句话说",
]
GENERIC_PHRASES = [
    "随着人工智能技术的快速发展", "随着科技的不断发展", "在数字化浪潮下", "众所周知",
    "不可否认", "具有重要意义", "具有非常重要的价值", "积极拥抱变化", "充分发挥",
    "进一步提升工作效率", "带来全新的体验", "开启新的可能性", "赋能", "降本增效",
]
ABSTRACT_TERMS = [
    "效率", "能力", "价值", "体验", "赋能", "创新", "生态", "生产力", "场景", "范式",
    "升级", "提升", "优化", "转型", "智能化", "高质量", "竞争力",
]
SUMMARY_STARTS = ["总之", "综上", "总的来说", "总体而言", "因此可以看出", "由此可见"]
LIST_MARKER_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)、]\s*)", re.M)
HEADING_RE = re.compile(r"^#{1,6}\s+", re.M)


def _paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def _sentences(text: str) -> list[str]:
    parts = [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]
    return [s for s in parts if not s.startswith("#")]


def _clean_len(s: str) -> int:
    return len(re.sub(r"\s+", "", s))


def _cv(values: list[int]) -> float:
    if len(values) < 2:
        return 0.0
    mean = statistics.fmean(values)
    if mean == 0:
        return 0.0
    return statistics.pstdev(values) / mean


def _repeat_bigrams(sentences: list[str]) -> list[tuple[str, int]]:
    chunks: Counter[str] = Counter()
    for sentence in sentences:
        cleaned = re.sub(r"[\s，。！？!?；;：:、（）()“”\"'`#*_\-]", "", sentence)
        # 6-character windows catch repeated formulaic fragments without being too noisy.
        for i in range(max(0, len(cleaned) - 5)):
            token = cleaned[i : i + 6]
            if len(token) == 6:
                chunks[token] += 1
    return [(k, v) for k, v in chunks.most_common() if v >= 2][:8]


def analyze_text(text: str) -> dict[str, Any]:
    paragraphs = _paragraphs(text)
    sentences = _sentences(text)
    sentence_lengths = [_clean_len(s) for s in sentences]
    paragraph_lengths = [_clean_len(p) for p in paragraphs]

    transition_hits = {t: text.count(t) for t in TRANSITIONS if text.count(t)}
    generic_hits = {p: text.count(p) for p in GENERIC_PHRASES if text.count(p)}
    abstract_hits = {p: text.count(p) for p in ABSTRACT_TERMS if text.count(p)}
    summary_hits = sum(text.count(p) for p in SUMMARY_STARTS)
    list_markers = len(LIST_MARKER_RE.findall(text))
    headings = len(HEADING_RE.findall(text))
    repeated_fragments = _repeat_bigrams(sentences)

    findings: list[dict[str, Any]] = []
    score = 100

    sentence_cv = _cv(sentence_lengths)
    paragraph_cv = _cv(paragraph_lengths)

    if len(sentences) >= 5 and sentence_cv < 0.28:
        findings.append({
            "code": "uniform_sentence_rhythm",
            "severity": "high",
            "message": f"句长变化较低（CV={sentence_cv:.2f}），检查是否存在连续同构句。",
        })
        score -= 14
    elif len(sentences) >= 5 and sentence_cv < 0.40:
        findings.append({
            "code": "slightly_uniform_sentence_rhythm",
            "severity": "medium",
            "message": f"句长变化偏低（CV={sentence_cv:.2f}）。",
        })
        score -= 7

    if len(paragraphs) >= 4 and paragraph_cv < 0.20:
        findings.append({
            "code": "uniform_paragraph_size",
            "severity": "medium",
            "message": f"段落长度过于整齐（CV={paragraph_cv:.2f}）。",
        })
        score -= 7

    transition_count = sum(transition_hits.values())
    if transition_count >= max(3, math.ceil(len(paragraphs) * 0.5)):
        findings.append({
            "code": "formulaic_transitions",
            "severity": "high" if transition_count >= 6 else "medium",
            "message": f"显式模板转折较多（{transition_count} 次）：{transition_hits}",
        })
        score -= min(16, 4 + transition_count * 2)

    generic_count = sum(generic_hits.values())
    if generic_count:
        findings.append({
            "code": "generic_ai_phrases",
            "severity": "high" if generic_count >= 3 else "medium",
            "message": f"发现泛化/模板表达（{generic_count} 次）：{generic_hits}",
        })
        score -= min(18, generic_count * 5)

    if summary_hits >= 2:
        findings.append({
            "code": "repeated_summary_language",
            "severity": "medium",
            "message": f"总结型开头出现 {summary_hits} 次，检查是否重复结论。",
        })
        score -= min(10, summary_hits * 3)

    abstract_count = sum(abstract_hits.values())
    per_1000 = abstract_count / max(1, len(text)) * 1000
    if abstract_count >= 8 and per_1000 >= 6:
        findings.append({
            "code": "abstract_term_density",
            "severity": "medium",
            "message": f"抽象词密度偏高（{abstract_count} 次，约 {per_1000:.1f}/千字），优先换成行为、结果或例子。",
        })
        score -= 8

    if list_markers >= 8 and len(text) < 2500:
        findings.append({
            "code": "list_density",
            "severity": "low",
            "message": f"短文中列表项较多（{list_markers} 项），确认不是把正文机械拆成清单。",
        })
        score -= 4

    if repeated_fragments:
        findings.append({
            "code": "repeated_fragments",
            "severity": "low",
            "message": "存在重复的 6 字片段，检查是否有车轱辘话。",
            "examples": repeated_fragments,
        })
        score -= min(8, len(repeated_fragments))

    paragraph_findings = []
    for idx, p in enumerate(paragraphs, start=1):
        p_hits = [x for x in TRANSITIONS + GENERIC_PHRASES if x in p]
        reasons = []
        if len(p_hits) >= 2:
            reasons.append("模板化连接/泛化表达较集中")
        if sum(p.count(a) for a in ABSTRACT_TERMS) >= 4 and _clean_len(p) < 220:
            reasons.append("抽象词密度高，缺少可观察细节")
        if any(p.startswith(x) for x in SUMMARY_STARTS):
            reasons.append("总结式段落，检查是否重复前文")
        if reasons:
            paragraph_findings.append({
                "paragraph": idx,
                "reasons": reasons,
                "preview": p[:120],
            })

    score = max(0, min(100, score))
    return {
        "score": score,
        "risk_level": "high" if score < 65 else "medium" if score < 80 else "low",
        "stats": {
            "characters": len(text),
            "paragraphs": len(paragraphs),
            "sentences": len(sentences),
            "sentence_length_mean": round(statistics.fmean(sentence_lengths), 2) if sentence_lengths else 0,
            "sentence_length_cv": round(sentence_cv, 3),
            "paragraph_length_mean": round(statistics.fmean(paragraph_lengths), 2) if paragraph_lengths else 0,
            "paragraph_length_cv": round(paragraph_cv, 3),
            "heading_count": headings,
            "list_item_count": list_markers,
        },
        "signals": {
            "transition_hits": transition_hits,
            "generic_phrase_hits": generic_hits,
            "abstract_term_hits": abstract_hits,
        },
        "findings": findings,
        "paragraph_findings": paragraph_findings,
        "note": "This is a deterministic writing-quality heuristic, not an AI detector.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Markdown/text article path")
    parser.add_argument("--json-out", help="Write JSON report to path")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    report = analyze_text(text)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
