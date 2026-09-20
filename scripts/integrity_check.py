#!/usr/bin/env python3
"""Check that protected technical/factual literals survive a rewrite."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

FENCED_CODE_RE = re.compile(r"```[^\n]*\n.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
URL_RE = re.compile(r"https?://[^\s)\]}>\"']+")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\((https?://[^)]+)\)")
VERSION_RE = re.compile(r"\b(?:v?\d+(?:\.\d+){1,3}(?:[-+][A-Za-z0-9.-]+)?|GPT-\d+(?:\.\d+)*)\b", re.I)
NUMBER_UNIT_RE = re.compile(
    r"(?<![\w.])\d+(?:\.\d+)?\s*(?:%|％|ms|s|秒|分钟|小时|天|元|美元|GB|MB|KB|TB|token|tokens|次|倍|字|万|亿)?",
    re.I,
)
API_PATH_RE = re.compile(r"(?<!\w)/(?:v\d+/)?[A-Za-z0-9_.~!$&'()*+,;=:@%/-]{3,}")
ENV_RE = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")
CLI_FLAG_RE = re.compile(r"(?<!\w)--[a-zA-Z0-9][a-zA-Z0-9_-]*")


def extract_literals(text: str) -> dict[str, list[str]]:
    categories = {
        "fenced_code": FENCED_CODE_RE.findall(text),
        "inline_code": INLINE_CODE_RE.findall(text),
        "urls": URL_RE.findall(text),
        "versions": VERSION_RE.findall(text),
        "numbers": [m.group(0).strip() for m in NUMBER_UNIT_RE.finditer(text)],
        "api_paths": API_PATH_RE.findall(text),
        "env_vars": ENV_RE.findall(text),
        "cli_flags": CLI_FLAG_RE.findall(text),
    }
    # Stable unique values, preserve encounter order.
    return {k: list(dict.fromkeys(v)) for k, v in categories.items()}


def compare_texts(original: str, revised: str) -> dict[str, Any]:
    original_lits = extract_literals(original)
    missing: dict[str, list[str]] = {}
    for category, values in original_lits.items():
        lost = [v for v in values if v not in revised]
        if lost:
            missing[category] = lost
    total = sum(len(v) for v in original_lits.values())
    missing_count = sum(len(v) for v in missing.values())
    return {
        "ok": missing_count == 0,
        "protected_literal_count": total,
        "missing_count": missing_count,
        "missing": missing,
        "note": "Review each missing literal. Some removals may be intentional, but none should be accidental.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("original")
    parser.add_argument("revised")
    parser.add_argument("--json-out")
    args = parser.parse_args()

    original = Path(args.original).read_text(encoding="utf-8")
    revised = Path(args.revised).read_text(encoding="utf-8")
    report = compare_texts(original, revised)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n", encoding="utf-8")
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
