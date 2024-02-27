from typing import List
from datetime import datetime

from pydantic import BaseModel


class ImageViewModel(BaseModel):
    filename: str
    url: str



class BuildingViewModel(BaseModel):
    territory: str
    area: int
    sell_type: str
    room_number: int
    land_area: float
    building_area: float
    price: int
    floor: int
    floor_number: int
    building_repair: str
    type_of_ad: str
    created_at: datetime
    source: str
    views: int
    user_name: str
    user_phone: str
    category_id: int

    images: List[ImageViewModel]
