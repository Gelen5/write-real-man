#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

REQUIRED = [
    "SKILL.md",
    "README.md",
    "references/article-types.md",
    "references/source-quality.md",
    "references/technical-explanation.md",
    "references/audience-ordinary-people.md",
    "references/scenario-first.md",
    "references/ordinary-writing-style.md",
    "references/technical-depth.md",
    "references/trend-discovery.md",
    "references/topic-ranking.md",
    "references/topic-hook-and-resonance.md",
    "references/humanization.md",
    "references/validated-human-style.md",
    "references/zhuque-loop.md",
    "scripts/article_lint.py",
    "scripts/preflight.py",
    "scripts/integrity_check.py",
    "scripts/zhuque_client.py",
    "scripts/build_rewrite_packet.py",
    "scripts/trends/collector.py",
    "scripts/trends/discover.py",
    "scripts/trends/normalizer.py",
    "scripts/trends/deduplicator.py",
    "scripts/trends/cluster.py",
    "scripts/trends/topic_ranker.py",
    "scripts/trends/topic_transformer.py",
    "templates/topic-list.md",
    "templates/scenario-tutorial.md",
    "examples/golden/01-workbuddy-weekly-report.md",
    "examples/topic-discovery/raw-trends.json",
    "examples/evals/topic-discovery-cases.json",
    "tests/test_topic_ranker.py",
    "tests/test_topic_transformer.py",
    "tests/test_trend_dedupe.py",
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
    if "references/topic-hook-and-resonance.md" not in skill:
        errors.append("SKILL.md does not route topic decisions to the hook and resonance gate")
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
