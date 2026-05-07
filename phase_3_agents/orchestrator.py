"""
Multi-Agent Event Planning Orchestrator for Bengaluru Events
Integrates Budget Prediction, Knowledge Base RAG, and LLM-powered planning.
"""

import os
import pickle
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any

# LangChain imports
from langchain.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# LLM imports - Try multiple providers
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    LLM_AVAILABLE = "google"
except ImportError:
    try:
        from langchain_openai import ChatOpenAI
        LLM_AVAILABLE = "openai"
    except ImportError:
        LLM_AVAILABLE = None

print("=" * 80)
print("FESTIVA MOMENTS - MULTI-AGENT EVENT PLANNING ORCHESTRATOR")
print("=" * 80)

# ============================================================================
# GLOBAL STATE
# ============================================================================
BUDGET_ENGINE = None
FAISS_INDEX = None
FEATURE_SCALER = None
EMBEDDINGS_MODEL = None

# ============================================================================
# PHASE 1: LOAD BUDGET ENGINE
# ============================================================================
print("\n[INIT] Loading Budget Prediction Engine...")

budget_path = Path(__file__).parent.parent / "phase_1_data_ml" / "budget_engine.pkl"

try:
    with open(budget_path, 'rb') as f:
        BUDGET_ENGINE = pickle.load(f)
    FEATURE_SCALER = BUDGET_ENGINE['feature_scaler']
    print(f"   ✓ Budget engine loaded from {budget_path}")
    print(f"   ✓ Models: {', '.join([k for k in BUDGET_ENGINE.keys() if k.endswith('_model')])}")
except FileNotFoundError:
    print(f"   ✗ Error: Budget engine not found at {budget_path}")
    exit(1)

# ============================================================================
# PHASE 2: LOAD FAISS INDEX
# ============================================================================
print("\n[INIT] Loading Knowledge Base (FAISS Index)...")

faiss_path = Path(__file__).parent.parent / "phase_2_nlp_rag" / "faiss_index"

try:
    EMBEDDINGS_MODEL = HuggingFaceEmbeddings(
        model_name='all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    FAISS_INDEX = FAISS.load_local(
        str(faiss_path),
        EMBEDDINGS_MODEL,
        allow_dangerous_deserialization=True
    )
    print(f"   ✓ FAISS index loaded from {faiss_path}")
    print(f"   ✓ Index contains {FAISS_INDEX.index.ntotal} vectors")
except Exception as e:
    print(f"   ✗ Error loading FAISS index: {e}")
    exit(1)

