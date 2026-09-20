#!/usr/bin/env python3
"""Tencent EdgeOne Makers Zhuque text client using Python stdlib only."""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_ENDPOINT = "https://ai-gateway.edgeone.link/v1/providers/zhuque-text/classify"
LABEL_NAMES = {0: "human", 1: "ai", 2: "suspected_ai"}


def normalize_response(data: dict[str, Any]) -> dict[str, Any]:
    labels = data.get("labels_ratio") or {}
    segments = []
    for raw in data.get("segment_labels") or []:
        label = int(raw.get("label", -1)) if str(raw.get("label", "")).lstrip("-").isdigit() else raw.get("label")
        item = dict(raw)
        item["label_name"] = LABEL_NAMES.get(label, "unknown")
        item["risky"] = label in (1, 2)
        segments.append(item)

    human = float(labels.get("0", 0) or 0)
    ai = float(labels.get("1", 0) or 0)
    suspected = float(labels.get("2", 0) or 0)
    return {
        "ok": data.get("status") == "success",
        "status": data.get("status"),
        "human_ratio": human,
        "ai_ratio": ai,
        "suspected_ai_ratio": suspected,
        "risk_ratio": ai + suspected,
        "ratio_confidence": data.get("ratio_confidence"),
        "softmax_confidence": data.get("softmax_confidence"),
        "segments": segments,
        "usage": data.get("usage"),
        "makers_models_usage": data.get("makers_models_usage"),
        "message": data.get("msg", ""),
        "raw": data,
    }


def classify_text(
    text: str,
    api_key: str,
    endpoint: str = DEFAULT_ENDPOINT,
    is_merge: bool = False,
    timeout: int = 30,
) -> dict[str, Any]:
    body = json.dumps({"text": text, "is_merge": is_merge}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "write-real-man/0.3.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Zhuque HTTP {exc.code}: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Zhuque network error: {exc}") from exc
    return normalize_response(data)


def str_to_bool(value: str) -> bool:
    lowered = value.lower()
    if lowered in {"1", "true", "yes", "y"}:
        return True
    if lowered in {"0", "false", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError("expected true/false")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file")
    group.add_argument("--text")
    parser.add_argument("--endpoint", default=os.environ.get("ZHUQUE_ENDPOINT", DEFAULT_ENDPOINT))
    parser.add_argument("--api-key-env", default="ZHUQUE_API_KEY")
    parser.add_argument("--is-merge", type=str_to_bool, default=False)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--json-out")
    args = parser.parse_args()

    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        print(f"Missing API key environment variable: {args.api_key_env}", file=sys.stderr)
        return 2

    text = Path(args.file).read_text(encoding="utf-8") if args.file else args.text
    if not text or not text.strip():
        print("Text is empty", file=sys.stderr)
        return 2

    try:
        result = classify_text(text, api_key, args.endpoint, args.is_merge, args.timeout)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 3

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n", encoding="utf-8")
    return 0 if result["ok"] else 4


if __name__ == "__main__":
    raise SystemExit(main())
