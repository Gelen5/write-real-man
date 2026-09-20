import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "trends"))
from topic_ranker import score_topic


class TopicRankerTests(unittest.TestCase):
    def test_technical_benchmark_is_excluded_from_ordinary_top_list(self):
        topic = {"representative": {"title": "New transformer inference engine improves throughput 34%", "summary": "Architecture optimization benchmark", "published_at": "2026-09-20T01:00:00Z"}, "evidence": [{"platform": "github", "source_type": "tool", "url": "https://github.com/example"}], "platforms": ["github"], "source_count": 1}
        scored = score_topic(topic, datetime(2026, 9, 20, 12, tzinfo=timezone.utc))
        self.assertLess(scored["dimensions"]["ordinary_people_relevance"], 0.45)
        self.assertFalse(scored["eligible"])
        self.assertTrue(scored["too_technical"])

    def test_everyday_file_task_scores_as_an_actionable_topic(self):
        topic = {"representative": {"title": "ChatGPT supports working with multiple uploaded files", "summary": "Office worker sorts a long batch of documents", "published_at": "2026-09-20T01:00:00Z", "rank_inputs": {"ordinary_people_relevance": .9, "usefulness": .9, "actionability": .85}}, "evidence": [{"platform": "official", "source_type": "official", "url": "https://example.com"}, {"platform": "reddit", "source_type": "community", "url": "https://reddit.com/example"}], "platforms": ["official", "reddit"], "source_count": 2}
        scored = score_topic(topic, datetime(2026, 9, 20, 12, tzinfo=timezone.utc))
        self.assertTrue(scored["eligible"])
        self.assertGreater(scored["score"], 60)

    def test_single_weak_news_source_does_not_enter_current_shortlist(self):
        topic = {"representative": {"title": "AI company announces a new product", "published_at": "2026-09-20T08:00:00Z"}, "evidence": [{"platform": "official", "source_type": "official", "url": "https://example.com"}], "platforms": ["official"], "source_count": 1}
        scored = score_topic(topic, datetime(2026, 9, 20, 12, tzinfo=timezone.utc))
        self.assertFalse(scored["eligible"])
        self.assertLess(scored["score"], 55)


if __name__ == "__main__":
    unittest.main()
