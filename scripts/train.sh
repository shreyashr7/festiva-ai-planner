#!/usr/bin/env bash
set -e

echo "=== Festiva AI - Training Budget Models ==="
cd "$(dirname "$0")/.."

source .venv/bin/activate 2>/dev/null || true
python -m festiva.ml.training
