"""Shared bounded HTTP and feed helpers for source adapters."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

USER_AGENT = "write-real-man-trend-discovery/0.3.0 (+public read-only research)"


def fetch_bytes(url: str, timeout: int = 10, headers: dict[str, str] | None = None) -> bytes:
    request_headers = {"User-Agent": USER_AGENT, "Accept": "application/json, application/rss+xml, application/atom+xml, application/xml, text/xml"}
    request_headers.update(headers or {})
    req = urllib.request.Request(url, headers=request_headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def fetch_json(url: str, timeout: int = 10, headers: dict[str, str] | None = None) -> Any:
    return json.loads(fetch_bytes(url, timeout, headers).decode("utf-8"))


def _text(parent: ET.Element, names: tuple[str, ...]) -> str:
    for name in names:
        node = parent.find(name)
        if node is not None and node.text:
            return node.text.strip()
    return ""


def read_feed(url: str, platform: str, source_type: str, timeout: int = 10) -> list[dict[str, Any]]:
    payload = fetch_bytes(url, timeout)
    root = ET.fromstring(payload)
    records: list[dict[str, Any]] = []
    for node in root.findall(".//item") + root.findall(".//{http://www.w3.org/2005/Atom}entry"):
        link = _text(node, ("link", "{http://www.w3.org/2005/Atom}link"))
        if not link:
            atom_link = node.find("{http://www.w3.org/2005/Atom}link")
            link = atom_link.get("href", "") if atom_link is not None else ""
        published = _text(node, ("pubDate", "published", "updated", "{http://www.w3.org/2005/Atom}published", "{http://www.w3.org/2005/Atom}updated"))
        try:
            dt = parsedate_to_datetime(published)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            published = dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        except (TypeError, ValueError, OverflowError):
            try:
                dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                published = dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
            except (TypeError, ValueError, OverflowError):
                published = ""
        records.append({
            "platform": platform,
            "source_type": source_type,
            "title": _text(node, ("title", "{http://www.w3.org/2005/Atom}title")),
            "summary": _text(node, ("description", "summary", "content", "{http://www.w3.org/2005/Atom}summary")),
            "url": link,
            "author": _text(node, ("author/name", "{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name")),
            "published_at": published,
        })
    return records
