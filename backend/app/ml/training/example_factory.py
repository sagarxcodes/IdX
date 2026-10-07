from typing import Any, Dict, List, Optional

from app.ml.training_schema import MLTrainingExample


class TrainingExampleFactory:
    """
    Converts real investigation transitions into ML training examples.

    The factory does not invent labels.
    Labels must come from investigation evidence,
    expert annotation, or observed outcomes.
    """

    def from_transition(
        self,
        case_state: Dict[str, Any],
        candidate_action: Dict[str, Any],
        *,
        evidence_context: Optional[List[Dict[str, Any]]] = None,
        historical_cases: Optional[List[Dict[str, Any]]] = None,
        preferred_action: bool = False,
        information_gain: float = 0.0,
        decision_impact: float = 0.0,
        evidence_value: float = 0.0,
        uncertainty_reduction: float = 0.0,
        user_effort: float = 0.0,
        downstream_decision_change: bool = False,
        outcome: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MLTrainingExample:

        return MLTrainingExample(
            case_state=case_state,
            candidate_action=candidate_action,
            evidence_context=evidence_context or [],
            historical_cases=historical_cases or [],
            preferred_action=preferred_action,
            information_gain=information_gain,
            decision_impact=decision_impact,
            evidence_value=evidence_value,
            uncertainty_reduction=uncertainty_reduction,
            user_effort=user_effort,
            downstream_decision_change=(
                downstream_decision_change
            ),
            outcome=outcome or {},
            metadata=metadata or {},
        )
