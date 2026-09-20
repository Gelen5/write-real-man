# Changelog

## 0.3.1 — 2026-09-21

- Added a reader-situation, cognitive-gap, hook, credibility and payoff gate to topic selection, adapting relevant dbskill editorial lenses.
- Separated trend suitability from editorial hook readiness; explicitly prohibited treating either as a click-through prediction.
- Expanded topic shortlist fields and added a worked review showing how to revise a flat everyday AI topic without inventing a reversal.
- Routed both user-provided and discovered topics through the same hook-and-resonance reference; validator now checks that the reference is discoverable from the Skill entrypoint.

## 0.3.0 — 2026-09-20

- Repositioned the Skill as AI × ordinary-people topic discovery and practical Chinese writing.
- Added two-mode routing for user-provided topics and live trend discovery.
- Added audience, scenario-first, ordinary-language, technical-depth, trend-discovery and topic-ranking references plus separate workflows.
- Added independent trend source adapters, normalization, deduplication, clustering, scoring, topic transformation and a 60-minute cache.
- Expanded article lint with ordinary-reader usefulness diagnostics and trend-to-human alignment.
- Added fixed topic fixtures, ranking/transformer/dedup tests, five golden scenario examples, three discovery acceptance records and one researched sample article.
- Kept Zhuque evaluation as an optional final quality signal; it is not a topic-selection criterion.

## 0.2.0 — 2026-09-19

- Added a detector-evidence workflow for user-provided screenshots, segment labels and confirmed-passing drafts.
- Added the five-round WorkBuddy case study with measured failure patterns, user-confirmed final acceptance, and a full analysis of title, opening, tutorial path, examples, transitions, factual boundaries, layout, reader value and ending.
- Added content-function diagnostics for explanation-after-example, exhaustive tutorial coverage and symmetrical rhetorical questions.
- Added rules to preserve confirmed stronger passages and report only measured detector results.
- Expanded humanization guidance to revise paragraph function before surface tone.

## 0.1.0 — 2026-09-19

- Initial AI-tech-only writing Skill.
- Added research, article-type, source-quality, fact-integrity and humanization references.
- Added deterministic local article linting.
- Added protected-literal integrity checks.
- Added Tencent EdgeOne Makers Zhuque text API client.
- Added user-defined Zhuque acceptance gate.
- Added lint + Zhuque targeted rewrite packet builder.
- Added one-command preflight runner.
- Added unit tests and synthetic examples.
