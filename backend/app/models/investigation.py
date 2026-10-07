from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Investigation:
    id: str
    original_idea: str
    domain: str = "unknown"
    domain_confidence: float = 0.0
    archetype: str = "unknown"
    objective: str = ""
    status: str = "investigating"

    facts: Dict[str, str] = field(default_factory=dict)
    assumptions: List[str] = field(default_factory=list)
    unknowns: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)

    answers: List[Dict[str, str]] = field(default_factory=list)
    questions_asked: List[str] = field(default_factory=list)

    current_question: Optional[Dict[str, str]] = None
    question_count: int = 0

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
