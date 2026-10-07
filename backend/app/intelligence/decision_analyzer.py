from __future__ import annotations

from typing import Any, Dict


class DecisionAnalyzer:
    """
    Transparent decision-analysis baseline.

    Converts the current investigation state into a concise,
    evidence-aware decision summary.

    This is intentionally deterministic for the submission.
    """

    def analyze(self, state) -> Dict[str, Any]:
        summary = getattr(state, "signal_summary", {}) or {}

        pain_points = summary.get("pain_points", [])
        needs = summary.get("needs", [])
        suggestions = summary.get("suggestions", [])
        failure_factors = summary.get("failure_factors", [])
        opportunity_factors = summary.get("opportunity_factors", [])
        recurring_factors = summary.get("recurring_factors", {})

        risks = []

        for factor in failure_factors:
            if factor not in risks:
                risks.append(factor)

        for factor in recurring_factors:
            if factor not in risks and factor in ("cost", "occupancy", "competition"):
                risks.append(factor)

        opportunities = list(opportunity_factors)

        guidance = []

        if risks:
            guidance.append(
                "Validate the factors associated with previous failures "
                "before committing resources."
            )

        if opportunities:
            guidance.append(
                "Investigate recurring opportunity signals and determine "
                "whether they represent a sufficiently large unmet need."
            )

        if state.constraints:
            guidance.append(
                "Test the proposed strategy against the stated constraints."
            )

        if not guidance:
            guidance.append(
                "Collect additional evidence before making a high-cost decision."
            )

        return {
            "objective": state.objective,
            "facts": dict(state.facts),
            "pain_points": pain_points,
            "needs": needs,
            "suggestions": suggestions,
            "failure_factors": failure_factors,
            "opportunity_factors": opportunities,
            "recurring_factors": recurring_factors,
            "risks": risks,
            "guidance": guidance,
            "evidence_count": len(state.evidence),
            "status": (
                "evidence_informed"
                if state.evidence
                else "insufficient_evidence"
            ),
        }


decision_analyzer = DecisionAnalyzer()
