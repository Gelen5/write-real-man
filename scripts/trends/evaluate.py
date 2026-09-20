#!/usr/bin/env python3
"""Run deterministic topic-discovery quality checks against the fixture."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from cluster import cluster
from deduplicator import deduplicate
from topic_ranker import rank_topics
from topic_transformer import transform_topics


def run(fixture: Path) -> dict:
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    items = payload["items"]
    ranked = rank_topics(cluster(deduplicate(items)))
    transformed = transform_topics(ranked)
    technical = next(row for row in ranked if "transformer inference" in row["representative"]["title"].casefold())
    files = next(row for row in ranked if "multiple uploaded files" in row["representative"]["title"].casefold())
    checks = {
        "engineering_benchmark_filtered": not technical["eligible"],
        "everyday_file_topic_is_eligible": files["eligible"],
        "file_topic_transformed": any("长文件" in row["title"] for row in transformed),
        "each_recommendation_names_person_and_problem": all(row.get("person") and row.get("problem") for row in transformed),
        "source_evidence_retained": all(row.get("evidence") is not None for row in ranked),
    }
    return {"fixture": str(fixture.relative_to(ROOT)), "passed": all(checks.values()), "checks": checks, "ranked_topics": ranked, "transformed_topics": transformed}


def main() -> int:
    fixture = ROOT / "examples" / "topic-discovery" / "raw-trends.json"
    result = run(fixture)
    print(json.dumps({"fixture": result["fixture"], "passed": result["passed"], "checks": result["checks"], "ranked_count": len(result["ranked_topics"]), "transformed_count": len(result["transformed_topics"])}, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
