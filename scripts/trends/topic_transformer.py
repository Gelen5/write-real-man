#!/usr/bin/env python3
"""Turn a ranked signal into a person/problem/action/result, or reject it."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def _has_cue(text: str, token: str) -> bool:
    """Match English cues as words/phrases so e.g. `profile` is not `file`."""
    if any(char.isascii() and char.isalpha() for char in token):
        phrase = re.escape(token).replace(r"\ ", r"\s+")
        return re.search(rf"(?<![a-z0-9]){phrase}(?![a-z0-9])", text, re.IGNORECASE) is not None
    return token in text


def transform_topic(topic: dict[str, Any], audience: str = "普通上班族和普通 AI 用户") -> dict[str, Any] | None:
    rep = topic.get("representative") or {}
    title = str(rep.get("title") or topic.get("topic") or "")
    text = (title + " " + str(rep.get("summary") or "")).casefold()
    cues = [
        (("knowledge base", "资料库", "参考文档", "知识库"), "需要反复整理资料的上班族", "每次开新任务都要重新找文件、补背景", "把一份现有资料作为参考，让 AI 先归纳待确认点", "一份带出处线索的任务草稿", "beginner-guide", "WorkBuddy 里资料太多？先把相关文件加进任务"),
        (("创意设计", "海报", "品牌设计", "poster"), "需要做简单配图或海报的普通创作者", "有想法却不熟悉设计工具", "先说清用途、主体、文字和尺寸，再检查生成结果", "一张还需核对文字的视觉草稿", "beginner-guide", "WorkBuddy 能做图以后，先拿一张简单活动海报练手"),
        (("视频生成", "短视频", "vlog", "分镜", "剪辑", "视频创作", "ai video"), "想做短视频但不熟悉剪辑的普通创作者", "脑子里有画面，拍起来却容易跑偏", "先让 AI 按现有素材列镜头顺序，再逐条检查", "一份能照着拍或修改的分镜清单", "scenario-tutorial", "短视频拍到一半容易跑偏？先让 AI 把镜头按顺序列出来"),
        (("workbuddy", "工作台", "入门", "界面"), "刚打开 WorkBuddy 的新手", "不知道第一件事该交给它做什么", "给它一小段现成材料，请它先整理成可检查的草稿", "一份能继续修改、没有补造事实的文件", "beginner-guide", "WorkBuddy 刚打开，先交给它整理一小份材料"),
        (("pdf", "file", "files", "文件", "文档", "合同"), "收到长文件的人", "文件太长，不知道先看哪几页", "让 AI 按问题提取重点，再回到原文核对", "一份可核对的重点清单", "scenario-tutorial", "长文件先别从第一页读起"),
        (("周报", "日报", "工作总结", "工作记录"), "需要交周报的上班族", "零散工作记录很难整理成进度", "让 AI 按已完成、待确认和下周安排归类", "一份没有夸大进度的周报草稿", "scenario-tutorial", "手头有几条工作记录时，先这样整理周报"),
        (("resume", "简历", "求职", "履历"), "正在找工作的普通求职者", "经历写得零散，不知道怎样对应岗位", "让 AI 对照真实经历和岗位要求找表达缺口", "一版保留事实、方便自己修改的简历草稿", "problem-solution", "简历没思路时，先让 AI 找出经历和岗位要求的对应处"),
        (("push back", "follow instructions", "follow more closely", "clarify what", "constraints", "改稿", "纠正", "没照办", "按要求修改"), "需要反复修改 AI 草稿的普通用户", "要求说了几遍，结果还是漏改或改偏", "指出具体句子、真实情况和必须保留的内容，再让 AI 局部修改", "一版待自己核对的修订稿", "problem-solution", "ChatGPT 写偏了，具体指出哪句话要改"),
        (("travel", "旅行", "旅游", "行程", "trip"), "正在安排出行的人", "景点、时间和交通混在一起不好取舍", "让 AI 按日期和限制排出可调整的行程", "一份标出交通与待确认事项的行程草稿", "scenario-tutorial", "旅行计划别先塞满景点，让 AI 按这些限制排一天"),
        (("meal", "做饭", "备餐", "食谱", "菜单", "meal plan"), "要安排一周饮食的家庭成员", "菜单、日程和买菜清单容易分开", "让 AI 按已有安排列一份可调整的菜单草稿", "一份要自己核对饮食限制的备餐清单", "use-case", "一周吃什么没想好时，让 AI 先按日程列个菜单草稿"),
        (("calendar", "日历", "日程安排"), "日程信息分散的普通用户", "时间、地点和待确认事项散在不同消息里", "让 AI 按日期整理事项，并标出冲突和未知项", "一份需要自己核对的日程清单", "problem-solution", "日程信息散在几条消息里，先让 AI 把时间列清楚"),
        (("school", "孩子", "家长群", "permission slip", "学校邮件", "school notice", "家长", "通知", "家庭协作"), "要同时记家务、日程或学校通知的家庭成员", "零碎通知容易漏掉时间和要准备的东西", "让 AI 把通知整理成日期、事项、待确认三栏", "一张需要自己核对的家庭待办清单", "use-case", "家长群消息太多时，先让 AI 挑出日期和要准备的东西"),
        (("image", "图片", "照片", "封面", "设计", "画图"), "需要做配图的普通创作者", "有想法却难把要求说清楚", "先让 AI 把用途、主体和尺寸整理成提示词", "一份能继续修改的配图需求", "beginner-guide", "想做一张配图却说不清要求，可以先补齐这几项"),
        (("content", "内容", "小红书", "公众号", "选题", "创作"), "需要持续发内容的小创作者", "有生活素材但一时想不到切口", "让 AI 从一段真实素材里列不同问题角度", "一组可以自己筛选的选题草稿", "use-case", "没选题时，先给 AI 一段真实素材，不要让它凭空想"),
        (("inbox triage", "email triage", "邮件分类", "inbox sorting", "收件箱", "长邮件"), "每天要处理很多邮件的上班族", "重要事项容易被促销和抄送消息淹没", "让 AI 按需回复、待办和仅供参考归类", "一份需要自己确认的邮件待办清单", "problem-solution", "邮件堆在一起时，先让 AI 标出需要回复的几封"),
        (("通知", "公告", "群消息", "announcement", "school", "家长", "孩子", "日程", "calendar", "家庭"), "常被通知和消息打断的人", "重要日期和需要回复的事项容易埋在长消息里", "让 AI 摘出日期、行动和未知项", "一份逐条回原文核对的行动清单", "problem-solution", "长通知读完就忘？让 AI 先圈出日期和要做的事"),
        (("schedule task", "scheduled task", "定时任务", "scheduled", "weekly task"), "经常重复查看通知、日程或清单的人", "固定重复的提醒和汇总总要重新做", "从低风险的定时摘要开始，检查来源和提醒时间", "一份能复查的周期摘要", "use-case", "每周都要重复整理的事，可以先试着交给 AI 汇总"),
    ]
    file_cues = {"pdf", "file", "files", "文件", "文档", "合同"}
    match = next((
        row for row in cues
        if any(_has_cue(title.casefold(), token) for token in row[0])
        and not (
            any(token in file_cues for token in row[0])
            and not any(_has_cue(title.casefold(), token) for token in row[0] if token in file_cues)
        )
    ), None)
    if any(_has_cue(text, token) for token in ("postdoc", "post doc", "fellowship", "professor", "研究职位")) and not any(_has_cue(text, token) for token in ("日程", "calendar", "family", "家长", "学校邮件")):
        return None
    if not match or not topic.get("eligible", False):
        return None
    _, person, problem, ai_action, result, content_type, headline = match
    sources = topic.get("sources") or []
    platforms = topic.get("platforms") or []
    return {
        "title": headline,
        "person": person,
        "audience": audience,
        "problem": problem,
        "ai_action": ai_action,
        "useful_result": result,
        "why_now": f"近期公开信号涉及：{title}。这是选题线索，不代表普遍用户需求。",
        "content_type": content_type,
        "technical_depth": 1,
        "classification": topic.get("classification", "trend"),
        "trend_types": topic.get("trend_types", []),
        "score": topic.get("score"),
        "score_dimensions": topic.get("dimensions", {}),
        "penalties": topic.get("penalties", []),
        "published_at": rep.get("published_at"),
        "freshness_score": topic.get("dimensions", {}).get("freshness"),
        "source_count": topic.get("source_count", len(topic.get("evidence", []))),
        "platforms": platforms,
        "platform_count": topic.get("platform_count", len(platforms)),
        "sources": sources,
        "evidence": topic.get("evidence", []),
        "risk": "按来源实际发布时间核对功能范围、地区和账号限制；演示输入需标注为示例。",
        "article_outline": ["摆出普通人的具体麻烦", "给一小段可复制的原始材料", "展示日常说法的提示词", "检查 AI 漏掉或误写的地方", "整理出能带走的结果"],
    }


def transform_topics(topics: list[dict[str, Any]], audience: str = "普通上班族和普通 AI 用户", limit: int = 10) -> list[dict[str, Any]]:
    output = []
    seen = set()
    for topic in topics:
        transformed = transform_topic(topic, audience)
        key = transformed["title"] if transformed else ""
        if transformed and key not in seen:
            seen.add(key)
            output.append(transformed)
        if len(output) >= limit:
            break
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--audience", default="普通上班族和普通 AI 用户")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--out")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    topics = payload if isinstance(payload, list) else payload.get("topics", [])
    output = json.dumps({"topics": transform_topics(topics, args.audience, args.limit)}, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
