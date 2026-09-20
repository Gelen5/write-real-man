import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "trends"))
from deduplicator import deduplicate
from cluster import cluster
from collector import collect_trends
from normalizer import normalize_item


class TrendDedupTests(unittest.TestCase):
    def test_same_url_seen_again_is_one_piece_of_evidence(self):
        items = [
            normalize_item({"platform": "reddit", "id": "thread-1", "title": "AI helps sort school calendar tasks", "url": "https://example.com/post", "engagement": {"likes": 0}}),
            normalize_item({"platform": "reddit", "id": "thread-1", "title": "AI helps sort school calendar tasks", "url": "https://example.com/post", "engagement": {"likes": 4}}),
        ]
        unique = deduplicate(items)
        grouped = cluster(unique)
        self.assertEqual(len(unique), 1)
        self.assertEqual(len(grouped), 1)
        self.assertEqual(grouped[0]["source_count"], 1)
        self.assertEqual(grouped[0]["platform_count"], 1)
        self.assertEqual(items[0]["engagement"]["likes"], 0)

    def test_distinct_platform_urls_remain_independent_evidence(self):
        items = [
            normalize_item({"platform": "x", "id": "post-x", "title": "AI helps sort school calendar tasks", "url": "https://x.example/post", "published_at": "2026-09-20T10:00:00Z"}),
            normalize_item({"platform": "reddit", "id": "post-r", "title": "AI helps sort school calendar tasks", "url": "https://reddit.example/post", "published_at": "2026-09-20T10:00:00Z"}),
        ]
        unique = deduplicate(items)
        grouped = cluster(unique)
        self.assertEqual(len(unique), 1)
        self.assertEqual(grouped[0]["source_count"], 2)
        self.assertEqual(grouped[0]["platform_count"], 2)

    def test_one_failed_source_does_not_cancel_other_adapters(self):
        class Good:
            @staticmethod
            def collect(**_kwargs):
                return [{"title": "Family uses AI for weekly meal plan", "platform": "reddit", "published_at": "2026-09-20T10:00:00Z"}]

        def loader(name):
            if name == "reddit":
                return Good
            raise RuntimeError("offline source")

        result = collect_trends("family AI", "72h", ["reddit", "x"], loader=loader, now=datetime(2026, 9, 20, 12, tzinfo=timezone.utc))
        statuses = {row["name"]: row["status"] for row in result["source_results"]}
        self.assertEqual(statuses["reddit"], "ok")
        self.assertEqual(statuses["x"], "unavailable")
        self.assertEqual(len(result["items"]), 1)
        self.assertTrue(result["partial"])


if __name__ == "__main__":
    unittest.main()
