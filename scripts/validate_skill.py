#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

REQUIRED = [
    "SKILL.md",
    "README.md",
    "references/article-types.md",
    "references/source-quality.md",
    "references/ai-tech-style.md",
    "references/humanization.md",
    "references/validated-human-style.md",
    "references/zhuque-loop.md",
    "scripts/article_lint.py",
    "scripts/preflight.py",
    "scripts/integrity_check.py",
    "scripts/zhuque_client.py",
    "scripts/build_rewrite_packet.py",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing = [p for p in REQUIRED if not (root / p).exists()]
    skill = (root / "SKILL.md").read_text(encoding="utf-8") if (root / "SKILL.md").exists() else ""
    errors = []
    if missing:
        errors.append(f"missing: {missing}")
    if not skill.startswith("---\n"):
        errors.append("SKILL.md missing YAML frontmatter")
    for key in ("name:", "description:", "version:"):
        if key not in skill[:600]:
            errors.append(f"SKILL.md missing frontmatter field {key}")
    if errors:
        print("INVALID")
        for error in errors:
            print("-", error)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
