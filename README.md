# v1.2.0 验收变更

当前唯一模式：AI 产业落地观察。人工特征 ≥70% 是逐稿实测目标，非稳定性保证。旧版 lint 分数和历史用法不再作为验收依据。当前命令和评审字段以 [验收流程](workflows/acceptance.md) 为准；preflight 默认离线接收手工检测记录，无检测或版本不匹配均不通过。历史教程模板仅作归档参考。

# write-real-man

**v1.1.0 · AI 智能落地观察写作与公众号排版 Skill**

默认参考已验收的环卫工单叙事案例，让对象流转带动论证。案例分析见 `references/validated-sanitation-case.md`。用户反馈该稿朱雀100%人工特征，属于单次用户报告，不能作为其他稿件通过保证。

公众号成稿后按 `workflows/gzh-layout.md` 调用外部 `gzh-design` 自动选择主题，保留定稿文字，生成正文HTML和复制预览。依赖来源：https://github.com/isjiamu/gzh-design-skill 。当前本机已安装；其他环境需另装此依赖。

从当前公开证据里找到一个真实事件，把政府通报、媒体报道、技术资料、企业案例和从业者信号放到同一条时间线，再把多个应用环节连接成一条可审查的技术或产业链。

## 只保留一个模式

```text
事件锚点 → 时间轴 → 关键数据 → 应用分层 → 环节交接
→ 作者判断 → 产业机会 → 现实卡点 → 人的落点
```

本版本不再路由到普通人教程、提示词合集、产品功能介绍或通用 AI 新闻摘要。

## 证据边界

每条关键判断属于一种状态：

- `verified_fact`：来源直接支持的事实；
- `reported_claim`：具名机构或人物的陈述；
- `author_inference`：作者根据事实作出的推断；
- `proposal`：作者提出的连接或产业设想；
- `unknown`：公开材料没有说明。

“A 已存在”和“B 已存在”不能直接写成“A、B 已经打通”。研究包必须记录来源、日期、支持范围和限制。

## 核心文件

- `SKILL.md`：唯一入口与完整工作流。
- `workflows/industry-research.md`：多源检索顺序。
- `workflows/industry-synthesis.md`：链路交接和三种链路状态。
- `workflows/industry-write.md`：成稿逻辑。
- `references/industry-evidence.md`：来源职责和证据等级。
- `references/industry-topic-selection.md`：事件强度、证据、链路、利害和认知差评分。
- `references/chain-synthesis.md`：产业链、机会与反事实检查。
- `references/industry-human-style.md`：基于事实判断的真人表达。
- `templates/industry-research-pack.md`：JSON 研究包。
- `templates/industry-observation.md`：文章骨架。

## 本地 lint

```powershell
python scripts/article_lint.py article.md --research-pack research-pack.json
python scripts/integrity_check.py source-notes.md article.md
python scripts/validate_skill.py
```

文章 lint 检查事件时间、数字锚点、直接来源、系统交接、作者判断、设想边界、未知项、现实卡点和人的落点。它是可解释的编辑检查，不是事实核验器，也不是 AI 检测器。

朱雀仍是可选的末端信号。任何结果只对应那一次提交的具体文本，不能承诺永久通过或百分百人工特征。
