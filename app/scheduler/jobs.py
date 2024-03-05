from app.extractor import BuildingExtractor
from app.extractor.strategies.uybor import UyBorExtractionStrategy
from app.dal.repositories import buildings as buildings_repository
from app.dal.models import Building, Image


def parse_uybor():
    extractor = BuildingExtractor(UyBorExtractionStrategy())
    for buildings in extractor.extract():
        for building in buildings:
            buildings_repository.save_building(Building(
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
                user_phone=building.user_phone
            ), list(map(lambda x: Image(
                filename=x.filename,
                url=x.url
            ), building.images)))