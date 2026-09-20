# Workflow: Optional Zhuque check

Zhuque is the final text-quality signal, not a topic filter or substitute for editing.

1. Confirm the article is useful, readable and factually checked.
2. If the user has not configured an API key, do not pretend a check ran. Continue with local checks or accept a user-provided screenshot/report.
3. If enabled, read `references/zhuque-loop.md`; use `scripts/zhuque_client.py` and preserve exact output for that draft.
4. Compare risky segments with stronger segments. Fix specific writing issues while protecting facts and reader value.
5. Run at most three iterations by default. Stop if another edit would harm clarity or evidence.
6. Report the result for that run only. User screenshots and statements are attributed as such; never invent ratios or universalize the result.
