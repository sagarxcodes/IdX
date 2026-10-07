from dataclasses import dataclass, field


@dataclass
class BusinessContext:
    original_idea: str
    domain: str = "unknown"

    facts: dict[str, str] = field(default_factory=dict)
    unknowns: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    answers: list[dict[str, str]] = field(default_factory=list)


def create_context(idea: str, domain: str) -> BusinessContext:
    return BusinessContext(
        original_idea=idea,
        domain=domain,
    )


def add_answer(
    context: BusinessContext,
    question_id: str,
    question: str,
    answer: str,
) -> BusinessContext:

    context.answers.append({
        "question_id": question_id,
        "question": question,
        "answer": answer,
    })

    return context
