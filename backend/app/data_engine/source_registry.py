from dataclasses import dataclass
from typing import Dict


@dataclass
class SourceSpec:
    source_id: str
    name: str
    category: str
    authority: str
    update_frequency: str
    enabled: bool = True


SOURCE_REGISTRY: Dict[str, SourceSpec] = {

    "government": SourceSpec(
        "government",
        "Government data",
        "regulatory",
        "high",
        "variable",
    ),

    "research": SourceSpec(
        "research",
        "Scientific research",
        "research",
        "high",
        "variable",
    ),

    "company": SourceSpec(
        "company",
        "Company information",
        "business",
        "variable",
        "daily",
    ),

    "market": SourceSpec(
        "market",
        "Market data",
        "financial",
        "high",
        "real_time",
    ),

    "news": SourceSpec(
        "news",
        "News and events",
        "events",
        "variable",
        "continuous",
    ),

    "user": SourceSpec(
        "user",
        "User-provided information",
        "case",
        "user",
        "on_demand",
    ),

    "historical_cases": SourceSpec(
        "historical_cases",
        "Historical decisions and outcomes",
        "decision",
        "variable",
        "continuous",
    ),
}
