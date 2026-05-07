"""Event plan generation API routes."""

import logging

from fastapi import APIRouter, HTTPException

from festiva.agents.orchestrator import plan_event
from festiva.api.schemas import EventPlanRequest, EventPlanResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["Planning"])


@router.post("/generate-plan", response_model=EventPlanResponse)
async def generate_plan(request: EventPlanRequest):
    """Generate a complete event plan."""
    try:
        logger.info(
            "Plan generation: %s, %d guests, ₹%s",
            request.event_type,
            request.guest_count,
            f"{request.total_budget:,.0f}",
        )
        result = plan_event(
            event_type=request.event_type,
            guest_count=request.guest_count,
            total_budget=request.total_budget,
            event_month=request.event_month,
            location=request.location,
        )
        return EventPlanResponse(**result)
    except Exception as e:
        logger.error("Plan generation failed: %s", e)
        raise HTTPException(status_code=500, detail="Plan generation failed")
