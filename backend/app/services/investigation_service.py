from datetime import datetime
from typing import Dict
from uuid import uuid4

from app.intelligence.case_model import CaseState
from app.intelligence.domain_detector import detect_domain
from app.intelligence.question_engine import (
    AdaptiveQuestionEngine,
)
from app.data_engine.retrieval.research import (
    retrieve_research_evidence,
)
from app.data_engine.retrieval.discussions import (
    retrieve_discussion_evidence,
)
from app.data_engine.synthesis.evidence_context import (
    evidence_context_builder,
)
from app.intelligence.signals.signal_engine import signal_engine
from app.intelligence.signals.case_signal_analyzer import case_signal_analyzer
from app.intelligence.decision_analyzer import decision_analyzer
from app.models.investigation import Investigation


class InvestigationService:

    def __init__(self) -> None:
        self._investigations: Dict[str, Investigation] = {}
        self._states: Dict[str, CaseState] = {}

        self.question_engine = AdaptiveQuestionEngine()

    def create(self, idea: str) -> Investigation:
        domain_result = detect_domain(idea)

        investigation_id = "inv_" + uuid4().hex[:12]

        state = CaseState(
            original_idea=idea,
            domain=domain_result.domain,
        )

        investigation = Investigation(
            id=investigation_id,
            original_idea=idea,
            domain=domain_result.domain,
            domain_confidence=domain_result.confidence,
        )

        self._states[investigation_id] = state
        self._investigations[investigation_id] = investigation

        self._sync_investigation(investigation_id)

        return investigation

    def get(
        self,
        investigation_id: str,
    ) -> Investigation:

        investigation = self._investigations.get(
            investigation_id
        )

        if investigation is None:
            raise KeyError(investigation_id)

        return investigation

    def answer(
        self,
        investigation_id: str,
        question_id: str,
        answer: str,
    ) -> Investigation:

        investigation = self.get(
            investigation_id
        )

        state = self._states[
            investigation_id
        ]

        current = investigation.current_question

        if current is None:
            raise ValueError(
                "Investigation has no active question."
            )

        if current["id"] != question_id:
            raise ValueError(
                "The supplied question is not the current "
                "investigation question."
            )

        state.conversation.append(
            {
                "question_id": question_id,
                "question": current["text"],
                "answer": answer,
            }
        )

        investigation.answers.append(
            {
                "question_id": question_id,
                "question": current["text"],
                "answer": answer,
            }
        )

        investigation.questions_asked.append(
            question_id
        )

        investigation.question_count += 1

        self._apply_answer(
            state,
            current,
            answer,
        )

        self._sync_investigation(
            investigation_id
        )

        return investigation

    def _apply_answer(
        self,
        state: CaseState,
        question: dict,
        answer: str,
    ) -> None:

        target = question.get(
            "target",
            question.get("category", "unknown"),
        )

        answer = answer.strip()

        if target == "objective":
            state.objective = answer
            return

        if target == "constraints":
            state.constraints["general"] = answer
            return

        # If the user explicitly describes their desired outcome
        # while answering a context question, preserve it as the
        # investigation objective instead of losing it as a generic fact.
        objective_markers = (
            "objective",
            "goal",
            "aim",
            "want to",
            "trying to",
            "financially viable",
            "successful",
        )

        if (
            target == "current_state"
            and any(marker in answer.lower() for marker in objective_markers)
        ):
            state.objective = answer

        state.add_fact(
            target,
            answer,
        )

    def _sync_investigation(
        self,
        investigation_id: str,
    ) -> None:

        investigation = self._investigations[
            investigation_id
        ]

        state = self._states[
            investigation_id
        ]

        research_query = self._build_research_query(state)

        research_evidence = retrieve_research_evidence(
            research_query,
            limit=3,
        )

        discussion_evidence = retrieve_discussion_evidence(
            research_query,
            limit=5,
        )

        state.evidence = research_evidence + discussion_evidence

        evidence_context = evidence_context_builder.build(
            research_query,
            state.evidence,
        )

        state.facts["_evidence_context"] = evidence_context.context_text
        state.facts["_evidence_source_types"] = (
            evidence_context.source_types
        )
        state.facts["_evidence_count"] = (
            evidence_context.evidence_count
        )

        signals = signal_engine.extract(
            state.evidence,
            case_text=research_query,
        )

        signal_summary = case_signal_analyzer.analyze(
            signals
        )

        state.signal_summary = {
            "pain_points": signal_summary.pain_points,
            "needs": signal_summary.needs,
            "suggestions": signal_summary.suggestions,
            "failure_factors": signal_summary.failure_factors,
            "opportunity_factors": signal_summary.opportunity_factors,
            "recurring_factors": signal_summary.recurring_factors,
        }

        state.facts["_decision_analysis"] = decision_analyzer.analyze(state)

        question = self.question_engine.next_question(
            state
        )

        investigation.archetype = state.archetype
        investigation.objective = state.objective

        investigation.facts = {
            key: str(value)
            for key, value in state.facts.items()
        }

        investigation.assumptions = list(
            state.assumptions
        )

        investigation.unknowns = list(
            state.unknowns
        )

        investigation.contradictions = list(
            state.contradictions
        )

        investigation.evidence = list(
            state.evidence
        )

        if question is None:
            investigation.current_question = None
            investigation.status = "analysis_ready"
        else:
            investigation.current_question = {
                "id": question.id,
                "text": question.text,
                "reason": question.reason,
                "category": question.category,
                "target": question.target,
            }

            investigation.status = "investigating"

        investigation.updated_at = datetime.utcnow()

    def _build_research_query(
        self,
        state: CaseState,
    ) -> str:
        parts = [
            state.original_idea,
            state.objective,
        ]

        parts.extend(
            str(value)
            for value in state.facts.values()
        )

        parts.extend(
            str(value)
            for value in state.constraints.values()
        )

        parts.extend(state.unknowns)
        parts.extend(state.assumptions)

        return " ".join(
            part.strip()
            for part in parts
            if part and str(part).strip()
        )


    def serialize(
        self,
        investigation: Investigation,
    ) -> dict:

        return {
            "id": investigation.id,
            "original_idea": investigation.original_idea,
            "domain": investigation.domain,
            "domain_confidence": investigation.domain_confidence,
            "archetype": investigation.archetype,
            "objective": investigation.objective,
            "status": investigation.status,
            "facts": investigation.facts,
            "assumptions": investigation.assumptions,
            "unknowns": investigation.unknowns,
            "contradictions": investigation.contradictions,
            "evidence": investigation.evidence,
            "signal_summary": self._states[investigation.id].signal_summary,
            "decision_analysis": self._states[investigation.id].facts.get(
                "_decision_analysis",
                {},
            ),
            "answers": investigation.answers,
            "questions_asked": investigation.questions_asked,
            "current_question": investigation.current_question,
            "question_count": investigation.question_count,
        }


investigation_service = InvestigationService()
