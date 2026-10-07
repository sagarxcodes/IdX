from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ResearchSource:
    source_id: str
    source_type: str
    title: str
    authors: List[str] = field(default_factory=list)
    publisher: str = ""
    url: str = ""
    doi: Optional[str] = None
    year: Optional[int] = None
    open_access: bool = False
    methodology: str = ""
    sample_size: Optional[int] = None
    geography: List[str] = field(default_factory=list)
    sectors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchClaim:
    claim_id: str
    source_id: str
    text: str

    claim_type: str = "finding"

    factors: List[str] = field(default_factory=list)
    sectors: List[str] = field(default_factory=list)

    conditions: List[Dict[str, Any]] = field(default_factory=list)
    geography: List[str] = field(default_factory=list)

    direction: str = "unknown"
    effect_size: Optional[float] = None
    effect_unit: str = ""

    confidence: float = 0.0
    evidence_strength: float = 0.0

    limitations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FactorEvidence:
    evidence_id: str
    factor_id: str
    claim_id: str

    relevance: float = 0.0
    evidence_strength: float = 0.0
    applicability: float = 0.0

    supporting: bool = True
    contradiction: bool = False

    conditions: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FactorKnowledge:
    factor_id: str
    canonical_name: str

    aliases: List[str] = field(default_factory=list)

    categories: List[str] = field(default_factory=list)
    sectors: List[str] = field(default_factory=list)
    archetypes: List[str] = field(default_factory=list)

    definitions: List[str] = field(default_factory=list)

    evidence_ids: List[str] = field(default_factory=list)
    related_factors: List[str] = field(default_factory=list)

    conditions: List[Dict[str, Any]] = field(default_factory=list)
    interactions: List[Dict[str, Any]] = field(default_factory=list)

    benchmarks: List[Dict[str, Any]] = field(default_factory=list)
    contradictions: List[Dict[str, Any]] = field(default_factory=list)

    research_gaps: List[str] = field(default_factory=list)

    confidence: float = 0.0
    uncertainty: float = 1.0

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SectorProfile:
    sector_id: str
    name: str

    parent_sector: Optional[str] = None

    factor_ids: List[str] = field(default_factory=list)

    advantages: List[str] = field(default_factory=list)
    challenges: List[str] = field(default_factory=list)

    economic_drivers: List[str] = field(default_factory=list)
    market_drivers: List[str] = field(default_factory=list)
    operational_drivers: List[str] = field(default_factory=list)
    technology_drivers: List[str] = field(default_factory=list)
    regulatory_drivers: List[str] = field(default_factory=list)
    risk_drivers: List[str] = field(default_factory=list)

    benchmarks: List[Dict[str, Any]] = field(default_factory=list)

    evidence_ids: List[str] = field(default_factory=list)
    research_gaps: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchGap:
    gap_id: str
    description: str

    factor_ids: List[str] = field(default_factory=list)
    sectors: List[str] = field(default_factory=list)

    missing_geographies: List[str] = field(default_factory=list)
    missing_populations: List[str] = field(default_factory=list)
    missing_time_periods: List[str] = field(default_factory=list)

    importance: float = 0.0
    evidence_uncertainty: float = 1.0

    metadata: Dict[str, Any] = field(default_factory=dict)
