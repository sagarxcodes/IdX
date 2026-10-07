from collections import Counter
from typing import List

from app.ml.training_schema import MLTrainingExample


def summarize(
    examples: List[MLTrainingExample],
):

    domains = Counter()
    preferred = 0
    rejected = 0
    outcomes = 0

    for example in examples:

        domains[
            example.case_state.get(
                "domain",
                "unknown",
            )
        ] += 1

        if example.preferred_action:
            preferred += 1
        else:
            rejected += 1

        if example.outcome:
            outcomes += 1

    return {
        "total": len(examples),
        "domains": dict(domains),
        "preferred_actions": preferred,
        "rejected_actions": rejected,
        "with_outcomes": outcomes,
    }
