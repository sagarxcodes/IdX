from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class EvidenceLink:
    evidence_id: str
    case_id: Optional[str] = None
    factor_id: Optional[str] = None
    decision_id: Optional[str] = None

    relevance: float = 0.0
    confidence: float = 0.0

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )


class EvidenceLedger:

    def __init__(self):
        self._links: List[EvidenceLink] = []

    def link(
        self,
        evidence_id: str,
        case_id: Optional[str] = None,
        factor_id: Optional[str] = None,
        decision_id: Optional[str] = None,
        relevance: float = 0.0,
        confidence: float = 0.0,
    ) -> EvidenceLink:

        link = EvidenceLink(
            evidence_id=evidence_id,
            case_id=case_id,
            factor_id=factor_id,
            decision_id=decision_id,
            relevance=relevance,
            confidence=confidence,
        )

        self._links.append(link)
        return link

    def for_case(self, case_id: str):
        return [
            link
            for link in self._links
            if link.case_id == case_id
        ]

    def for_factor(self, factor_id: str):
        return [
            link
            for link in self._links
            if link.factor_id == factor_id
        ]

    def for_decision(self, decision_id: str):
        return [
            link
            for link in self._links
            if link.decision_id == decision_id
        ]

    def count(self) -> int:
        return len(self._links)
