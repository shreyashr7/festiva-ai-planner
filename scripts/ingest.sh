#!/usr/bin/env bash
set -e

echo "=== Festiva AI - RAG Knowledge Ingestion ==="
cd "$(dirname "$0")/.."

source .venv/bin/activate 2>/dev/null || true
python -m festiva.rag.ingest
