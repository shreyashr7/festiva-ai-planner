"""
Multi-Agent Event Planning Orchestrator
Integrates Budget Prediction, Knowledge Base RAG, and LLM-powered planning.
"""

import json
import logging
import pickle
from datetime import datetime
from typing import Any

import numpy as np
from langchain.tools import tool

from festiva.config import MODELS_DIR, FAISS_INDEX_DIR, EMBEDDING_MODEL

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Lazy-loaded globals
# ---------------------------------------------------------------------------
_budget_engine: dict | None = None
_faiss_index = None

# ---------------------------------------------------------------------------
# Bengaluru vendor database (structured data for demo mode)
# ---------------------------------------------------------------------------
VENUE_DB: dict[str, list[dict]] = {
    "Wedding": [
        {
            "name": "The King's Meadows",
            "location": "Hebbal, North Bengaluru",
            "rating": 4.8,
            "description": "Premium lush green outdoor venue with Balinese architecture and vast lawns",
        },
        {
            "name": "Gowri Kalyana Mantapa",
            "location": "Basavanagudi, South Bengaluru",
            "rating": 4.6,
            "description": "Traditional heritage hall with classic South Indian architecture",
        },
        {
            "name": "Manpho Convention Centre",
            "location": "Manyata Tech Park, North Bengaluru",
            "rating": 4.5,
            "description": "Massive multi-hall facility for large-scale traditional weddings",
        },
    ],
    "Corporate": [
        {
            "name": "Rustique Winds",
            "location": "Whitefield, East Bengaluru",
            "rating": 4.7,
            "description": "Corporate event space blending rustic aesthetic with high-tech AV",
        },
        {
            "name": "Sheraton Grand Whitefield",
            "location": "Whitefield, East Bengaluru",
            "rating": 4.8,
            "description": "Luxury hotel with ballroom spaces for high-end corporate galas",
        },
        {
            "name": "Royal Orchid",
            "location": "Old Airport Road, Central Bengaluru",
            "rating": 4.5,
            "description": "Landmark venue for corporate award ceremonies and rooftop events",
        },
    ],
    "Birthday": [
        {
            "name": "The Black Rabbit",
            "location": "Indiranagar, Central Bengaluru",
            "rating": 4.4,
            "description": "Trendy space for social mixers and creative celebrations",
        },
        {
            "name": "The Zuri",
            "location": "Whitefield, East Bengaluru",
            "rating": 4.6,
            "description": "Known for poolside events and sophisticated indoor halls",
        },
        {
            "name": "Vara The Pavilion",
            "location": "Yelahanka, North Bengaluru",
            "rating": 4.5,
            "description": "Serene upscale venue for intimate celebrations and retreats",
        },
    ],
}

CATERER_DB: dict[str, list[dict]] = {
    "Wedding": [
        {
            "name": "Nandi Grand Caterers",
            "location": "Jayanagar, Bengaluru",
            "rating": 4.7,
            "description": "Specializes in multi-cuisine South Indian wedding feasts",
        },
        {
            "name": "Purple Basil Events Catering",
            "location": "Koramangala, Bengaluru",
            "rating": 4.6,
            "description": "Modern fusion catering with live counters and presentation",
        },
    ],
    "Corporate": [
        {
            "name": "Swadisht Kitchen",
            "location": "Whitefield, Bengaluru",
            "rating": 4.5,
            "description": "Multi-cuisine corporate catering with dietary accommodations",
        },
        {
            "name": "The Bangalore Catering Co.",
            "location": "Indiranagar, Bengaluru",
            "rating": 4.4,
            "description": "Premium business lunch and conference catering specialists",
        },
    ],
    "Birthday": [
        {
            "name": "Crave Kitchen",
            "location": "HSR Layout, Bengaluru",
            "rating": 4.5,
            "description": "Creative party catering with custom themed menus",
        },
        {
            "name": "Purple Basil Events Catering",
            "location": "Koramangala, Bengaluru",
            "rating": 4.6,
            "description": "Trendy small-plate catering and dessert bars for celebrations",
        },
    ],
}

DECOR_DB: dict[str, list[dict]] = {
    "Wedding": [
        {
            "name": "Bloom & Glow Events",
            "location": "JP Nagar, Bengaluru",
            "rating": 4.7,
            "description": "Sustainable floral arrangements and mandap design specialists",
        },
    ],
    "Corporate": [
        {
            "name": "Pristine Decor Studio",
            "location": "MG Road, Bengaluru",
            "rating": 4.6,
            "description": "Minimalist corporate staging with immersive LED mapping",
        },
    ],
    "Birthday": [
        {
            "name": "Ethereal Floral Designs",
            "location": "Indiranagar, Bengaluru",
            "rating": 4.5,
            "description": "Whimsical party decor with balloon art and themed setups",
        },
    ],
}


def _load_budget_engine() -> dict:
    global _budget_engine
    if _budget_engine is None:
        path = MODELS_DIR / "budget_engine.pkl"
        with open(path, "rb") as f:
            _budget_engine = pickle.load(f)
    return _budget_engine


def _load_faiss_index():
    global _faiss_index
    if _faiss_index is None:
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS

        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        _faiss_index = FAISS.load_local(
            str(FAISS_INDEX_DIR), embeddings, allow_dangerous_deserialization=True
        )
    return _faiss_index


# ---------------------------------------------------------------------------
# Budget prediction
# ---------------------------------------------------------------------------
def predict_budget_splits_impl(
    event_type: str,
    guest_count: int,
    total_budget_inr: float,
    event_month: int = 5,
) -> dict[str, Any]:
    """
    Predict budget allocation in INR.

    Args:
        event_type: 'Wedding', 'Corporate', or 'Birthday'
        guest_count: Number of guests (100-1200)
        total_budget_inr: Total budget in INR
        event_month: Month of event (1-12)

    Returns:
        Dict with predicted spending breakdown
    """
    engine = _load_budget_engine()
    scaler = engine["feature_scaler"]

    event_types = ["Wedding", "Corporate", "Birthday"]
    event_encoded = [1 if et == event_type else 0 for et in event_types]

    features = np.array(
        [[
            guest_count,
            total_budget_inr,
            event_month,
            0,  # is_weekend default
            event_encoded[2],  # Birthday
            event_encoded[1],  # Corporate
            event_encoded[0],  # Wedding
        ]]
    )

    X_scaled = scaler.transform(features)

    catering_pred = float(engine["catering_model"].predict(X_scaled)[0])
    venue_pred = float(engine["venue_model"].predict(X_scaled)[0])
    decor_pred = float(engine["decor_model"].predict(X_scaled)[0])

    # Normalize so allocations sum to total budget
    total_pred = catering_pred + venue_pred + decor_pred
    if total_pred > 0:
        catering_pred = (catering_pred / total_pred) * total_budget_inr
        venue_pred = (venue_pred / total_pred) * total_budget_inr
        decor_pred = (decor_pred / total_pred) * total_budget_inr

    return {
        "event_type": event_type,
        "guest_count": guest_count,
        "total_budget": round(total_budget_inr, 2),
        "catering_spend": round(catering_pred, 2),
        "venue_spend": round(venue_pred, 2),
        "decor_spend": round(decor_pred, 2),
        "catering_pct": round((catering_pred / total_budget_inr) * 100, 1),
        "venue_pct": round((venue_pred / total_budget_inr) * 100, 1),
        "decor_pct": round((decor_pred / total_budget_inr) * 100, 1),
    }


@tool
def predict_budget_splits(
    event_type: str,
    guest_count: int,
    total_budget: float,
    event_month: int = 5,
) -> str:
    """Predicts budget allocation (Catering, Venue, Decor) based on event details."""
    result = predict_budget_splits_impl(event_type, guest_count, total_budget, event_month)
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Knowledge retrieval
# ---------------------------------------------------------------------------
def search_venue_and_timeline_advice_impl(query: str, k: int = 3) -> str:
    """Search FAISS index for venue recommendations and planning advice."""
    index = _load_faiss_index()
    results = index.similarity_search(query, k=k)

    parts = []
    for i, doc in enumerate(results, 1):
        parts.append(f"**Recommendation {i}:**\n{doc.page_content}")

    return "\n\n".join(parts) if parts else "No relevant information found."


@tool
def search_venue_and_timeline_advice(query: str, k: int = 3) -> str:
    """Searches FAISS index for venue recommendations and planning timeline advice."""
    return search_venue_and_timeline_advice_impl(query, k)


# ---------------------------------------------------------------------------
# LLM + Agent
# ---------------------------------------------------------------------------
def _get_llm():
    from festiva.config import GOOGLE_API_KEY, OPENAI_API_KEY

    if GOOGLE_API_KEY and not GOOGLE_API_KEY.startswith("your-"):
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            convert_system_message_to_human=True,
        )
    if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("your-"):
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    return None


SYSTEM_PROMPT = (
    "You are the Lead Event Strategist at Festiva Moments, a premium event "
    "planning firm in Bengaluru. Analyze requirements, predict budget allocations, "
    "match vendors, and create structured recommendations with costs and ratings."
)


def _create_agent():
    llm = _get_llm()
    if llm is None:
        return None
    tools = [predict_budget_splits, search_venue_and_timeline_advice]
    try:
        from langgraph.prebuilt import create_react_agent

        return create_react_agent(llm, tools, state_modifier=SYSTEM_PROMPT)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Structured plan builders
# ---------------------------------------------------------------------------
def _build_timeline(budget: dict) -> list[dict]:
    """Build a structured 6-week timeline."""
    venue = budget["venue_spend"]
    catering = budget["catering_spend"]
    decor = budget["decor_spend"]

    return [
        {
            "week": "Week 1–2",
            "phase": "Foundation & Booking",
            "icon": "building",
            "tasks": [
                "Finalize and book venue",
                "Onboard catering vendor",
                "Lock in total budget allocation",
                "Prepare preliminary guest list",
            ],
            "budget_note": f"₹{venue * 0.5 / 100000:.1f}L venue advance",
        },
        {
            "week": "Week 3–4",
            "phase": "Design & Planning",
            "icon": "palette",
            "tasks": [
                "Attend menu tasting session",
                "Approve decor design and theme",
                "Finalize guest list and send invitations",
                "Coordinate logistics and transport",
            ],
            "budget_note": f"₹{catering * 0.5 / 100000:.1f}L catering advance",
        },
        {
            "week": "Week 5",
            "phase": "Technical Rehearsal",
            "icon": "settings",
            "tasks": [
                "AV equipment setup and checks",
                "Final vendor walkthroughs",
                "Lighting and stage verification",
                "Run full timeline rehearsal",
            ],
            "budget_note": f"₹{decor * 0.6 / 100000:.1f}L decor setup",
        },
        {
            "week": "Week 6",
            "phase": "Event Execution",
            "icon": "party-popper",
            "tasks": [
                "Day-of event coordination",
                "Guest arrival and registration",
                "Vendor supervision and timing",
                "Post-event settlement and review",
            ],
            "budget_note": f"₹{(catering * 0.5 + venue * 0.5) / 100000:.1f}L final payments",
        },
    ]


def _build_vendors(event_type: str, budget: dict) -> list[dict]:
    """Build structured vendor recommendations."""
    vendors = []

    venues = VENUE_DB.get(event_type, VENUE_DB["Wedding"])
    for v in venues:
        vendors.append({
            "name": v["name"],
            "category": "Venue",
            "estimated_cost": round(budget["venue_spend"] / len(venues)),
            "rating": v["rating"],
            "description": v["description"],
            "location": v["location"],
        })

    caterers = CATERER_DB.get(event_type, CATERER_DB["Wedding"])
    for c in caterers:
        vendors.append({
            "name": c["name"],
            "category": "Catering",
            "estimated_cost": round(budget["catering_spend"] / len(caterers)),
            "rating": c["rating"],
            "description": c["description"],
            "location": c["location"],
        })

    decorators = DECOR_DB.get(event_type, DECOR_DB["Wedding"])
    for d in decorators:
        vendors.append({
            "name": d["name"],
            "category": "Decor",
            "estimated_cost": round(budget["decor_spend"] / len(decorators)),
            "rating": d["rating"],
            "description": d["description"],
            "location": d["location"],
        })

    return vendors


