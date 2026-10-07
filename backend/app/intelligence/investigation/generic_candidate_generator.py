from __future__ import annotations

from typing import List

from app.intelligence.case.schema import CaseState
from app.intelligence.investigation.action import CandidateAction
from app.intelligence.investigation.action_taxonomy import ActionType
from app.intelligence.investigation.candidate_generator import (
    CandidateActionGenerator,
)


class GenericCandidateActionGenerator(
    CandidateActionGenerator
):
    """
    Temporary candidate generator.

    It does NOT decide the best action.
    It only proposes broadly applicable actions
    based on the current case state.

    The production version will use learned factor/action
    discovery and retrieval rather than fixed heuristics.
    """

    def generate(
        self,
        case: CaseState,
    ) -> List[CandidateAction]:

        actions: List[CandidateAction] = []

        unknowns = list(case.unknowns)
        factors = list(case.factors)

        # ---------------------------------------------------------
        # User information
        # ---------------------------------------------------------

        if unknowns:
            target = unknowns[0]

            actions.append(
                CandidateAction(
                    action_id=f"question_{target}",
                    action_type=ActionType.QUESTION,
                    description=(
                        f"Ask the user for the missing information "
                        f"needed to understand {target}."
                    ),
                    target=target,
                    target_unknowns=[target],
                    estimated_user_effort=0.20,
                )
            )

        # ---------------------------------------------------------
        # Evidence acquisition
        # ---------------------------------------------------------

        if unknowns:
            target = unknowns[0]

            actions.append(
                CandidateAction(
                    action_id=f"research_{target}",
                    action_type=ActionType.RESEARCH,
                    description=(
                        f"Research reliable external evidence "
                        f"about {target}."
                    ),
                    target=target,
                    target_unknowns=[target],
                    estimated_user_effort=0.0,
                )
            )

            actions.append(
                CandidateAction(
                    action_id=f"verify_{target}",
                    action_type=ActionType.VERIFY,
                    description=(
                        f"Verify the most decision-relevant claims "
                        f"related to {target}."
                    ),
                    target=target,
                    target_unknowns=[target],
                    estimated_user_effort=0.0,
                )
            )

        # ---------------------------------------------------------
        # Factor analysis
        # ---------------------------------------------------------

        if factors:
            actions.append(
                CandidateAction(
                    action_id="analyze_factors",
                    action_type=ActionType.ANALYZE,
                    description=(
                        "Analyze relationships among the currently "
                        "known decision factors."
                    ),
                    target_factors=factors,
                    estimated_user_effort=0.0,
                )
            )

            actions.append(
                CandidateAction(
                    action_id="compare_factors",
                    action_type=ActionType.COMPARE,
                    description=(
                        "Compare the most important available "
                        "alternatives or factor values."
                    ),
                    target_factors=factors,
                    estimated_user_effort=0.0,
                )
            )

        # ---------------------------------------------------------
        # Constraint analysis
        # ---------------------------------------------------------

        if case.constraints:
            actions.append(
                CandidateAction(
                    action_id="check_constraints",
                    action_type=ActionType.CHECK_CONSTRAINT,
                    description=(
                        "Check whether the current proposal satisfies "
                        "its important constraints."
                    ),
                    estimated_user_effort=0.0,
                )
            )

        # ---------------------------------------------------------
        # Similar historical cases
        # ---------------------------------------------------------

        actions.append(
            CandidateAction(
                action_id="similar_cases",
                action_type=ActionType.FIND_SIMILAR_CASE,
                description=(
                    "Find historically similar cases and examine "
                    "their decisions and outcomes."
                ),
                estimated_user_effort=0.0,
            )
        )

        # ---------------------------------------------------------
        # Investigation stopping decision
        # ---------------------------------------------------------

        actions.append(
            CandidateAction(
                action_id="evaluate_stopping",
                action_type=ActionType.STOP_INVESTIGATION,
                description=(
                    "Evaluate whether additional investigation "
                    "is unlikely to materially change the decision."
                ),
                estimated_user_effort=0.0,
            )
        )

        return actions
