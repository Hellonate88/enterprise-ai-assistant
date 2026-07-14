from fastapi import FastAPI
from app.api import health


app = FastAPI(
    title="Enterprise AI Assistant"
)


app.include_router(
    health.router
)