def _build_risks(total_budget: float, guest_count: int) -> list[dict]:
    """Build structured risk assessment."""
    contingency = total_budget * 0.12
    return [
        {
            "risk": "Guest Count Fluctuation (±10%)",
            "impact": "high",
            "mitigation": (
                "Keep catering flexible with final headcount confirmation by Week 5. "
                "Negotiate per-plate pricing with tiered guest ranges."
            ),
            "buffer": round(total_budget * 0.04),
        },
        {
            "risk": "Bengaluru Traffic Delays",
            "impact": "medium",
            "mitigation": (
                "Schedule starts at 11:00 AM or 7:30 PM to avoid Silk Board / "
                "Marathahalli rush. Arrange shuttle services for North Bengaluru venues."
            ),
            "buffer": round(total_budget * 0.02),
        },
        {
            "risk": "Monsoon Weather Impact",
            "impact": "medium",
            "mitigation": (
                "Ensure backup indoor spaces for outdoor venues. Check monsoon "
                "(June–September) policies with venue. Keep waterproof staging ready."
            ),
            "buffer": round(contingency * 0.3),
        },
        {
            "risk": "Last-Minute Vendor Changes",
            "impact": "low",
            "mitigation": (
                "Maintain backup vendor contacts for each category. Include "
                "cancellation clauses in all vendor contracts."
            ),
            "buffer": round(contingency * 0.2),
        },
    ]


# ---------------------------------------------------------------------------
# Main plan generation
# ---------------------------------------------------------------------------
def plan_event(
    event_type: str,
    guest_count: int,
    total_budget: float,
    event_month: int = 5,
    location: str = "Bengaluru",
) -> dict[str, Any]:
    """
    Generate a complete event plan with structured data.

    Args:
        event_type: Type of event
        guest_count: Number of guests
        total_budget: Budget in INR
        event_month: Month of event
        location: Event location

    Returns:
        Dict with budget, timeline, vendors, risks, and recommendations
    """
    budget = predict_budget_splits_impl(event_type, guest_count, total_budget, event_month)
    timeline = _build_timeline(budget)
    vendors = _build_vendors(event_type, budget)
    risks = _build_risks(total_budget, guest_count)

    # Knowledge retrieval for recommendations text
    try:
        venue_advice = search_venue_and_timeline_advice_impl(
            f"{event_type} venue {location}", k=3
        )
    except Exception:
        venue_advice = ""

    # Try agent-based enrichment
    recommendations = ""
    agent = _create_agent()
    if agent:
        try:
            query = (
                f"Plan a {event_type} in {location} for {guest_count} guests "
                f"with budget ₹{total_budget:,.0f} in month {event_month}"
            )
            result = agent.invoke({"messages": [("user", query)]})
            recommendations = result["messages"][-1].content
        except Exception as exc:
            logger.warning("Agent planning failed, using template: %s", exc)

    if not recommendations:
        recommendations = _generate_template_plan(
            event_type, guest_count, total_budget, budget, venue_advice
        )

    return {
        "status": "success",
        "request_id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "event_type": event_type,
        "guest_count": guest_count,
        "total_budget": total_budget,
        "location": location,
        "event_month": event_month,
        "budget_allocation": budget,
        "per_guest_cost": round(total_budget / guest_count, 2),
        "contingency_budget": round(total_budget * 0.12, 2),
        "timeline": timeline,
        "vendors": vendors,
        "risks": risks,
        "recommendations": recommendations,
        "generated_at": datetime.now().isoformat(),
    }


def _generate_template_plan(
    event_type: str,
    guest_count: int,
    total_budget: float,
    budget: dict,
    venue_advice: str,
) -> str:
    return (
        f"## Event Plan: {event_type}\n\n"
        f"**Guests:** {guest_count} | **Budget:** ₹{total_budget:,.0f}\n\n"
        f"### Budget Allocation\n"
        f"- Catering: ₹{budget['catering_spend']:,.0f} ({budget['catering_pct']}%)\n"
        f"- Venue: ₹{budget['venue_spend']:,.0f} ({budget['venue_pct']}%)\n"
        f"- Decor: ₹{budget['decor_spend']:,.0f} ({budget['decor_pct']}%)\n\n"
        f"### Venue Recommendations\n{venue_advice}\n\n"
        f"### 6-Week Timeline\n"
        f"- Week 6: Finalize venue and catering\n"
        f"- Week 5: Confirm decor and entertainment\n"
        f"- Week 4: Send invitations, confirm guest list\n"
        f"- Week 3: Final vendor meetings\n"
        f"- Week 2: Rehearsal and logistics check\n"
        f"- Week 1: Final confirmations and event execution\n"
    )
