from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class ActionType(str, Enum):
    QUESTION = "question"
    RESEARCH = "research"
    RETRIEVE_EVIDENCE = "retrieve_evidence"
    VERIFY = "verify"
    CALCULATE = "calculate"
    COMPARE = "compare"
    ANALYZE = "analyze"
    SIMULATE = "simulate"
    ESTIMATE = "estimate"
    CHECK_CONSTRAINT = "check_constraint"
    CHECK_REGULATION = "check_regulation"
    TEST_ASSUMPTION = "test_assumption"
    FIND_SIMILAR_CASE = "find_similar_case"
    ANALYZE_MARKET = "analyze_market"
    ANALYZE_COMPETITION = "analyze_competition"
    ANALYZE_FINANCIALS = "analyze_financials"
    RUN_EXPERIMENT = "run_experiment"
    STOP_INVESTIGATION = "stop_investigation"


@dataclass(frozen=True)
class ActionDefinition:
    action_type: ActionType
    description: str
    requires_user_input: bool
    requires_external_evidence: bool


ACTION_DEFINITIONS: Dict[ActionType, ActionDefinition] = {
    ActionType.QUESTION: ActionDefinition(
        ActionType.QUESTION,
        "Ask the user for information that materially reduces uncertainty.",
        True,
        False,
    ),

    ActionType.RESEARCH: ActionDefinition(
        ActionType.RESEARCH,
        "Research an unresolved case factor using external sources.",
        False,
        True,
    ),

    ActionType.RETRIEVE_EVIDENCE: ActionDefinition(
        ActionType.RETRIEVE_EVIDENCE,
        "Retrieve relevant evidence supporting or challenging a case claim.",
        False,
        True,
    ),

    ActionType.VERIFY: ActionDefinition(
        ActionType.VERIFY,
        "Verify whether an important fact or claim is actually true.",
        False,
        True,
    ),

    ActionType.CALCULATE: ActionDefinition(
        ActionType.CALCULATE,
        "Calculate a quantitative quantity required for the decision.",
        False,
        False,
    ),

    ActionType.COMPARE: ActionDefinition(
        ActionType.COMPARE,
        "Compare alternatives, competitors, strategies, or scenarios.",
        False,
        False,
    ),

    ActionType.ANALYZE: ActionDefinition(
        ActionType.ANALYZE,
        "Analyze relationships among known case factors.",
        False,
        False,
    ),

    ActionType.SIMULATE: ActionDefinition(
        ActionType.SIMULATE,
        "Simulate possible outcomes under different assumptions.",
        False,
        False,
    ),

    ActionType.ESTIMATE: ActionDefinition(
        ActionType.ESTIMATE,
        "Estimate an unknown quantity using available information.",
        False,
        False,
    ),

    ActionType.CHECK_CONSTRAINT: ActionDefinition(
        ActionType.CHECK_CONSTRAINT,
        "Determine whether a physical, financial, technical, or operational constraint is satisfied.",
        False,
        False,
    ),

    ActionType.CHECK_REGULATION: ActionDefinition(
        ActionType.CHECK_REGULATION,
        "Determine whether regulations or legal requirements affect the case.",
        False,
        True,
    ),

    ActionType.TEST_ASSUMPTION: ActionDefinition(
        ActionType.TEST_ASSUMPTION,
        "Challenge an assumption that could materially change the decision.",
        False,
        True,
    ),

    ActionType.FIND_SIMILAR_CASE: ActionDefinition(
        ActionType.FIND_SIMILAR_CASE,
        "Find historically similar cases and examine their outcomes.",
        False,
        True,
    ),

    ActionType.ANALYZE_MARKET: ActionDefinition(
        ActionType.ANALYZE_MARKET,
        "Analyze market demand, pricing, size, trends, or customer behavior.",
        False,
        True,
    ),

    ActionType.ANALYZE_COMPETITION: ActionDefinition(
        ActionType.ANALYZE_COMPETITION,
        "Analyze competitors, positioning, pricing, strengths, and weaknesses.",
        False,
        True,
    ),

    ActionType.ANALYZE_FINANCIALS: ActionDefinition(
        ActionType.ANALYZE_FINANCIALS,
        "Analyze revenue, costs, margins, cash flow, or financial viability.",
        False,
        False,
    ),

    ActionType.RUN_EXPERIMENT: ActionDefinition(
        ActionType.RUN_EXPERIMENT,
        "Run a controlled experiment to obtain real-world evidence.",
        True,
        False,
    ),

    ActionType.STOP_INVESTIGATION: ActionDefinition(
        ActionType.STOP_INVESTIGATION,
        "Stop investigating because additional information is unlikely to materially change the decision.",
        False,
        False,
    ),
}


def get_action_definition(
    action_type: ActionType,
) -> ActionDefinition:
    return ACTION_DEFINITIONS[action_type]


def all_action_types() -> List[str]:
    return [
        action_type.value
        for action_type in ActionType
    ]
