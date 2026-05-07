"""Budget prediction API routes."""

import logging

from fastapi import APIRouter, HTTPException

from festiva.agents.orchestrator import predict_budget_splits_impl
from festiva.api.schemas import BudgetPredictionRequest, BudgetAllocation

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["Budget"])


@router.post("/predict-budget", response_model=BudgetAllocation)
async def predict_budget(request: BudgetPredictionRequest):
    """Predict budget allocation for an event."""
    try:
        logger.info("Budget prediction: %s, %d guests", request.event_type, request.guest_count)
        result = predict_budget_splits_impl(
            event_type=request.event_type,
            guest_count=request.guest_count,
            total_budget_inr=request.total_budget,
            event_month=request.event_month,
        )
        return BudgetAllocation(**result)
    except Exception as e:
        logger.error("Budget prediction failed: %s", e)
        raise HTTPException(status_code=500, detail="Budget prediction failed")
