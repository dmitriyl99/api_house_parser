from abc import ABC
from typing import List, Generator

from app.dal.models import Building


class BuildingExtractionStrategy(ABC):
    def extract() -> Generator[List[Building]]:
        raise NotImplementedError("Subclasses must implement the extract method.")
