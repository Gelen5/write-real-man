import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from article_lint import analyze_text  # noqa: E402


class ArticleLintTests(unittest.TestCase):
    def test_formulaic_text_is_flagged(self):
        text = (
            "随着人工智能技术的快速发展，我们需要关注新的工具。首先，它能提升效率。其次，它能提升体验。最后，它能创造价值。\n\n"
            "总的来说，这项技术具有非常重要的价值。我们应该积极拥抱变化，充分发挥它的能力，进一步提升工作效率。"
        )
        report = analyze_text(text)
        codes = {x["code"] for x in report["findings"]}
        self.assertIn("generic_ai_phrases", codes)
        self.assertLess(report["score"], 90)

    def test_specific_text_scores_better(self):
        text = (
            "我把同一段 620 行的接口测试交给两个 coding agent。一个直接改了 14 个文件，另一个先问我是否允许调整数据库迁移。\n\n"
            "真正影响结果的不是生成速度，而是它会不会在动代码前确认边界。这个差异会直接决定你后面要花多少时间 review。\n\n"
            "如果仓库没有测试，我宁愿它慢一点，也不希望它一次改完再让我猜哪里出了问题。"
        )
        report = analyze_text(text)
        self.assertGreaterEqual(report["score"], 80)

    def test_ordinary_reader_metrics_are_reported(self):
        text = "家长群里有四条通知。比如周一带美术袋，周三交签字回执。把通知贴给 AI，问：帮我列出日期和待确认项，别猜。最后保存成一张清单。"
        report = analyze_text(text, trend_linked=True)
        metrics = report["ordinary_reader_metrics"]
        self.assertGreaterEqual(metrics["ordinary_reader_score"], 70)
        self.assertTrue(metrics["scenario_presence"])
        self.assertTrue(metrics["actionability"])
        self.assertTrue(metrics["concrete_material"])
        self.assertIsNotNone(metrics["trend_to_human_alignment"])


if __name__ == "__main__":
    unittest.main()
