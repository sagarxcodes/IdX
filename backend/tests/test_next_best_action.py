from app.intelligence.case.schema import CaseState
from app.intelligence.investigation.action_ranker import ActionRanker
from app.intelligence.investigation.generic_candidate_generator import (
    GenericCandidateActionGenerator,
)
from app.intelligence.investigation.next_best_action import (
    NextBestActionEngine,
)


def build_engine():
    return NextBestActionEngine(
        generator=GenericCandidateActionGenerator(),
        ranker=ActionRanker(),
    )


def test_engine_returns_action():

    case = CaseState(
        case_id="test-1",
        original_idea=(
            "I want to build an AI inventory-management "
            "platform for small restaurants in India."
        ),
        objective="Determine whether the business is viable.",
        unknowns=[
            "customer willingness to pay",
            "market demand",
        ],
    )

    result = build_engine().decide(case)

    assert result.selected is not None
    assert result.selected.action.action_id
    assert result.selected.score >= 0


def test_contradiction_prioritizes_verification():

    case = CaseState(
        case_id="test-2",
        original_idea="Test business idea.",
        objective="Determine viability.",
        unknowns=["market demand"],
        contradictions=[
            "Two evidence sources disagree about demand."
        ],
    )

    result = build_engine().decide(case)

    assert result.selected is not None
    assert result.selected.action.action_type.value == "verify"


def test_engine_is_not_question_only():

    case = CaseState(
        case_id="test-3",
        original_idea="Evaluate a new product.",
        objective="Determine whether to launch.",
        unknowns=["market demand"],
    )

    result = build_engine().decide(case)

    action_types = {
        candidate.action.action_type.value
        for candidate in result.candidates
    }

    assert "question" in action_types
    assert "research" in action_types
    assert "verify" in action_types


def test_bootstrap_prefers_objective_question():

    case = CaseState(
        case_id="test-4",
        original_idea="I want to build something new.",
    )

    result = build_engine().decide(case)

    assert result.selected is not None
    assert result.selected.action.action_type.value == "question"
    assert result.selected.action.target == "objective"
