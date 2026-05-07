"""FastAPI application entry point."""

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from festiva.api.routes import budget, knowledge, plans
from festiva.config import HOST, PORT, LOG_LEVEL, ROOT_DIR

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Festiva Moments API",
    description="AI-Powered Event Planning Engine for Bengaluru",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(budget.router)
app.include_router(knowledge.router)
app.include_router(plans.router)

# Serve frontend build if available
frontend_dist = ROOT_DIR / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")


@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "ok",
        "service": "Festiva Moments Event Planning API",
        "version": "1.0.0",
    }


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    from datetime import datetime

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Festiva Moments API",
    }


def start():
    """CLI entry point."""
    uvicorn.run("festiva.api.main:app", host=HOST, port=PORT, reload=True, log_level=LOG_LEVEL)


if __name__ == "__main__":
    start()
