from __future__ import annotations

from dataclasses import dataclass
from typing import List

from app.intelligence.case.schema import CaseState
from app.intelligence.investigation.action import CandidateAction
from app.intelligence.investigation.action_ranker import (
    ActionRanker,
    RankedAction,
)
from app.intelligence.investigation.candidate_generator import (
    CandidateActionGenerator,
)


@dataclass
class NextBestActionResult:
    selected: RankedAction | None
    candidates: List[RankedAction]


class NextBestActionEngine:
    """
    Central adaptive action-selection layer.

    CaseState
        -> candidate generation
        -> ranking
        -> next best action

    Execution is intentionally separate.
    """

    def __init__(
        self,
        generator: CandidateActionGenerator,
        ranker: ActionRanker,
    ):
        self.generator = generator
        self.ranker = ranker

    def decide(
        self,
        case: CaseState,
    ) -> NextBestActionResult:

        candidates: List[CandidateAction] = (
            self.generator.generate(case)
        )

        ranked = self.ranker.rank(
            case,
            candidates,
        )

        return NextBestActionResult(
            selected=ranked[0] if ranked else None,
            candidates=ranked,
        )
