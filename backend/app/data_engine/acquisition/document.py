from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class AcquiredDocument:
    document_id: str

    source_id: str

    title: str

    content: str

    url: Optional[str] = None

    author: Optional[str] = None

    publisher: Optional[str] = None

    published_at: Optional[datetime] = None

    retrieved_at: datetime = field(
        default_factory=datetime.utcnow
    )

    document_type: str = "unknown"

    language: str = "en"

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class ExtractedClaim:
    claim_id: str

    document_id: str

    text: str

    subject: Optional[str] = None

    predicate: Optional[str] = None

    object_value: Optional[str] = None

    source_span: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class ExtractedEntity:
    entity_id: str

    document_id: str

    name: str

    entity_type: str

    confidence: float = 0.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class ExtractedEvent:
    event_id: str

    document_id: str

    event_type: str

    description: str

    timestamp: Optional[datetime] = None

    entity_ids: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )
