from app.extractor import BuildingExtractor
from app.extractor.strategies.uybor import UyBorExtractionStrategy
from app.extractor.strategies.olx import OlxExtractionStrategy
from app.extractor.viewmodels import BuildingViewModel
from app.dal.repositories import buildings as buildings_repository
from app.dal.models import Building, Image

from time import sleep


def parse_uybor():
    extractor = BuildingExtractor(UyBorExtractionStrategy())
    for buildings in extractor.extract():
        for building in buildings:
            _save_building_to_repository(building)
        sleep(5)


def parse_olx():
    extractor = BuildingExtractor(OlxExtractionStrategy())
    for buildings in extractor.extract():
        for building in buildings:
            _save_building_to_repository(building)


def _save_building_to_repository(building: BuildingViewModel):
    buildings_repository.save_building(Building(
        title=building.title,
        description=building.description,
        territory=building.territory,
        area=building.area,
        sell_type=building.sell_type,
        room_number=building.room_number,
        land_area=building.land_area,
        building_area=building.building_area,
        price=building.price,
        floor=building.floor,
        floor_number=building.floor_number,
        building_repair=building.building_repair,
        type_of_ad=building.type_of_ad,
        source=building.source,
        views=building.views,
        user_name=building.user_name,
        user_phone=building.user_phone,
        olx_id=building.olx_id,
        category_id=building.category_id,
        uybor_id=building.uybor_id,
        url=building.url,
    ), list(map(lambda x: Image(
        filename=x.filename,
        url=x.url
    ), building.images)))
