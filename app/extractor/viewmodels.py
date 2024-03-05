from typing import List
from datetime import datetime

from pydantic import BaseModel


class ImageViewModel(BaseModel):
    filename: str
    url: str


class BuildingViewModel(BaseModel):
    territory: str
    area: str
    sell_type: str
    room_number: int | None = None
    land_area: float | None = None
    building_area: float
    price: int
    floor: int | None = None
    floor_number: int
    building_repair: str
    type_of_ad: str
    source: str
    views: int | None = None
    user_name: str
    user_phone: str | None = None
    category_id: int | None = None

    images: List[ImageViewModel]
