# Protected literals

Treat the following as immutable by default during humanization and detector-driven rewriting:

- fenced code blocks
- inline code
- shell commands and flags
- environment variable names
- API paths and endpoints
- URLs
- Markdown link targets
- version strings such as `1.2.3`, `v0.9.0`, `GPT-5.6`
- exact dates and numeric claims
- model/product/repository names
- quoted source wording when fidelity matters

If a protected literal appears wrong, do not silently “fix” it. Verify against evidence first.
