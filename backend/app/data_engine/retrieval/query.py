from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class RetrievalQuery:
    query: str

    entity_types: List[str] = field(
        default_factory=list
    )

    domains: List[str] = field(
        default_factory=list
    )

    date_from: Any = None
    date_to: Any = None

    filters: Dict[str, Any] = field(
        default_factory=dict
    )

    limit: int = 20
