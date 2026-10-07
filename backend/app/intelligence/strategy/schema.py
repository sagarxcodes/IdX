from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Strategy:
    id: str
    decision_id: str

    objectives: List[str] = field(default_factory=list)
    initiatives: List[str] = field(default_factory=list)

    resources: Dict[str, Any] = field(default_factory=dict)
    timeline: Dict[str, Any] = field(default_factory=dict)

    risks: List[str] = field(default_factory=list)
    experiments: List[str] = field(default_factory=list)

    success_metrics: Dict[str, Any] = field(default_factory=dict)
