#!/usr/bin/env python3
"""Merge local lint + Zhuque segment signals into a minimal paragraph rewrite packet."""
from __future__ import annotations

import argparse
import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def normalize(s: str) -> str:
    return re.sub(r"\s+", "", s)


def match_segment(segment_text: str, ps: list[str]) -> tuple[int | None, float]:
    target = normalize(segment_text)
    if not target:
        return None, 0.0
    best_idx, best_score = None, 0.0
    for i, p in enumerate(ps, start=1):
        candidate = normalize(p)
        if target in candidate or candidate in target:
            score = min(len(target), len(candidate)) / max(len(target), len(candidate))
            if score > best_score:
                best_idx, best_score = i, score
        else:
            score = SequenceMatcher(None, target[:500], candidate[:500]).ratio()
            if score > best_score:
                best_idx, best_score = i, score
    return best_idx, best_score


def build_packet(article: str, lint: dict[str, Any] | None, zhuque: dict[str, Any] | None) -> dict[str, Any]:
    ps = paragraphs(article)
    targets: dict[int, dict[str, Any]] = {}

    if lint:
        for item in lint.get("paragraph_findings", []):
            idx = int(item.get("paragraph", 0))
            if 1 <= idx <= len(ps):
                target = targets.setdefault(idx, {"paragraph": idx, "reasons": [], "signals": []})
                target["reasons"].extend(item.get("reasons", []))
                target["signals"].append("local_lint")

    if zhuque:
        segments = zhuque.get("segments") or zhuque.get("segment_labels") or []
        for seg in segments:
            label = seg.get("label")
            risky = seg.get("risky", label in (1, 2, "1", "2"))
            if not risky:
                continue
            idx, confidence = match_segment(str(seg.get("text", "")), ps)
            if idx and confidence >= 0.35:
                target = targets.setdefault(idx, {"paragraph": idx, "reasons": [], "signals": []})
                name = seg.get("label_name") or {1: "AI", 2: "疑似 AI", "1": "AI", "2": "疑似 AI"}.get(label, str(label))
                target["reasons"].append(f"Zhuque segment={name}, conf={seg.get('conf')}")
                target["signals"].append("zhuque")

    ordered = []
    for idx in sorted(targets):
        item = targets[idx]
        item["reasons"] = list(dict.fromkeys(item["reasons"]))
        item["signals"] = list(dict.fromkeys(item["signals"]))
        item["text"] = ps[idx - 1]
        item["rewrite_constraints"] = [
            "preserve facts and technical literals",
            "do not invent first-person experience",
            "fix the diagnosed writing problem rather than adding random noise",
            "keep the paragraph's role in the article",
        ]
        ordered.append(item)

    return {
        "paragraph_count": len(ps),
        "target_count": len(ordered),
        "targets": ordered,
        "strategy": "Rewrite only target paragraphs, then rerun integrity check and external evaluation.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--article", required=True)
    parser.add_argument("--lint")
    parser.add_argument("--zhuque")
    parser.add_argument("--out")
    args = parser.parse_args()

    article = Path(args.article).read_text(encoding="utf-8")
    lint = json.loads(Path(args.lint).read_text(encoding="utf-8")) if args.lint else None
    zhuque = json.loads(Path(args.zhuque).read_text(encoding="utf-8")) if args.zhuque else None
    packet = build_packet(article, lint, zhuque)
    payload = json.dumps(packet, ensure_ascii=False, indent=2)
    print(payload)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
