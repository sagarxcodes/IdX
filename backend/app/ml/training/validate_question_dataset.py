from __future__ import annotations

import json
from pathlib import Path


DATASET = Path("data/training/bootstrap/question_ranking.jsonl")

REQUIRED_LABELS = {
    "preferred",
    "information_gain",
    "decision_impact",
    "evidence_value",
    "uncertainty_reduction",
    "user_effort",
}

REQUIRED_ACTION_FIELDS = {
    "action_id",
    "action_type",
    "description",
}

def validate():
    if not DATASET.exists():
        raise FileNotFoundError(DATASET)

    rows = []
    errors = []

    with DATASET.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc}")
                continue

            rows.append(row)

            if not row.get("case_id"):
                errors.append(f"line {line_number}: missing case_id")

            state = row.get("case_state", {})
            if not state.get("objective"):
                errors.append(f"line {line_number}: missing objective")

            action = row.get("candidate_action", {})
            missing_actions = REQUIRED_ACTION_FIELDS - action.keys()

            for field in sorted(missing_actions):
                errors.append(
                    f"line {line_number}: missing action field: {field}"
                )

            labels = row.get("labels", {})
            missing_labels = REQUIRED_LABELS - labels.keys()

            for field in sorted(missing_labels):
                errors.append(
                    f"line {line_number}: missing label: {field}"
                )

            for field in REQUIRED_LABELS - {"preferred"}:
                value = labels.get(field)

                if value is None:
                    continue

                if not isinstance(value, (int, float)):
                    errors.append(
                        f"line {line_number}: {field} must be numeric"
                    )
                elif not 0.0 <= float(value) <= 1.0:
                    errors.append(
                        f"line {line_number}: {field} must be between 0 and 1"
                    )

    # ------------------------------------------------------------
    # Check case/action structure
    # ------------------------------------------------------------

    cases = {}

    for row in rows:
        case_id = row["case_id"]
        cases.setdefault(case_id, []).append(row)

    if not cases:
        errors.append("dataset contains zero examples")

    for case_id, examples in cases.items():

        preferred_count = sum(
            bool(example.get("labels", {}).get("preferred"))
            for example in examples
        )

        rejected_count = sum(
            not bool(example.get("labels", {}).get("preferred"))
            for example in examples
        )

        if preferred_count == 0:
            errors.append(
                f"case {case_id}: no preferred action"
            )

        if rejected_count == 0:
            errors.append(
                f"case {case_id}: no rejected action"
            )

    # ------------------------------------------------------------
    # Dataset statistics
    # ------------------------------------------------------------

    preferred = sum(
        bool(row.get("labels", {}).get("preferred"))
        for row in rows
    )

    rejected = len(rows) - preferred

    print("=== IdX Question Ranking Dataset ===")
    print(f"Examples:       {len(rows)}")
    print(f"Cases:          {len(cases)}")
    print(f"Preferred:      {preferred}")
    print(f"Rejected:       {rejected}")

    print("\nCases:")
    for case_id, examples in sorted(cases.items()):
        print(
            f"  {case_id}: "
            f"{len(examples)} candidates"
        )

    if errors:
        print("\n=== VALIDATION FAILED ===")
        for error in errors:
            print(f"ERROR: {error}")

        raise SystemExit(1)

    print("\n=== VALIDATION PASSED ===")
    print("Dataset structure is valid.")


if __name__ == "__main__":
    validate()
