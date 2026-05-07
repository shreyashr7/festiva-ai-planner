FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/
RUN pip install --upgrade pip && pip install .

COPY data/ data/
COPY models/ models/
COPY dashboard/ dashboard/

EXPOSE 8000 8501

CMD ["uvicorn", "festiva.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
