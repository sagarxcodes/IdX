from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Source:
    id: str
    name: str
    url: Optional[str] = None
    publisher: Optional[str] = None
    source_type: str = "unknown"
    published_at: Optional[datetime] = None
    retrieved_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Evidence:
    id: str
    claim: str
    value: Any = None
    source_ids: List[str] = field(default_factory=list)
    confidence: float = 0.0
    freshness: float = 0.0
    relevance: float = 0.0
    provenance: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Entity:
    id: str
    entity_type: str
    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    source_ids: List[str] = field(default_factory=list)


@dataclass
class Event:
    id: str
    event_type: str
    timestamp: Optional[datetime] = None
    entities: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    source_ids: List[str] = field(default_factory=list)


@dataclass
class Factor:
    id: str
    name: str
    category: str
    value: Any = None
    uncertainty: float = 1.0
    importance: float = 0.0
    evidence_ids: List[str] = field(default_factory=list)


@dataclass
class Outcome:
    id: str
    decision_id: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    success: Optional[bool] = None
    observations: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[datetime] = None
