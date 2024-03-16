from typing import Type

from sqlalchemy.orm import Session

from . import engine
from app.dal.models import Category


def find_category_by_name(category_name: str) -> Type[Category]:
    with Session(engine) as session:
        return session.query(Category).filter(Category.name == category_name).first()
