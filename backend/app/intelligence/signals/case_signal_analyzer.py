from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from app.intelligence.signals.signal_engine import EvidenceSignal


@dataclass
class CaseSignalSummary:
    pain_points: List[str] = field(default_factory=list)
    needs: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    failure_factors: List[str] = field(default_factory=list)
    opportunity_factors: List[str] = field(default_factory=list)
    recurring_factors: Dict[str, int] = field(default_factory=dict)


class CaseSignalAnalyzer:
    """
    Aggregates heterogeneous evidence signals into case-level intelligence.

    This is a transparent submission baseline.
    It does not claim that one discussion proves a market need.
    """

    def analyze(
        self,
        signals: List[EvidenceSignal],
    ) -> CaseSignalSummary:

        summary = CaseSignalSummary()

        factor_counts: Dict[str, int] = {}

        for signal in signals:

            for factor in signal.factors:
                factor_counts[factor] = (
                    factor_counts.get(factor, 0) + 1
                )

            if signal.signal_type == "complaint":
                summary.pain_points.append(signal.text)

                if signal.source_type == "historical_case":
                    summary.failure_factors.extend(
                        signal.factors
                    )

            elif signal.signal_type == "need":
                summary.needs.append(signal.text)

            elif signal.signal_type == "suggestion":
                summary.suggestions.append(signal.text)

        summary.recurring_factors = {
            factor: count
            for factor, count in factor_counts.items()
            if count >= 2
        }

        # A recurring factor appearing across evidence sources
        # is a candidate opportunity, not a proven opportunity.
        summary.opportunity_factors = list(
            summary.recurring_factors.keys()
        )

        return summary


case_signal_analyzer = CaseSignalAnalyzer()
