# 🎉 Festiva Moments - Phase 4: Deployment & Production

Complete deployment guide for the Festiva AI Event Planning Platform.

## 📋 Overview

Phase 4 provides:
- **FastAPI Backend Server** (`server.py`) - REST API for event planning
- **Streamlit Dashboard** (`app.py`) - Interactive UI for event planning
- **Docker Containerization** - Single command deployment for any machine
- **Production-Ready** - Load balanced, health checked, and monitored

---

## 🚀 Quick Start (Docker)

### Prerequisites
- Docker & Docker Compose installed
- No API keys required (demo mode available)

### Run Everything

```bash
# Navigate to project root
cd festiva_planner_final

# Start all services
docker-compose up --build

# Or in detached mode
docker-compose up -d --build
```

### Access the Application

- **Streamlit Dashboard**: http://localhost:8501
- **FastAPI Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/api/v1/health

### Stop Services

```bash
docker-compose down

# With volume cleanup
docker-compose down -v
```

---

## 🛠️ Manual Setup (Without Docker)

### Step 1: Install Dependencies

```bash
pip install -r phase_4_deployment/requirements.txt
```

### Step 2: Start FastAPI Server

```bash
cd phase_4_deployment
python server.py

# Or use uvicorn directly
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 3: Start Streamlit Dashboard (New Terminal)

```bash
cd phase_4_deployment
streamlit run app.py

# Or
streamlit run app.py --server.port 8501
```

**Output:**
```
  You can now view your Streamlit app in your browser.
  URL: http://localhost:8501
```

---

## 📡 API Endpoints

### Health Check
```bash
GET /api/v1/health

# Response
{
  "status": "healthy",
  "timestamp": "2026-05-07T15:49:16.123456",
  "service": "Festiva Moments API"
}
```

### Budget Prediction
```bash
POST /api/v1/predict-budget

# Request Body
{
  "event_type": "Wedding",
  "guest_count": 500,
  "total_budget": 2500000,
  "event_month": 5
}

# Response
{
  "event_type": "Wedding",
  "guest_count": 500,
  "total_budget": 2500000,
  "catering_spend": 1246654.13,
  "venue_spend": 751040.70,
  "decor_spend": 502305.17,
  "catering_pct": 49.9,
  "venue_pct": 30.0,
  "decor_pct": 20.1
}
```

### Knowledge Search
```bash
POST /api/v1/search-knowledge

# Request Body
{
  "query": "wedding venue in Hebbal",
  "k": 3
}

# Response
{
  "query": "wedding venue in Hebbal",
  "results_count": 3,
  "results": "Recommendation 1:\n..."
}
```

### Generate Complete Event Plan
```bash
POST /api/v1/generate-plan

# Request Body
{
  "event_type": "Wedding",
  "guest_count": 500,
  "total_budget": 2500000,
  "event_month": 5,
  "location": "Hebbal"
}

# Response
{
  "status": "success",
  "request_id": "abc123de",
  "event_type": "Wedding",
  "guest_count": 500,
  "total_budget": 2500000,
  "budget_allocation": {
    "catering_spend": 1246654.13,
    "venue_spend": 751040.70,
    "decor_spend": 502305.17
  },
  "recommendations": "[Markdown report]",
  "generated_at": "2026-05-07T15:49:16.123456"
}
```

---

## 📊 Streamlit Dashboard Features

### Input Controls (Sidebar)
- **Event Type**: Dropdown (Wedding, Corporate, Birthday)
- **Guest Count**: Slider (100-1200)
- **Budget**: Slider (₹5L-₹60L)
- **Event Month**: Selector (1-12)
- **Location**: Text input

### Output Sections
1. **Financial Summary** - Total budget with metric cards
2. **Budget Allocation** - Pie chart showing % split
3. **Per-Guest Costs** - Breakdown per attendee
4. **6-Week Timeline** - Expandable week-by-week plan
5. **Venue Recommendations** - From knowledge base
6. **Risk Mitigation** - Contingency scenarios
7. **Export Options** - Download as Markdown or JSON

---

## 🐳 Docker Details

### Service Architecture

```
┌─────────────────────────────────────────────┐
│         Docker Compose Network              │
├─────────────────────────────────────────────┤
│                                             │
│  ┌───────────────┐    ┌──────────────────┐ │
│  │ Streamlit     │    │ FastAPI Backend  │ │
│  │ (Port 8501)   │───▶│ (Port 8000)      │ │
│  └───────────────┘    └──────────────────┘ │
│         │                      │            │
│         └──────────┬───────────┘            │
│                    │                        │
│         ┌──────────▼──────────┐            │
│         │  Shared Volumes     │            │
│         │ (Models, Data, RAG) │            │
│         └─────────────────────┘            │
│                                             │
│         ┌──────────────────────┐           │
│         │  Redis Cache (Opt.)  │           │
│         │  (Port 6379)         │           │
│         └──────────────────────┘           │
│                                             │
└─────────────────────────────────────────────┘
```

### File Structure in Container

```
/app/
├── phase_1_data_ml/           (Read-only)
│   ├── train_engine.py
│   └── budget_engine.pkl      (ML models)
├── phase_2_nlp_rag/           (Read-only)
│   ├── ingest.py
│   ├── knowledge.txt
│   └── faiss_index/           (Vector DB)
├── phase_3_agents/            (Read-only)
│   └── orchestrator.py        (Agent logic)
├── phase_4_deployment/        (Application)
│   ├── server.py              (FastAPI)
│   ├── app.py                 (Streamlit)
│   └── requirements.txt
└── logs/                       (Writable)
    └── *.log
