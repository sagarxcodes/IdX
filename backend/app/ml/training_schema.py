from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class MLTrainingExample:
    """
    One supervised investigation decision.

    This records why one candidate action was preferred
    over another. It does NOT imply that bootstrap labels
    are real-world outcomes.
    """

    case_state: Dict[str, Any]

    preferred_action: Dict[str, Any]
    rejected_action: Dict[str, Any]

    evidence_context: List[Dict[str, Any]] = field(
        default_factory=list
    )

    historical_cases: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # Supervision.
    preferred: bool = True

    information_gain: float = 0.0
    decision_impact: float = 0.0
    evidence_value: float = 0.0
    uncertainty_reduction: float = 0.0
    user_effort: float = 0.0

    downstream_decision_change: bool = False

    outcome: Dict[str, Any] = field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )
