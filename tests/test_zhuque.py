import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from zhuque_client import normalize_response  # noqa: E402
from zhuque_gate import evaluate  # noqa: E402


class ZhuqueTests(unittest.TestCase):
    def test_normalize_response(self):
        raw = {
            "status": "success",
            "labels_ratio": {"0": 0.8, "1": 0.1, "2": 0.1},
            "segment_labels": [
                {"text": "a", "label": 0, "conf": 0.1},
                {"text": "b", "label": 2, "conf": 0.7},
            ],
        }
        result = normalize_response(raw)
        self.assertTrue(result["ok"])
        self.assertAlmostEqual(result["risk_ratio"], 0.2)
        self.assertFalse(result["segments"][0]["risky"])
        self.assertTrue(result["segments"][1]["risky"])

    def test_internal_gate(self):
        result = {"human_ratio": 0.82, "ai_ratio": 0.08, "suspected_ai_ratio": 0.10}
        gate = evaluate(result, 0.7, 0.15, 0.25)
        self.assertTrue(gate["pass"])


if __name__ == "__main__":
    unittest.main()
