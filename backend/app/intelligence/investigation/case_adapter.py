from __future__ import annotations

from app.intelligence.case_model import CaseState as LegacyCaseState
from app.intelligence.case.schema import CaseState


def to_investigation_case(
    state: LegacyCaseState,
    case_id: str,
) -> CaseState:
    """
    Adapter from the existing investigation state to the newer
    generic intelligence CaseState.

    This allows incremental migration without breaking the
    existing research/signal/question pipeline.
    """

    factors = []

    signal_summary = getattr(
        state,
        "signal_summary",
        {},
    )

    for key in (
        "recurring_factors",
        "opportunity_factors",
        "failure_factors",
    ):
        values = signal_summary.get(key, [])

        if isinstance(values, list):
            factors.extend(
                str(value)
                for value in values
            )

    factors = list(dict.fromkeys(factors))

    evidence_ids = []

    for item in getattr(state, "evidence", []):
        if isinstance(item, dict):
            evidence_id = item.get("evidence_id")

            if evidence_id:
                evidence_ids.append(
                    str(evidence_id)
                )

    return CaseState(
        case_id=case_id,
        original_idea=state.original_idea,
        objective=getattr(state, "objective", ""),
        domain=getattr(state, "domain", "unknown"),
        archetype=getattr(state, "archetype", "unknown"),
        facts=dict(getattr(state, "facts", {})),
        constraints=dict(getattr(state, "constraints", {})),
        factors=factors,
        unknowns=list(getattr(state, "unknowns", [])),
        assumptions=list(getattr(state, "assumptions", [])),
        contradictions=list(
            getattr(state, "contradictions", [])
        ),
        evidence_ids=evidence_ids,
        conversation=list(
            getattr(state, "conversation", [])
        ),
    )
