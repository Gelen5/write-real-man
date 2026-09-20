# Research Pack schema

Build this before drafting when external facts matter.

```yaml
topic: ""
article_type: ""
as_of_date: "YYYY-MM-DD"

thesis_candidate: ""
reader_payoff: ""

verified_facts:
  - claim: ""
    source: ""
    source_type: "primary|practitioner|community"
    date: ""

user_experience:
  - statement: ""
    evidence: "user-provided note/screenshot/log"

community_observations:
  - observation: ""
    source: ""
    caveat: "anecdotal / sample limitation"

uncertain_claims:
  - claim: ""
    reason_uncertain: ""

protected_literals:
  - "GPT-5.6"
  - "codex --full-auto"
  - "https://..."

possible_angles:
  - ""

counterpoints:
  - ""
```

Rules:

- Facts without a source stay in `uncertain_claims`.
- User experience is not interchangeable with internet evidence.
- Community reaction must be attributed as reaction.
- The draft may omit Research Pack material; it may not silently strengthen uncertain material into fact.
