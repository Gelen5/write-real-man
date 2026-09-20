# Ordinary People Topic Ranking

## Positive score (0–100)

| Criterion | Weight | High score means |
| --- | ---: | --- |
| `ordinary_people_relevance` | 30 | a clear everyday reader or recurring nontechnical need |
| `usefulness` | 20 | the article could solve a task, reduce effort or improve a decision |
| `actionability` | 15 | the reader can try a bounded step today |
| `freshness` | 10 | the signal is within the selected window |
| `cross_platform_heat` | 10 | independent platforms/users discuss the same event or use |
| `novelty` | 10 | the angle is not a generic product announcement or worn-out list |
| `evidence_quality` | 5 | original, dated, attributable sources support the topic |

Each criterion is normalized to its weight. Engagement may contribute to cross-platform signal only; it does not directly rank usefulness.

## Penalties

- `too_technical`: −20 when ordinary readers cannot use the core action.
- `pure_news`: −15 when no human problem or practical action follows the announcement.
- `pure_marketing`: −20 for promotional copy without independent evidence or limits.
- `weak_evidence`: −15 when the claim has only an unclear, anonymous or secondary source.
- `stale`: −10 to −20 based on how far the signal exceeds the selected window.

Floor the final score at 0 and preserve the raw dimensions, penalties and evidence. These are transparent heuristics for sorting candidates, not audience measurements. The writer should review ambiguous cases.

The default current-trend admission threshold is 55/100. Also require dated evidence inside the chosen collection window, ordinary-person relevance of at least 0.45 and usefulness of at least 0.40. An item without a publication date may be reviewed as an undated lead, but it cannot enter a current-trend shortlist.

## Admission rule

Before a candidate enters a reader-facing top list, state:

- **who** has the problem
- **what** is hard, repetitive, confusing or easy to miss
- **how** AI can help with a bounded action
- **what** useful result can be checked

If a candidate only supports “this company launched a feature,” it does not qualify. If no recent candidate qualifies, return fewer and add a separate evergreen section.
