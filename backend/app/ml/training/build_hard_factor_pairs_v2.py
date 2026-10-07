from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path


INPUT = Path(
    "data/training/factor_corpus/"
    "factor_knowledge_v2.jsonl"
)

OUTPUT = Path(
    "data/training/factor_corpus/"
    "hard_factor_pairs_v2.jsonl"
)


def load():
    records = []

    with INPUT.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    return records


def build_pairs(records):
    by_case = {}

    for record in records:
        by_case.setdefault(
            record["case_id"], []
        ).append(record)

    pairs = []

    for case_id, factors in by_case.items():

        # Only compare factors that are BOTH
        # genuinely relevant.
        relevant = [
            r for r in factors
            if r["labels"]["relevant"]
        ]

        for a, b in combinations(relevant, 2):

            ia = a["labels"]["importance"]
            ib = b["labels"]["importance"]

            # Skip near ties for now.
            # We want meaningful but difficult
            # contextual comparisons.
            margin = abs(ia - ib)

            if margin < 0.05:
                continue

            preferred = a if ia > ib else b
            rejected = b if ia > ib else a

            pairs.append(
                {
                    "case_id": case_id,
                    "case_state": factors[0]["case_state"],
                    "preferred_factor": preferred["factor"],
                    "rejected_factor": rejected["factor"],
                    "preferred_importance":
                        preferred["labels"]["importance"],
                    "rejected_importance":
                        rejected["labels"]["importance"],
                    "importance_margin": margin,

                    "preferred_reason":
                        preferred["relevance_reason"],

                    "rejected_reason":
                        rejected["relevance_reason"],

                    "preferred_evidence":
                        preferred["evidence_requirements"],

                    "rejected_evidence":
                        rejected["evidence_requirements"],

                    "metadata": {
                        "pair_type": "hard_contextual",
                        "annotation_type":
                            "expert_bootstrap_v2",
                    },
                }
            )

    return pairs


def main():
    records = load()
    pairs = build_pairs(records)

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT.open("w", encoding="utf-8") as f:
        for pair in pairs:
            f.write(
                json.dumps(
                    pair,
                    ensure_ascii=False
                ) + "\n"
            )

    print("=== HARD FACTOR PAIRS V2 ===")
    print("Pairs:", len(pairs))
    print(
        "Cases:",
        len({
            p["case_id"]
            for p in pairs
        })
    )
    print("Output:", OUTPUT)

    print("\nExamples:")

    for pair in pairs[:10]:
        print(
            f"  {pair['case_id']}: "
            f"{pair['preferred_factor']['name']} "
            f"> "
            f"{pair['rejected_factor']['name']} "
            f"(margin="
            f"{pair['importance_margin']:.2f})"
        )


if __name__ == "__main__":
    main()
