"""Offline version locking, layout comparison and consecutive-cohort reporting."""
import argparse, hashlib, json, re
from pathlib import Path
from html.parser import HTMLParser

def fingerprint(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def plain(md):
    md=re.sub(r"\[([^\]]+)\]\(([^)]+)\)",r"\1",md)
    md=re.sub(r"(?m)^\s*(?:#{1,6} |[-*] |\d+\. |>[ ]?)","",md)
    md=md.replace("**","").replace("`","")
    return re.sub(r"\s+","",md)
class Reader(HTMLParser):
    def __init__(self): super().__init__(); self.text=[]; self.links=[]
    def handle_data(self,data): self.text.append(data)
    def handle_starttag(self,tag,attrs):
        if tag=='a': self.links.append(dict(attrs).get('href'))
def layout(md,html):
    reader=Reader(); reader.feed(html)
    actual=plain(''.join(reader.text))
    expected=plain(md)
    links=re.findall(r"\[[^\]]+\]\(([^)]+)\)",md)
    return {"passed":expected==actual and links==reader.links,"text_equal":expected==actual,"links_equal":links==reader.links}
def cohort(data):
    entries=data['articles']; ids=[x['article_id'] for x in entries]
    if len(ids)!=len(set(ids)): raise ValueError('duplicate article IDs')
    first=within=complete=0
    for entry in entries:
        attempts=entry.get('attempts',[])
        valid=[x for x in attempts if x.get('evidence') and x.get('article_sha256') and x.get('source') and isinstance(x.get('human_ratio'),(int,float)) and 0<=x['human_ratio']<=1 and x.get('round') in (0,1,2,3)]
        complete+=bool(valid)
        first+=any(x['round']==0 and x['human_ratio']>=.7 and x.get('editorial_passed') is True for x in valid)
        within+=any(x['human_ratio']>=.7 and x.get('editorial_passed') is True for x in valid)
    n=len(entries)
    return {"registered":n,"measured_articles":complete,"pending":n-complete,"first_draft_pass_rate":first/n if n else None,"within_three_revisions_pass_rate":within/n if n else None,"cohort_complete":n>=20 and complete==n,"note":"Descriptive user-reported batch evidence, not a future guarantee."}
def main():
    p=argparse.ArgumentParser(); p.add_argument('action',choices=['prepare','layout','cohort']); p.add_argument('input'); p.add_argument('output',nargs='?'); a=p.parse_args(); src=Path(a.input)
    if a.action=='prepare':
        out=Path(a.output); out.mkdir(parents=True,exist_ok=True); (out/'detection.txt').write_bytes(src.read_bytes())
        report={'article_sha256':fingerprint(src),'scope':'full_markdown_utf8','status':'pending_detection'}
        (out/'manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    elif a.action=='layout': report=layout(src.read_text(encoding='utf-8'),Path(a.output).read_text(encoding='utf-8'))
    else: report=cohort(json.loads(src.read_text(encoding='utf-8')))
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if report.get('passed') is False else 0
if __name__=='__main__': raise SystemExit(main())
