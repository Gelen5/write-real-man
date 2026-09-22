"""Validate actual detector evidence; never infer a result from local prose."""
import argparse, json, math
from pathlib import Path
from datetime import datetime

def evaluate(data, min_human=0.70, max_ai=None, max_suspected=None, expected_hash=None):
    errors=[]
    if data.get("status") != "success": errors.append("detector did not succeed")
    unit=data.get("unit")
    if unit not in ("fraction","percent"): errors.append("explicit ratio unit required")
    values=[]
    for key in ("human_ratio","ai_ratio","suspected_ai_ratio"):
        value=data.get(key)
        if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value):
            errors.append("invalid or missing "+key); values.append(0); continue
        value=value/100 if unit=="percent" else value
        if not 0<=value<=1: errors.append("out of range "+key)
        values.append(value)
    if abs(sum(values)-1)>0.015: errors.append("ratios do not sum to one")
    if expected_hash is not None and data.get("article_sha256")!=expected_hash: errors.append("draft hash mismatch")
    if expected_hash is not None:
        if data.get("scope")!="full_markdown_utf8": errors.append("scope mismatch")
        if data.get("source") not in ("manual_report","manual_screenshot","api"): errors.append("source required")
        if not data.get("evidence"): errors.append("evidence reference required")
        try: datetime.fromisoformat(data["checked_at"].replace("Z","+00:00"))
        except (KeyError,ValueError,TypeError,AttributeError): errors.append("valid checked_at required")
    passed=not errors and values[0]>=min_human
    if max_ai is not None: passed=passed and values[1]<=max_ai
    if max_suspected is not None: passed=passed and values[2]<=max_suspected
    return {"pass":passed,"status":"invalid_evidence" if errors else "passed" if passed else "below_target","human_ratio":values[0] if not errors else None,"errors":errors,"target":min_human,"source":data.get("source"),"note":"Project threshold for this exact draft, not a guarantee or an official pass standard."}

def main():
    p=argparse.ArgumentParser(); p.add_argument("result"); p.add_argument("--article",required=True); p.add_argument("--min-human",type=float,default=.7); p.add_argument("--json-out")
    a=p.parse_args()
    from acceptance import fingerprint
    report=evaluate(json.loads(Path(a.result).read_text(encoding="utf-8")),a.min_human,expected_hash=fingerprint(Path(a.article)))
    payload=json.dumps(report,ensure_ascii=False,indent=2); print(payload)
    if a.json_out: Path(a.json_out).write_text(payload,encoding="utf-8")
    return 0 if report["pass"] else 1
if __name__=="__main__": raise SystemExit(main())
