from dataclasses import dataclass
from typing import List

from app.ml.training_schema import MLTrainingExample


@dataclass
class PairwiseExample:
    case_state: dict
    preferred: dict
    rejected: dict
    metadata: dict


def build_pairwise_examples(
    examples: List[MLTrainingExample],
) -> List[PairwiseExample]:

    grouped = {}

    for example in examples:

        case_id = example.case_state.get(
            "case_id"
        )

        if not case_id:
            continue

        grouped.setdefault(
            case_id,
            []
        ).append(example)

    pairs = []

    for case_id, group in grouped.items():

        preferred = [
            item
            for item in group
            if item.preferred_action
        ]

        rejected = [
            item
            for item in group
            if not item.preferred_action
        ]

        for positive in preferred:

            for negative in rejected:

                pairs.append(
                    PairwiseExample(
                        case_state=(
                            positive.case_state
                        ),
                        preferred=(
                            positive.candidate_action
                        ),
                        rejected=(
                            negative.candidate_action
                        ),
                        metadata={
                            "case_id": case_id
                        },
                    )
                )

    return pairs
