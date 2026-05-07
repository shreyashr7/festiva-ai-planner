.PHONY: install dev train ingest server frontend test lint format clean docker-up docker-down

install:
	pip install -e .

dev:
	pip install -e ".[dev]"
	cd frontend && npm install

train:
	python -m festiva.ml.training

ingest:
	python -m festiva.rag.ingest

server:
	uvicorn festiva.api.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm run dev

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/
	ruff format --check src/ tests/

format:
	ruff format src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist build .pytest_cache .ruff_cache

docker-up:
	cd docker && docker compose up --build -d

docker-down:
	cd docker && docker compose down
