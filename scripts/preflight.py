#!/usr/bin/env python3
"""One-command preflight for a draft.

Runs local lint, optional integrity comparison, and optional Zhuque evaluation.
Does not rewrite content automatically; the Agent Skill consumes the reports.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from article_lint import analyze_text
from integrity_check import compare_texts
from zhuque_client import DEFAULT_ENDPOINT, classify_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("article")
    parser.add_argument("--original")
    parser.add_argument("--research-pack", help="JSON evidence pack for industry-observation checks")
    parser.add_argument("--zhuque", action="store_true")
    parser.add_argument("--out-dir", default=".write-real-man")
    parser.add_argument("--endpoint", default=os.environ.get("ZHUQUE_ENDPOINT", DEFAULT_ENDPOINT))
    parser.add_argument("--api-key-env", default="ZHUQUE_API_KEY")
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    article_path = Path(args.article)
    article = article_path.read_text(encoding="utf-8")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    lint = analyze_text(article, research_pack=args.research_pack)
    (out_dir / "lint.json").write_text(json.dumps(lint, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = {"lint_score": lint["score"], "lint_risk_level": lint["risk_level"]}

    if args.original:
        original = Path(args.original).read_text(encoding="utf-8")
        integrity = compare_texts(original, article)
        (out_dir / "integrity.json").write_text(json.dumps(integrity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary["integrity_ok"] = integrity["ok"]
        summary["missing_protected_literals"] = integrity["missing_count"]

    if args.zhuque:
        api_key = os.environ.get(args.api_key_env)
        if not api_key:
            summary["zhuque_error"] = f"missing environment variable {args.api_key_env}"
        else:
            try:
                zhuque = classify_text(article, api_key, args.endpoint, is_merge=False, timeout=args.timeout)
                (out_dir / "zhuque.json").write_text(json.dumps(zhuque, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                summary["zhuque_ok"] = zhuque["ok"]
                summary["zhuque_human_ratio"] = zhuque["human_ratio"]
                summary["zhuque_ai_ratio"] = zhuque["ai_ratio"]
                summary["zhuque_suspected_ai_ratio"] = zhuque["suspected_ai_ratio"]
            except RuntimeError as exc:
                summary["zhuque_error"] = str(exc)

    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
