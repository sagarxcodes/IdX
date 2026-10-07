from typing import Iterable, List

from app.data_engine.records import (
    RawRecord,
    NormalizedRecord,
)


class IngestionPipeline:

    def ingest(
        self,
        records: Iterable[RawRecord],
    ) -> List[RawRecord]:

        return list(records)

    def normalize(
        self,
        records: Iterable[RawRecord],
    ) -> List[NormalizedRecord]:

        normalized = []

        for record in records:
            normalized.append(
                NormalizedRecord(
                    record_id=record.record_id
                )
            )

        return normalized
