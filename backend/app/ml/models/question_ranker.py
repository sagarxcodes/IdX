from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class QuestionRankingPrediction:
    question_id: str
    score: float
    confidence: float


class QuestionRankingModel:
    """
    Learned next-question / next-action ranking model.

    Input:
        current investigation state
        candidate actions/questions
        evidence state
        objective
        uncertainty
        previous outcomes

    Output:
        expected value of each candidate.

    This intentionally has no domain-specific logic.
    """

    model_name = "question-ranking"

    def rank(
        self,
        state: Dict[str, Any],
        candidates: List[Dict[str, Any]],
    ) -> List[QuestionRankingPrediction]:
        raise NotImplementedError
