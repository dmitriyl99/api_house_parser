from fastapi import FastAPI

from contextlib import asynccontextmanager

from app import scheduler



@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()

    yield

    scheduler.stop()


app = FastAPI(lifespan=lifespan)
