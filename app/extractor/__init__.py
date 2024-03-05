from typing import List, Generator

from .strategies import BuildingExtractionStrategy
from .viewmodels import BuildingViewModel
from app.dal.models import Building


class BuildingExtractor:
    _extractor: BuildingExtractionStrategy

    def __init__(self, extractor: BuildingExtractionStrategy) -> None:
        self._extractor = extractor
    
    def extract(self) -> Generator[List[BuildingViewModel], None, None]:
        return self._extractor.extract()
