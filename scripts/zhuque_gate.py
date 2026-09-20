#!/usr/bin/env python3
"""Apply user-defined acceptance thresholds to a normalized Zhuque result."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def evaluate(data: dict, min_human: float, max_ai: float, max_suspected: float) -> dict:
    human = float(data.get("human_ratio", (data.get("labels_ratio") or {}).get("0", 0)) or 0)
    ai = float(data.get("ai_ratio", (data.get("labels_ratio") or {}).get("1", 0)) or 0)
    suspected = float(data.get("suspected_ai_ratio", (data.get("labels_ratio") or {}).get("2", 0)) or 0)
    checks = {
        "human_ratio": {"value": human, "operator": ">=", "target": min_human, "ok": human >= min_human},
        "ai_ratio": {"value": ai, "operator": "<=", "target": max_ai, "ok": ai <= max_ai},
        "suspected_ai_ratio": {"value": suspected, "operator": "<=", "target": max_suspected, "ok": suspected <= max_suspected},
    }
    return {
        "pass": all(x["ok"] for x in checks.values()),
        "checks": checks,
        "note": "These are project-defined thresholds, not an official Tencent pass/fail standard.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result")
    parser.add_argument("--min-human", type=float, default=0.70)
    parser.add_argument("--max-ai", type=float, default=0.15)
    parser.add_argument("--max-suspected", type=float, default=0.25)
    parser.add_argument("--json-out")
    args = parser.parse_args()

    data = json.loads(Path(args.result).read_text(encoding="utf-8"))
    report = evaluate(data, args.min_human, args.max_ai, args.max_suspected)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        Path(args.json_out).write_text(payload + "\n", encoding="utf-8")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
