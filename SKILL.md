---
name: write-real-man
description: Research and write Chinese AI industry landing-observation articles from current public evidence. Use for AI industry topics, application cases, government or media evidence, multi-layer technical or business chains, industry opportunities, constraints, and readable author judgment. Produces one evidence-led mode only; it does not route to ordinary-person tutorials.
metadata:
  version: 1.2.0
---

# Write Real Man

Write one kind of article: **AI 智能落地观察**.

`事件锚点 → 时间轴 → 关键数据 → 多个真实应用 → 技术分层 → 环节衔接 → 作者判断 → 产业机会 → 现实卡点 → 人的落点`

## Boundaries

- Search current public sources. Do not invent recent cases from memory.
- Keep `verified_fact`, `reported_claim`, `author_inference`, `proposal`, and `unknown` separate.
- A source proves only the claim it supports. Several reposts of one release are one evidence origin.
- Never invent personal experience, interviews, adoption, revenue, effectiveness, quotes, or consensus.
- Do not promise a Zhuque score. Feedback applies only to the exact tested draft and run.
- Do not switch into beginner tutorials, prompt collections, product tours, or generic AI news summaries.

## Mandatory acceptance contract

Read `workflows/acceptance.md` before drafting. Local lint is not a human-writing score. Every delivery states editorial status and detector status separately. An untested draft is pending detection, never accepted. Preserve one industry-observation mode. Legacy tutorial resources are historical only.

## Workflow

### 1. Discover a chainable event

Read `workflows/industry-research.md`, `references/industry-evidence.md`, and `references/industry-topic-selection.md`.

Search government sites, regulators, official documents, original papers, credible media, company cases, public reports, and attributed practitioner or platform discussions. Prefer an event with a date, place, action, measurable stake, and human consequence.

If the user asks for topics, use `templates/industry-topic-list.md` and return a shortlist. Otherwise select the strongest supported event and continue. A strong topic has one authoritative anchor, at least three connectable stages, a supportable non-obvious thesis, and consequences a reader can picture.

### 2. Build the evidence pack

Use `templates/industry-research-pack.md`. Record URL, publisher, date, source type, exact supported claim, and limitations. Build an event timeline, at most three anchor numbers, three to six application layers, their handoffs and failure modes, opportunities, bottlenecks, and an explicit chain hypothesis.

The chain hypothesis is the author's synthesis. Label it. Do not turn “A exists” and “B exists” into “A and B are already integrated.”

### 3. Stress-test the chain

Read `workflows/industry-synthesis.md` and `references/chain-synthesis.md`.

Reject or narrow cases that merely share an AI label. For every adjacent layer identify what moves, who receives it, who decides, what fails, and whether the connection is observed, inferred, or proposed.

### 4. Draft

Read `workflows/industry-write.md`, `references/industry-human-style.md`, and `templates/industry-observation.md`.

Before drafting, read `references/validated-sanitation-case.md`. Its object-led progression is the default for connected operational cases. The sectioned observation template is optional: do not force numbered headings, data cards, a repeated thesis, or a summary into a continuous narrative. Research completeness does not require displaying every research field in the article.

Choose a title exposing the real consequence; do not force a number into it. Before drafting identify a traceable object and one unresolved question. A launch or laboratory announcement alone is insufficient without concrete operational evidence. Use an event-anchor title with a concrete number, time window, action, or consequence. Open inside the event and state the question the article answers. Optional research coverage (never a compulsory section sequence):

1. event and timeline;
2. wider operational or market pressure;
3. technical/application stack;
4. AI boundary and human authority;
5. business or public-service opportunities;
6. two or three real bottlenecks;
7. the human action or consequence at the end of the chain.

Weave sources beside claims and include a source list. Use author judgment only where a comparison or decision exists.

### 5. Audit and deliver

Run:

```powershell
python scripts/article_lint.py article.md --research-pack research-pack.json
python scripts/integrity_check.py source-notes.md article.md
```

Use the integrity comparison when source notes or a previous draft exist. Read `workflows/zhuque.md` only when Zhuque is enabled or the user supplies a result. Revise paragraph function before surface wording: replace empty explanation with evidence, a handoff, a constraint, a decision, or a consequence.

Deliver the article first, then sources and a compact note separating facts, inference, proposals, and unknowns. Run the version-bound acceptance workflow before claiming acceptance. Never add unsupported handoffs to satisfy lint keywords.

### 6. Match layout to the finished article

For a completed WeChat article, follow `workflows/gzh-layout.md` and invoke the installed `gzh-design` skill. The user has requested automatic content-based theme selection. Deliver Markdown, clean HTML and a copy-button preview after HTML validation. Topic-only requests stop before this stage. Preserve approved prose, paragraph order, numbers, links and the ending; layout must not add introduction cards, invented headings, slogans, signatures or CTAs. User-specified plain-text-only output takes precedence.
