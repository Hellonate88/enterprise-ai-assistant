import logging
import os
from pathlib import Path

from fastapi import FastAPI
from app.api import health
from app.api import documents
from app.api.chat import router as chat_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]

        os.environ.setdefault(key, value)


load_env_file(Path(__file__).resolve().parents[2] / ".env")


app = FastAPI(
    title="Enterprise AI Assistant"
)


app.include_router(
    health.router
)

app.include_router(
    documents.router
)

app.include_router(chat_router)