#!/usr/bin/env python3
"""Editorial lint for AI industry observation articles; not an AI detector."""
from __future__ import annotations
import argparse, json, re, statistics
from pathlib import Path
from typing import Any

GENERIC=("随着人工智能技术的快速发展","在数字化浪潮下","赋能千行百业","未来可期","开启新的可能性","充分体现了","具有重要意义","降本增效")
FORMULAIC=("首先","其次","再次","最后","综上所述","总的来说","值得注意的是","与此同时")
EVIDENCE=("据","通报","公告","报告","数据显示","官方","研究","发布","来源")
INFERENCE=("我认为","在我看来","我的判断","由此可以推断","更准确地说")
PROPOSAL=("我的设想","如果把","可以尝试","值得考虑","下一步可以")
BOUNDARY=("尚不清楚","公开材料没有说明","仍待","并不意味着","不能证明","仅限","试点")
HANDOFF=("发送","回传","接入","交给","转交","触达","上报","下发","调度","收到","传给","进入下一")
HUMAN=("人","居民","员工","患者","司机","工人","村民","用户","负责人","值班","转移","决定","签字","审核")
BOTTLENECK=("误报","漏报","成本","责任","接口","数据","维护","信任","合规","卡点","瓶颈","限制","故障")
URL_RE=re.compile(r"https?://[^\s)>]+")
DATE_RE=re.compile(r"(?:20\d{2}[年./-]\d{1,2}(?:[月./-]\d{1,2}日?)?|\d{1,2}月\d{1,2}日)")
NUMBER_RE=re.compile(r"\d+(?:\.\d+)?(?:万|亿|%|％|天|小时|分钟|人|个|处|次|元|公里|立方米)?")
HEADING_RE=re.compile(r"^#{1,6}\s+(.+)$",re.M)

def _parts(text:str, paragraph:bool)->list[str]:
    pattern=r"\n\s*\n" if paragraph else r"(?<=[。！？!?；;])\s*"
    return [x.strip() for x in re.split(pattern,text) if x.strip() and (paragraph or not x.startswith("#"))]

def _cv(values:list[int])->float:
    return statistics.pstdev(values)/statistics.fmean(values) if len(values)>1 and statistics.fmean(values) else 0.0

def _hits(text:str,terms:tuple[str,...])->dict[str,int]:
    return {x:text.count(x) for x in terms if text.count(x)}

def _load_pack(path:str|None)->tuple[dict[str,Any]|None,list[str]]:
    if not path:return None,[]
    try: pack=json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:return None,[f"research pack unreadable: {exc}"]
    required=("topic","as_of_date","event_anchor","thesis","anchor_numbers","timeline","layers","claims","opportunities","bottlenecks","sources")
    errors=[f"research pack missing key: {k}" for k in required if k not in pack]
    states={"verified_fact","reported_claim","author_inference","proposal","unknown"}
    source_ids={x.get("id") for x in pack.get("sources",[]) if x.get("id")}
    for claim in pack.get("claims",[]):
        if claim.get("state") not in states:errors.append(f"claim {claim.get('id','?')} has invalid state")
        for sid in claim.get("source_ids",[]):
            if sid not in source_ids:errors.append(f"claim {claim.get('id','?')} references missing source {sid}")
        if claim.get("state") in {"verified_fact","reported_claim"} and not claim.get("source_ids"):errors.append(f"claim {claim.get('id','?')} lacks source_ids")
    return pack,errors

