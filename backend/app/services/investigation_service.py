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

from app.intelligence.investigation.action_ranker import (
    ActionRanker,
)
from app.intelligence.investigation.case_adapter import (
    to_investigation_case,
)
from app.intelligence.investigation.generic_candidate_generator import (
    GenericCandidateActionGenerator,
)
from app.intelligence.investigation.next_best_action import (
    NextBestActionEngine,
)


class InvestigationService:

    def __init__(self) -> None:
        self._investigations: Dict[str, Investigation] = {}
        self._states: Dict[str, CaseState] = {}

        self.question_engine = AdaptiveQuestionEngine()

        self.action_engine = NextBestActionEngine(
            generator=GenericCandidateActionGenerator(),
            ranker=ActionRanker(),
        )

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

    def _select_next_action(
        self,
        investigation_id: str,
    ):
        state = self._states[
            investigation_id
        ]

        intelligence_case = to_investigation_case(
            state,
            investigation_id,
        )

        return self.action_engine.decide(
            intelligence_case
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

        action_result = self._select_next_action(
            investigation_id
        )

        selected_action = action_result.selected

        investigation.candidate_actions = [
            {
                "id": ranked.action.action_id,
                "action_type": ranked.action.action_type.value,
                "description": ranked.action.description,
                "target": ranked.action.target,
                "score": ranked.score,
                "reasons": ranked.reasons,
            }
            for ranked in action_result.candidates
        ]

        investigation.current_action = None

        question = None

        if selected_action is not None:

            investigation.current_action = {
                "id": selected_action.action.action_id,
                "action_type": selected_action.action.action_type.value,
                "description": selected_action.action.description,
                "target": selected_action.action.target,
                "score": selected_action.score,
                "reasons": selected_action.reasons,
            }

            if (
                selected_action.action.action_type.value
                == "question"
            ):
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
            "current_action": investigation.current_action,
            "candidate_actions": investigation.candidate_actions,
        }


investigation_service = InvestigationService()
