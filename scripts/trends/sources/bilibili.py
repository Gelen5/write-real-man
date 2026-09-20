"""Optional Bilibili public search via existing OpenCLI; no login bypass."""
from social import collect as _collect

def collect(query="AI 普通人 教程", window="72h", limit=20):
    return _collect("bilibili", query, window, limit)