```

### Environment Variables

```bash
# For Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true

# For FastAPI
LOG_LEVEL=info
PYTHONUNBUFFERED=1
```

### Volume Mounts

| Host Path | Container Path | Mode | Purpose |
|-----------|---|---|---|
| `./phase_1_data_ml` | `/app/phase_1_data_ml` | ro | Budget engine models |
| `./phase_2_nlp_rag` | `/app/phase_2_nlp_rag` | ro | FAISS vector index |
| `./phase_3_agents` | `/app/phase_3_agents` | ro | Orchestrator logic |
| `./phase_4_deployment` | `/app/phase_4_deployment` | ro | API & Dashboard code |
| `./logs` | `/app/logs` | rw | Server logs |

---

## 🔧 Configuration & Customization

### Modify Port Numbers

Edit `docker-compose.yml`:

```yaml
services:
  api:
    ports:
      - "9000:8000"  # Map host port 9000 to container 8000
  
  dashboard:
    ports:
      - "9501:8501"  # Map host port 9501 to container 8501
```

### Add Environment Variables

```yaml
services:
  api:
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - LOG_LEVEL=debug
      - MAX_WORKERS=4
```

### Scale Services

```bash
# Run multiple API instances
docker-compose up --scale api=3

# Note: Requires load balancer (nginx) for production
```

---

## 📊 Monitoring & Logs

### View Real-time Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f dashboard

# Last 100 lines
docker-compose logs --tail=100
```

### Health Status

```bash
# Check service health
docker-compose ps

# Manual health check
curl http://localhost:8000/api/v1/health
curl http://localhost:8501/healthz
```

### Performance Monitoring

```bash
# Resource usage
docker stats

# Container inspection
docker inspect festiva-api
docker inspect festiva-dashboard
```

---

## 🚨 Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port in docker-compose.yml
```

### API Connection Error in Dashboard

**Problem**: Dashboard shows "❌ API Offline"

**Solution**:
1. Check if API service is running: `docker-compose ps`
2. View API logs: `docker-compose logs api`
3. Restart API: `docker-compose restart api`
4. Check firewall: Ensure port 8000 is not blocked

### Out of Memory

```bash
# Check available memory
docker stats

# Increase memory in docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 2G
```

### Model Loading Timeout

**Problem**: "FAISS index loading timeout"

**Solution**:
- First load takes time to download embeddings model
- Wait for "✓ FAISS index loaded" in logs
- Subsequent loads are cached

---

## 🔒 Security Considerations

### For Production:
1. **Use environment variables** for API keys:
   ```bash
   docker-compose -f docker-compose.yml --env-file .env up
   ```

2. **Add authentication** to FastAPI:
   ```python
   from fastapi.security import HTTPBearer
   security = HTTPBearer()
   ```

3. **Use HTTPS/TLS**:
   - Add nginx reverse proxy
   - Configure SSL certificates
   - Redirect HTTP to HTTPS

4. **Rate limiting**:
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

5. **API Key validation**:
   ```python
   @app.post("/api/v1/generate-plan")
   async def generate_plan(request: EventPlanRequest, api_key: str = Depends(verify_api_key)):
       ...
   ```

---

## 📦 Deployment to Cloud

### AWS ECS
```bash
# Push image to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <ECR_URI>
docker tag festiva-api:latest <ECR_URI>/festiva-api:latest
docker push <ECR_URI>/festiva-api:latest
```

### Google Cloud Run
```bash
# Build and deploy
gcloud run deploy festiva-api --source . --platform managed
```

### Azure Container Instances
```bash
# Build and push to ACR
az acr build --registry <registry_name> --image festiva:latest .

# Deploy
az container create --resource-group mygroup --name festiva --image <registry>/festiva:latest --ports 8000 8501
```

### Heroku
```bash
# Create app
heroku create festiva-moments

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

---

## ✅ Pre-Production Checklist

- [ ] All models loaded successfully (check logs)
- [ ] FAISS index initialized (no timeout errors)
- [ ] API endpoints responding (curl tests)
- [ ] Dashboard loads without errors
- [ ] Budget predictions accurate (test cases)
- [ ] Knowledge retrieval working
- [ ] Markdown export functional
- [ ] JSON export functional
- [ ] Health checks passing
- [ ] Logs rotating properly
- [ ] Environment variables configured
- [ ] Error handling tested
- [ ] Rate limiting enabled
- [ ] API authentication configured
- [ ] Database backups scheduled

---

## 📞 Support & Documentation

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **API Schema**: http://localhost:8000/openapi.json
- **Project Root**: `/app/`
- **Logs**: `/app/logs/`
- **Models**: `/app/phase_1_data_ml/budget_engine.pkl`
- **Knowledge Base**: `/app/phase_2_nlp_rag/faiss_index/`

---

## 🎓 Next Steps

1. **Customize Branding**: Modify colors in `app.py`
2. **Add Authentication**: Implement user login
3. **Database Integration**: Connect PostgreSQL for user data
4. **Caching Layer**: Implement Redis caching
5. **Analytics**: Add event tracking and metrics
6. **Notifications**: Integrate email/SMS alerts
7. **Payment Integration**: Add Stripe/Razorpay
8. **Mobile App**: Build React Native frontend

---

**Built with ❤️ for Premium Event Planning**

*Last Updated: May 7, 2026*
