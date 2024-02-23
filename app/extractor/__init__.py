from typing import List

from .strategies import BuildingExtractionStrategy
from app.dal.models import Building


class BuildingExtractor:
    _extractor: BuildingExtractionStrategy

    def __init__(self, extractor: BuildingExtractionStrategy) -> None:
        self._extractor = extractor
    
    def extract(self) -> List[Building]:
        return self._extractor.extract()
