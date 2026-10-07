from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


INPUT = Path("data/training/factor_corpus/factors_v1.jsonl")
OUTPUT = Path("data/training/factor_corpus/factor_pairs_v1.jsonl")


def load_records():
    records = []

    with INPUT.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    return records


def make_pairs(records):
    by_case = defaultdict(list)

    for record in records:
        by_case[record["case_id"]].append(record)

    pairs = []

    for case_id, case_records in by_case.items():
        case_state = case_records[0]["case_state"]

        for preferred in case_records:
            for rejected in case_records:
                if preferred is rejected:
                    continue

                p_score = preferred["labels"]["importance"]
                r_score = rejected["labels"]["importance"]

                # Only create meaningful comparisons.
                if p_score <= r_score:
                    continue

                # Require a reasonable margin.
                if p_score - r_score < 0.20:
                    continue

                pairs.append(
                    {
                        "case_id": case_id,
                        "case_state": case_state,
                        "preferred_factor": preferred["factor"],
                        "rejected_factor": rejected["factor"],
                        "preferred_importance": p_score,
                        "rejected_importance": r_score,
                        "importance_margin": p_score - r_score,
                        "metadata": {
                            "annotation_type": "expert_bootstrap_pairwise",
                            "source": "factor_corpus_v1",
                        },
                    }
                )

    return pairs


def main():
    records = load_records()
    pairs = make_pairs(records)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", encoding="utf-8") as f:
        for pair in pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    cases = len({p["case_id"] for p in pairs})

    print("=== FACTOR PAIRWISE CORPUS V1 ===")
    print(f"Pairs: {len(pairs)}")
    print(f"Cases: {cases}")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
