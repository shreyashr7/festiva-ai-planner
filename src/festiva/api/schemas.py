"""Pydantic request/response schemas for the API."""

from typing import Literal

from pydantic import BaseModel, Field

EventType = Literal["Wedding", "Corporate", "Birthday"]


class BudgetPredictionRequest(BaseModel):
    event_type: EventType = Field(..., description="Type of event")
    guest_count: int = Field(..., ge=100, le=1200, description="Number of guests (100-1200)")
    total_budget: float = Field(
        ..., ge=500000, le=6000000, description="Total budget in INR (₹5L-₹60L)"
    )
    event_month: int = Field(default=5, ge=1, le=12, description="Month of event (1-12)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_type": "Wedding",
                "guest_count": 500,
                "total_budget": 2500000,
                "event_month": 5,
            }
        }
    }


class BudgetAllocation(BaseModel):
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
    query: str = Field(..., min_length=1, max_length=500, description="Search query")
    k: int = Field(default=3, ge=1, le=10, description="Number of results")

    model_config = {
        "json_schema_extra": {"example": {"query": "corporate event in Whitefield", "k": 3}}
    }


class KnowledgeSearchResponse(BaseModel):
    query: str
    results_count: int
    results: str


class TimelineWeek(BaseModel):
    week: str
    phase: str
    icon: str
    tasks: list[str]
    budget_note: str


class VendorRecommendation(BaseModel):
    name: str
    category: str
    estimated_cost: float
    rating: float
    description: str
    location: str


class RiskItem(BaseModel):
    risk: str
    impact: str
    mitigation: str
    buffer: float


class EventPlanRequest(BaseModel):
    event_type: EventType = Field(..., description="Type of event")
    guest_count: int = Field(..., ge=100, le=1200, description="Number of guests (100-1200)")
    total_budget: float = Field(
        ..., ge=500000, le=6000000, description="Total budget in INR (₹5L-₹60L)"
    )
    event_month: int = Field(default=5, ge=1, le=12, description="Month of event (1-12)")
    location: str = Field(default="Bengaluru", max_length=100, description="Event location")

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_type": "Wedding",
                "guest_count": 500,
                "total_budget": 2500000,
                "event_month": 5,
                "location": "Hebbal",
            }
        }
    }


class EventPlanResponse(BaseModel):
    status: str
    request_id: str
    event_type: str
    guest_count: int
    total_budget: float
    location: str
    event_month: int
    budget_allocation: BudgetAllocation
    per_guest_cost: float
    contingency_budget: float
    timeline: list[TimelineWeek]
    vendors: list[VendorRecommendation]
    risks: list[RiskItem]
    recommendations: str
    generated_at: str
