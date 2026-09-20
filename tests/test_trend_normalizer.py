import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "trends"))
from normalizer import normalize_item


class TrendNormalizerTests(unittest.TestCase):
    def test_wechat_search_tokens_do_not_make_same_article_look_new(self):
        first = normalize_item({"title": "AI 日常使用小技巧", "url": "https://weixin.sogou.com/link?url=article-key&type=2&query=AI&token=first"})
        second = normalize_item({"title": "AI 日常使用小技巧", "url": "https://weixin.sogou.com/link?url=article-key&type=2&query=WorkBuddy&token=second"})
        self.assertEqual(first["url"], second["url"])

    def test_relative_chinese_published_date_is_normalized(self):
        item = normalize_item({"title": "三天前发布的文章", "published_at": "3天前"})
        self.assertIsNotNone(item["published_at"])
        self.assertEqual(item["published_at"][-1], "Z")


if __name__ == "__main__":
    unittest.main()
