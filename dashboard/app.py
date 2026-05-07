"""
Festiva AI Dashboard - Streamlit Application
Interactive Event Planning Interface for Bengaluru Events
"""

import json
from datetime import datetime
from typing import Any, Dict, cast

import plotly.graph_objects as go
import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Festiva AI Dashboard",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================================
# HEADER
# ============================================================================
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 🎉 Festiva AI Dashboard")
    st.markdown("**Premium Event Planning for Bengaluru**")
with col2:
    st.info(f"📅 {datetime.now().strftime('%B %d, %Y')}")

st.divider()

# ============================================================================
# SIDEBAR - INPUT CONTROLS
# ============================================================================
with st.sidebar:
    st.header("⚙️ Event Configuration")

    event_type = st.selectbox(
        "📋 Event Type",
        options=["Wedding", "Corporate", "Birthday"],
    )

    guest_count = st.slider(
        "👥 Expected Guests",
        min_value=100,
        max_value=1200,
        value=500,
        step=50,
    )

    budget_lakhs = st.slider(
        "💰 Total Budget (₹ Lakhs)",
        min_value=5,
        max_value=60,
        value=25,
        step=1,
    )
    total_budget = budget_lakhs * 100000

    event_month = st.selectbox(
        "📅 Event Month",
        options=list(range(1, 13)),
        format_func=lambda x: [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        ][x - 1],
        index=4,
    )

    location = st.text_input("📍 Event Location", value="Bengaluru")

    st.divider()

    generate_button = st.button(
        "🚀 Generate Event Plan",
        use_container_width=True,
        type="primary",
    )

    st.markdown("### 🔗 API Status")
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/health", timeout=5)
        if response.status_code == 200:
            st.success("✓ API Connected")
        else:
            st.error(f"✗ API Error: {response.status_code}")
    except Exception:
        st.error("✗ API Offline")
        st.caption("Start server with: festiva-server")

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================
if "plan_response" not in st.session_state:
    st.session_state.plan_response = None
if "budget_data" not in st.session_state:
    st.session_state.budget_data = None

# ============================================================================
# HANDLE PLAN GENERATION
# ============================================================================
if generate_button:
    with st.spinner("🔄 Generating your event plan..."):
        try:
            payload = {
                "event_type": event_type,
                "guest_count": guest_count,
                "total_budget": total_budget,
                "event_month": event_month,
                "location": location,
            }
            response = requests.post(
                f"{API_BASE_URL}/api/v1/generate-plan",
                json=payload,
                timeout=30,
            )
            if response.status_code == 200:
                st.session_state.plan_response = response.json()
                st.session_state.budget_data = response.json().get("budget_allocation", {})
                st.success("✓ Event plan generated successfully!")
            else:
                st.error(f"API Error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API server")
            st.info("Make sure the FastAPI server is running: `festiva-server`")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ============================================================================
# DISPLAY RESULTS
# ============================================================================
if st.session_state.plan_response:
    plan = cast(Dict[str, Any], st.session_state.plan_response)
    budget = cast(Dict[str, Any], st.session_state.budget_data or {})

    st.markdown("## 💰 Financial Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Budget", f"₹{plan['total_budget']/100000:.1f}L")
    with col2:
        st.metric("Catering", f"₹{budget.get('catering_spend', 0)/100000:.2f}L",
                  f"{budget.get('catering_pct', 0):.1f}%")
    with col3:
        st.metric("Venue", f"₹{budget.get('venue_spend', 0)/100000:.2f}L",
                  f"{budget.get('venue_pct', 0):.1f}%")
    with col4:
        st.metric("Decor", f"₹{budget.get('decor_spend', 0)/100000:.2f}L",
                  f"{budget.get('decor_pct', 0):.1f}%")

    st.divider()

    # Budget chart
    st.markdown("## 📊 Budget Allocation")
    col_chart, col_details = st.columns([2, 1])
    with col_chart:
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Catering", "Venue", "Decor"],
                    values=[
                        budget.get("catering_spend", 0),
                        budget.get("venue_spend", 0),
                        budget.get("decor_spend", 0),
                    ],
                    marker=dict(colors=["#667eea", "#764ba2", "#f093fb"]),
                    textinfo="label+percent",
                    textposition="inside",
                )
            ]
        )
        fig.update_layout(height=400, showlegend=True, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_details:
        st.markdown("### Per-Guest Costs")
        gc = plan["guest_count"]
        st.info(
            f"**Catering:** ₹{budget.get('catering_spend', 0)/gc:,.0f}/guest\n\n"
            f"**Venue:** ₹{budget.get('venue_spend', 0)/gc:,.0f}/guest\n\n"
            f"**Decor:** ₹{budget.get('decor_spend', 0)/gc:,.0f}/guest\n\n"
            f"**Total:** ₹{plan['total_budget']/gc:,.0f}/guest"
        )

    st.divider()

    # Timeline
    st.markdown("## 📅 6-Week Implementation Timeline")
    timeline_data = [
        ("Week 1-2", "🏗️ Foundation", ["Finalize venue", "Vendor onboarding", "Budget locking"]),
        ("Week 3-4", "🎨 Design & Menu", ["Catering tasting", "Decor approval", "Guest list final"]),
        ("Week 5", "🔧 Rehearsal", ["AV checks", "Vendor walkthroughs", "Timeline rehearsal"]),
        ("Week 6", "🎊 Execution", ["Event coordination", "Guest management", "Post-event settlement"]),
    ]
    for week, phase, tasks in timeline_data:
        with st.expander(f"{week} — {phase}", expanded=True):
            for task in tasks:
                st.markdown(f"- ✓ {task}")

    st.divider()

    # Recommendations
    st.markdown("## 🏢 Vendor Recommendations")
    recommendations = plan.get("recommendations", "")
    if recommendations:
        st.markdown(recommendations)
    else:
        st.info("No vendor recommendations available yet.")

    st.divider()

    # Export
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📄 Download Markdown Report",
            data=plan.get("recommendations", "No report available"),
            file_name=f"event_plan_{event_type}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col2:
        export_data = {
            "event_type": plan["event_type"],
            "guest_count": plan["guest_count"],
            "total_budget": plan["total_budget"],
            "budget_allocation": plan["budget_allocation"],
            "generated_at": plan["generated_at"],
        }
        st.download_button(
            "📋 Download JSON",
            data=json.dumps(export_data, indent=2),
            file_name=f"event_plan_{event_type}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True,
        )

else:
    st.markdown(
        """
    ## 🎯 Welcome to Festiva AI Dashboard

    Your AI-powered event planning assistant for Bengaluru.

    ### How It Works:
    1. **Configure** your event in the sidebar
    2. **Generate** a comprehensive event plan
    3. **Review** budget allocations, timelines, and recommendations
    4. **Export** your plan as Markdown or JSON

    ---
    **Start by selecting your event details in the sidebar and click "Generate Event Plan"**
    """
    )
