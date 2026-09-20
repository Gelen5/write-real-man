# write-real-man

面向 **AI 技术分享赛道** 的研究驱动写作 Skill。

它不是一个“万能去 AI Prompt”，而是一条可执行工作流：

> 资料核验 → 文章结构 → 技术写作 → 活人感编辑 → 本地预检 → 事实保护 → 朱雀分段检测（可选）→ 高风险段落局部重写 → 再验证

## 目标

- 写教程、测评、AI 新闻分析、案例复盘、行业观点
- 避免“报告腔 / 模板腔 / 总结腔”
- 不编造用户体验、数据、来源或技术细节
- 保护代码、命令、模型名、版本号、URL、数字
- 支持腾讯朱雀官方 `zhuque-text` 接口作为质量反馈信号
- 只修改真正需要修改的段落，避免全文反复重写

> 重要：任何检测器都会更新，本项目不承诺“永久 100% 通过”。应以当次真实检测结果作为验收依据。

## 目录

```text
write-real-man/
├── SKILL.md
├── README.md
├── config.example.json
├── references/
├── templates/
├── scripts/
├── tests/
└── examples/
```

## 快速使用

把整个目录放到支持 Agent Skills 的工具中，然后直接提出 AI 技术写作需求，例如：

```text
基于 OpenAI 官方资料和我提供的使用记录，写一篇 1800 字公众号文章：
“我用 Codex 做了一个真实项目后，发现最值钱的不是写代码”
文章类型：case-study
受众：会用 ChatGPT、但没用过 coding agent 的普通用户
要求：不编造体验，保留所有技术名词和数据，最后执行本地 lint；如果配置了朱雀，再做分段检测和局部修改。
```

## 一键预检

```bash
python scripts/preflight.py article.md
```

如果有原稿/事实底稿：

```bash
python scripts/preflight.py article.md --original original.md
```

如果已配置朱雀 API Key：

```bash
python scripts/preflight.py article.md --original original.md --zhuque
```

报告默认写入 `.write-real-man/`。

## 本地诊断

纯 Python 标准库，不要求额外依赖：

```bash
python scripts/article_lint.py article.md
```

输出 JSON：

```bash
python scripts/article_lint.py article.md --json-out lint.json
```

## 使用分段检测结果继续改稿

如果用户提供了朱雀截图、段落标签或一版已确认通过的文本，先保留已被
确认的段落，再比较强弱段落在内容功能、具体细节、节奏、转场和结尾上的
差异。不要只换近义词或堆入口语表达。

详细方法见 `references/validated-human-style.md`。其中记录了一次五轮
WorkBuddy 教程迭代：前四轮的具体失败模式，以及第五轮由用户确认通过后
提取出的可复用写作逻辑。该案例用于指导比较，不代表固定检测通过模板。

## 事实/技术字面量保护

```bash
python scripts/integrity_check.py original.md revised.md
```

它会检查改写后是否意外删除：

- URL
- Markdown 链接地址
- 代码块 / 行内代码
- 版本号
- 数字与常见单位
- CLI 参数、环境变量、API 路径等技术字面量

## 朱雀官方 API

腾讯 EdgeOne Makers 提供 `zhuque-text` 文本检测接口。建议使用官方 API，而不是依赖网页自动化。

设置 API Key：

```bash
export ZHUQUE_API_KEY="your-key"
```

Windows PowerShell：

```powershell
$env:ZHUQUE_API_KEY="your-key"
```

检测：

```bash
python scripts/zhuque_client.py --file article.md --is-merge false
```

默认端点：

```text
https://ai-gateway.edgeone.link/v1/providers/zhuque-text/classify
```

也可以自定义：

```bash
export ZHUQUE_ENDPOINT="https://your-gateway-domain/v1/providers/zhuque-text/classify"
```

### 内部 Gate（可选）

朱雀官方没有定义一个通用的“过/不过”阈值。本项目的 gate 只是你自己的验收规则：

```bash
python scripts/zhuque_gate.py zhuque.json \
  --min-human 0.70 \
  --max-ai 0.15 \
  --max-suspected 0.25
```

不要把内部阈值描述成腾讯官方标准。

## 构建局部重写任务

```bash
python scripts/build_rewrite_packet.py \
  --article article.md \
  --lint lint.json \
  --zhuque zhuque.json \
  --out rewrite-packet.json
```

Skill 根据 packet 只重写被标记的段落。

## 测试

```bash
python -m unittest discover -s tests -v
```

## 设计原则

1. **先材料，后文风**：没材料就不靠套话补长度。
2. **先正确，后检测**：任何 detector 反馈都不能覆盖事实。
3. **生成时去模板化**：不要先写一篇标准 AI 稿，再疯狂“洗稿”。
4. **局部迭代**：只改有问题的段落。
5. **真实作者感来自取舍和判断**，不是错别字。
6. **检测器是回归测试，不是作者。**

## 参考与独立实现

项目架构受公开的 research-first writing、human-writing、technical-writing 和 Zhuque tooling 思路启发，但脚本与规则均为本仓库独立实现。见 `THIRD_PARTY_NOTES.md`。
