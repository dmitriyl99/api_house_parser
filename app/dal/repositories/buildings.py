from typing import List, Type

from sqlalchemy import text
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


def get_buildings(source: str = None, page: int = 1, per_page: int = 20) -> List[Type[Building]]:
    with Session(engine) as session:
        query = session.query(Building).options(joinedload(Building.category), joinedload(Building.images))
        if source:
            query = query.filter(Building.source == source)
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        return items


def get_olx_buildings() -> List[Type[Building]]:
    with Session(engine) as session:
        return session.query(Building).filter(Building.olx_id.isnot(None)).all()


def set_title_and_description(building_id, title, description):
    with Session(engine) as session:
        session.query(Building).filter(Building.id == building_id).update({'title': title, 'description': description})
        session.commit()


def get_building_by_olx_id(olx_id: int) -> Type[Building]:
    with Session(engine) as session:
        return session.query(Building).filter(Building.olx_id == olx_id).first()


def find_building_by_uybor_id(uybor_id: int) -> Type[Building]:
    with Session(engine) as session:
        return session.query(Building).filter(Building.uybor_id == uybor_id).first()
