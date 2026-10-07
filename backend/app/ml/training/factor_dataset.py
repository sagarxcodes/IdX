from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class FactorTrainingExample:
    """
    Supervision for discovering decision-relevant factors.

    A positive factor is one that materially contributed to
    investigation, decision, or outcome.

    Labels must eventually come from evidence, experts,
    historical cases, or observed outcomes.
    """

    case_state: Dict[str, Any]

    factor: Dict[str, Any]

    relevant: bool = False

    importance: float = 0.0

    uncertainty: float = 1.0

    evidence_ids: List[str] = field(
        default_factory=list
    )

    decision_impact: float = 0.0

    outcome_impact: float = 0.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )
