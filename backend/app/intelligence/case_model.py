from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class CaseState:
    """
    Domain-independent representation of an IdX investigation.

    This is intentionally not business-specific.
    The same structure can represent a hotel, SaaS product,
    engineering system, investment, agriculture problem, etc.
    """

    original_idea: str

    domain: str = "unknown"
    archetype: str = "unknown"
    objective: str = ""

    facts: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)

    unknowns: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)

    evidence: List[Dict[str, Any]] = field(default_factory=list)
    signal_summary: Dict[str, Any] = field(default_factory=dict)

    decisions: List[Dict[str, Any]] = field(default_factory=list)
    experiments: List[Dict[str, Any]] = field(default_factory=list)
    outcomes: List[Dict[str, Any]] = field(default_factory=list)

    conversation: List[Dict[str, str]] = field(default_factory=list)

    def add_fact(self, key: str, value: Any) -> None:
        self.facts[key] = value

    def add_unknown(self, unknown: str) -> None:
        if unknown not in self.unknowns:
            self.unknowns.append(unknown)

    def resolve_unknown(self, unknown: str) -> None:
        if unknown in self.unknowns:
            self.unknowns.remove(unknown)

    def add_assumption(self, assumption: str) -> None:
        if assumption not in self.assumptions:
            self.assumptions.append(assumption)

    def add_contradiction(self, contradiction: str) -> None:
        if contradiction not in self.contradictions:
            self.contradictions.append(contradiction)
