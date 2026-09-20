"""Optional WeChat public search via existing OpenCLI; no login bypass."""
from social import collect as _collect

def collect(query="AI 普通人 实用", window="72h", limit=20):
    return _collect("weixin", query, window, limit)
