# Version-bound writing and acceptance

## Before writing
Choose an event with operational detail and a human consequence. Keep the original China-first research and at least three evidenced applications. An announcement is background until deployment evidence is found. Select one object and question; do not invent a scene to fill the brief.

## Editorial review
Read validated-sanitation-case.md. Each paragraph should advance an action, substantiate a fact, expose a mismatch, make a reasoned decision or explain a necessary constraint. Delete repeated significance, unanswered question lists and speculative business lists without buyers or operational need. Preserve complete sentences and readable transitions; do not insert mistakes or slang to influence detection.

Save review.json with article_sha256 (raw UTF-8 file bytes), facts and readability objects, each containing status (passed/needs_revision), reviewer, and notes. Facts notes must map material claims to source, subject/place, event date, publication date, number/unit, scope, and evidence state. Explain changes from an earlier version. This is an agent/human semantic review, not proof supplied by a keyword script. Do not claim a numeric literal check establishes factual accuracy.

## Detection and freezing
Use acceptance.py prepare ARTICLE DIRECTORY. detection.txt contains the exact Markdown article including title and sources; this scope is fixed for comparisons. Keep internal review notes in separate files. Do not silently remove sources for a better score.

Manual feedback is the default. Do not upload a draft merely because keys exist. Record feedback.json with status=success, article_sha256, scope=full_markdown_utf8, checked_at (ISO timestamp), source (manual_report/manual_screenshot/api), evidence (report path or a precise user-report reference), unit (fraction/percent), and human_ratio, ai_ratio, suspected_ai_ratio. Unknown fields stay unknown, not zero. User reports remain attributed and are not independent measurements. API usage requires explicit enablement; verify current endpoint/schema before using it.

Run preflight.py ARTICLE --research-pack PACK --review REVIEW --feedback FEEDBACK --html CLEAN_HTML --out-dir DIRECTORY. Missing detection is pending_detection. Missing or stale review is pending_review. Invalid ratios, failed service calls and mismatched hashes are invalid_evidence, never passed. Acceptance requires both semantic reviews passed, matching successful detector evidence with human >= 0.70, and exact layout text/link preservation when layout is requested.

Below threshold: revise concrete weak passages, preserve stronger passages and factual limits, then create a new version and new review/detection record. Maximum three revisions; stop sooner if edits harm readability or accuracy. Deliver unresolved drafts with their actual state. Never promise an external detector outcome.

## Layout
After the tested text is frozen, use gzh-design. Do not add a summary, directory, English tags, repeated quotations, END text, invented numbering or byline. Copy only the article's existing text. acceptance.py layout compares rendered text and ordered source URLs; visual formatting may change, wording may not. Run upstream HTML validation too.

## Stability cohort
Register 20 consecutive new article IDs before detecting; retain all failures, pending articles and revisions. Golden examples are development evidence, not holdout tests. Each cohort entry has article_id, topic, attempts (round, article_sha256, human_ratio, source, evidence, editorial_passed). Use acceptance.py cohort COHORT.json for first-draft and within-three-revisions rates over all registered articles. Keep missing results in the denominator and report them separately. No stability claim until the batch has complete results; even a completed batch does not guarantee the next article.
