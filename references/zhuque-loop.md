# Zhuque evaluation loop

## Role of Zhuque

Use Zhuque as an external regression signal after the article is already factually correct and publishable.

Tencent's current text response exposes:
- label `0`: Human
- label `1`: AI
- label `2`: suspected AI
- `labels_ratio`
- `segment_labels`
- `ratio_confidence`
- `softmax_confidence`

Prefer `is_merge=false` for local diagnosis.

## Loop

1. local lint
2. integrity check
3. Zhuque evaluation
4. identify risky segments
5. diagnose why those segments are weak as writing
6. rewrite only those segments
7. integrity check again
8. rerun Zhuque

Default maximum: 3 rounds.

## Stop conditions

Stop when any is true:
- configured internal gate is satisfied
- next rewrite would weaken factual precision
- three rounds completed
- remaining flagged text is mostly protected technical material

## Reporting

Report measured ratios and date/time if useful. Do not call an internal threshold “腾讯官方通过线”.
