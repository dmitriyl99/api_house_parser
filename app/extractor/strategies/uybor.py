from typing import List, Tuple, Generator
from functools import partial
import logging
import re

from . import BuildingExtractionStrategy
from ..viewmodels import BuildingViewModel, ImageViewModel
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
        self.session.headers = {
            'Accept': '*/*',
            'Accept-Language': 'ru',
            'Connection': 'keep-alive',
            'Origin': 'https://uybor.uz',
            'Referer': 'https://uybor.uz/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
        }
        self.logger = logging.getLogger("uybor-extraction")

    def extract(self) -> Generator[List[BuildingViewModel], None, None]:
        def convert_building(raw_building: dict):
            building = BuildingViewModel(
                territory=raw_building['region']['name']['ru'],
                area=f"{raw_building['district']['name']['ru'] if raw_building['district'] else ''} "
                     f"{raw_building['street']['name']['ru'] if raw_building['street'] else ''} "
                     f"{raw_building['zone']['name']['ru'] if raw_building['zone'] else ''}",
                sell_type=raw_building['operationType'],
                room_number=int(
                    re.search(r'\d+', raw_building['room']).group()) if raw_building['room'] else None,
                land_area=raw_building['squareGround'] if 'squareGround' in raw_building else None,
                building_area=raw_building['square'] if 'square' in raw_building else None,
                price=raw_building['price'],
                floor=raw_building['floor'] if 'floor' in raw_building else None,
                floor_number=raw_building['floorTotal'] if 'floorTotal' in raw_building else None,
                building_repair=raw_building['repair'] if 'repair' in raw_building else None,
                type_of_ad=raw_building['user']['role'] if 'user' in raw_building and 'role' in raw_building['user'] else None,
                source='uybor',
                views=raw_building['views'] if 'views' in raw_building else None,
                user_name=raw_building['user']['displayName'] if 'displayName' in raw_building['user'] else
                raw_building['user']['firstName'] + ' ' + raw_building['user']['lastName'],
                images=list(map(lambda raw_media: ImageViewModel(filename=raw_media['fileName'], url=raw_media['url']),
                                raw_building['media']))
            )
            building.user_phone = self._extract_phone(raw_building['id'])
            return building

        self.logger.info(f"Start extracting buildings from {settings.uybor_hostname}/api/{settings.uybor_api_version}")
        has_buildings = True
        counter = 1
        limit = 100
        while has_buildings:
            total, buildings = self._extract_buildings(
                currency='usd', limit=limit)
            has_buildings = len(buildings) != 0
            self.logger.debug(f"Get {counter * limit}/{total} buildings")
            yield list(map(convert_building, buildings))
        self.logger.info("Done extracting buildings from {settings.uybor_hostname}/api/{settings.uybor_api_version}")

    def _get_categories(self) -> List[dict]:
        return self.session.get('/listings/categories', params={'limit': 999}).json()

    def _extract_buildings(self, currency: str, limit: int = 20, operation_type: str = None, category_id: int = None,
                           page: int = 1) -> Tuple[int, List[dict]]:
        if currency not in ['usd', 'uzs']:
            raise ValueError(f"Incorrect currency {currency}")
        params = {
            'includeFeatured': True,
            'limit': limit,
            'embed': 'category,subCategory,residentialComplex,region,city,district,zone,street,metro,user,media',
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

    def _extract_phone(self, building_id: int) -> str | None:
        response: requests.Response = self.session.get(f"/listings/{building_id}/phone")
        data: dict = response.json()
        if 'phone' in data:
            return data['phone']
        return None
