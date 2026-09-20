"""Optional Xiaohongshu public search via existing OpenCLI; no login bypass."""
from social import collect as _collect

def collect(query="AI 日常 使用", window="72h", limit=20):
    return _collect("xiaohongshu", query, window, limit)
