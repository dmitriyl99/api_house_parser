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
    building_area: float | None
    price: float
    floor: int | None = None
    floor_number: int | None = None
    building_repair: str | None = None
    type_of_ad: str
    source: str
    views: int | None = None
    user_name: str | None = None
    user_phone: str | None = None
    category_id: int | None = None
    olx_id: int | None = None

    images: List[ImageViewModel]