# ============================================================================
# TOOL 1: BUDGET PREDICTION FUNCTION (CORE LOGIC)
# ============================================================================
def predict_budget_splits_impl(
    event_type: str,
    guest_count: int,
    total_budget: float,
    event_month: int = 5
) -> str:
    """
    Predicts budget allocation (Catering, Venue, Decor) based on event details.
    
    Args:
        event_type: Type of event ('Wedding', 'Corporate', or 'Birthday')
        guest_count: Number of guests (100-1200)
        total_budget: Total budget in Lakhs (multiply by 100,000 for INR)
        event_month: Month of event (1-12, default 5)
    
    Returns:
        JSON string with predicted spending breakdown
    """
    # Convert total_budget from Lakhs to INR
    total_budget_inr = total_budget * 100000
    
    # One-hot encode event_type to match training format
    # Features: [guest_count, total_budget, event_month, is_weekend, event_type_Birthday, event_type_Corporate, event_type_Wedding]
    event_types = ['Wedding', 'Corporate', 'Birthday']
    event_encoded = [1 if et == event_type else 0 for et in event_types]
    
    # Create feature vector matching training format
    is_weekend = 0  # Default assumption
    features = np.array([[
        guest_count,
        total_budget_inr,
        event_month,
        is_weekend,
        event_encoded[2],  # event_type_Birthday (index 2)
        event_encoded[1],  # event_type_Corporate (index 1)
        event_encoded[0]   # event_type_Wedding (index 0)
    ]])
    
    # Scale features
    X_scaled = FEATURE_SCALER.transform(features)
    
    # Predict
    catering_pred = BUDGET_ENGINE['catering_model'].predict(X_scaled)[0]
    venue_pred = BUDGET_ENGINE['venue_model'].predict(X_scaled)[0]
    decor_pred = BUDGET_ENGINE['decor_model'].predict(X_scaled)[0]
    
    # Normalize to match total budget
    total_pred = catering_pred + venue_pred + decor_pred
    catering_pred = (catering_pred / total_pred) * total_budget_inr
    venue_pred = (venue_pred / total_pred) * total_budget_inr
    decor_pred = (decor_pred / total_pred) * total_budget_inr
    
    result = {
        'event_type': event_type,
        'guest_count': guest_count,
        'total_budget': round(total_budget_inr, 2),
        'catering_spend': round(catering_pred, 2),
        'venue_spend': round(venue_pred, 2),
        'decor_spend': round(decor_pred, 2),
        'catering_pct': round((catering_pred / total_budget_inr) * 100, 1),
        'venue_pct': round((venue_pred / total_budget_inr) * 100, 1),
        'decor_pct': round((decor_pred / total_budget_inr) * 100, 1)
    }
    
    return json.dumps(result, indent=2)

# Wrap for agent framework
@tool
def predict_budget_splits(
    event_type: str,
    guest_count: int,
    total_budget: float,
    event_month: int = 5
) -> str:
    """Predicts budget allocation (Catering, Venue, Decor) based on event details."""
    return predict_budget_splits_impl(event_type, guest_count, total_budget, event_month)

# ============================================================================
# TOOL 2: KNOWLEDGE BASE RETRIEVAL FUNCTION (CORE LOGIC)
# ============================================================================
def search_venue_and_timeline_advice_impl(query: str, k: int = 3) -> str:
    """
    Searches the FAISS index for venue recommendations and planning timeline advice.
    
    Args:
        query: Search query (e.g., 'corporate event in Whitefield', 'wedding planning timeline')
        k: Number of results to retrieve (default 3)
    
    Returns:
        Formatted string with relevant knowledge base chunks
    """
    results = FAISS_INDEX.similarity_search(query, k=k)
    
    advice_list = []
    for i, doc in enumerate(results, 1):
        advice_list.append(f"**Recommendation {i}:**\n{doc.page_content}")
    
    return "\n\n".join(advice_list) if advice_list else "No relevant information found."

# Wrap for agent framework
@tool
def search_venue_and_timeline_advice(query: str, k: int = 3) -> str:
    """Searches the FAISS index for venue recommendations and planning timeline advice."""
    return search_venue_and_timeline_advice_impl(query, k)

# ============================================================================
# PHASE 3: CREATE LLM AGENT
# ============================================================================
print("\n[INIT] Initializing LLM Agent...")

# Check LLM availability
if LLM_AVAILABLE == "google":
    print("   ✓ Using ChatGoogleGenerativeAI")
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            convert_system_message_to_human=True
        )
    except Exception as e:
        print(f"   ⚠ ChatGoogleGenerativeAI initialized but API key may be missing")
        print(f"   → Set GOOGLE_API_KEY environment variable to use it")
        llm = None
elif LLM_AVAILABLE == "openai":
    print("   ✓ Using ChatOpenAI")
    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7
        )
    except Exception as e:
        print(f"   ⚠ ChatOpenAI initialized but API key may be missing")
        print(f"   → Set OPENAI_API_KEY environment variable to use it")
        llm = None
else:
    print("   ⚠ No LLM API available. Install langchain-google-genai or langchain-openai")
    print("   → For Google: pip install langchain-google-genai google-generativeai")
    print("   → For OpenAI: pip install langchain-openai openai")
    llm = None

if llm is None:
    print("   ⚠ Falling back to Demo Mode (no API calls)")
    print("   → Models will be loaded and tools will work, but responses will be templated")

# ============================================================================
# PHASE 4: DEFINE AGENT TOOLS
# ============================================================================
tools = [predict_budget_splits, search_venue_and_timeline_advice]

# ============================================================================
# PHASE 5: CREATE AGENT WITH SYSTEM PROMPT
# ============================================================================
print("\n[INIT] Setting up Planner Agent...")

system_prompt = """You are the Lead Event Strategist at Festiva Moments, a premium event planning firm in Bengaluru.

Your role is to:
1. Analyze event requirements (type, guest count, budget)
2. Use the Budget Tool to predict financial allocations and retrieve budget percentages
3. Use the Knowledge Tool to match vendors with real vendor names from the knowledge base
4. Create a structured vendor recommendation list with costs and ratings

When given an event request, ALWAYS:
- First call predict_budget_splits with the event details to get catering_pct, venue_pct, and decor_pct
- Calculate estimated costs for each category: multiply the budget by each percentage
- Call search_venue_and_timeline_advice with queries for each category (e.g., "catering vendors Bengaluru", "venue options Bengaluru", "decoration services Bengaluru")
- Match real vendor names from the Knowledge Tool to each budget category

Return the final answer as a structured list of vendors in the following format:
For each vendor, include:
- 'Vendor Name': Specific name from knowledge base
- 'Category': One of Venue, Catering, or Decor
- 'Estimated Cost': Calculate from budget percentage (e.g., if total_budget = 2500000 and catering_pct = 50, estimated cost = 1250000)
- 'Rating': A realistic rating between 4.2 and 4.9 (varies by vendor)

Be professional, detail-oriented, and ensure all vendors and costs are based on the knowledge base and budget calculations."""

# Create agent executor if LLM is available
agent_executor = None
if llm is not None:
    try:
        from langgraph.prebuilt import create_react_agent
        agent_executor = create_react_agent(llm, tools, state_modifier=system_prompt)
        print("   ✓ Planner Agent initialized with ReAct framework")
    except Exception as e:
        print(f"   ⚠ Agent framework initialization: {e}")
        print("   → Using demo mode with direct tool calls")
else:
    print("   ⚠ Agent in Demo Mode (LLM not available)")

print("   ✓ Tools: Budget Prediction, Knowledge Retrieval")

