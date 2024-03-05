from abc import ABC
from typing import List, Generator

from app.dal.models import Building


class BuildingExtractionStrategy(ABC):
    def extract(self) -> Generator[List[Building], None, None]:
        raise NotImplementedError("Subclasses must implement the extract method.")
