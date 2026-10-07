from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class CaseFactor:
    """
    A variable that may materially influence a case decision.
    """

    factor_id: str
    name: str

    category: str = "unknown"

    description: str = ""

    value: Any = None

    unit: str = ""

    # 1 = highly important to the current decision.
    importance: float = 0.0

    # 1 = highly uncertain.
    uncertainty: float = 1.0

    # Evidence supporting this factor.
    evidence_ids: List[str] = field(
        default_factory=list
    )

    # Relationships to other factors.
    related_factors: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )
