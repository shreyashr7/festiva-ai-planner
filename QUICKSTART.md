# Phase 4 Deployment - Quick Reference

## 🎯 One-Line Start

### Linux/Mac
```bash
cd festiva_planner_final && ./start.sh
```

### Windows
```bash
cd festiva_planner_final && start.bat
```

### Manual Docker
```bash
docker-compose up --build -d
```

---

## 🔗 Quick Links (After Starting)

| Service | URL | Purpose |
|---------|-----|---------|
| Dashboard | http://localhost:8501 | Web UI for event planning |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| API Health | http://localhost:8000/api/v1/health | Health check |
| ReDoc | http://localhost:8000/redoc | Alternative API docs |

---

## 📡 API Endpoints

```bash
# 1. Health Check
GET /api/v1/health

# 2. Predict Budget
POST /api/v1/predict-budget
Body: {
  "event_type": "Wedding",
  "guest_count": 500,
  "total_budget": 2500000,
  "event_month": 5
}

# 3. Search Knowledge
POST /api/v1/search-knowledge
Body: {
  "query": "wedding venue in Hebbal",
  "k": 3
}

# 4. Generate Full Plan
POST /api/v1/generate-plan
Body: {
  "event_type": "Wedding",
  "guest_count": 500,
  "total_budget": 2500000,
  "event_month": 5,
  "location": "Hebbal"
}
```

---

## 🛑 Common Commands

| Task | Command |
|------|---------|
| Start Services | `docker-compose up -d` |
| Stop Services | `docker-compose down` |
| View Logs | `docker-compose logs -f` |
| View API Logs | `docker-compose logs -f api` |
| View Dashboard Logs | `docker-compose logs -f dashboard` |
| Restart All | `docker-compose restart` |
| Check Status | `docker-compose ps` |
| Remove Everything | `docker-compose down -v` |
| Rebuild Images | `docker-compose up --build -d` |

---

## 📊 File Structure

```
festiva_planner_final/
├── README.md                     # Main documentation
├── Dockerfile                    # Container specification
├── docker-compose.yml            # Multi-service orchestration
├── start.sh                      # Linux/Mac startup
├── start.bat                     # Windows startup
├── .dockerignore                 # Docker build optimization
│
├── phase_1_data_ml/              # ✅ Budget ML Engine
│   ├── train_engine.py           # Generates 1,200 events + trains models
│   └── budget_engine.pkl         # Serialized RandomForest models
│
├── phase_2_nlp_rag/              # ✅ Knowledge Base (RAG)
│   ├── ingest.py                 # FAISS indexing pipeline
│   ├── knowledge.txt             # Venue & planning knowledge
│   └── faiss_index/              # Vector database
│       ├── index.faiss
│       └── index.pkl
│
├── phase_3_agents/               # ✅ Multi-Agent Orchestration
│   ├── orchestrator.py           # Budget + Knowledge tool orchestration
│   └── event_plan_report.md      # Sample generated report
│
└── phase_4_deployment/           # ✅ Production Services
    ├── server.py                 # FastAPI REST backend
    ├── app.py                    # Streamlit web dashboard
    ├── requirements.txt          # Python dependencies
    └── DEPLOYMENT.md             # Detailed deployment guide
```

---

## 🌍 Network & Ports

```
┌─────────────────────────────────────────────┐
│         Docker Container Network            │
├─────────────────────────────────────────────┤
│                                             │
│  Streamlit Dashboard                        │
│  Port: 8501                                 │
│  Host: http://localhost:8501                │
│                                             │
│         ↓ HTTP Requests                     │
│                                             │
│  FastAPI Backend                            │
│  Port: 8000                                 │
│  Host: http://localhost:8000                │
│                                             │
│  Endpoints:                                 │
│  - /api/v1/health                          │
│  - /api/v1/predict-budget                  │
│  - /api/v1/search-knowledge                │
│  - /api/v1/generate-plan                   │
│  - /docs (Swagger UI)                      │
│  - /redoc (ReDoc)                          │
│                                             │
│  Shared Volumes:                           │
│  - /app/phase_1_data_ml (ML models)        │
│  - /app/phase_2_nlp_rag (FAISS index)      │
│  - /app/phase_3_agents (Orchestrator)      │
│  - /app/logs (Output logs)                 │
│                                             │
│  Optional: Redis Cache                      │
│  Port: 6379                                 │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 💡 Example Usage

### Using curl

```bash
# 1. Check if API is alive
curl http://localhost:8000/api/v1/health

# 2. Predict budget for a wedding
curl -X POST http://localhost:8000/api/v1/predict-budget \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "Wedding",
    "guest_count": 500,
    "total_budget": 2500000,
    "event_month": 5
  }'

# 3. Search for venue recommendations
curl -X POST http://localhost:8000/api/v1/search-knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "query": "wedding venue recommendations",
    "k": 3
  }'

# 4. Generate complete event plan
curl -X POST http://localhost:8000/api/v1/generate-plan \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "Wedding",
    "guest_count": 500,
    "total_budget": 2500000,
    "event_month": 5,
    "location": "Hebbal"
  }'
```

### Using Python

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{BASE_URL}/api/v1/health")
print(response.json())

# Generate plan
payload = {
    "event_type": "Wedding",
    "guest_count": 500,
    "total_budget": 2500000,
    "event_month": 5,
    "location": "Hebbal"
}
response = requests.post(
    f"{BASE_URL}/api/v1/generate-plan",
    json=payload
)
plan = response.json()
print(json.dumps(plan, indent=2))
```

---

## 🔧 Troubleshooting

### "Cannot connect to API"
```bash
# Check if API is running
docker-compose ps

# View API logs
docker-compose logs api

# Restart API
docker-compose restart api
```

### "Port already in use"
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### "Models won't load"
```bash
# Verify files exist
ls -la phase_1_data_ml/budget_engine.pkl
ls -la phase_2_nlp_rag/faiss_index/

# Check full logs
docker-compose logs
```

### "FAISS index loading timeout"
```bash
# First load downloads embedding model (~400MB)
# Wait for "✓ FAISS index loaded" in logs
# Subsequent loads are much faster (cached)

docker-compose logs -f
```

---

## 📈 Performance Tips

1. **Caching**: Results are cached by Streamlit automatically
2. **Scaling**: Run `docker-compose up --scale api=3` for multiple API instances
3. **Monitoring**: Use `docker stats` to monitor resource usage
4. **Logs**: Rotate logs monthly to prevent disk space issues

---

## 🔒 Security Checklist

- [ ] API keys stored in `.env` (not in code)
- [ ] HTTPS enabled for production
- [ ] Rate limiting configured
- [ ] Input validation enabled
- [ ] CORS restrictions set
- [ ] Logs don't contain sensitive data
- [ ] Database credentials secured
- [ ] Docker images scanned for vulnerabilities

---

## 📊 Key Files Reference

| File | Purpose | Key Content |
|------|---------|-------------|
| `server.py` | FastAPI backend | 4 endpoints, Pydantic models |
| `app.py` | Streamlit frontend | UI with sliders, charts, markdown |
| `orchestrator.py` | Agent orchestration | Budget + Knowledge tools, report generation |
| `budget_engine.pkl` | ML models | 3 RandomForest models + scaler |
| `faiss_index/` | Vector database | 6 semantic chunks of Bengaluru knowledge |
| `docker-compose.yml` | Service orchestration | API, Dashboard, optional Cache |
| `Dockerfile` | Container spec | Python 3.11, dependencies, volumes |

---

## ✅ Pre-Production Checklist

- [ ] All services start without errors
- [ ] API health check passes
- [ ] Budget predictions are accurate
- [ ] Knowledge retrieval works
- [ ] Dashboard renders correctly
- [ ] Export (Markdown/JSON) functions work
- [ ] Logs are clean (no errors)
- [ ] Load test passes (simulate 10+ concurrent users)
- [ ] Error handling tested
- [ ] CORS working for frontend calls

---

## 🚀 Deployment Options

### Local Development
```bash
docker-compose up -d
```

### AWS ECS
```bash
aws ecr get-login-password | docker login ...
docker push <ECR_URI>/festiva-api:latest
```

### Google Cloud Run
```bash
gcloud run deploy festiva-api --source .
```

### Heroku
```bash
heroku create festiva-moments
git push heroku main
```

### DigitalOcean App Platform
```bash
doctl apps create --spec app.yaml
```

---

## 📞 Support Resources

- **API Docs**: http://localhost:8000/docs
- **Project Docs**: See `/README.md`
- **Deployment Guide**: See `phase_4_deployment/DEPLOYMENT.md`
- **Code**: Check `phase_4_deployment/server.py` and `app.py`

---

**🎉 Ready to launch! Start with `./start.sh` or `start.bat`**

*Last Updated: May 7, 2026*
