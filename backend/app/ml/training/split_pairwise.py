from __future__ import annotations

import json
import random
from pathlib import Path


INPUT = Path(
    "data/training/bootstrap/question_ranking_pairs.jsonl"
)

OUTPUT_DIR = Path(
    "data/training/bootstrap/splits"
)

SEED = 42


def load_pairs():
    pairs = []

    with INPUT.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                pairs.append(json.loads(line))

    return pairs


def split_by_case(pairs):
    grouped = {}

    for pair in pairs:
        grouped.setdefault(pair["case_id"], []).append(pair)

    case_ids = list(grouped)

    random.Random(SEED).shuffle(case_ids)

    n = len(case_ids)

    if n < 3:
        raise ValueError(
            "Need at least 3 distinct cases for "
            "train/validation/test splitting."
        )

    train_end = max(1, int(n * 0.6))
    validation_end = max(
        train_end + 1,
        int(n * 0.8),
    )

    # Make sure at least one case remains for test.
    validation_end = min(validation_end, n - 1)

    train_cases = case_ids[:train_end]
    validation_cases = case_ids[train_end:validation_end]
    test_cases = case_ids[validation_end:]

    def collect(ids):
        result = []

        for case_id in ids:
            result.extend(grouped[case_id])

        return result

    return (
        train_cases,
        validation_cases,
        test_cases,
        collect(train_cases),
        collect(validation_cases),
        collect(test_cases),
    )


def write_split(name, cases, pairs):
    path = OUTPUT_DIR / f"{name}.jsonl"

    with path.open("w", encoding="utf-8") as f:
        for pair in pairs:
            f.write(
                json.dumps(pair, ensure_ascii=False)
                + "\n"
            )

    print(
        f"{name:10s}: "
        f"{len(cases)} cases / "
        f"{len(pairs)} pairs"
    )


def main():
    pairs = load_pairs()

    (
        train_cases,
        validation_cases,
        test_cases,
        train_pairs,
        validation_pairs,
        test_pairs,
    ) = split_by_case(pairs)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=== CASE-LEVEL SPLIT ===")
    print(f"Total cases: {len(set(p['case_id'] for p in pairs))}")
    print(f"Total pairs: {len(pairs)}")
    print()

    write_split(
        "train",
        train_cases,
        train_pairs,
    )

    write_split(
        "validation",
        validation_cases,
        validation_pairs,
    )

    write_split(
        "test",
        test_cases,
        test_pairs,
    )

    all_cases = (
        set(train_cases)
        | set(validation_cases)
        | set(test_cases)
    )

    assert len(all_cases) == len(
        train_cases
        + validation_cases
        + test_cases
    )

    assert not (
        set(train_cases)
        & set(validation_cases)
    )

    assert not (
        set(train_cases)
        & set(test_cases)
    )

    assert not (
        set(validation_cases)
        & set(test_cases)
    )

    print("\n=== LEAKAGE CHECK ===")
    print("No case appears in more than one split.")
    print("Split validation passed.")


if __name__ == "__main__":
    main()
