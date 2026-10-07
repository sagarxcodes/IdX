from dataclasses import dataclass
from typing import Dict, List

from app.ml.training_schema import MLTrainingExample


REQUIRED_CASE_FIELDS = {
    "case_id",
    "objective",
}

REQUIRED_ACTION_FIELDS = {
    "action_id",
    "action_type",
    "description",
}


@dataclass
class ValidationReport:
    valid: bool
    total: int
    valid_examples: int
    invalid_examples: int
    errors: List[str]


def validate_example(
    example: MLTrainingExample,
):

    errors = []

    case_state = example.case_state
    action = example.candidate_action

    missing_case = (
        REQUIRED_CASE_FIELDS
        - set(case_state.keys())
    )

    missing_action = (
        REQUIRED_ACTION_FIELDS
        - set(action.keys())
    )

    if missing_case:
        errors.append(
            "Missing case fields: "
            + ", ".join(sorted(missing_case))
        )

    if missing_action:
        errors.append(
            "Missing action fields: "
            + ", ".join(sorted(missing_action))
        )

    numeric_fields = [
        "information_gain",
        "decision_impact",
        "evidence_value",
        "uncertainty_reduction",
        "user_effort",
    ]

    for field in numeric_fields:

        value = getattr(
            example,
            field,
        )

        if not 0.0 <= value <= 1.0:

            errors.append(
                f"{field} must be between 0 and 1"
            )

    return errors


def validate_dataset(
    examples: List[MLTrainingExample],
):

    errors = []
    valid_count = 0

    for index, example in enumerate(examples):

        example_errors = validate_example(
            example
        )

        if example_errors:

            for error in example_errors:

                errors.append(
                    f"example[{index}]: {error}"
                )

        else:
            valid_count += 1

    return ValidationReport(
        valid=not errors,
        total=len(examples),
        valid_examples=valid_count,
        invalid_examples=(
            len(examples) - valid_count
        ),
        errors=errors,
    )
