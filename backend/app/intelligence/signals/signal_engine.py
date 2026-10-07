from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class EvidenceSignal:
    signal_id: str
    signal_type: str
    text: str
    source_type: str
    source_id: str
    strength: float = 0.0
    relevance: float = 0.0
    factors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class SignalEngine:
    """
    Converts heterogeneous evidence into decision-relevant signals.

    This is intentionally a transparent baseline for the submission.
    A learned signal extraction/ranking model can replace the heuristics later.
    """

    COMPLAINT_TERMS = {
        "problem",
        "issue",
        "difficult",
        "bad",
        "poor",
        "lack",
        "lacking",
        "expensive",
        "unavailable",
        "crowded",
        "slow",
        "failed",
        "failure",
        "disappointed",
        "complaint",
        "couldn't",
        "cannot",
    }

    NEED_TERMS = {
        "need",
        "needs",
        "looking for",
        "wish",
        "want",
        "require",
        "required",
        "prefer",
        "would like",
    }

    SUGGESTION_TERMS = {
        "should",
        "could",
        "suggest",
        "recommend",
        "offer",
        "provide",
        "add",
        "improve",
        "better",
    }

    def extract(
        self,
        evidence: List[Dict[str, Any]],
        case_text: str = "",
    ) -> List[EvidenceSignal]:

        signals: List[EvidenceSignal] = []

        case_lower = case_text.lower()

        for index, item in enumerate(evidence):
            text = str(
                item.get("text")
                or item.get("claim")
                or item.get("content")
                or ""
            ).strip()

            if not text:
                continue

            lower = text.lower()

            signal_type = self._classify(lower)

            if signal_type == "neutral":
                continue

            factors = self._extract_factors(lower)

            relevance = self._relevance(
                lower,
                case_lower,
                factors,
            )

            strength = self._strength(item)

            signals.append(
                EvidenceSignal(
                    signal_id=f"signal_{index + 1}",
                    signal_type=signal_type,
                    text=text,
                    source_type=item.get(
                        "source_type",
                        "unknown",
                    ),
                    source_id=str(
                        item.get(
                            "source_id",
                            item.get("id", "unknown"),
                        )
                    ),
                    strength=round(strength, 4),
                    relevance=round(relevance, 4),
                    factors=factors,
                    metadata={
                        "title": item.get("title"),
                        "retrieval_method": item.get(
                            "retrieval_method"
                        ),
                    },
                )
            )

        signals.sort(
            key=lambda signal: (
                signal.relevance * signal.strength,
                signal.relevance,
            ),
            reverse=True,
        )

        return signals

    def _classify(self, text: str) -> str:
        complaint_score = sum(
            term in text
            for term in self.COMPLAINT_TERMS
        )

        need_score = sum(
            term in text
            for term in self.NEED_TERMS
        )

        suggestion_score = sum(
            term in text
            for term in self.SUGGESTION_TERMS
        )

        scores = {
            "complaint": complaint_score,
            "need": need_score,
            "suggestion": suggestion_score,
        }

        signal_type = max(
            scores,
            key=scores.get,
        )

        return (
            signal_type
            if scores[signal_type] > 0
            else "neutral"
        )

    def _extract_factors(self, text: str) -> List[str]:
        factor_terms = [
            "price",
            "pricing",
            "cost",
            "quality",
            "location",
            "demand",
            "competition",
            "availability",
            "service",
            "customer",
            "customers",
            "booking",
            "rooms",
            "occupancy",
            "amenities",
            "transport",
            "family",
            "seasonality",
        ]

        return [
            factor
            for factor in factor_terms
            if factor in text
        ]

    def _relevance(
        self,
        text: str,
        case_text: str,
        factors: List[str],
    ) -> float:

        if not case_text:
            return min(
                1.0,
                0.2 + 0.1 * len(factors),
            )

        case_terms = set(case_text.split())

        overlap = sum(
            1
            for word in factors
            if word in case_terms
        )

        return min(
            1.0,
            0.25
            + (0.10 * len(factors))
            + (0.10 * overlap),
        )

    def _strength(
        self,
        item: Dict[str, Any],
    ) -> float:

        # Preserve source confidence when available.
        if item.get("confidence") is not None:
            try:
                return max(
                    0.0,
                    min(
                        1.0,
                        float(item["confidence"]),
                    ),
                )
            except (TypeError, ValueError):
                pass

        # Discussion/social evidence is a signal,
        # not automatically a verified fact.
        if item.get("source_type") in {
            "discussion",
            "social",
            "forum",
        }:
            return 0.35

        # Research sources remain evidence, not claims.
        if item.get("source_type") == "research_paper":
            return 0.50

        return 0.40


signal_engine = SignalEngine()
