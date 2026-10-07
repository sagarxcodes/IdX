from dataclasses import dataclass


@dataclass
class DomainResult:
    domain: str
    confidence: float
    signals: list[str]


DOMAIN_SIGNALS = {
    "hospitality": [
        "hotel",
        "resort",
        "hostel",
        "homestay",
        "rooms",
        "hospitality",
    ],
    "saas": [
        "saas",
        "software",
        "subscription",
        "platform",
        "software product",
    ],
    "marketplace": [
        "marketplace",
        "buyers",
        "sellers",
        "connect buyers",
        "connect sellers",
    ],
    "restaurant": [
        "restaurant",
        "cafe",
        "food business",
        "dining",
    ],
    "agriculture": [
        "farm",
        "farmer",
        "agriculture",
        "crop",
        "farming",
    ],
}


def detect_domain(text: str) -> DomainResult:
    normalized = text.lower()

    scores: dict[str, list[str]] = {}

    for domain, signals in DOMAIN_SIGNALS.items():
        matches = [
            signal
            for signal in signals
            if signal in normalized
        ]

        if matches:
            scores[domain] = matches

    if not scores:
        return DomainResult(
            domain="unknown",
            confidence=0.0,
            signals=[],
        )

    domain, signals = max(
        scores.items(),
        key=lambda item: len(item[1]),
    )

    confidence = min(
        0.95,
        0.5 + (len(signals) * 0.15),
    )

    return DomainResult(
        domain=domain,
        confidence=confidence,
        signals=signals,
    )
