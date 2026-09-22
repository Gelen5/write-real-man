#!/usr/bin/env python3
from pathlib import Path

REQUIRED = [
    "references/validated-sanitation-case.md", "workflows/gzh-layout.md", "examples/golden/07-sanitation-work-order-passed.md",
    "SKILL.md", "README.md", "CHANGELOG.md",
    "workflows/industry-research.md", "workflows/industry-synthesis.md", "workflows/industry-write.md", "workflows/zhuque.md",
    "references/industry-evidence.md", "references/industry-topic-selection.md", "references/chain-synthesis.md", "references/industry-human-style.md", "references/fact-integrity.md", "references/research-pack-schema.md",
    "templates/industry-topic-list.md", "templates/industry-research-pack.md", "templates/industry-observation.md",
    "scripts/article_lint.py", "scripts/integrity_check.py", "scripts/preflight.py", "scripts/zhuque_client.py",
]

ROUTES = [
    "references/validated-sanitation-case.md", "workflows/gzh-layout.md",
    "workflows/industry-research.md", "workflows/industry-synthesis.md", "workflows/industry-write.md",
    "references/industry-evidence.md", "references/industry-topic-selection.md", "references/chain-synthesis.md", "references/industry-human-style.md",
    "templates/industry-topic-list.md", "templates/industry-research-pack.md", "templates/industry-observation.md",
]

FORBIDDEN_ROUTING = ("Route the request", "scenario-tutorial` or `problem-solution")

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing = [p for p in REQUIRED if not (root / p).exists()]
    skill = (root / "SKILL.md").read_text(encoding="utf-8") if (root / "SKILL.md").exists() else ""
    errors = []
    if missing: errors.append(f"missing: {missing}")
    if not skill.startswith("---\n"): errors.append("SKILL.md missing YAML frontmatter")
    for key in ("name:", "description:", "version:"):
        if key not in skill[:700]: errors.append(f"SKILL.md missing frontmatter field {key}")
    for route in ROUTES:
        if route not in skill: errors.append(f"SKILL.md does not route to {route}")
    if "version: 1.2.0" not in skill[:700]: errors.append("expected version 1.2.0")
    for phrase in FORBIDDEN_ROUTING:
        if phrase in skill: errors.append(f"legacy dual-route phrase remains: {phrase}")
    print("INVALID" if errors else "VALID")
    for error in errors: print("-", error)
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
