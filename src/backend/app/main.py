import logging

from fastapi import FastAPI
from app.api import health
from app.api import documents


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)


app = FastAPI(
    title="Enterprise AI Assistant"
)


app.include_router(
    health.router
)

app.include_router(
    documents.router
)