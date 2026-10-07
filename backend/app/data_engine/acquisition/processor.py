from dataclasses import dataclass, field
from typing import List

from app.data_engine.acquisition.document import (
    AcquiredDocument,
    ExtractedClaim,
    ExtractedEntity,
    ExtractedEvent,
)


@dataclass
class AcquisitionResult:

    document: AcquiredDocument

    claims: List[ExtractedClaim] = field(
        default_factory=list
    )

    entities: List[ExtractedEntity] = field(
        default_factory=list
    )

    events: List[ExtractedEvent] = field(
        default_factory=list
    )


class AcquisitionProcessor:

    def process(
        self,
        document: AcquiredDocument,
    ) -> AcquisitionResult:

        # Deliberately conservative.
        #
        # Extraction models will be connected here.
        # We do not invent entities or claims.

        return AcquisitionResult(
            document=document
        )
