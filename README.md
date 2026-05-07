# Festiva AI Planner

AI-powered event planning platform for Bengaluru — ML budget prediction, RAG knowledge retrieval, and multi-agent orchestration.

## Project Structure

```
festiva-ai-planner/
├── src/festiva/              # Main application package
│   ├── config.py             # Centralized configuration
│   ├── ml/                   # Budget prediction (RandomForest)
│   │   └── training.py       # Synthetic data generation & model training
│   ├── rag/                  # Knowledge base (FAISS + embeddings)
│   │   └── ingest.py         # Text chunking & vector store creation
│   ├── agents/               # Multi-agent orchestration
│   │   └── orchestrator.py   # LLM agent with budget & knowledge tools
│   └── api/                  # FastAPI REST API
│       ├── main.py           # Application entry point
│       ├── schemas.py        # Pydantic request/response models
│       └── routes/           # Endpoint handlers
│           ├── budget.py
│           ├── knowledge.py
│           └── plans.py
├── dashboard/                # Streamlit frontend
│   └── app.py
├── data/                     # Knowledge base & vector index
├── models/                   # Trained model artifacts (.pkl)
├── tests/                    # Test suite
├── scripts/                  # Utility scripts
├── docker/                   # Docker configuration
├── docs/                     # Documentation
├── pyproject.toml            # Project metadata & dependencies
├── Makefile                  # Development commands
└── .env.example              # Environment variable template
```

## Quick Start

### 1. Setup Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your API keys (GOOGLE_API_KEY or OPENAI_API_KEY)
```

### 3. Train Models

```bash
make train
```

### 4. Ingest Knowledge Base

```bash
make ingest
```

### 5. Run the API Server

```bash
make server
```

### 6. Run the Dashboard

```bash
make dashboard
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/predict-budget` | Predict budget allocation |
| POST | `/api/v1/search-knowledge` | Search knowledge base |
| POST | `/api/v1/generate-plan` | Generate full event plan |

## Docker Deployment

```bash
make docker-up
```

## Development

```bash
make dev       # Install with dev dependencies
make test      # Run tests
make lint      # Check code style
make format    # Auto-format code
```