def analyze_text(text:str,research_pack:str|None=None,trend_linked:bool=False)->dict[str,Any]:
    paragraphs,sentences=_parts(text,True),_parts(text,False)
    sentence_cv=_cv([len(re.sub(r"\s+","",x)) for x in sentences]); paragraph_cv=_cv([len(re.sub(r"\s+","",x)) for x in paragraphs])
    generic,formulaic=_hits(text,GENERIC),_hits(text,FORMULAIC); pack,pack_errors=_load_pack(research_pack)
    headings=HEADING_RE.findall(text); urls=URL_RE.findall(text); findings=[]; score=100
    def add(code:str,severity:str,message:str,points:int)->None:
        nonlocal score; findings.append({"code":code,"severity":severity,"message":message}); score-=points
    if not DATE_RE.search(text):add("missing_event_time","high","正文没有可识别的事件日期或时间锚点。",14)
    if len(NUMBER_RE.findall(text))<3:add("weak_numeric_anchor","medium","少于三个具体数字，检查事件规模和关键数据是否落地。",8)
    if not urls:add("missing_direct_sources","high","没有直接来源链接。",18)
    if sum(text.count(x) for x in EVIDENCE)<3:add("thin_evidence_language","high","可归属的证据表达偏少。",14)
    if sum(text.count(x) for x in HANDOFF)<2:add("missing_handoffs","high","没有写清两个以上系统或角色之间的交接。",14)
    # Judgment is semantic; absence of a stock phrase cannot establish its absence.
    if not any(x in text for x in PROPOSAL):add("missing_proposal_boundary","medium","没有明确标出作者设想或提议。",8)
    if not any(x in text for x in BOUNDARY):add("missing_uncertainty_boundary","medium","没有写出公开证据的限制或未知项。",8)
    if sum(x in text for x in BOTTLENECK)<2:add("weak_bottlenecks","medium","现实卡点少于两类。",7)
    if not any(x in text for x in HUMAN):add("missing_human_endpoint","high","链路没有落到具体的人或人的决定。",12)
    # Continuous object-led prose needs no minimum heading count.
    if generic:add("generic_ai_phrases","high" if sum(generic.values())>1 else "medium",f"发现泛化表达：{generic}",min(16,6*sum(generic.values())))
    if sum(formulaic.values())>=5:add("formulaic_transitions","medium",f"模板连接词偏多：{formulaic}",8)
    if len(sentences)>=6 and sentence_cv<.30:add("uniform_sentence_rhythm","medium",f"句长变化偏低（CV={sentence_cv:.2f}）。",7)
    if len(paragraphs)>=5 and paragraph_cv<.22:add("uniform_paragraph_size","low",f"段落长度过于整齐（CV={paragraph_cv:.2f}）。",4)
    for error in pack_errors:add("research_pack_error","high",error,10)
    layer_count=len(pack.get("layers",[])) if pack else None; source_count=len(pack.get("sources",[])) if pack else None
    if pack and layer_count<3:add("research_pack_too_few_layers","high","研究包少于三个产业链层级。",14)
    if pack and source_count<3:add("research_pack_too_few_sources","high","研究包少于三个来源。",14)
    score=max(0,min(100,score))
    return {"score":score,"risk_level":"high" if score<65 else "medium" if score<82 else "low","stats":{"characters":len(text),"paragraphs":len(paragraphs),"sentences":len(sentences),"sentence_length_cv":round(sentence_cv,3),"paragraph_length_cv":round(paragraph_cv,3),"heading_count":len(headings),"direct_source_count":len(urls)},"industry_observation":{"event_time":bool(DATE_RE.search(text)),"numeric_anchors":len(NUMBER_RE.findall(text)),"evidence_markers":sum(text.count(x) for x in EVIDENCE),"handoff_markers":sum(text.count(x) for x in HANDOFF),"author_judgment":any(x in text for x in INFERENCE),"proposal_boundary":any(x in text for x in PROPOSAL),"uncertainty_boundary":any(x in text for x in BOUNDARY),"human_endpoint":any(x in text for x in HUMAN),"research_pack_layers":layer_count,"research_pack_sources":source_count},"signals":{"generic_phrase_hits":generic,"formulaic_transition_hits":formulaic},"findings":findings,"note":"Deterministic editorial heuristic, not an AI detector or factual verifier. --trend-linked is deprecated."}

def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("file"); parser.add_argument("--research-pack"); parser.add_argument("--json-out"); parser.add_argument("--trend-linked",action="store_true",help=argparse.SUPPRESS); args=parser.parse_args()
    report=analyze_text(Path(args.file).read_text(encoding="utf-8"),args.research_pack,args.trend_linked); payload=json.dumps(report,ensure_ascii=False,indent=2); print(payload)
    if args.json_out:
        out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(payload+"\n",encoding="utf-8")
    return 0
if __name__=="__main__":raise SystemExit(main())
