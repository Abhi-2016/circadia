from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.logging_config import setup_logging
from app.routers import session

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info({"event": "startup", "service": "circadia-brain"})
    yield
    logger.info({"event": "shutdown", "service": "circadia-brain"})


app = FastAPI(title="Circadia Brain", lifespan=lifespan)

app.include_router(session.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "circadia-brain"}
