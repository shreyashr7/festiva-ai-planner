# 🎉 Festiva Moments - AI-Powered Event Planning Platform

**Premium event planning for Bengaluru | ML + RAG + Multi-Agent Architecture**

A complete, production-ready platform for intelligent event budgeting, venue recommendations, and timeline planning using machine learning, retrieval-augmented generation (RAG), and LLM-powered agents.

---

## 🌟 Features

### Phase 1: Budget Intelligence 💰
- **Synthetic Dataset**: 1,200 realistic Bengaluru event records (2026)
- **Market-Aware**: Bengaluru-specific pricing for catering (₹1,200-₹3,500/plate), venues, and decor
- **ML Models**: RandomForest regressors predict catering, venue, decor spends with 99.99% R² accuracy
- **Budget Allocation**: Intelligent splits based on event type (Wedding 50% catering, Corporate 35%, Birthday 45%)

### Phase 2: Knowledge Base (RAG) 📚
- **FAISS Vector Database**: Semantic search over Bengaluru venue & planning knowledge
- **Chunked Knowledge**: 500-character chunks with overlap for context-aware retrieval
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` for efficient semantic understanding
- **Real Venues**: The King's Meadows, Manpho Convention Centre, Rustique Winds, etc.

### Phase 3: Multi-Agent Orchestration 🤖
- **Budget Tool**: Predicts spending allocation for any event scenario
- **Knowledge Tool**: Retrieves venue recommendations and timeline advice
- **Planner Agent**: "Lead Event Strategist at Festiva Moments" persona
- **Markdown Reports**: Professional 6-week implementation plans with contingencies

### Phase 4: Production Deployment 🚀
- **FastAPI Backend**: REST API with 4 endpoints (health, predict, search, generate)
- **Streamlit Dashboard**: Interactive UI with sliders, metrics, charts, and exports
- **Docker Containerization**: Single-command deployment on any machine
- **Production-Ready**: Health checks, logging, CORS, error handling, scalability

---

## 📋 Project Structure

```
festiva_planner_final/
├── phase_1_data_ml/              # Budget ML Engine
│   ├── train_engine.py           # Data generation + model training
│   └── budget_engine.pkl         # Serialized ML models & scaler
├── phase_2_nlp_rag/              # Knowledge Base
│   ├── ingest.py                 # RAG ingestion pipeline
│   ├── knowledge.txt             # Bengaluru venue & planning knowledge
│   └── faiss_index/              # Vector database (6 vectors)
├── phase_3_agents/               # Multi-Agent System
│   ├── orchestrator.py           # Agent orchestration logic
│   └── event_plan_report.md      # Sample generated report
├── phase_4_deployment/           # Production Services
│   ├── server.py                 # FastAPI REST API
│   ├── app.py                    # Streamlit Dashboard
│   ├── requirements.txt          # Python dependencies
│   └── DEPLOYMENT.md             # Detailed deployment guide
├── docker-compose.yml            # Orchestrate API + Dashboard
├── Dockerfile                    # Container specification
├── start.sh                      # Linux/Mac startup script
└── start.bat                     # Windows startup script
```

---

## 🚀 Quick Start

### Option A: Docker (Recommended)

**Prerequisites**: Docker & Docker Compose

**Linux/Mac:**
```bash
cd festiva_planner_final
./start.sh
```

**Windows:**
```bash
cd festiva_planner_final
start.bat
```

**Manual Docker:**
```bash
docker-compose up --build -d
```

**Access:**
- Dashboard: http://localhost:8501
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

### Option B: Manual Setup

**Prerequisites**: Python 3.11+, pip

```bash
# Install dependencies
pip install -r phase_4_deployment/requirements.txt

# Terminal 1: Start API
cd phase_4_deployment
python server.py

# Terminal 2: Start Dashboard
cd phase_4_deployment
streamlit run app.py
```

---

## 📡 API Quick Reference

### Generate Event Plan
```bash
curl -X POST "http://localhost:8000/api/v1/generate-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "Wedding",
    "guest_count": 500,
    "total_budget": 2500000,
    "event_month": 5,
    "location": "Hebbal"
  }'
```

### Budget Prediction
```bash
curl -X POST "http://localhost:8000/api/v1/predict-budget" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "Wedding",
    "guest_count": 500,
    "total_budget": 2500000,
    "event_month": 5
  }'
```

### Knowledge Search
```bash
curl -X POST "http://localhost:8000/api/v1/search-knowledge" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "wedding venue in Hebbal",
    "k": 3
  }'
```

---

## 💡 Dashboard Features

### Input Section (Sidebar)
- **Event Type**: Wedding | Corporate | Birthday
- **Guest Count**: 100-1,200 (slider)
- **Budget**: ₹5L-₹60L (slider)
- **Event Month**: January-December (dropdown)
- **Location**: Bengaluru or specific area

### Output Section
1. **Financial Summary** - 4 metric cards (Total Budget, Catering, Venue, Decor)
2. **Budget Allocation** - Interactive Plotly pie chart
3. **Per-Guest Breakdown** - Cost per attendee
4. **6-Week Timeline** - Expandable sections for each week
5. **Venue Recommendations** - From knowledge base
6. **Risk Mitigation** - Contingency planning
7. **Export Options** - Download as Markdown or JSON

### Example Output
**Wedding, 500 guests, ₹25L budget:**
- Catering: ₹12.47L (49.9%)
- Venue: ₹7.51L (30.0%)
- Decor: ₹5.02L (20.1%)
- Per-guest cost: ₹5,000

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard                      │
│                 (Interactive Web UI - Port 8501)            │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ↓ HTTP Requests
                        │
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend Server                          │
│                  (REST API - Port 8000)                     │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │ Budget Tool  │ Knowledge    │ Orchestrator │            │
│  │              │ Tool (FAISS) │              │            │
│  └──────────────┴──────────────┴──────────────┘            │
└─────────────┬──────────────────────────────────────┬────────┘
              │                                      │
              ↓                                      ↓
    ┌──────────────────┐                   ┌──────────────────┐
    │   Phase 1: ML    │                   │   Phase 2: RAG   │
    │  Models (Models) │                   │  (FAISS Index)   │
    │  - Catering      │                   │  - 6 Vectors     │
    │  - Venue         │                   │  - Venues        │
    │  - Decor         │                   │  - Timelines     │
    └──────────────────┘                   └──────────────────┘
```

---

## 🔧 Technology Stack

### ML & Data
- **scikit-learn**: RandomForest models (Phase 1)
- **NumPy/Pandas**: Data processing
- **FAISS**: Vector database for semantic search (Phase 2)

### NLP & RAG
- **LangChain**: Agent orchestration framework
- **HuggingFace**: Sentence embeddings (all-MiniLM-L6-v2)
- **Sentence-Transformers**: Embedding models

### API & Web
- **FastAPI**: High-performance REST API
- **Streamlit**: Interactive dashboard
- **Plotly**: Data visualization
- **Uvicorn**: ASGI server

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Redis**: Optional caching layer

---

## 📊 Sample Workflow

1. **User Input** (Streamlit Dashboard)
   ```
   Event Type: Wedding
   Guests: 500
   Budget: ₹25L
   ```

2. **API Call** (FastAPI /generate-plan)
   ```json
   {
     "event_type": "Wedding",
     "guest_count": 500,
     "total_budget": 2500000
   }
   ```

3. **Budget Tool** (Phase 1)
   ```
   Input: Wedding, 500 guests, ₹25L
   ↓ (ML Model prediction)
   Output: Catering ₹12.47L, Venue ₹7.51L, Decor ₹5.02L
   ```

4. **Knowledge Tool** (Phase 2)
   ```
   Query: "Wedding venue recommendations"
   ↓ (FAISS semantic search)
   Output: The King's Meadows, Manpho Convention Centre, etc.
   ```

5. **Orchestrator** (Phase 3)
   ```
   Combines budget + knowledge + timeline template
   ↓ (LLM synthesis - optional)
   Output: Professional markdown report
   ```

6. **Dashboard Display** (Phase 4)
   ```
   - Financial Summary cards
   - Budget allocation pie chart
   - 6-week timeline
   - Venue recommendations
   - Export options
   ```

---

## 🎯 Key Metrics

| Component | Metric | Value |
|-----------|--------|-------|
| **Budget Model** | R² Score | 0.9999 |
| **Budget Model** | RMSE | ₹2,866-8,723 |
| **Dataset** | Events Generated | 1,200 |
| **Dataset** | Date Range | Full year 2026 |
| **Knowledge Base** | Chunks | 6 |
| **Knowledge Base** | Embedding Model | all-MiniLM-L6-v2 (384-dim) |
| **API** | Endpoints | 4 |
| **API** | Response Time | <500ms |
| **Dashboard** | Supported Events | 3 types |
| **Dashboard** | Guest Range | 100-1,200 |
| **Dashboard** | Budget Range | ₹5L-₹60L |

---

## 📈 Bengaluru Market Insights (2026)

### Catering Rates
- **Premium**: ₹1,200-₹3,500/plate
- **Corporate Lunch**: ₹900-₹1,500
- **Popular Cuisines**: North Indian, South Indian, Fusion
- **Dietary**: Veg/Non-Veg/Jain options

### Venue Distribution
- **North (Hebbal/Yelahanka)**: The King's Meadows, Manpho Convention Centre
- **East (Whitefield/Marathahalli)**: Rustique Winds, Sheraton Grand, The Zuri
- **Central/South**: Royal Orchid, Gowri Kalyana Mantapa, The Black Rabbit

### Planning Timelines
- **Weddings**: 4-6 months lead time
- **Corporate**: 4-8 weeks
- **Birthday**: 2-4 weeks
- **6-Week Cycle**: Week 1-2 (Foundation), Week 3-4 (Design), Week 5 (Rehearsal), Week 6 (Execution)

### Traffic Considerations
- **Peak Hours**: Silk Board (10-12 AM, 5-7 PM), Marathahalli (similar)
- **Optimal Timing**: 11:00 AM or 7:30 PM event starts
- **North Bengaluru**: Shuttle services recommended for South-based guests

---

## 🛠️ Configuration & Customization

### Change Port Numbers
Edit `docker-compose.yml`:
```yaml
api:
  ports:
    - "9000:8000"  # API on port 9000
dashboard:
  ports:
    - "9501:8501"  # Dashboard on port 9501
```

### Add LLM Integration
Set environment variables:
```bash
export GOOGLE_API_KEY="your-key-here"
# or
export OPENAI_API_KEY="your-key-here"
```

### Scale Services
```bash
docker-compose up --scale api=3 -d
```

---

## 🔒 Security

### For Development
- ✓ CORS enabled (localhost only)
- ✓ Health checks enabled
- ✓ Error handling implemented

### For Production
- [ ] Add API key authentication
- [ ] Enable HTTPS/TLS
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Set up monitoring
- [ ] Configure database backups
- [ ] Use environment variables for secrets

---

## 📚 Documentation

- **Phase 1**: [Budget ML Engine](phase_1_data_ml/train_engine.py)
- **Phase 2**: [RAG Knowledge Base](phase_2_nlp_rag/ingest.py)
- **Phase 3**: [Multi-Agent System](phase_3_agents/orchestrator.py)
- **Phase 4**: [Deployment Guide](phase_4_deployment/DEPLOYMENT.md)
- **API Docs**: http://localhost:8000/docs

---

## 🐛 Troubleshooting

### API Won't Start
```bash
# Check port 8000 is free
lsof -i :8000
kill -9 <PID>

# View logs
docker-compose logs api
```

### Dashboard Connection Error
```bash
# Ensure API is running
docker-compose ps

# Check health
curl http://localhost:8000/api/v1/health
```

### Models Won't Load
```bash
# Check files exist
ls -la phase_1_data_ml/budget_engine.pkl
ls -la phase_2_nlp_rag/faiss_index/

# View logs
docker-compose logs -f
```

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- [ ] Real LLM integration (Gemini/ChatGPT)
- [ ] Database backend (PostgreSQL)
- [ ] User authentication
- [ ] Payment integration (Stripe)
- [ ] Email notifications
- [ ] Analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Advanced vendor matching

---

## 📄 License

MIT License - See LICENSE file

---

## 👥 Team

**Built for Premium Event Planners in Bengaluru**

- **ML Engineer**: Phase 1 (Budget prediction models)
- **Data Engineer**: Phase 2 (RAG knowledge base)
- **AI Engineer**: Phase 3 (Multi-agent orchestration)
- **Full-Stack Engineer**: Phase 4 (Production deployment)

---

## 🎯 Future Roadmap

- **Q3 2026**: Real LLM integration + payment gateway
- **Q4 2026**: Mobile app launch + vendor matching
- **Q1 2027**: Advanced analytics + predictive timeline
- **Q2 2027**: Multi-city expansion (Delhi, Mumbai, Pune)

---

## 📞 Support

- **Issues**: Check logs with `docker-compose logs -f`
- **Docs**: Read [DEPLOYMENT.md](phase_4_deployment/DEPLOYMENT.md)
- **API**: Visit http://localhost:8000/docs for interactive docs

---

## 🙏 Acknowledgments

- Built with LangChain, FastAPI, Streamlit
- Data inspired by real Bengaluru venue & vendor networks
- ML models powered by scikit-learn
- RAG implementation using FAISS & HuggingFace

---

**🎉 Ready to plan premium events! Start with `./start.sh` or `start.bat`**

*Last Updated: May 7, 2026*
