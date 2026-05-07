"""Knowledge base search API routes."""

import logging

from fastapi import APIRouter, HTTPException

from festiva.agents.orchestrator import search_venue_and_timeline_advice_impl
from festiva.api.schemas import KnowledgeSearchRequest, KnowledgeSearchResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["Knowledge"])


@router.post("/search-knowledge", response_model=KnowledgeSearchResponse)
async def search_knowledge(request: KnowledgeSearchRequest):
    """Search the knowledge base for venue/timeline advice."""
    try:
        logger.info("Knowledge search: '%s'", request.query)
        results = search_venue_and_timeline_advice_impl(query=request.query, k=request.k)
        return KnowledgeSearchResponse(
            query=request.query,
            results_count=request.k,
            results=results,
        )
    except Exception as e:
        logger.error("Knowledge search failed: %s", e)
        raise HTTPException(status_code=500, detail="Knowledge search failed")
