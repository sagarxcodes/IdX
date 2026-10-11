from __future__ import annotations

from dataclasses import dataclass
from typing import List

from app.intelligence.case.schema import CaseState
from app.intelligence.investigation.action import CandidateAction
from app.intelligence.investigation.action_taxonomy import ActionType


@dataclass
class RankedAction:
    action: CandidateAction
    score: float
    reasons: List[str]


class ActionRanker:
    """
    Transparent baseline action-ranking engine.

    Candidate generation proposes possibilities.
    This component determines which possibility is currently
    most valuable.

    Later this can be replaced/augmented by a learned ranking
    model trained from IdX interaction outcomes.
    """

    def rank(
        self,
        case: CaseState,
        candidates: List[CandidateAction],
    ) -> List[RankedAction]:

        ranked = []

        for action in candidates:
            score, reasons = self._score(case, action)

            ranked.append(
                RankedAction(
                    action=action,
                    score=score,
                    reasons=reasons,
                )
            )

        ranked.sort(
            key=lambda item: item.score,
            reverse=True,
        )


        # ----------------------------------------------------------
        # IdX investigation-phase priority
        # ----------------------------------------------------------
        if not case.objective:
            for _item in ranked:
                _action = getattr(_item, "action", _item)
                _action_id = str(getattr(_action, "action_id", "")).lower()
                _action_type = getattr(_action, "action_type", None)
                _action_type_value = str(getattr(_action_type, "value", _action_type)).lower()
                if _action_id == "question_objective":
                    _item.score += 100.0
                elif "similar_case" in _action_id or "find_similar_case" in _action_type_value:
                    _item.score -= 50.0
                elif "stop_investigation" in _action_type_value:
                    _item.score -= 100.0

        elif not case.facts:
            for _item in ranked:
                _action = getattr(_item, "action", _item)
                _action_id = str(getattr(_action, "action_id", "")).lower()
                _action_type = getattr(_action, "action_type", None)
                _action_type_value = str(getattr(_action_type, "value", _action_type)).lower()
                if _action_id == "question_current_state":
                    _item.score += 80.0
                elif "similar_case" in _action_id or "find_similar_case" in _action_type_value:
                    _item.score -= 30.0

        ranked.sort(key=lambda _item: _item.score, reverse=True)

        # ==========================================================
        # IdX investigation priority policy
        # ==========================================================
        # Critical contradictions must be resolved before asking
        # generic questions or performing lower-value research.
        if case.contradictions:
            for _item in ranked:
                _action = getattr(_item, "action", _item)
                _action_id = str(getattr(_action, "action_id", "")).lower()
                _action_type = getattr(_action, "action_type", None)
                _action_type_value = str(
                    getattr(_action_type, "value", _action_type)
                ).lower()
        
                if _action_type_value == "verify":
                    _item.score += 1000.0
                elif "stop_investigation" in _action_type_value:
                    _item.score -= 1000.0
        
        # Bootstrap: establish the objective before deeper analysis.
        elif not case.objective:
            for _item in ranked:
                _action = getattr(_item, "action", _item)
                _action_id = str(getattr(_action, "action_id", "")).lower()
                _action_type = getattr(_action, "action_type", None)
                _action_type_value = str(
                    getattr(_action_type, "value", _action_type)
                ).lower()
        
                if _action_id == "question_objective":
                    _item.score += 1000.0
                elif "similar_case" in _action_id:
                    _item.score -= 500.0
                elif "stop_investigation" in _action_type_value:
                    _item.score -= 1000.0
        
        # Bootstrap: after objective, establish the current state.
        elif not case.facts:
            for _item in ranked:
                _action = getattr(_item, "action", _item)
                _action_id = str(getattr(_action, "action_id", "")).lower()
                _action_type = getattr(_action, "action_type", None)
                _action_type_value = str(
                    getattr(_action_type, "value", _action_type)
                ).lower()
        
                if _action_id == "question_current_state":
                    _item.score += 900.0
                elif "similar_case" in _action_id:
                    _item.score -= 300.0
        
        ranked.sort(
            key=lambda _item: _item.score,
            reverse=True,
        )

        # ==========================================================
        # IdX investigation priority policy
        # ==========================================================
        # Critical contradictions must be resolved before asking
        # generic questions or performing lower-value research.
        if case.contradictions:
            for _item in ranked:
                _action = getattr(_item, "action", _item)
                _action_id = str(getattr(_action, "action_id", "")).lower()
                _action_type = getattr(_action, "action_type", None)
                _action_type_value = str(
                    getattr(_action_type, "value", _action_type)
                ).lower()
        
                if _action_type_value == "verify":
                    _item.score += 1000.0
                elif "stop_investigation" in _action_type_value:
                    _item.score -= 1000.0
        
        # Bootstrap: establish the objective before deeper analysis.
        elif not case.objective:
            for _item in ranked:
                _action = getattr(_item, "action", _item)
                _action_id = str(getattr(_action, "action_id", "")).lower()
                _action_type = getattr(_action, "action_type", None)
                _action_type_value = str(
                    getattr(_action_type, "value", _action_type)
                ).lower()
        
                if _action_id == "question_objective":
                    _item.score += 1000.0
                elif "similar_case" in _action_id:
                    _item.score -= 500.0
                elif "stop_investigation" in _action_type_value:
                    _item.score -= 1000.0
        
        # Bootstrap: after objective, establish the current state.
        elif not case.facts:
            for _item in ranked:
                _action = getattr(_item, "action", _item)
                _action_id = str(getattr(_action, "action_id", "")).lower()
                _action_type = getattr(_action, "action_type", None)
                _action_type_value = str(
                    getattr(_action_type, "value", _action_type)
                ).lower()
        
                if _action_id == "question_current_state":
                    _item.score += 900.0
                elif "similar_case" in _action_id:
                    _item.score -= 300.0
        
        ranked.sort(
            key=lambda _item: _item.score,
            reverse=True,
        )
        return ranked

    def select(
        self,
        case: CaseState,
        candidates: List[CandidateAction],
    ) -> RankedAction | None:

        ranked = self.rank(case, candidates)

        return ranked[0] if ranked else None

    def _score(
        self,
        case: CaseState,
        action: CandidateAction,
    ) -> tuple[float, List[str]]:

        reasons: List[str] = []

        information_gain = self._clamp(
            action.expected_information_gain
        )
        decision_impact = self._clamp(
            action.expected_decision_impact
        )
        evidence_value = self._clamp(
            action.expected_evidence_value
        )
        uncertainty_reduction = self._clamp(
            action.expected_uncertainty_reduction
        )
        user_effort = self._clamp(
            action.estimated_user_effort
        )

        unknown_count = len(case.unknowns)

        uncertainty = (
            min(1.0, 0.30 + unknown_count * 0.10)
            if unknown_count
            else 0.10
        )

        if case.contradictions:
            uncertainty = max(uncertainty, 0.80)
            reasons.append(
                "Unresolved contradictions are present."
            )

        evidence_count = len(case.evidence_ids)

        if evidence_count == 0:
            evidence_gap = 1.0
        elif evidence_count < 3:
            evidence_gap = 0.75
        elif evidence_count < 8:
            evidence_gap = 0.45
        else:
            evidence_gap = 0.20

        relevance = self._calculate_relevance(
            case,
            action,
        )

        action_prior = 0.0

        if action.action_type == ActionType.VERIFY:
            if case.contradictions:
                action_prior += 0.35
                reasons.append(
                    "Verification is prioritized because evidence conflicts."
                )

        elif action.action_type == ActionType.RESEARCH:
            if evidence_gap > 0.7:
                action_prior += 0.30
                reasons.append(
                    "The case has a large evidence gap."
                )

        elif action.action_type == ActionType.RETRIEVE_EVIDENCE:
            if evidence_gap > 0.5:
                action_prior += 0.25

        elif action.action_type == ActionType.QUESTION:
            if unknown_count:
                action_prior += 0.20
                reasons.append(
                    "Important information is missing."
                )

        elif action.action_type == ActionType.ANALYZE:
            if case.factors:
                action_prior += 0.15

        elif action.action_type == ActionType.COMPARE:
            if len(case.factors) >= 2:
                action_prior += 0.15

        elif action.action_type == ActionType.FIND_SIMILAR_CASE:
            if evidence_gap > 0.5:
                action_prior += 0.10

        elif action.action_type == ActionType.STOP_INVESTIGATION:
            if (
                evidence_gap < 0.25
                and uncertainty < 0.25
                and not case.contradictions
            ):
                action_prior += 0.50
            else:
                action_prior -= 0.30

        raw_value = (
            0.25 * information_gain
            + 0.25 * decision_impact
            + 0.15 * evidence_value
            + 0.15 * uncertainty_reduction
            + 0.10 * uncertainty
            + 0.10 * evidence_gap
        )

        raw_value *= relevance
        raw_value += action_prior

        score = raw_value - (0.20 * user_effort)

        if action.action_type in {
            ActionType.RESEARCH,
            ActionType.RETRIEVE_EVIDENCE,
            ActionType.VERIFY,
            ActionType.FIND_SIMILAR_CASE,
        } and evidence_gap > 0.7:
            score += 0.10

        if unknown_count:
            reasons.append(
                f"{unknown_count} unresolved unknown(s)."
            )

        if evidence_count == 0:
            reasons.append(
                "No evidence is currently attached."
            )

        reasons.append(
            f"Relevance={relevance:.2f}"
        )
        reasons.append(
            f"DecisionImpact={decision_impact:.2f}"
        )
        reasons.append(
            f"InformationGain={information_gain:.2f}"
        )

        return max(0.0, score), reasons

    def _calculate_relevance(
        self,
        case: CaseState,
        action: CandidateAction,
    ) -> float:

        relevance = 0.50

        if action.target_unknowns:
            matching = sum(
                1
                for unknown in action.target_unknowns
                if unknown in case.unknowns
            )

            if matching:
                relevance += 0.30

        if action.target_factors:
            matching = sum(
                1
                for factor in action.target_factors
                if factor in case.factors
            )

            relevance += min(
                0.20,
                matching * 0.05,
            )

        if (
            case.contradictions
            and action.action_type == ActionType.VERIFY
        ):
            relevance += 0.20

        return min(1.0, relevance)

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(1.0, float(value)))
