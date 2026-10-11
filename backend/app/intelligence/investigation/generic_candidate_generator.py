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
    Domain-agnostic action proposal layer.

    This component proposes possibilities.
    It does NOT decide which one is best.
    """

    def generate(
        self,
        case: CaseState,
    ) -> List[CandidateAction]:

        actions: List[CandidateAction] = []

        unknowns = list(case.unknowns)
        factors = list(case.factors)

        # ---------------------------------------------------------
        # Bootstrap
        # ---------------------------------------------------------

        if not case.objective:
            actions.append(
                CandidateAction(
                    action_id="question_objective",
                    action_type=ActionType.QUESTION,
                    description=(
                        "Ask the user what decision, outcome, "
                        "or objective this investigation should support."
                    ),
                    target="objective",
                    expected_information_gain=0.90,
                    expected_decision_impact=0.95,
                    expected_evidence_value=0.10,
                    expected_uncertainty_reduction=0.90,
                    estimated_user_effort=0.15,
                )
            )

        if not case.facts:
            actions.append(
                CandidateAction(
                    action_id="question_current_state",
                    action_type=ActionType.QUESTION,
                    description=(
                        "Ask the user for the most important "
                        "known facts or current situation."
                    ),
                    target="current_state",
                    expected_information_gain=0.80,
                    expected_decision_impact=0.75,
                    expected_evidence_value=0.10,
                    expected_uncertainty_reduction=0.75,
                    estimated_user_effort=0.20,
                )
            )

        # ---------------------------------------------------------
        # Unknowns
        # ---------------------------------------------------------

        for unknown in unknowns[:3]:

            actions.append(
                CandidateAction(
                    action_id=f"question_{unknown}",
                    action_type=ActionType.QUESTION,
                    description=(
                        f"Ask the user for information about {unknown}."
                    ),
                    target=unknown,
                    target_unknowns=[unknown],
                    expected_information_gain=0.70,
                    expected_decision_impact=0.60,
                    expected_evidence_value=0.10,
                    expected_uncertainty_reduction=0.65,
                    estimated_user_effort=0.20,
                )
            )

            actions.append(
                CandidateAction(
                    action_id=f"research_{unknown}",
                    action_type=ActionType.RESEARCH,
                    description=(
                        f"Research external evidence relevant to {unknown}."
                    ),
                    target=unknown,
                    target_unknowns=[unknown],
                    expected_information_gain=0.75,
                    expected_decision_impact=0.65,
                    expected_evidence_value=0.85,
                    expected_uncertainty_reduction=0.70,
                    estimated_user_effort=0.0,
                )
            )

            actions.append(
                CandidateAction(
                    action_id=f"verify_{unknown}",
                    action_type=ActionType.VERIFY,
                    description=(
                        f"Verify important claims associated with {unknown}."
                    ),
                    target=unknown,
                    target_unknowns=[unknown],
                    expected_information_gain=0.65,
                    expected_decision_impact=0.75,
                    expected_evidence_value=0.90,
                    expected_uncertainty_reduction=0.70,
                    estimated_user_effort=0.0,
                )
            )

        # ---------------------------------------------------------
        # Factors
        # ---------------------------------------------------------

        if factors:
            actions.append(
                CandidateAction(
                    action_id="analyze_factors",
                    action_type=ActionType.ANALYZE,
                    description=(
                        "Analyze relationships among known decision factors."
                    ),
                    target_factors=factors,
                    expected_information_gain=0.40,
                    expected_decision_impact=0.60,
                    expected_evidence_value=0.20,
                    expected_uncertainty_reduction=0.35,
                    estimated_user_effort=0.0,
                )
            )

            if len(factors) >= 2:
                actions.append(
                    CandidateAction(
                        action_id="compare_factors",
                        action_type=ActionType.COMPARE,
                        description=(
                            "Compare the most decision-relevant "
                            "alternatives or factors."
                        ),
                        target_factors=factors,
                        expected_information_gain=0.50,
                        expected_decision_impact=0.65,
                        expected_evidence_value=0.20,
                        expected_uncertainty_reduction=0.40,
                        estimated_user_effort=0.0,
                    )
                )

        # ---------------------------------------------------------
        # Constraints
        # ---------------------------------------------------------

        if case.constraints:
            actions.append(
                CandidateAction(
                    action_id="check_constraints",
                    action_type=ActionType.CHECK_CONSTRAINT,
                    description=(
                        "Check whether the current proposal satisfies "
                        "important constraints."
                    ),
                    expected_information_gain=0.50,
                    expected_decision_impact=0.70,
                    expected_evidence_value=0.30,
                    expected_uncertainty_reduction=0.50,
                    estimated_user_effort=0.0,
                )
            )

        # ---------------------------------------------------------
        # Similar cases
        # ---------------------------------------------------------

        actions.append(
            CandidateAction(
                action_id="similar_cases",
                action_type=ActionType.FIND_SIMILAR_CASE,
                description=(
                    "Find historically similar cases and examine "
                    "their decisions and outcomes."
                ),
                expected_information_gain=0.45,
                expected_decision_impact=0.45,
                expected_evidence_value=0.65,
                expected_uncertainty_reduction=0.40,
                estimated_user_effort=0.0,
            )
        )

        # ---------------------------------------------------------
        # Stop
        # ---------------------------------------------------------

        actions.append(
            CandidateAction(
                action_id="evaluate_stopping",
                action_type=ActionType.STOP_INVESTIGATION,
                description=(
                    "Evaluate whether additional investigation "
                    "is unlikely to materially change the decision."
                ),
                expected_information_gain=0.05,
                expected_decision_impact=0.50,
                expected_evidence_value=0.0,
                expected_uncertainty_reduction=0.05,
                estimated_user_effort=0.0,
            )
        )

        return actions
