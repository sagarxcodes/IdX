from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class FactorKnowledgeRecord:
    case_id: str
    case_state: Dict[str, Any]

    factor: Dict[str, Any]

    relevant: bool
    importance: float
    uncertainty: float

    # Why this factor matters in this case.
    relevance_reason: str = ""

    # What evidence would allow IdX to evaluate it.
    evidence_requirements: List[str] = field(default_factory=list)

    # Relationships to other factors.
    relationships: List[Dict[str, Any]] = field(default_factory=list)

    # Whether importance depends on another condition.
    conditions: List[Dict[str, Any]] = field(default_factory=list)

    # Expected effect on a decision.
    decision_impact: float = 0.0

    # Expected effect on eventual real-world outcome.
    outcome_impact: float = 0.0

    metadata: Dict[str, Any] = field(default_factory=dict)
