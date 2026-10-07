from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class QuestionTrainingRecord:
    """
    Training/evaluation record for the future learned question-ranking model.

    Each interaction can eventually become a training example.

    The key learning target is not:
        "Which question comes next?"

    It is:
        "Given this case state, which question produces the
         greatest useful reduction in decision uncertainty?"
    """

    case_state: Dict[str, Any]
    candidate_question: Dict[str, Any]

    information_gain: Optional[float] = None
    decision_impact: Optional[float] = None
    evidence_value: Optional[float] = None
    uncertainty_reduction: Optional[float] = None

    user_effort: Optional[float] = None

    answer: Optional[str] = None
    downstream_decision_change: Optional[bool] = None
    outcome: Optional[Dict[str, Any]] = None
