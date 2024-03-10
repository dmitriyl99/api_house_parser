from fastapi import FastAPI
import logging

from contextlib import asynccontextmanager

from app import scheduler


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