# ============================================================================
# PHASE 6: HELPER FUNCTION TO GENERATE MARKDOWN REPORT
# ============================================================================
def generate_markdown_report(user_request: str, agent_response: str, budget_data: Dict) -> str:
    """
    Generates a professional markdown event planning report.
    """
    event_type = budget_data.get('event_type', 'Event')
    guest_count = budget_data.get('guest_count', 0)
    total_budget = budget_data.get('total_budget', 0)
    
    report = f"""# 🎉 Festiva Moments - Event Planning Report

**Prepared for:** Your Upcoming {event_type}  
**Event Date:** {datetime.now().strftime('%B %d, %Y')}  
**Lead Strategist:** Festiva Moments Team

---

## 📋 Event Summary

| Detail | Value |
|--------|-------|
| **Event Type** | {event_type} |
| **Expected Guests** | {guest_count:,} |
| **Total Budget** | ₹{total_budget:,.2f} |

---

## 💰 Financial Breakdown

Based on Bengaluru market rates and your event profile:

| Category | Amount | Percentage | Budget Range |
|----------|--------|-----------|--------------|
| **Catering** | ₹{budget_data.get('catering_spend', 0):,.2f} | {budget_data.get('catering_pct', 0)}% | ₹{int(budget_data.get('catering_spend', 0) * 0.9):,} - ₹{int(budget_data.get('catering_spend', 0) * 1.1):,} |
| **Venue** | ₹{budget_data.get('venue_spend', 0):,.2f} | {budget_data.get('venue_pct', 0)}% | ₹{int(budget_data.get('venue_spend', 0) * 0.9):,} - ₹{int(budget_data.get('venue_spend', 0) * 1.1):,} |
| **Decor** | ₹{budget_data.get('decor_spend', 0):,.2f} | {budget_data.get('decor_pct', 0)}% | ₹{int(budget_data.get('decor_spend', 0) * 0.9):,} - ₹{int(budget_data.get('decor_spend', 0) * 1.1):,} |
| **Total** | ₹{total_budget:,.2f} | 100% | — |

**Key Insights:**
- Per-guest catering cost: ₹{budget_data.get('catering_spend', 0) / guest_count:,.2f}
- Venue budget per guest: ₹{budget_data.get('venue_spend', 0) / guest_count:,.2f}
- Decor investment: {budget_data.get('decor_pct', 0)}% of total (trending 2026 aesthetic)

---

## 📍 Local Recommendations

**Venue & Timeline Insights from Bengaluru Knowledge Base:**

{agent_response}

---

## 📅 6-Week Implementation Timeline

### **Week 1-2: Foundation Phase**
- [ ] Finalize venue booking (essential for popular locations in Hebbal/Whitefield)
- [ ] Vendor onboarding (catering, decor, AV specialists)
- [ ] Budget locking and contingency planning
- [ ] Guest list preliminary finalization
- **Budget Allocation:** ₹{int(budget_data.get('venue_spend', 0) * 0.3):,} (venue advance, vendor deposits)

### **Week 3-4: Design & Menu Phase**
- [ ] Catering menu tasting (₹5K-₹10K for 1-2 tastings)
- [ ] Decor design approval with mood boards
- [ ] Guest list final count (impacts catering quantities)
- [ ] Traffic coordination for shuttle services
- **Budget Allocation:** ₹{int(budget_data.get('catering_spend', 0) * 0.5):,} (menu tastings, decor design)

### **Week 5: Technical Rehearsal**
- [ ] AV equipment checks and soundcheck
- [ ] Final vendor walkthroughs at venue
- [ ] Lighting and projection mapping verification
- [ ] Timeline rehearsal (entry, speeches, entertainment)
- **Budget Allocation:** ₹{int((budget_data.get('venue_spend', 0) + budget_data.get('decor_spend', 0)) * 0.2):,} (final AV/tech payments)

### **Week 6: Event Execution**
- [ ] Event day coordination and setup (6-8 hours pre-event)
- [ ] Guest arrival management
- [ ] Real-time vendor supervision
- [ ] Post-event settlement with vendors
- **Budget Allocation:** ₹{int(budget_data.get('catering_spend', 0) * 0.5):,} (final catering payment, tips, post-event)

---

## ⚠️ Risk Mitigation & Contingencies

**12% Contingency Budget:** ₹{int(total_budget * 0.12):,.2f}

### Potential Scenarios:
1. **Guest Count Fluctuation (±10%):** Keep catering flexible; negotiable final headcount with caterer by Week 5
2. **Traffic Delays:** For North Bengaluru venues (Hebbal), always arrange shuttle services; schedule event starts at 11:00 AM or 7:30 PM
3. **Weather Impact:** Backup indoor spaces essential for outdoor venues; check monsoon (June-Sept) policies
4. **Last-minute Changes:** Allocate contingency for decor adjustments, additional entertainment, or AV upgrades

---

## 📞 Next Steps

1. **Confirm Venue** → Share shortlist of Bengaluru venues (Rustique Winds, Sheraton Whitefield, The King's Meadows, etc.)
2. **Vendor Introductions** → Connect with premium caterers (₹1,200-₹3,500/plate for corporate/weddings)
3. **Design Workshop** → Zero-plastic floral and sustainable decor options (2026 trend)
4. **Timeline Finalization** → Lock Week 1-2 bookings to secure peak-season venues

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Agency:** Festiva Moments - Premium Event Planning, Bengaluru  
**Expertise:** Weddings | Corporate Events | Birthday Celebrations | Product Launches

---
"""
    return report

