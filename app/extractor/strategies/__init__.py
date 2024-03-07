from abc import ABC
from typing import List, Generator

from app.dal.models import Building
from app.extractor.viewmodels import BuildingViewModel


class BuildingExtractionStrategy(ABC):
    def extract(self) -> Generator[List[BuildingViewModel], None, None]:
        raise NotImplementedError("Subclasses must implement the extract method.")
