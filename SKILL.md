---
name: write-real-man
description: A Chinese AI content discovery and practical-writing skill for ordinary people. Discover current public trends when the user has no topic, rank them by everyday relevance and usefulness, and turn selected topics into clear, actionable articles. Use when finding AI topics or writing practical AI content for general readers; keep developer-level detail only when asked.
metadata:
  version: 0.3.1
---

# Write Real Man

An AI × ordinary people content discovery and writing Skill.

> **One article, one real problem, one useful result.**

AI is the tool in the story. The reader's problem is the subject. A reader should finish thinking: “I can try this today.”

## Route the request

### A. The user already gave a topic

Go directly to Topic Understanding → Article Research → Scenario → Writing. Read only the needed workflow and references:

- Start with `workflows/choose-topic.md` to define who has what problem and what result the article promises.
- For any topic choice or title pitch, apply `references/topic-hook-and-resonance.md`; do not treat usefulness or trend score as proof that a reader has a reason to click.
- For current product behavior, read `workflows/research.md` and `references/source-quality.md`.
- If the user explicitly requests technical depth 3, read `references/technical-explanation.md`; otherwise keep technical detail at the minimum needed for the task.
- For practical prose, read `workflows/write.md`, `references/audience-ordinary-people.md`, `references/scenario-first.md`, and `references/ordinary-writing-style.md`.
- Read `references/technical-depth.md` only when technical explanation is needed.
- Run local quality checks and factual integrity checks. Zhuque is an optional final signal; read `workflows/zhuque.md` only when enabled or the user provides results.

### B. The user did not give a topic

Enter Trend Discovery. Do not invent “today's hot topics” from model memory.

1. Set the audience (default: ordinary office workers and everyday AI users) and time window (default: 72 hours).
2. Read `workflows/trend-discovery.md` and `references/trend-discovery.md`.
3. Collect public signals from available Chinese self-media platforms and global sources through independent adapters; label unavailable sources and preserve per-source failures.
4. Normalize, deduplicate and cluster related items before ranking.
5. Score whether a trend can solve an ordinary person's specific problem; do not rank by raw likes or stars.
6. Transform technical headlines into human-centered opportunities. Remove items with no clear person, problem, action and useful result.
7. Run the separate editorial hook gate in `workflows/choose-topic.md` and `references/topic-hook-and-resonance.md`. A trend score cannot rescue a flat idea; a strong hook cannot make an unsupported claim true.
8. Return up to 10 opportunities with dated sources for trend claims, source limitations, a clear reason to click and the promised reader payoff. Do not pad a weak list. Keep evergreen ideas separate from live trends.

If the user asks “you choose and write it”, select the strongest ordinary-person opportunity and continue to Article Research. Otherwise, return the topic list and let the user choose.

## Write the article

1. Define one reader, one real problem and one useful result. Apply the editorial hook gate before accepting a title; if the topic cannot answer “why should an ordinary person care?”, “what makes this angle worth opening?” and “what can they do after reading?”, change the angle or drop it.
2. Research facts only after the topic is selected. Keep official sources for product facts and community posts for attributed user signals.
3. Choose `scenario-tutorial` or `problem-solution` by default. Follow one small task from its starting material to a checked result.
4. Use ordinary spoken prompts, actual or clearly labeled fictional source material, a plausible first output, a precise correction and a final artifact or action.
5. Explain product terms where the reader needs them. Default `technical_depth` is 1 (0–3); use level 3 only when requested.
6. Do not invent first-person experience, user results, numbers, quotes or feature availability. State plan, region, waitlist and experimental limits when relevant.
7. Run `python scripts/article_lint.py article.md`, review `ordinary_reader_score` and any high-severity findings, then run `python scripts/integrity_check.py original.md article.md` when an original exists.
8. Only after usefulness, readability and factual checks, run Zhuque when configured. Never select a topic or weaken the article to chase a detector score. Do not promise 100% human or permanent detector passage.

For a full response, deliver the article first, then source links and short verification notes. Use `templates/final-report.md` only when a report is requested.
