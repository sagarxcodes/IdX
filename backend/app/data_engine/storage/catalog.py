from dataclasses import dataclass, field
from typing import Dict, List

from app.data_engine.records import (
    EvidenceRecord,
    NormalizedRecord,
    RawRecord,
)


@dataclass
class DataCatalog:

    raw: Dict[str, RawRecord] = field(
        default_factory=dict
    )

    normalized: Dict[str, NormalizedRecord] = field(
        default_factory=dict
    )

    evidence: Dict[str, EvidenceRecord] = field(
        default_factory=dict
    )

    def add_raw(self, record: RawRecord):
        self.raw[record.record_id] = record

    def add_normalized(
        self,
        record: NormalizedRecord,
    ):
        self.normalized[record.record_id] = record

    def add_evidence(
        self,
        record: EvidenceRecord,
    ):
        self.evidence[record.evidence_id] = record

    def counts(self):
        return {
            "raw": len(self.raw),
            "normalized": len(self.normalized),
            "evidence": len(self.evidence),
        }
