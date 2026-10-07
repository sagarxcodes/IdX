from dataclasses import dataclass


@dataclass
class EvidenceQuality:
    reliability: float
    relevance: float
    freshness: float
    completeness: float

    @property
    def overall(self) -> float:
        return (
            self.reliability
            * 0.35
            + self.relevance
            * 0.30
            + self.freshness
            * 0.20
            + self.completeness
            * 0.15
        )
