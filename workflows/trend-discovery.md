# Workflow: Trend Discovery

Read `references/trend-discovery.md` and `references/topic-ranking.md` before running.

## Run

1. Use the audience and date window from the user, defaulting to everyday AI users and 72 hours.
2. Run `python scripts/trends/discover.py --window 72h --out .cache/trends/discovery.json` with any platform list or audience override from the user. Set `--refresh` when the user asks for a live refresh or cached results are stale.
3. `discover.py` runs the adapters, normalization, deduplication, clustering, scoring and topic transformation. If fewer than ten eligible topics survive, it retries with a 7-day window and identifies that fallback in the result.
4. Inspect sources and candidate evidence. Verify product facts on official pages; do not treat a high score or duplicated reposts as proof.
5. Treat the rule-based transformer's title as a topic seed, not the final reader-facing headline. For each human-centered candidate, apply `workflows/choose-topic.md` and `references/topic-hook-and-resonance.md`; rewrite a merely descriptive seed into a supported reader-facing hook before showing it. The automated trend score is not the hook judgment. Reject practical but flat ideas until the angle exposes a supportable reader-relevant tension.
6. If fewer than ten candidates pass both gates, report fewer. Add evergreen opportunities separately; never label them today's trend.
7. Return the structured list in `templates/topic-list.md`, with an evidence-backed reason to click and a payoff. Do not write the full article until asked, except when the user explicitly asks the Skill to choose and write.

## Output contract

For each candidate include a recommended title, intended reader and scene, pain/stakes, cognitive gap, hook rationale, promised payoff, content type, suggested technical depth, trend score and explanation, trend window, source count, platform count, dated evidence links and risks/availability limits. Mark `trend`, `hybrid` or `evergreen`. State the editorial gate as `pass`, `revise` or `reject`; do not present it as a click-through estimate.

Always include a compact source-availability note. Never hide collector errors that materially limit the sample.

For Chinese platform searches, use the same query when the user specifies a product such as WorkBuddy or ChatGPT. The default query is bilingual and includes domestic products. Do not substitute a generic “AI” query for a user-named product. Explain that some platforms return undated ranked posts; only dated items that fall within the selected window count as current signals.
