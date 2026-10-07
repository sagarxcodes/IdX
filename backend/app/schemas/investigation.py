from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class CreateInvestigationRequest(BaseModel):
    idea: str = Field(min_length=3)


class AnswerRequest(BaseModel):
    question_id: str
    answer: str = Field(min_length=1)


class QuestionResponse(BaseModel):
    id: str
    text: str
    reason: str
    category: str


class InvestigationResponse(BaseModel):
    id: str
    original_idea: str
    domain: str
    domain_confidence: float
    archetype: str
    objective: str
    status: str

    facts: Dict[str, str]
    assumptions: List[str]
    unknowns: List[str]
    contradictions: List[str]
    evidence: List[dict]

    answers: List[Dict[str, str]]
    questions_asked: List[str]

    current_question: Optional[QuestionResponse]
    question_count: int


class AnswerResponse(BaseModel):
    status: str
    investigation_id: str
    next_question: Optional[QuestionResponse]
    question_count: int
