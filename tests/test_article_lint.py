import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from article_lint import analyze_text
class LintTests(unittest.TestCase):
    def test_urls_do_not_supply_numbers(self):
        result=analyze_text('报道 https://example.com/20260922/12345')
        self.assertEqual(result['industry_observation']['numeric_anchors'],0)
        self.assertNotIn('score',result)
    def test_repeated_source_is_one(self):
        self.assertEqual(analyze_text('https://example.com/a https://example.com/a')['stats']['direct_source_count'],1)
    def test_no_keyword_handoff_gate(self):
        codes=[x['code'] for x in analyze_text('具体订单仍在等待复核。')['findings']]
        self.assertNotIn('missing_handoffs',codes)
