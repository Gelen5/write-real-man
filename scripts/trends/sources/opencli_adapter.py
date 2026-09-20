"""Read-only social search through an already installed OpenCLI adapter."""
from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from typing import Any


def run_json(platform: str, args: list[str], timeout: int = 25) -> Any:
    executable = shutil.which("opencli")
    if not executable:
        raise RuntimeError("opencli is not installed")
    command = [executable, platform, *args, "-f", "json"]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"opencli {platform} search timed out after {timeout}s") from exc
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "command failed").strip().splitlines()
        raise RuntimeError(f"opencli {platform}: {detail[0][:240] if detail else 'command failed'}")
    try:
        payload = json.loads(completed.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"opencli {platform} returned non-JSON output") from exc
    if isinstance(payload, dict) and payload.get("ok") is False:
        detail = payload.get("error") or payload.get("message") or "adapter reported ok=false"
        raise RuntimeError(f"opencli {platform}: {str(detail)[:240]}")
    return payload


def _records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = next((payload[key] for key in ("items", "results", "data", "posts", "list") if isinstance(payload.get(key), list)), [])
    else:
        records = []
    return [row for row in records if isinstance(row, dict)]


def search(platform: str, query: str, window: str, limit: int = 20, timeout: int = 25) -> list[dict[str, Any]]:
    if platform in {"twitter", "x"}:
        days = {"24h": 1, "72h": 3, "7d": 7, "30d": 30}.get(window, 3)
        since = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()
        query = f"{query} since:{since}"
        payload = run_json("twitter", ["search", query, "--product", "live", "--limit", str(limit)], timeout)
    elif platform == "reddit":
        time_filter = {"24h": "day", "72h": "week", "7d": "week", "30d": "month"}.get(window, "week")
        payload = run_json("reddit", ["search", query, "--sort", "new", "--time", time_filter, "--limit", str(limit)], timeout)
    elif platform in {"weixin", "wechat", "xiaohongshu", "bilibili", "zhihu", "weibo", "douyin", "36kr"}:
        cli_name = "weixin" if platform == "wechat" else platform
        payload = run_json(cli_name, ["search", query, "--limit", str(limit)], timeout)
    else:
        payload = run_json(platform, ["search", query, "--limit", str(limit)], timeout)
    return _records(payload)
