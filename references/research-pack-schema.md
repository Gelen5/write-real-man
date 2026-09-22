# Industry research pack schema

Use JSON so `article_lint.py` can validate coverage. See `templates/industry-research-pack.md`.

Required keys: `topic`, `as_of_date`, `event_anchor`, `thesis`, `anchor_numbers`, `timeline`, `layers`, `claims`, `opportunities`, `bottlenecks`, and `sources`.

Every claim has `id`, `text`, `state`, and `source_ids`. Allowed states: `verified_fact`, `reported_claim`, `author_inference`, `proposal`, `unknown`.

Every layer has `name`, `input`, `operation`, `output`, `recipient`, `decision_owner`, `failure_mode`, `state`, and `source_ids`.

Unknown values remain empty or use `state: unknown`. Never fill gaps with plausible detail.
