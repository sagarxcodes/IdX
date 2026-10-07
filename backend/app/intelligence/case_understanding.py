import re
from dataclasses import dataclass, field
from typing import Any, Dict, List

from .case_model import CaseState


@dataclass
class ExtractedEntity:
    key: str
    value: Any
    confidence: float
    source: str


@dataclass
class CaseUnderstanding:
    domain: str
    archetype: str
    entities: List[ExtractedEntity] = field(default_factory=list)
    claims: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)


class CaseUnderstandingEngine:
    """
    First implementation of IdX case understanding.

    IMPORTANT:
    This is an extraction baseline, not the final ML model.

    The interface is deliberately model-independent so it can later
    be replaced by a trained information-extraction model / LLM
    without changing the rest of IdX.
    """

    PRICE_PATTERN = re.compile(
        r"(?:₹|rs\.?|inr)\s*([0-9][0-9,]*)",
        re.IGNORECASE,
    )

    ROOM_PATTERN = re.compile(
        r"(\d+)\s*(?:rooms?|keys?)",
        re.IGNORECASE,
    )

    def understand(
        self,
        idea: str,
        domain: str,
    ) -> CaseUnderstanding:

        normalized = idea.lower()

        archetype = self._detect_archetype(
            normalized,
            domain,
        )

        entities: List[ExtractedEntity] = []
        constraints: Dict[str, Any] = {}

        price_match = self.PRICE_PATTERN.search(
            idea,
        )

        if price_match:
            price = int(
                price_match.group(1).replace(",", "")
            )

            entities.append(
                ExtractedEntity(
                    key="price_per_night",
                    value=price,
                    confidence=0.98,
                    source="user_statement",
                )
            )

        room_match = self.ROOM_PATTERN.search(
            idea,
        )

        if room_match:
            rooms = int(
                room_match.group(1)
            )

            entities.append(
                ExtractedEntity(
                    key="room_count",
                    value=rooms,
                    confidence=0.98,
                    source="user_statement",
                )
            )

        if "airport" in normalized:
            entities.append(
                ExtractedEntity(
                    key="location_relation",
                    value="airport",
                    confidence=0.95,
                    source="user_statement",
                )
            )

        if any(
            phrase in normalized
            for phrase in [
                "business traveller",
                "business traveler",
                "business travellers",
                "business travelers",
            ]
        ):
            entities.append(
                ExtractedEntity(
                    key="customer_segment",
                    value="business_travellers",
                    confidence=0.95,
                    source="user_statement",
                )
            )

        if "boutique hotel" in normalized:
            entities.append(
                ExtractedEntity(
                    key="hotel_type",
                    value="boutique",
                    confidence=0.98,
                    source="user_statement",
                )
            )

        for entity in entities:
            constraints[entity.key] = entity.value

        return CaseUnderstanding(
            domain=domain,
            archetype=archetype,
            entities=entities,
            claims=[idea],
            constraints=constraints,
        )

    def apply(
        self,
        state: CaseState,
        understanding: CaseUnderstanding,
    ) -> CaseState:

        state.archetype = understanding.archetype

        for entity in understanding.entities:
            state.add_fact(
                entity.key,
                entity.value,
            )

        for key, value in understanding.constraints.items():
            state.constraints[key] = value

        self._derive_unknowns(state)

        return state

    def _detect_archetype(
        self,
        text: str,
        domain: str,
    ) -> str:

        if domain == "hospitality":
            if "boutique hotel" in text:
                return "boutique_hotel"

            if "hotel" in text:
                return "hotel"

            if "resort" in text:
                return "resort"

        if domain == "saas":
            if "subscription" in text:
                return "subscription_software"

            return "software_product"

        if domain == "marketplace":
            return "marketplace"

        if domain == "restaurant":
            return "restaurant"

        if domain == "agriculture":
            return "agricultural_business"

        return "unknown"

    def _derive_unknowns(
        self,
        state: CaseState,
    ) -> None:

        important_dimensions = [
            "exact_location",
            "property_status",
            "capital_budget",
            "customer_segment",
            "demand",
            "competition",
            "pricing_validation",
            "operating_cost",
            "regulatory_constraints",
            "differentiation",
        ]

        known = set(state.facts.keys())

        for dimension in important_dimensions:
            if dimension not in known:
                state.add_unknown(dimension)
