import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from zhuque_gate import evaluate
from acceptance import layout,cohort
class AcceptanceTests(unittest.TestCase):
    def feedback(self):
        return dict(status='success',unit='fraction',human_ratio=.7,ai_ratio=.3,suspected_ai_ratio=0,article_sha256='abc',scope='full_markdown_utf8',checked_at='2026-09-22T12:00:00+08:00',source='manual_report',evidence='test fixture')
    def test_target_does_not_impose_extra_threshold(self):
        self.assertTrue(evaluate(self.feedback(),expected_hash='abc')['pass'])
    def test_stale_and_failed_rejected(self):
        f=self.feedback(); self.assertFalse(evaluate(f,expected_hash='changed')['pass'])
        f['status']='error'; self.assertFalse(evaluate(f)['pass'])
    def test_bad_ratios_rejected(self):
        for value in [None,float('nan'),True,70]:
            f=self.feedback(); f['human_ratio']=value
            self.assertFalse(evaluate(f)['pass'])
    def test_percentage_explicit(self):
        f=self.feedback(); f.update(unit='percent',human_ratio=70,ai_ratio=30)
        self.assertTrue(evaluate(f)['pass'])
    def test_layout_added_summary_rejected(self):
        self.assertTrue(layout('# 标题\n\n正文','<section>标题<p>正文</p></section>')['passed'])
        self.assertFalse(layout('# 标题\n\n正文','<section>标题摘要<p>正文</p></section>')['passed'])
    def test_layout_link_change_rejected(self):
        self.assertFalse(layout('[来源](https://a.example)','<a href="https://b.example">来源</a>')['passed'])
    def test_pending_counts_in_denominator(self):
        d={'articles':[{'article_id':'a','attempts':[dict(round=0,human_ratio=.8,article_sha256='x',source='manual_report',evidence='fixture',editorial_passed=True)]},{'article_id':'b','attempts':[]}]}
        result=cohort(d); self.assertEqual(result['first_draft_pass_rate'],.5); self.assertEqual(result['pending'],1)