# ============================================================================
# PHASE 7: MAIN ORCHESTRATION FUNCTION
# ============================================================================
def plan_event(user_request: str) -> str:
    """
    Main orchestration function that processes a user's event request.
    
    Args:
        user_request: Natural language event planning request
    
    Returns:
        Markdown report with complete event plan
    """
    print(f"\n{'='*80}")
    print(f"PROCESSING REQUEST: {user_request}")
    print(f"{'='*80}")
    
    # Extract event details from request (simple parsing)
    budget_data = {
        'event_type': 'Wedding',
        'guest_count': 500,
        'total_budget': 2500000,
        'catering_spend': 1250000,
        'venue_spend': 750000,
        'decor_spend': 500000,
        'catering_pct': 50,
        'venue_pct': 30,
        'decor_pct': 20
    }
    
    # Parse request for numbers and event type
    request_lower = user_request.lower()
    
    # Extract event type
    for et in ['wedding', 'corporate', 'birthday']:
        if et in request_lower:
            budget_data['event_type'] = et.capitalize()
            break
    
    # Extract guest count
    import re
    guest_match = re.search(r'(\d+)\s*(?:guests?|people|attendees)', request_lower)
    if guest_match:
        budget_data['guest_count'] = int(guest_match.group(1))
    
    # Extract budget (look for "X lakhs", "X L", or "₹X")
    budget_match = re.search(r'(\d+)\s*(?:lakh|lakhs|l)', request_lower)
    if budget_match:
        budget_data['total_budget'] = int(budget_match.group(1)) * 100000
    
    # Call budget prediction tool with extracted data
    print("\n[TOOLS] Calling Budget Prediction Tool...")
    budget_json = predict_budget_splits_impl(
        event_type=budget_data['event_type'],
        guest_count=budget_data['guest_count'],
        total_budget=budget_data['total_budget'],
        event_month=5
    )
    
    # Parse the returned JSON
    try:
        budget_result = json.loads(budget_json)
        budget_data.update(budget_result)
        print(f"   ✓ Predicted spend: Catering ₹{budget_data['catering_spend']:,.0f}, Venue ₹{budget_data['venue_spend']:,.0f}, Decor ₹{budget_data['decor_spend']:,.0f}")
    except:
        pass
    
    # Call knowledge retrieval tool
    print("\n[TOOLS] Calling Knowledge Retrieval Tool...")
    knowledge_query = f"{budget_data['event_type']} venue recommendations and planning timeline"
    knowledge_response = search_venue_and_timeline_advice_impl(knowledge_query, k=3)
    print(f"   ✓ Retrieved {len(knowledge_response)} characters of venue/timeline advice")
    
    # Generate markdown report
    print("\n[REPORT] Generating professional event planning report...")
    report = generate_markdown_report(user_request, knowledge_response, budget_data)
    
    return report

# ============================================================================
# PHASE 8: TEST ORCHESTRATOR
# ============================================================================
if __name__ == "__main__":
    # Example request
    test_request = "I'm planning a Wedding in Hebbal with 500 guests and a budget of 25 lakhs. What venues would you recommend and how should I allocate the budget?"
    
    print("\n[TEST] Running orchestrator with sample request...")
    print(f"Request: {test_request}\n")
    
    # Generate plan
    event_plan = plan_event(test_request)
    
    # Save report
    report_path = Path(__file__).parent / "event_plan_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(event_plan)
    
    print(f"\n✓ Event plan saved to: {report_path}")
    print("\n" + "="*80)
    print("REPORT PREVIEW:")
    print("="*80)
    print(event_plan[:1000] + "...\n[Truncated for display]")
