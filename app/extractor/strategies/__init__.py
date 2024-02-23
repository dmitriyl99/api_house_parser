from abc import ABC
from typing import List

from app.dal.models import Building


class BuildingExtractionStrategy(ABC):
    def extract() -> List[Building]:
        raise NotImplementedError("Subclasses must implement the extract method.")
