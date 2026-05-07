# Multi-stage Dockerfile for Festiva Moments Event Planning Engine
# Containerizes FastAPI backend and Streamlit frontend

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# ============================================================================
# STAGE 2: COPY APPLICATION
# ============================================================================
FROM base

# Copy entire project structure
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/models \
    && mkdir -p /app/logs \
    && mkdir -p /app/cache

# Set permissions
RUN chmod +x /app/*.py 2>/dev/null || true

# ============================================================================
# EXPOSE PORTS
# ============================================================================
# FastAPI server on 8000
EXPOSE 8000
# Streamlit on 8501
EXPOSE 8501

# ============================================================================
# HEALTHCHECK
# ============================================================================
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# ============================================================================
# DEFAULT COMMAND (runs FastAPI server)
# ============================================================================
# Use docker-compose to run both services
CMD ["uvicorn", "phase_4_deployment.server:app", "--host", "0.0.0.0", "--port", "8000"]
