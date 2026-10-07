from dataclasses import dataclass
from typing import List, Optional

from .case_model import CaseState


@dataclass
class QuestionCandidate:
    id: str
    text: str
    category: str
    target: str

    relevance: float = 0.0
    information_gain: float = 0.0
    decision_impact: float = 0.0
    evidence_value: float = 0.0
    uncertainty_reduction: float = 0.0
    user_effort: float = 0.0

    reason: str = ""

    def score(self) -> float:
        """
        Temporary transparent scoring function.

        This is NOT the final ML model.

        Later:
            score = trained_model(case_state, candidate)
        """

        return (
            self.relevance
            + self.information_gain
            + self.decision_impact
            + self.evidence_value
            + self.uncertainty_reduction
            - self.user_effort
        )


class QuestionGenerator:
    """
    Produces candidate questions from the current case state.

    Important:
    There are no hotel_question_1 / hotel_question_2 flows here.

    This interface is designed so candidate generation can later
    be backed by an LLM, retrieval system, learned model, or
    multiple specialist models.
    """

    def generate(
        self,
        state: CaseState,
    ) -> List[QuestionCandidate]:
        candidates: List[QuestionCandidate] = []

        if not state.objective:
            candidates.append(
                QuestionCandidate(
                    id="objective",
                    text=(
                        "What outcome are you trying to achieve, "
                        "and how will you decide whether the idea succeeded?"
                    ),
                    category="objective",
                    target="objective",
                    relevance=1.0,
                    information_gain=0.9,
                    decision_impact=1.0,
                    uncertainty_reduction=0.8,
                    user_effort=0.2,
                    reason="A decision system needs a measurable objective.",
                )
            )

        if not state.facts:
            candidates.append(
                QuestionCandidate(
                    id="current_state",
                    text=(
                        "What do you already have today, and what has "
                        "already been validated?"
                    ),
                    category="context",
                    target="current_state",
                    relevance=0.95,
                    information_gain=0.95,
                    decision_impact=0.85,
                    evidence_value=0.7,
                    uncertainty_reduction=0.9,
                    user_effort=0.25,
                    reason=(
                        "Understanding the starting state prevents IdX "
                        "from making unsupported assumptions."
                    ),
                )
            )

        if not state.constraints:
            candidates.append(
                QuestionCandidate(
                    id="constraints",
                    text=(
                        "What constraints could materially limit the "
                        "decision — budget, location, time, resources, "
                        "regulation, technology, or other restrictions?"
                    ),
                    category="constraints",
                    target="constraints",
                    relevance=0.9,
                    information_gain=0.9,
                    decision_impact=0.95,
                    uncertainty_reduction=0.85,
                    user_effort=0.35,
                    reason=(
                        "Constraints can eliminate otherwise attractive "
                        "strategies."
                    ),
                )
            )

        if state.unknowns:
            candidates.append(
                QuestionCandidate(
                    id="highest_impact_unknown",
                    text=(
                        "Which of the important unknowns are you currently "
                        "least certain about?"
                    ),
                    category="uncertainty",
                    target="unknowns",
                    relevance=1.0,
                    information_gain=1.0,
                    decision_impact=0.95,
                    uncertainty_reduction=1.0,
                    user_effort=0.25,
                    reason=(
                        "Reducing the most decision-relevant uncertainty "
                        "should take priority."
                    ),
                )
            )

        if state.contradictions:
            candidates.append(
                QuestionCandidate(
                    id="resolve_contradiction",
                    text=(
                        "There is conflicting information in the current "
                        "investigation. Which statement or assumption "
                        "should be verified first?"
                    ),
                    category="contradiction",
                    target="contradictions",
                    relevance=1.0,
                    information_gain=0.95,
                    decision_impact=1.0,
                    evidence_value=1.0,
                    uncertainty_reduction=0.95,
                    user_effort=0.3,
                    reason=(
                        "Contradictions can invalidate downstream analysis."
                    ),
                )
            )

        candidates.append(
            QuestionCandidate(
                id="decision_critical_factor",
                text=(
                    "What factor, if it turned out to be substantially "
                    "different from your current expectation, would most "
                    "change your decision?"
                ),
                category="decision",
                target="decision_critical_factor",
                relevance=0.55,
                information_gain=0.55,
                decision_impact=0.65,
                evidence_value=0.55,
                uncertainty_reduction=0.55,
                user_effort=0.3,
                reason=(
                    "IdX should investigate variables that can materially "
                    "change the final decision."
                ),
            )
        )

        return candidates


class QuestionRanker:
    """
    Ranks generated questions.

    This class deliberately has a clean model boundary.

    Current implementation:
        transparent scoring baseline.

    Future implementation:
        trained ML ranking model.
    """

    def rank(
        self,
        state: CaseState,
        candidates: List[QuestionCandidate],
    ) -> Optional[QuestionCandidate]:

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda candidate: candidate.score(),
        )


class AdaptiveQuestionEngine:
    def __init__(self) -> None:
        self.generator = QuestionGenerator()
        self.ranker = QuestionRanker()

    def next_question(
        self,
        state: CaseState,
    ) -> Optional[QuestionCandidate]:

        candidates = self.generator.generate(state)

        # Never ask the same question twice in one investigation.
        asked_ids = {
            item.get("question_id")
            for item in state.conversation
            if item.get("question_id")
        }

        candidates = [
            candidate
            for candidate in candidates
            if candidate.id not in asked_ids
        ]

        return self.ranker.rank(
            state,
            candidates,
        )
