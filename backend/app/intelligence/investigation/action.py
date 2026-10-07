from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from app.intelligence.investigation.action_taxonomy import ActionType


@dataclass
class CandidateAction:
    action_id: str
    action_type: ActionType

    description: str
    target: str = ""

    # What this action is expected to change.
    target_factors: List[str] = field(
        default_factory=list
    )

    target_unknowns: List[str] = field(
        default_factory=list
    )

    # Current contextual information.
    required_information: List[str] = field(
        default_factory=list
    )

    available_evidence_ids: List[str] = field(
        default_factory=list
    )

    # These are EXPECTATIONS, not ground-truth labels.
    expected_information_gain: float = 0.0
    expected_decision_impact: float = 0.0
    expected_evidence_value: float = 0.0
    expected_uncertainty_reduction: float = 0.0
    estimated_user_effort: float = 0.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )
