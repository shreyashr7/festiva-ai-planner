"""
FastAPI Server for Festiva Moments Event Planning Engine
Exposes REST API endpoints for event plan generation
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import logging

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "phase_3_agents"))

from orchestrator import (
    plan_event,
    predict_budget_splits_impl,
    search_venue_and_timeline_advice_impl
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# FASTAPI APP INITIALIZATION
# ============================================================================
app = FastAPI(
    title="Festiva Moments API",
    description="AI-Powered Event Planning Engine for Bengaluru",
    version="1.0.0"
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================
class BudgetPredictionRequest(BaseModel):
    """Request model for budget prediction"""
    event_type: str = Field(..., description="Type of event: Wedding, Corporate, or Birthday")
    guest_count: int = Field(..., ge=100, le=1200, description="Number of guests (100-1200)")
    total_budget: float = Field(..., ge=500000, le=6000000, description="Total budget in INR (₹5L-₹60L)")
    event_month: int = Field(default=5, ge=1, le=12, description="Month of event (1-12)")

    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "Wedding",
                "guest_count": 500,
                "total_budget": 2500000,
                "event_month": 5
            }
        }


class BudgetPredictionResponse(BaseModel):
    """Response model for budget prediction"""
    event_type: str
    guest_count: int
    total_budget: float
    catering_spend: float
    venue_spend: float
    decor_spend: float
    catering_pct: float
    venue_pct: float
    decor_pct: float


class KnowledgeSearchRequest(BaseModel):
    """Request model for knowledge base search"""
    query: str = Field(..., description="Search query for venue/timeline advice")
    k: int = Field(default=3, ge=1, le=10, description="Number of results to retrieve")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "corporate event in Whitefield",
                "k": 3
            }
        }


class KnowledgeSearchResponse(BaseModel):
    """Response model for knowledge search"""
    query: str
    results_count: int
    results: str


class EventPlanRequest(BaseModel):
    """Request model for full event planning"""
    event_type: str = Field(..., description="Type of event: Wedding, Corporate, or Birthday")
    guest_count: int = Field(..., ge=100, le=1200, description="Number of guests (100-1200)")
    total_budget: float = Field(..., ge=500000, le=6000000, description="Total budget in INR (₹5L-₹60L)")
    event_month: int = Field(default=5, ge=1, le=12, description="Month of event (1-12)")
    location: Optional[str] = Field(default="Bengaluru", description="Event location")

    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "Wedding",
                "guest_count": 500,
                "total_budget": 2500000,
                "event_month": 5,
                "location": "Hebbal"
            }
        }


class EventPlanResponse(BaseModel):
    """Response model for event plan"""
    status: str
    request_id: str
    event_type: str
    guest_count: int
    total_budget: float
    budget_allocation: Dict
    timeline: str
    recommendations: str
    generated_at: str

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "ok",
        "service": "Festiva Moments Event Planning API",
        "version": "1.0.0",
        "endpoints": [
            "/api/v1/health",
            "/api/v1/predict-budget",
            "/api/v1/search-knowledge",
            "/api/v1/generate-plan"
        ]
    }


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Festiva Moments API"
    }

# ============================================================================
# BUDGET PREDICTION ENDPOINT
# ============================================================================
@app.post("/api/v1/predict-budget", response_model=BudgetPredictionResponse, tags=["Budget"])
async def predict_budget(request: BudgetPredictionRequest):
    """
    Predict budget allocation for event
    
    Args:
        request: Budget prediction request with event details
    
    Returns:
        Budget breakdown with catering, venue, and decor allocations
    """
    try:
        logger.info(f"Processing budget prediction for {request.event_type} with {request.guest_count} guests")
        
        # Call the budget prediction function
        budget_json = predict_budget_splits_impl(
            event_type=request.event_type,
            guest_count=request.guest_count,
            total_budget=request.total_budget,
            event_month=request.event_month
        )
        
        # Parse and return
        budget_data = json.loads(budget_json)
        return BudgetPredictionResponse(**budget_data)
    
    except Exception as e:
        logger.error(f"Error in budget prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Budget prediction failed: {str(e)}")

# ============================================================================
# KNOWLEDGE SEARCH ENDPOINT
# ============================================================================
@app.post("/api/v1/search-knowledge", response_model=KnowledgeSearchResponse, tags=["Knowledge"])
async def search_knowledge(request: KnowledgeSearchRequest):
    """
    Search knowledge base for venue and timeline advice
    
    Args:
        request: Knowledge search request with query
    
    Returns:
        Relevant venue recommendations and planning advice
    """
    try:
        logger.info(f"Processing knowledge search: {request.query}")
        
        # Call the knowledge search function
        results = search_venue_and_timeline_advice_impl(
            query=request.query,
            k=request.k
        )
        
        return KnowledgeSearchResponse(
            query=request.query,
            results_count=request.k,
            results=results
        )
    
    except Exception as e:
        logger.error(f"Error in knowledge search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Knowledge search failed: {str(e)}")

# ============================================================================
# FULL EVENT PLAN ENDPOINT
# ============================================================================
@app.post("/api/v1/generate-plan", response_model=EventPlanResponse, tags=["Planning"])
async def generate_event_plan(request: EventPlanRequest):
    """
    Generate complete event plan with budget allocation and recommendations
    
    Args:
        request: Event plan request with all event details
    
    Returns:
        Complete event plan including budget, timeline, and venue recommendations
    """
    try:
        import uuid
        request_id = str(uuid.uuid4())[:8]
        logger.info(f"[{request_id}] Generating event plan for {request.event_type}")
        
        # Build a natural language request for the orchestrator
        nl_request = f"I'm planning a {request.event_type} in {request.location} with {request.guest_count} guests and a budget of ₹{request.total_budget / 100000:.0f} lakhs."
        
        # Call orchestrator to generate full plan
        markdown_report = plan_event(nl_request)
        
        # Parse budget from markdown report
        budget_data: Dict[str, float] = {
            "catering_spend": 0.0,
            "venue_spend": 0.0,
            "decor_spend": 0.0,
            "catering_pct": 0.0,
            "venue_pct": 0.0,
            "decor_pct": 0.0
        }
        
        # Extract numbers from markdown
        import re
        lines = markdown_report.split('\n')
        for line in lines:
            if 'Catering' in line and '₹' in line:
                match = re.search(r'₹([\d,]+)', line)
                if match:
                    budget_data['catering_spend'] = float(match.group(1).replace(',', ''))
            elif 'Venue' in line and '₹' in line and 'Decor' not in line:
                match = re.search(r'₹([\d,]+)', line)
                if match:
                    budget_data['venue_spend'] = float(match.group(1).replace(',', ''))
            elif 'Decor' in line and '₹' in line:
                match = re.search(r'₹([\d,]+)', line)
                if match:
                    budget_data['decor_spend'] = float(match.group(1).replace(',', ''))
        
        return EventPlanResponse(
            status="success",
            request_id=request_id,
            event_type=request.event_type,
            guest_count=request.guest_count,
            total_budget=request.total_budget,
            budget_allocation=budget_data,
            timeline="See recommendations below",
            recommendations=markdown_report,
            generated_at=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error generating event plan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Event plan generation failed: {str(e)}")

# ============================================================================
# ERROR HANDLERS
# ============================================================================
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "detail": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    
    print("=" * 80)
    print("Starting Festiva Moments API Server")
    print("=" * 80)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
