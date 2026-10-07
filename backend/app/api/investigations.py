from fastapi import APIRouter, HTTPException

from app.schemas.investigation import (
    AnswerRequest,
    AnswerResponse,
    CreateInvestigationRequest,
    InvestigationResponse,
    QuestionResponse,
)
from app.services.investigation_service import investigation_service


router = APIRouter(
    prefix="/api/investigations",
    tags=["investigations"],
)


@router.post(
    "",
    response_model=InvestigationResponse,
)
def create_investigation(
    request: CreateInvestigationRequest,
):
    investigation = investigation_service.create(request.idea)

    return investigation_service.serialize(investigation)


@router.get(
    "/{investigation_id}",
    response_model=InvestigationResponse,
)
def get_investigation(
    investigation_id: str,
):
    try:
        investigation = investigation_service.get(investigation_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found.",
        )

    return investigation_service.serialize(investigation)


@router.post(
    "/{investigation_id}/answers",
    response_model=AnswerResponse,
)
def answer_investigation(
    investigation_id: str,
    request: AnswerRequest,
):
    try:
        investigation = investigation_service.answer(
            investigation_id,
            request.question_id,
            request.answer,
        )
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Investigation not found.",
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    current_question = investigation.current_question

    next_question = None

    if current_question is not None:
        next_question = QuestionResponse(
            id=current_question["id"],
            text=current_question["text"],
            reason=current_question["reason"],
            category=current_question["category"],
        )

    return AnswerResponse(
        status=investigation.status,
        investigation_id=investigation.id,
        next_question=next_question,
        question_count=investigation.question_count,
    )
