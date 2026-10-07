from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class CaseState:
    case_id: str
    original_idea: str

    objective: str = ""

    domain: str = "unknown"
    archetype: str = "unknown"

    facts: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)

    factors: List[str] = field(default_factory=list)
    unknowns: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)

    evidence_ids: List[str] = field(default_factory=list)
    entity_ids: List[str] = field(default_factory=list)
    event_ids: List[str] = field(default_factory=list)

    decisions: List[str] = field(default_factory=list)
    experiments: List[str] = field(default_factory=list)
    outcomes: List[str] = field(default_factory=list)

    conversation: List[Dict[str, Any]] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)
