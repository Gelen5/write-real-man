import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "trends"))
from topic_transformer import transform_topic


class TopicTransformerTests(unittest.TestCase):
    def test_engineering_headline_without_human_problem_is_rejected(self):
        topic = {"title": "New transformer inference engine improves throughput", "eligible": False, "representative": {"title": "New transformer inference engine improves throughput"}}
        self.assertIsNone(transform_topic(topic))

    def test_multi_file_feature_becomes_a_person_problem_action(self):
        topic = {"title": "ChatGPT supports working with multiple uploaded files", "eligible": True, "score": 76, "source_count": 2, "platforms": ["official", "reddit"], "evidence": [], "representative": {"title": "ChatGPT supports working with multiple uploaded files"}}
        result = transform_topic(topic)
        self.assertIsNotNone(result)
        self.assertTrue(result["person"])
        self.assertTrue(result["problem"])
        self.assertTrue(result["ai_action"])
        self.assertTrue(result["useful_result"])
        self.assertIn("长文件", result["title"])

    def test_postdoc_email_is_not_misclassified_as_family_notice(self):
        title = "How to apply for a post doc program? Emails with professor and fellowship details"
        topic = {"title": title, "eligible": True, "score": 70, "representative": {"title": title}}
        self.assertIsNone(transform_topic(topic))

    def test_profile_does_not_trigger_long_file_topic(self):
        title = "Show HN: Forexfin – Trading calculators, alerts and a journal in one place"
        summary = "I built my own stuff for position sizing. I previously used ChatGPT and Codex; the app imports a broker profile."
        topic = {"title": title, "eligible": True, "score": 70, "representative": {"title": title, "summary": summary}}
        self.assertIsNone(transform_topic(topic))

    def test_calendar_in_a_comment_does_not_trigger_family_topic(self):
        title = "My work gives me lots of Gemini credits every month; how should I experiment with them?"
        summary = "We are a small business. I am thinking in terms of a calendar schedule: Monday SEO audits, Tuesday email marketing, Wednesday security review."
        topic = {"title": title, "eligible": True, "score": 70, "representative": {"title": title, "summary": summary}}
        self.assertIsNone(transform_topic(topic))


if __name__ == "__main__":
    unittest.main()
