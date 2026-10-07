from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class InvestigationAction:
    id: str
    action_type: str
    description: str

    target: str = ""

    expected_information_gain: float = 0.0
    expected_decision_impact: float = 0.0
    expected_evidence_value: float = 0.0
    expected_uncertainty_reduction: float = 0.0
    estimated_user_effort: float = 0.0

    evidence_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InvestigationStep:
    step_id: str
    action_id: str
    answer: Any = None

    evidence_ids: List[str] = field(default_factory=list)

    state_before: Dict[str, Any] = field(default_factory=dict)
    state_after: Dict[str, Any] = field(default_factory=dict)

    decision_changed: bool = False
    outcome: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Investigation:
    id: str
    case_id: str

    status: str = "active"

    steps: List[InvestigationStep] = field(default_factory=list)
    candidate_actions: List[InvestigationAction] = field(default_factory=list)

    selected_actions: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)
