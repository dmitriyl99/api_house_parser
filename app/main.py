from fastapi import FastAPI
import logging

from contextlib import asynccontextmanager

from app import scheduler
from app.dal.repositories import buildings


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()

    yield

    scheduler.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/api/buildings")
async def get_buildings(page: int = 1, source: str | None = None):
    return buildings.get_buildings(source, page)
