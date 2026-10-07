from app.intelligence.case_model import CaseState
from app.intelligence.question_engine import AdaptiveQuestionEngine


def test_question_engine_works_without_domain_specific_flow():
    state = CaseState(
        original_idea="I want to open a hotel in Kochi",
        domain="hospitality",
    )

    engine = AdaptiveQuestionEngine()

    question = engine.next_question(state)

    assert question is not None
    assert question.text
    assert question.category


def test_question_engine_works_for_online_store():
    state = CaseState(
        original_idea="I want to start an online sneaker store",
        domain="unknown",
    )

    engine = AdaptiveQuestionEngine()

    question = engine.next_question(state)

    assert question is not None


def test_question_engine_works_for_engineering_problem():
    state = CaseState(
        original_idea="I want to build a powered exoskeleton",
        domain="engineering",
    )

    engine = AdaptiveQuestionEngine()

    question = engine.next_question(state)

    assert question is not None


def test_contradiction_gets_high_priority():
    state = CaseState(
        original_idea="I want to open a hotel",
        domain="hospitality",
        contradictions=[
            "Expected customers may only pay 3000, "
            "but comparable properties appear to charge 6000."
        ],
    )

    engine = AdaptiveQuestionEngine()

    question = engine.next_question(state)

    assert question is not None
    assert question.category == "contradiction"
