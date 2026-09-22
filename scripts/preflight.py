"""Offline acceptance: semantic review, actual detection, optional layout."""
import argparse,json
from pathlib import Path
from article_lint import analyze_text
from acceptance import fingerprint,layout
from zhuque_gate import evaluate

def inspect(article,pack=None,review=None,feedback=None,html=None):
    path=Path(article); text=path.read_text(encoding='utf-8'); digest=fingerprint(path)
    lint=analyze_text(text,pack)
    reviewed=bool(review and review.get('article_sha256')==digest and all(review.get(k,{}).get('status')=='passed' and review[k].get('reviewer') and review[k].get('notes') for k in ('facts','readability')))
    detection=evaluate(feedback,expected_hash=digest) if feedback is not None else {'pass':False,'status':'pending_detection'}
    layout_result=layout(text,html) if html is not None else None
    mechanical=not any(x['severity']=='high' for x in lint['findings']) and bool(pack)
    passed=reviewed and mechanical and detection['pass'] and (layout_result is None or layout_result['passed'])
    return {'accepted':bool(passed),'article_sha256':digest,'editorial_status':'passed' if reviewed and mechanical else 'pending_review','detector':detection,'layout':layout_result,'lint':lint}
def main():
    p=argparse.ArgumentParser(); p.add_argument('article'); p.add_argument('--research-pack'); p.add_argument('--review'); p.add_argument('--feedback'); p.add_argument('--html'); p.add_argument('--out-dir',default='.write-real-man'); a=p.parse_args()
    def read(path): return json.loads(Path(path).read_text(encoding='utf-8')) if path else None
    try: report=inspect(a.article,a.research_pack,read(a.review),read(a.feedback),Path(a.html).read_text(encoding='utf-8') if a.html else None)
    except (ValueError,TypeError,KeyError,OSError) as exc: report={'accepted':False,'status':'invalid_evidence','error':str(exc)}
    out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True); payload=json.dumps(report,ensure_ascii=False,indent=2); (out/'summary.json').write_text(payload,encoding='utf-8'); print(payload)
    return 0 if report['accepted'] else 1
if __name__=='__main__': raise SystemExit(main())
