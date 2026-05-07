#!/bin/bash

# Festiva Moments - Startup Script
# Simplified deployment for local development and testing

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================================================
# HEADER
# ============================================================================
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        🎉 Festiva Moments - Event Planning Platform           ║"
echo "║                  Phase 4: Deployment & Production             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ============================================================================
# CHECK PREREQUISITES
# ============================================================================
echo -e "${YELLOW}[1/4] Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo "   Install from: https://www.docker.com/products/docker-desktop"
    exit 1
fi
echo -e "${GREEN}✓ Docker found: $(docker --version)${NC}"

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    echo "   Install from: https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose found: $(docker-compose --version)${NC}"

# ============================================================================
# VERIFY PROJECT STRUCTURE
# ============================================================================
echo -e "${YELLOW}[2/4] Verifying project structure...${NC}"

required_files=(
    "phase_1_data_ml/budget_engine.pkl"
    "phase_2_nlp_rag/faiss_index/index.faiss"
    "phase_3_agents/orchestrator.py"
    "phase_4_deployment/server.py"
    "phase_4_deployment/app.py"
    "docker-compose.yml"
    "Dockerfile"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ] && [ ! -d "$file" ]; then
        echo -e "${RED}❌ Missing: $file${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Found: $file${NC}"
done

# ============================================================================
# BUILD & START SERVICES
# ============================================================================
echo -e "${YELLOW}[3/4] Building Docker images and starting services...${NC}"
echo "This may take a few minutes on first run..."

docker-compose up --build -d

# ============================================================================
# WAIT FOR SERVICES TO BE READY
# ============================================================================
echo -e "${YELLOW}[4/4] Waiting for services to be healthy...${NC}"

# Wait for API to be ready
echo "⏳ Waiting for API (port 8000)..."
for i in {1..30}; do
    if curl -f http://localhost:8000/api/v1/health &> /dev/null; then
        echo -e "${GREEN}✓ API is ready${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# Wait for Dashboard to be ready
echo "⏳ Waiting for Dashboard (port 8501)..."
for i in {1..30}; do
    if curl -f http://localhost:8501/healthz &> /dev/null; then
        echo -e "${GREEN}✓ Dashboard is ready${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

sleep 2

# ============================================================================
# DISPLAY SERVICE INFORMATION
# ============================================================================
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           ✅ Festiva Moments is ready to use!                 ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Get local IP
LOCAL_IP=$(hostname -I | awk '{print $1}')
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP="127.0.0.1"
fi

echo -e "${YELLOW}📊 Dashboard (Web UI)${NC}"
echo -e "   ${GREEN}→ http://localhost:8501${NC}"
echo -e "   ${GREEN}→ http://$LOCAL_IP:8501${NC}"
echo ""

echo -e "${YELLOW}📡 API Server${NC}"
echo -e "   ${GREEN}→ http://localhost:8000${NC}"
echo -e "   ${GREEN}→ http://$LOCAL_IP:8000${NC}"
echo ""

echo -e "${YELLOW}📖 API Documentation${NC}"
echo -e "   ${GREEN}→ http://localhost:8000/docs${NC}"
echo -e "   ${GREEN}→ http://localhost:8000/redoc${NC}"
echo ""

echo -e "${YELLOW}🏥 Health Check${NC}"
echo -e "   ${GREEN}→ http://localhost:8000/api/v1/health${NC}"
echo ""

echo -e "${YELLOW}🛑 Stop Services${NC}"
echo -e "   ${GREEN}→ docker-compose down${NC}"
echo ""

echo -e "${YELLOW}📋 View Logs${NC}"
echo -e "   ${GREEN}→ docker-compose logs -f${NC}"
echo -e "   ${GREEN}→ docker-compose logs -f api${NC}"
echo -e "   ${GREEN}→ docker-compose logs -f dashboard${NC}"
echo ""

echo -e "${YELLOW}🔄 Restart Services${NC}"
echo -e "   ${GREEN}→ docker-compose restart${NC}"
echo ""

echo -e "${YELLOW}📊 Service Status${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}Ready to plan events! 🎉${NC}"
