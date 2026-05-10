from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.logging_config import setup_logging
from app.routers import stress_triage

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info({"event": "startup", "service": "circadia-brain"})
    yield
    logger.info({"event": "shutdown", "service": "circadia-brain"})


app = FastAPI(title="Circadia Brain", lifespan=lifespan)

app.include_router(stress_triage.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "circadia-brain"}
