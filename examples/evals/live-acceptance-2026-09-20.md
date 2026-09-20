# v0.3.0 实时验收记录

**验收日期：2026-09-20（UTC）；默认窗口 72 小时，合格选题不足时自动扩展到 7 天。**

## 验收结果

| 场景 | 输入 | 原始记录数 | 7 天后合格趋势 | 返回的常青题 | 结果 |
| --- | --- | ---: | ---: | ---: | --- |
| A | AI 日常 | 300 | 0 | 10 | 无误报；显示 10 条 evergreen |
| B | WorkBuddy | 118 | 0 | 7 | 无误报；显示 7 条 evergreen |
| C | ChatGPT | 122 | 0 | 7 | 无误报；显示 7 条 evergreen |

A/B/C 都触发了 72 小时→7 天回退。没有用常青题填充实时趋势数量。每轮原始记录数是两个窗口的采集总和，窗口间可能包含重复项，不等于独立内容数。

## 各平台最新窗口状态（7 天）

`ok` 表示接口返回正常，不保证有匹配文章；数字是窗口过滤后的记录数。`partial` 表示官方源中的部分 feed 超时。

| 来源 | A：AI 日常 | B：WorkBuddy | C：ChatGPT |
| --- | --- | --- | --- |
| 小红书 | ok · 1 | ok · 8 | ok · 0 |
| 知乎 | ok · 20 | ok · 10 | ok · 10 |
| 微博 | unavailable · 0 | unavailable · 0 | unavailable · 0 |
| 抖音 | unavailable · 0 | ok · 10 | ok · 10 |
| B站 | ok · 20 | ok · 10 | ok · 10 |
| 微信公众号文章搜索 | unavailable · 0 | unavailable · 0 | ok · 0 |
| 今日头条 | ok · 0 | ok · 0 | ok · 0 |
| 掘金 | ok · 20 | ok · 0 | ok · 0 |
| 36氪 | unavailable · 0 | unavailable · 0 | unavailable · 0 |
| Reddit | ok · 20 | ok · 10 | ok · 10 |
| X | ok · 20 | ok · 10 | ok · 10 |
| GitHub | ok · 19 | unavailable · 0（超时） | ok · 10 |
| Hacker News | ok · 5 | ok · 0 | ok · 10 |
| Product Hunt | unavailable · 0（缺 API token） | unavailable · 0（缺 API token） | unavailable · 0（缺 API token） |
| 官方源 | partial · 10（部分 feed 超时） | partial · 0（部分 feed 超时） | partial · 3（部分 feed 超时） |

接入的国内公开来源包括小红书、知乎、微博、抖音、B站、微信公众号文章搜索、今日头条、掘金和 36 氪。本轮微博三组查询均失败；微信、36 氪在部分查询中失败。视频号没有可用的公开只读搜索 Adapter；Product Hunt 需要 API token。适配器不绕过登录和验证码。

## A 轮补充选题（常青，不是当前热点）

- 手头有几条工作记录，怎么让 AI 帮忙整理周报（普通上班族）
- 收到几十页 PDF，怎样让 AI 按问题找重点（需要处理长文件的人）
- 简历没思路时，先让 AI 对照经历和岗位要求（普通求职者）
- 旅行计划别排太满，让 AI 按真实限制做减法（正在安排出行的人）
- 没选题时，先给 AI 一段真实素材（自媒体创作者）
- 家长群通知太长，让 AI 先列日期、物品和待确认项（家长）
- 会议记录很零散，让 AI 先整理决定和待办（经常参加会议的上班族）
- 冰箱里食材有限时，让 AI 按现有东西列几种晚饭思路（需要安排家常饭菜的人）
- 收到退换货说明时，让 AI 把期限和需要准备的材料列出来（经常网购的普通消费者）
- 家电说明书太长时，让 AI 按你的问题找相关步骤（需要查操作说明的人）

## B 轮补充选题（WorkBuddy 常青题）

1. WorkBuddy 刚打开，先让它整理一小段工作记录
2. 周报只有几条零散记录时，怎么让 WorkBuddy 整理又不夸大进度
3. WorkBuddy 里已有资料太多，怎样选一份作为当前任务的参考
4. 客户的问题还没解决，怎么让 WorkBuddy 先整理成待确认清单
5. 不会做海报时，怎样用 WorkBuddy 起一版可修改的草稿
6. 会议记录太乱时，怎样让 WorkBuddy 分开列决定和待办
7. 让 WorkBuddy 处理文件前，先检查它有没有把待确认写成已完成

## C 轮补充选题（ChatGPT 常青题）

1. 收到几十页 PDF，怎样让 ChatGPT 按问题找重点
2. 简历没思路时，先让 ChatGPT 对照经历和岗位要求
3. 家庭通知太多时，怎样让 ChatGPT 列出日期和待确认项
4. 旅行计划别排太满，让 ChatGPT 按真实限制做减法
5. 每周都要重复整理的事，先试着让 ChatGPT 汇总成清单
6. 没选题时，先给 ChatGPT 一段真实素材
7. ChatGPT 给错日期时，怎么按原文逐项校正

## 文章样稿

样稿：[examples/golden/06-family-notices-ai.md](../golden/06-family-notices-ai.md)，共 1,517 字符。练习通知和 AI 输出均明确标成虚构，避免伪装成亲身经历或实际测试。

资料核实：Google Labs 于 2026-09-17 介绍 CC 家庭协作实验项目，当前面向美国 18 岁以上、使用个人 Google 账号的人；Reddit 于 2026-09-14 的一条 r/ChatGPT 帖子中，有用户分享用定时任务整理学校邮件与家庭日历的做法。这是单个社区帖里的个人描述，不代表普遍用户情况。样稿与实时榜单分开；当前管线 C 轮没有把该场景列为合格实时选题。

- [Google Labs：The new CC, an AI agent built for families](https://blog.google/innovation-and-ai/models-and-research/google-labs/cc-expanding-to-groups/)
- [Reddit：What are people actually using ChatGPT scheduled tasks for?](https://www.reddit.com/r/ChatGPT/comments/1wg0edy/what_are_people_actually_using_chatgpt_scheduled/)

样稿 lint：总分 100，普通读者分 97，趋势到人对齐 1.0，未报告问题。Lint 是本地可解释的写作质量规则，不是 AI 检测器。

## 迭代记录

- 查询摘要里的 `profile` 曾触发 `file` 选题；英文关键词改为整词匹配，文件类场景需在标题中明确出现。
- 一条小企业帖子正文提到 `calendar`，曾误转成家长通知；现在由标题中的场景词触发转换，日历类选题使用通用日程角度。
- 同一条内容在 72 小时与 7 天回采不会增加重复证据；OpenCLI 以退出码 0 返回 `ok=false` 时，会记录为来源失败。
- 回归覆盖 23 项单元测试与固定样本 eval。

## 后续可改进

1. 各平台发布时间和互动量含义不一致，需继续按平台校验字段并标注时间精度。
2. 趋势词与人群场景映射仍以规则为主；继续用真实误报和漏报补回归样本，避免为了多出选题而放松门槛。
3. 微博、微信等来源取决于本机 OpenCLI Adapter；视频号没有公开只读适配器，Product Hunt 缺 token 时明确降级。
4. A/B/C 实时验收最终都未凑出 10 条合格趋势，A 轮另给 10 条 evergreen。提高召回应优先增加带明确日期的国内来源与跨平台聚类，不应降低普通人相关性门槛。
