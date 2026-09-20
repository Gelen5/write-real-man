# Workflow: Improve naturalness and readability

Run local lint before editing. Use `ordinary_reader_score` and paragraph findings as diagnostic clues, not writing targets.

1. Find paragraphs that explain AI instead of helping the reader do the task.
2. Replace abstract advice with the actual material, prompt, wrong result, correction or verification step when evidence allows.
3. Cut repeated explanation and unnecessary product-tour content.
4. Preserve facts, uncertainty, natural syntax and punctuation. Do not add personal experience, mistakes, slang or arbitrary fragments.
5. Keep the example's facts consistent from input to final result.
6. Re-run lint; inspect readability manually. Use the validated WorkBuddy case as one sample in `references/validated-human-style.md`, not as a universal template.

Zhuque is considered only after usefulness, readability and factual checks. Never promise 100% human classification.
