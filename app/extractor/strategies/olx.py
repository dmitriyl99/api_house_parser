from typing import List, Generator
from functools import partial
import logging
import time

import requests

from . import BuildingExtractionStrategy
from ..viewmodels import BuildingViewModel, ImageViewModel
from app.dal.models import Building
from app.dal.repositories import buildings as buildings_repository

from app.settings import settings


class OlxExtractionStrategy(BuildingExtractionStrategy):
    session: requests.Session
    logger: logging.Logger

    def __init__(self) -> None:
        super().__init__()
        self.session = requests.Session()
        self.session.request = partial(
            lambda prefix, f, method, url, *
            args, **kwargs: f(method, prefix + url, *args, **kwargs),
            f'{settings.olx_hostname}/api/{settings.olx_api_version}', self.session.request
        )
        self.logger = logging.getLogger("olx-extraction")

    def extract(self) -> Generator[List[Building], None, None]:
        def convert_building(raw_building: dict, sell_type: str, category: str) -> BuildingViewModel:
            time.sleep(0.5)

            def find_param(params: List[dict], param_name: str):
                found_params = list(filter(lambda x: x['key'] == param_name, params))
                if len(found_params) > 0:
                    return found_params[0]['value']['value']
                return None

            def find_input(params: List[dict], param_name: str, value_field_name: str = 'key'):
                found_params = list(filter(lambda x: x['key'] == param_name, params))
                if len(found_params) > 0:
                    param = found_params[0]
                    if type(param['value'][value_field_name]) is list:
                        return param['value']['label']
                    else:
                        return param['value'][value_field_name]

            price = find_param(raw_building['params'], 'price')
            number_of_rooms = find_input(raw_building['params'], 'number_of_rooms')
            land_area = find_input(raw_building['params'], 'plot')
            building_area = find_input(raw_building['params'], 'total_living_area')
            if building_area is None:
                building_area = find_input(raw_building['params'], 'total_area')
            floor_number = find_input(raw_building['params'], 'total_floors')
            floor = find_input(raw_building['params'], 'floor')
            repair = find_input(raw_building['params'], 'house_repairs', 'label')
            user_name = raw_building['user']['name']
            user_phone = raw_building['contact']['name']
            territory = raw_building['location']['region']['name']
            area = raw_building['location']['city']['name'] + ' ' + (raw_building['location']['district']['name'] if 'district' in raw_building['location'] else '')

            images = list(
                map(
                    lambda x: ImageViewModel(
                        filename=x['filename'],
                        url=x['link']
                    ), raw_building['photos']
                )
            )

            views = OlxExtractionStrategy._extract_views_for_building(raw_building['id'])

            return BuildingViewModel(
                territory=territory,
                area=area,
                price=price,
                room_number=number_of_rooms,
                land_area=land_area,
                building_area=building_area,
                floor=floor,
                floor_number=floor_number,
                building_repair=repair,
                type_of_ad='n/d',
                source='olx',
                sell_type=sell_type,
                user_name=user_name,
                user_phone=user_phone,
                images=images,
                views=views,
                olx_id=raw_building['id']
            )

        self.logger.info(f"Start extracting buildings from {settings.olx_hostname}/api/{settings.olx_api_version}")
        has_buildings = True
        counter = 1
        offset = 0
        limit = 40
        max_offset = 1000
        category_sell_type_param = [
            {
                'olx_category_id': 1147,
                'category': 'Квартира',
                'sell_type': 'rent'
            },
            {
                'olx_category_id': 13,
                'category': 'Квартира',
                'sell_type': 'sale'
            },
            {
                'olx_category_id': 330,
                'category': 'Дом',
                'sell_type': 'rent'
            },
            {
                'olx_category_id': 40,
                'category': 'Дом',
                'sell_type': 'sale'
            },
            {
                'olx_category_id': 1533,
                'category': 'Земельный участок',
                'sell_type': 'rent'
            },
            {
                'olx_category_id': 10,
                'category': 'Земельный участок',
                'sell_type': 'sale'
            },
            {
                'olx_category_id': 11,
                'category': 'Для бизнеса',
                'sell_type': 'rent'
            },
            {
                'olx_category_id': 14,
                'category': 'Для бизнеса',
                'sell_type': 'sale'
            }
        ]
        for param in category_sell_type_param:
            while has_buildings:
                if offset > max_offset:
                    break
                buildings: List[dict] = self._extract_building(param['olx_category_id'], offset, limit)
                has_buildings = len(buildings) != 0
                self.logger.info(f"Get {counter * limit} buildings")
                offset += limit
                buildings_to_yield = []
                for building in buildings:
                    building_exists = buildings_repository.get_building_by_olx_id(building['id'])
                    if building_exists:
                        continue
                    buildings_to_yield.append(convert_building(building, param['sell_type'], param['category']))
                yield buildings_to_yield

    def _extract_building(self, category_id: int = 1, offset: int = 0, limit: int = 50) -> List[dict]:
        response: requests.Response = self.session.get(
            '/offers/', params={'category_id': 1, 'offset': offset, 'limit': limit}
        )
        if response.status_code != 200:
            print(response.json())
            raise ValueError("Response from olx wasn't successful")
        return response.json()['data']

    @staticmethod
    def _extract_views_for_building(building_id: int) -> int | None:
        response: requests.Response = requests.post('https://production-graphql.eu-sharedservices.olxcdn.com/graphql', json={
            'query': 'query PageViews($adId: String!) {b2c {pageViews(adId: $adId) {pageViews}}}',
            'variables': {
                'adId': str(building_id)
            }
        }, headers={
            'Authorization': 'Bearer 03805c4503dc1ca61f47055cf4693b467aa5efec,fa7ad9528c2c1ed1bd8d638336e942f0eeb5664d',
            'Site': 'olxuz'
        })
        response_data = response.json()
        try:
            return response_data['data']['b2c']['pageViews']['pageViews']
        except TypeError:
            print(response_data)
            return None
