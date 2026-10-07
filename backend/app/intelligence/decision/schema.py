from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class DecisionOption:
    id: str
    name: str
    description: str = ""

    expected_value: float = 0.0
    risk: float = 0.0
    feasibility: float = 0.0

    supporting_evidence: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)


@dataclass
class Decision:
    id: str
    case_id: str
    objective: str

    options: List[DecisionOption] = field(default_factory=list)

    selected_option: str = ""
    rationale: str = ""

    confidence: float = 0.0
    evidence_ids: List[str] = field(default_factory=list)

    risks: List[str] = field(default_factory=list)
    alternatives: List[str] = field(default_factory=list)
