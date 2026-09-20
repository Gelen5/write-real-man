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
JARGON_TERMS = ["API", "SDK", "MCP", "Transformer", "Attention", "Benchmark", "推理吞吐", "上下文窗口", "向量数据库", "多模态", "端到端", "Agent 架构"]
EVERYDAY_TERMS = ["上班", "家长", "孩子", "学生", "周报", "简历", "旅行", "文件", "通知", "邮件", "做饭", "买菜", "封面", "照片", "客户", "老板", "同事", "出门", "家里"]
ACTION_TERMS = ["打开", "复制", "粘贴", "输入", "上传", "点击", "先写", "检查", "核对", "改成", "保存", "试试", "可以这样问", "提示词", "列出", "整理", "分类", "对照"]
RESULT_TERMS = ["清单", "草稿", "结果", "表格", "行程", "周报", "简历", "待办", "文件夹", "邮件"]
PROMPT_SCAFFOLD = ["Role:", "Context:", "Task:", "Constraints:", "Output:", "角色：", "背景：", "任务：", "约束：", "输出格式："]
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
    # Two occurrences often mean the source material is correctly carried into
    # the result table; only repeated fragments seen at least three times are
    # surfaced as a possible verbal loop.
    return [(k, v) for k, v in chunks.most_common() if v >= 3][:8]


def analyze_text(text: str, trend_linked: bool = False) -> dict[str, Any]:
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

    # Reader usefulness checks are deliberately separate from style diagnostics.
    # They are transparent editorial heuristics, not detector scores.
    clean_length = max(1, len(re.sub(r"\s+", "", text)))
    jargon_hits = {term: text.casefold().count(term.casefold()) for term in JARGON_TERMS if text.casefold().count(term.casefold())}
    jargon_density = sum(jargon_hits.values()) / clean_length * 100
    abstract_density = sum(abstract_hits.values()) / clean_length * 100
    lower_text = text.casefold()
    has_scenario = any(term in lower_text for term in EVERYDAY_TERMS) and any(mark in text for mark in ("比如", "例如", "假设", "这时", "现在", "遇到"))
    has_action = sum(term.casefold() in lower_text for term in ACTION_TERMS) >= 2
    has_material = bool(re.search(r"\d+|[“\"「].{3,}[”\"」]|周一|周二|下周|今天|明天", text))
    has_result = any(term in text for term in RESULT_TERMS) and any(term in text for term in ("最后", "拿到", "整理成", "保存", "结果", "完成"))
    scaffold_hits = [term for term in PROMPT_SCAFFOLD if term.casefold() in lower_text]
    marketing_hits = [phrase for phrase in ("赋能", "颠覆", "革命性", "全新体验", "效率翻倍", "彻底改变", "人人都该用") if phrase in text]
    news_markers = sum(text.count(term) for term in ("发布", "上线", "推出", "宣布", "更新"))
    human_problem_markers = sum(text.count(term) for term in EVERYDAY_TERMS)
    metrics = {
        "jargon_density": round(jargon_density, 4),
        "abstract_language": round(abstract_density, 4),
        "scenario_presence": has_scenario,
        "actionability": has_action,
        "concrete_material": has_material,
        "result_presence": has_result,
        "ai_marketing_tone": {"hits": marketing_hits, "count": len(marketing_hits)},
        "prompt_naturalness": {"scaffold_labels": scaffold_hits, "natural_question_markers": sum(text.count(x) for x in ("帮我", "看一下", "先", "别猜", "如果不确定"))},
        "trend_to_human_alignment": None,
    }
    ordinary_score = 100
    if jargon_density > 1.5:
        ordinary_score -= min(25, int((jargon_density - 1.5) * 8) + 8)
    if abstract_density > 2:
        ordinary_score -= min(20, int((abstract_density - 2) * 5) + 5)
    ordinary_score -= 0 if has_scenario else 20
    ordinary_score -= 0 if has_action else 12
    ordinary_score -= 0 if has_material else 10
    ordinary_score -= 0 if has_result else 12
    ordinary_score -= min(20, len(marketing_hits) * 8)
    ordinary_score -= min(12, len(scaffold_hits) * 3)
    ordinary_score = max(0, min(100, ordinary_score))
    metrics["ordinary_reader_score"] = ordinary_score
    if not has_scenario:
        findings.append({"code": "missing_everyday_scenario", "severity": "medium", "message": "没有识别到明确的日常人物和具体情境。"})
    if not has_action:
        findings.append({"code": "low_actionability", "severity": "medium", "message": "缺少可照着做的动作步骤。"})
    if not has_result:
        findings.append({"code": "missing_useful_result", "severity": "medium", "message": "没有清楚交代读者最后能拿到什么结果。"})
    if trend_linked:
        alignment = round(min(1.0, human_problem_markers / max(1, news_markers + human_problem_markers)), 3)
        metrics["trend_to_human_alignment"] = alignment
        if news_markers >= 4 and alignment < 0.35:
            findings.append({"code": "trend_still_news_centered", "severity": "high", "message": "发布信息比普通人的实际问题更突出；压缩新闻背景，增加可操作场景。"})

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
        "ordinary_reader_metrics": metrics,
        "findings": findings,
        "paragraph_findings": paragraph_findings,
        "note": "This is a deterministic writing-quality heuristic, not an AI detector.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Markdown/text article path")
    parser.add_argument("--json-out", help="Write JSON report to path")
    parser.add_argument("--trend-linked", action="store_true", help="Check whether a trend article pivots from news to a human problem")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    report = analyze_text(text, trend_linked=args.trend_linked)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
