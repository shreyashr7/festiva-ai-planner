"""Application configuration and settings."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = ROOT_DIR / os.getenv("DATA_DIR", "data")
MODELS_DIR = ROOT_DIR / os.getenv("MODELS_DIR", "models")
FAISS_INDEX_DIR = DATA_DIR / "faiss_index"
KNOWLEDGE_FILE = DATA_DIR / "knowledge.txt"

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

# LLM settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ML settings
RANDOM_SEED = 42
N_EVENTS = 1200
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
