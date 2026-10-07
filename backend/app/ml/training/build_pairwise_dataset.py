from __future__ import annotations

import json
from pathlib import Path
from itertools import combinations


INPUT = Path("data/training/bootstrap/question_ranking.jsonl")
OUTPUT = Path("data/training/bootstrap/question_ranking_pairs.jsonl")


def load_examples():
    examples = []

    with INPUT.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                examples.append(json.loads(line))

    return examples


def build_pairs(examples):
    grouped = {}

    for example in examples:
        grouped.setdefault(example["case_id"], []).append(example)

    pairs = []

    for case_id, candidates in grouped.items():
        preferred = [
            x for x in candidates
            if x["labels"]["preferred"]
        ]

        rejected = [
            x for x in candidates
            if not x["labels"]["preferred"]
        ]

        for winner in preferred:
            for loser in rejected:
                pairs.append({
                    "case_id": case_id,
                    "case_state": winner["case_state"],
                    "preferred_action": winner["candidate_action"],
                    "rejected_action": loser["candidate_action"],
                    "preferred_labels": winner["labels"],
                    "rejected_labels": loser["labels"],
                    "metadata": {
                        "source": "initial_expert_bootstrap",
                        "annotation_type": "expert_bootstrap",
                    },
                })

    return pairs


def main():
    examples = load_examples()
    pairs = build_pairs(examples)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", encoding="utf-8") as f:
        for pair in pairs:
            f.write(
                json.dumps(pair, ensure_ascii=False)
                + "\n"
            )

    print("=== PAIRWISE DATASET ===")
    print(f"Input examples:  {len(examples)}")
    print(f"Output pairs:    {len(pairs)}")
    print(f"Output:          {OUTPUT}")

    for pair in pairs:
        print(
            f"  {pair['case_id']}: "
            f"{pair['preferred_action']['action_id']} "
            f"> "
            f"{pair['rejected_action']['action_id']}"
        )


if __name__ == "__main__":
    main()
