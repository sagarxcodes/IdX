from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class FactorPrediction:
    factor_id: str
    name: str
    category: str

    relevance: float
    uncertainty: float
    importance: float

    reasoning: str = ""


class FactorDiscoveryModel:
    """
    Contract for the learned IdX factor-discovery model.

    Production implementation will be learned from cases,
    evidence, decisions and outcomes.
    """

    model_name = "factor-discovery"

    def predict(
        self,
        case_state: Dict[str, Any],
        context: Dict[str, Any],
    ) -> List[FactorPrediction]:
        raise NotImplementedError
