from abc import ABC, abstractmethod
from typing import Any, Iterable


class DataConnector(ABC):

    name = "unknown"

    @abstractmethod
    def fetch(self, query: Any) -> Iterable[Any]:
        raise NotImplementedError
