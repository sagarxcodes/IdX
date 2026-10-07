from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app.intelligence.case.schema import CaseState
from app.intelligence.investigation.action import CandidateAction


class CandidateActionGenerator(ABC):

    @abstractmethod
    def generate(
        self,
        case: CaseState,
    ) -> List[CandidateAction]:
        """
        Generate plausible next investigation actions.

        This component proposes possibilities.
        The ML ranker decides which action is best.
        """
        raise NotImplementedError
