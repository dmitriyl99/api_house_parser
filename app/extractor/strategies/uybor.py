from typing import List, Tuple, Generator
from functools import partial
import logging
import re

from app.dal.models import Building
from . import BuildingExtractionStrategy
from app.settings import settings

import requests


class UyBorExtractionStrategy(BuildingExtractionStrategy):
    session: requests.Session
    logger: logging.Logger

    def __init__(self) -> None:
        super().__init__()
        self.session = requests.Session()
        self.session.request = partial(
            lambda prefix, f, method, url, *
            args, **kwargs: f(method, prefix + url, *args, **kwargs),
            f'{settings.uybor_hostname}/api/{settings.uybor_api_version}', self.session.request
        )
        self.logger = logging.getLogger("uybor-extraction")

    def extract(self) -> Generator[List[Building]]:
        self.logger.info(f"Start extracting buildings from {settings.uybor_hostname}/api/{settings.uybor_api_version}")
        has_buildings = True
        counter = 1
        limit = 100
        while has_buildings:
            total, buildings = self._extract_buildings(
                currency='usd', limit=limit)
            has_buildings = len(buildings) != 0
            self.logger.debug(f"Get {counter * limit}/{total} buildings")
            yield list(map(lambda raw_building: Building(
                territory=raw_building['region']['name']['ru'],
                area=f'{raw_building['district']['name']['ru'] + ''} {
                    raw_building['street']['name']['ru']} {raw_building['zone']['name']['ru']}',
                sell_type=raw_building['operationType'],
                room_number=int(
                    re.search(r'\d+', raw_building['room']).group()),
                land_area=raw_building['squareGround'] if 'squareGround' in raw_building else None,
                building_area=raw_building['square'],
                price=raw_building['price'],
                floor=raw_building['floor'],
                floor_number=raw_building['floorTotal'],
                building_repair=raw_building['repair'],
                type_of_ad=raw_building['user']['role'],
                source='uybor'
            ), buildings))
        self.logger.info("Done extracting buildings from {settings.uybor_hostname}/api/{settings.uybor_api_version}")

    def _get_categories(self) -> List[dict]:
        return self.session.get('/listings/categories', params={'limit': 999})

    def _extract_buildings(self, currency: str, limit: int = 20, operation_type: str = None, category_id: int = None, page: int = 1) -> Tuple[int, List[dict]]:
        if currency not in ['usd', 'uzs']:
            raise ValueError(f"Incorrect currency {currency}")
        params = {
            'includeFeatured': True,
            'limit': limit,
            'embed': 'category,subCategory,residentialComplex,region,city,district,zone,street,metro',
            'priceCurrency__eq': currency,
            'page': page
        }
        if operation_type:
            params['operationType__eq'] = operation_type
        if category_id:
            params['category__eq'] = category_id
        response: requests.Response = self.session.get(
            '/listings', params=params)
        data = response.json()
        return data['total'], data['results']
