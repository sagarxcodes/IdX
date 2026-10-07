from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class RawRecord:
    record_id: str
    source_id: str
    source_type: str

    content: Any

    retrieved_at: datetime = field(
        default_factory=datetime.utcnow
    )

    published_at: Optional[datetime] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class NormalizedRecord:
    record_id: str

    entities: List[Dict[str, Any]] = field(
        default_factory=list
    )

    claims: List[Dict[str, Any]] = field(
        default_factory=list
    )

    events: List[Dict[str, Any]] = field(
        default_factory=list
    )

    factors: List[Dict[str, Any]] = field(
        default_factory=list
    )

    relationships: List[Dict[str, Any]] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class EvidenceRecord:
    evidence_id: str

    claim: str

    source_id: str

    source_url: Optional[str] = None

    published_at: Optional[datetime] = None

    retrieved_at: datetime = field(
        default_factory=datetime.utcnow
    )

    confidence: float = 0.0

    relevance: float = 0.0

    freshness: float = 0.0

    supporting_records: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )
