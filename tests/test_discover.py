import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "trends"))
import discover as discovery


class DiscoveryFlowTests(unittest.TestCase):
    def test_fallback_runs_seven_days_and_keeps_evergreen_separate(self):
        fixture = json.loads((ROOT / "examples" / "topic-discovery" / "raw-trends.json").read_text(encoding="utf-8"))
        seen = []

        def fake_collect(query, window, platforms, limit, cache_dir, cache_minutes, refresh):
            seen.append(window)
            items = [] if window == "72h" else fixture["items"]
            return {"items": items, "source_results": [{"name": "fixture", "status": "ok", "window": window}], "window": window, "cache": "fixture", "partial": False}

        with patch.object(discovery, "collect_cached", side_effect=fake_collect):
            result = discovery.discover("AI files", "普通上班族", platforms=["reddit"], top_n=10)
        self.assertEqual(seen, ["72h", "7d"])
        self.assertTrue(result["fallback_used"])
        self.assertEqual(result["window"], "7d")
        self.assertTrue(result["eligible_count"] < 10)
        self.assertTrue(all(row["classification"] == "evergreen" for row in result["evergreen_opportunities"]))


if __name__ == "__main__":
    unittest.main()
