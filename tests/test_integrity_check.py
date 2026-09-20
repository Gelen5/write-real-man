import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from integrity_check import compare_texts  # noqa: E402


class IntegrityTests(unittest.TestCase):
    def test_detects_removed_url_and_version(self):
        original = "使用 GPT-5.6，文档是 https://example.com/docs ，版本 v1.2.3。"
        revised = "使用这个模型，文档之后再补。"
        report = compare_texts(original, revised)
        self.assertFalse(report["ok"])
        self.assertIn("urls", report["missing"])
        self.assertIn("versions", report["missing"])

    def test_preserved_literals_pass(self):
        original = "运行 `codex --full-auto`，访问 https://example.com/api 。"
        revised = "先运行 `codex --full-auto`。接口仍然是 https://example.com/api ，别改地址。"
        report = compare_texts(original, revised)
        self.assertTrue(report["ok"])


if __name__ == "__main__":
    unittest.main()
