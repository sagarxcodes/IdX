from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class CaseKnowledge:

    case_id: str

    facts: Dict[str, Any] = field(
        default_factory=dict
    )

    factors: Dict[str, Any] = field(
        default_factory=dict
    )

    evidence_ids: List[str] = field(
        default_factory=list
    )

    entities: Dict[str, Any] = field(
        default_factory=dict
    )

    events: Dict[str, Any] = field(
        default_factory=dict
    )

    relationships: List[Dict[str, Any]] = field(
        default_factory=list
    )

    unknowns: List[str] = field(
        default_factory=list
    )

    contradictions: List[str] = field(
        default_factory=list
    )


class KnowledgeStore:

    def __init__(self):
        self._cases: Dict[str, CaseKnowledge] = {}

    def create_case(self, case_id: str) -> CaseKnowledge:

        if case_id not in self._cases:
            self._cases[case_id] = CaseKnowledge(
                case_id=case_id
            )

        return self._cases[case_id]

    def get_case(self, case_id: str):
        return self._cases.get(case_id)

    def add_fact(
        self,
        case_id: str,
        key: str,
        value: Any,
    ):

        case = self.create_case(case_id)
        case.facts[key] = value

    def add_factor(
        self,
        case_id: str,
        factor_id: str,
        factor: Any,
    ):

        case = self.create_case(case_id)
        case.factors[factor_id] = factor

    def add_evidence(
        self,
        case_id: str,
        evidence_id: str,
    ):

        case = self.create_case(case_id)

        if evidence_id not in case.evidence_ids:
            case.evidence_ids.append(evidence_id)

    def add_unknown(
        self,
        case_id: str,
        unknown: str,
    ):

        case = self.create_case(case_id)

        if unknown not in case.unknowns:
            case.unknowns.append(unknown)

    def add_contradiction(
        self,
        case_id: str,
        contradiction: str,
    ):

        case = self.create_case(case_id)

        if contradiction not in case.contradictions:
            case.contradictions.append(
                contradiction
            )
