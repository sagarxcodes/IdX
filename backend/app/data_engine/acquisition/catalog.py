from typing import Dict, List

from app.data_engine.acquisition.document import (
    AcquiredDocument,
)
from app.data_engine.acquisition.processor import (
    AcquisitionResult,
)


class AcquisitionCatalog:

    def __init__(self):

        self.documents: Dict[
            str,
            AcquiredDocument,
        ] = {}

        self.results: Dict[
            str,
            AcquisitionResult,
        ] = {}

    def add(
        self,
        result: AcquisitionResult,
    ):

        document_id = result.document.document_id

        self.documents[
            document_id
        ] = result.document

        self.results[
            document_id
        ] = result

    def get(
        self,
        document_id: str,
    ):

        return self.results.get(
            document_id
        )

    def count(self):

        return {
            "documents": len(
                self.documents
            ),
            "processed": len(
                self.results
            ),
        }
