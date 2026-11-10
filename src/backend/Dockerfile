FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_URL=sqlite:////data/enterprise_ai.db

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY create_tables.py .

RUN mkdir -p /data app/storage \
    && useradd --create-home --uid 10001 backend \
    && chown -R backend:backend /data app/storage

USER backend

EXPOSE 8000
VOLUME ["/data", "/app/app/storage"]

CMD ["sh", "-c", "python create_tables.py && exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]
