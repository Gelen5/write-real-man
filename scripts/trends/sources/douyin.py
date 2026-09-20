"""Optional public Douyin video search via the read-only OpenCLI command."""
from social import collect as _collect


def collect(query="AI 日常 普通人", window="72h", limit=20):
    return _collect("douyin", query, window, limit)
