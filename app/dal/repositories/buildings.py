from typing import List, Type

from sqlalchemy.orm import Session, joinedload

from . import engine
from app.dal.models import Building, Image


def save_buildings(objects: List[Building]):
    with Session(engine) as session:
        session.add_all(objects)
        session.commit()


def save_building(object: Building, images: List[Image] | None = None):
    with Session(engine) as session:
        session.add(object)
        session.commit()
        if images:
            session.refresh(object)
            for image in images:
                image.building_id = object.id
                session.add(image)
            session.commit()


def get_buildings() -> List[Type[Building]]:
    with Session(engine) as session:
        return session.query(Building).options(joinedload(Building.categ)).all()


def get_building_by_olx_id(olx_id: int) -> Type[Building]:
    with Session(engine) as session:
        return session.query(Building).filter(Building.olx_id == olx_id).first()
