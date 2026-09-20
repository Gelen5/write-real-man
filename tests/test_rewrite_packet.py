import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_rewrite_packet import build_packet  # noqa: E402


class RewritePacketTests(unittest.TestCase):
    def test_merges_lint_and_zhuque(self):
        article = "第一段是事实。\n\n第二段比较模板化，需要修改。\n\n第三段保持不动。"
        lint = {"paragraph_findings": [{"paragraph": 2, "reasons": ["模板化"]}]}
        zhuque = {"segments": [{"text": "第二段比较模板化，需要修改。", "label": 2, "risky": True, "conf": 0.8}]}
        packet = build_packet(article, lint, zhuque)
        self.assertEqual(packet["target_count"], 1)
        self.assertEqual(packet["targets"][0]["paragraph"], 2)
        self.assertIn("local_lint", packet["targets"][0]["signals"])
        self.assertIn("zhuque", packet["targets"][0]["signals"])


if __name__ == "__main__":
    unittest.main()
