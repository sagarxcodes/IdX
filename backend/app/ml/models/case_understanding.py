from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ModelPrediction:
    label: str
    confidence: float


@dataclass
class CaseUnderstandingPrediction:
    domain: ModelPrediction
    archetype: ModelPrediction
    entities: Dict[str, Any]
    claims: List[str]
    constraints: Dict[str, Any]


class CaseUnderstandingModel:
    """
    Interface for the learned Case Understanding Model.

    Production implementations may use:
        - transformer encoder
        - instruction-tuned LLM
        - fine-tuned extraction model
        - hybrid retrieval + model architecture

    The rest of IdX must depend on this interface,
    not on keyword rules.
    """

    model_name = "case-understanding"

    def predict(
        self,
        text: str,
        context: Dict[str, Any],
    ) -> CaseUnderstandingPrediction:
        raise NotImplementedError
