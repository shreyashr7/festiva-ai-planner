"""
Festiva AI Dashboard - Streamlit Application
Interactive Event Planning Interface for Bengaluru Events
"""

import streamlit as st
import requests
import json
import re
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, cast

API_BASE_URL = "http://127.0.0.1:8000"

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Festiva AI Dashboard",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        margin-top: 10px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .header-title {
        color: #667eea;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

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
    
    # Event Type Selection
    event_type = st.selectbox(
        "📋 Event Type",
        options=["Wedding", "Corporate", "Birthday"],
        help="Select the type of event you're planning"
    )
    
    # Guest Count Slider
    guest_count = st.slider(
        "👥 Expected Guests",
        min_value=100,
        max_value=1200,
        value=500,
        step=50,
        help="Number of guests (100-1200)"
    )
    
    # Budget Slider (in lakhs)
    budget_lakhs = st.slider(
        "💰 Total Budget (₹ Lakhs)",
        min_value=5,
        max_value=60,
        value=25,
        step=1,
        help="Budget range: ₹5L to ₹60L"
    )
    total_budget = budget_lakhs * 100000
    
    # Event Month
    event_month = st.selectbox(
        "📅 Event Month",
        options=list(range(1, 13)),
        format_func=lambda x: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][x-1],
        index=4,  # Default to May
        help="Planned month for the event"
    )
    
    # Location
    location = st.text_input(
        "📍 Event Location",
        value="Bengaluru",
        help="City/area where event will be held"
    )
    
    st.divider()
    
    # Generate Plan Button
    generate_button = st.button(
        "🚀 Generate Event Plan",
        use_container_width=True,
        type="primary"
    )
    
    # API Status
    st.markdown("### 🔗 API Status")
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/health", timeout=5)
        if response.status_code == 200:
            st.success("✓ API Connected")
        else:
            st.error(f"✗ API Error: {response.status_code}")
    except Exception as e:
        st.error("✗ API Offline")
        st.caption(f"Error: {str(e)}")
        st.caption("Start server with: python server.py")

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

# Initialize session state for API response
if 'plan_response' not in st.session_state:
    st.session_state.plan_response = None
if 'budget_data' not in st.session_state:
    st.session_state.budget_data = None

# ============================================================================
# HANDLE PLAN GENERATION
# ============================================================================
if generate_button:
    with st.spinner("🔄 Generating your event plan..."):
        try:
            # Prepare request payload
            payload = {
                "event_type": event_type,
                "guest_count": guest_count,
                "total_budget": total_budget,
                "event_month": event_month,
                "location": location
            }
            
            # Call FastAPI endpoint
            response = requests.post(
                f"{API_BASE_URL}/api/v1/generate-plan",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                st.session_state.plan_response = response.json()
                st.session_state.budget_data = response.json().get('budget_allocation', {})
                st.success("✓ Event plan generated successfully!")
            else:
                st.error(f"API Error: {response.status_code}")
                st.write(response.json())
        
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API server")
            st.info("Make sure the FastAPI server is running: `python server.py`")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ============================================================================
# DISPLAY RESULTS IF AVAILABLE
# ============================================================================
if st.session_state.plan_response:
    plan = cast(Dict[str, Any], st.session_state.plan_response)
    budget = cast(Dict[str, Any], st.session_state.budget_data or {})
    
    # =========================================================================
    # SECTION 1: BUDGET OVERVIEW
    # =========================================================================
    st.markdown("## 💰 Financial Summary")
    
    # Create metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Budget",
            f"₹{plan['total_budget']/100000:.1f}L",
            delta=None,
            delta_color="normal"
        )
    
    with col2:
        catering = budget.get('catering_spend', 0)
        st.metric(
            "Catering",
            f"₹{catering/100000:.2f}L",
            f"{budget.get('catering_pct', 0):.1f}%"
        )
    
    with col3:
        venue = budget.get('venue_spend', 0)
        st.metric(
            "Venue",
            f"₹{venue/100000:.2f}L",
            f"{budget.get('venue_pct', 0):.1f}%"
        )
    
    with col4:
        decor = budget.get('decor_spend', 0)
        st.metric(
            "Decor",
            f"₹{decor/100000:.2f}L",
            f"{budget.get('decor_pct', 0):.1f}%"
        )
    
    st.divider()
    
    # =========================================================================
    # SECTION 2: BUDGET ALLOCATION VISUALIZATION
    # =========================================================================
    st.markdown("## 📊 Budget Allocation")
    
    col_chart, col_details = st.columns([2, 1])
    
    with col_chart:
        # Pie chart
        labels = ["Catering", "Venue", "Decor"]
        values = [
            budget.get('catering_spend', 0),
            budget.get('venue_spend', 0),
            budget.get('decor_spend', 0)
        ]
        colors = ["#667eea", "#764ba2", "#f093fb"]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            textinfo="label+percent",
            textposition="inside",
            hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>"
        )])
        
        fig.update_layout(
            height=400,
            showlegend=True,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_details:
        st.markdown("### Per-Guest Costs")
        st.info(
            f"""
            **Catering:** ₹{budget.get('catering_spend', 0) / plan['guest_count']:,.0f}/guest
            
            **Venue:** ₹{budget.get('venue_spend', 0) / plan['guest_count']:,.0f}/guest
            
            **Decor:** ₹{budget.get('decor_spend', 0) / plan['guest_count']:,.0f}/guest
            
            **Total:** ₹{plan['total_budget'] / plan['guest_count']:,.0f}/guest
            """
        )
    
    st.divider()
    
    # =========================================================================
    # SECTION 3: 6-WEEK IMPLEMENTATION TIMELINE
    # =========================================================================
    st.markdown("## 📅 6-Week Implementation Timeline")
    
    # Parse timeline from recommendations
    timeline_data = [
        {
            "Week": "Week 1-2",
            "Phase": "🏗️ Foundation",
            "Tasks": [
                "✓ Finalize venue booking",
                "✓ Vendor onboarding",
                "✓ Budget locking",
                "✓ Guest list preliminary"
            ],
            "Budget": f"₹{budget.get('venue_spend', 0) * 0.3 / 100000:.2f}L"
        },
        {
            "Week": "Week 3-4",
            "Phase": "🎨 Design & Menu",
            "Tasks": [
                "✓ Catering menu tasting",
                "✓ Decor design approval",
                "✓ Guest list final count",
                "✓ Traffic coordination"
            ],
            "Budget": f"₹{budget.get('catering_spend', 0) * 0.5 / 100000:.2f}L"
        },
        {
            "Week": "Week 5",
            "Phase": "🔧 Technical Rehearsal",
            "Tasks": [
                "✓ AV equipment checks",
                "✓ Vendor walkthroughs",
                "✓ Lighting verification",
                "✓ Timeline rehearsal"
            ],
            "Budget": f"₹{(budget.get('venue_spend', 0) + budget.get('decor_spend', 0)) * 0.2 / 100000:.2f}L"
        },
        {
            "Week": "Week 6",
            "Phase": "🎊 Execution",
            "Tasks": [
                "✓ Event day coordination",
                "✓ Guest arrival management",
                "✓ Vendor supervision",
                "✓ Post-event settlement"
            ],
            "Budget": f"₹{budget.get('catering_spend', 0) * 0.5 / 100000:.2f}L"
        }
    ]
    
    for week_plan in timeline_data:
        with st.expander(f"{week_plan['Week']} — {week_plan['Phase']}", expanded=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("**Tasks:**")
                for task in week_plan['Tasks']:
                    st.markdown(f"- {task}")
            with col2:
                st.markdown("**Budget Allocation**")
                st.info(week_plan['Budget'])
    
    st.divider()
    
    # =========================================================================
    # SECTION 4: VENDOR RECOMMENDATIONS
    # =========================================================================
    st.markdown("## 🏢 Vendor Recommendations")
    
    recommendations = plan.get('recommendations', '')
    
    # Display vendors from recommendations
    if recommendations:
        # Parse vendor information from recommendations
        st.markdown("### Recommended Vendors & Pricing")
        
        # Split recommendations by vendor (heuristic: look for numbered items or vendor patterns)
        vendor_lines = recommendations.split('\n')
        current_vendor = {}
        vendors_list = []
        
        for line in vendor_lines:
            line = line.strip()
            if not line:
                continue
            # Try to extract vendor info from the line
            if any(marker in line for marker in ['Vendor Name:', 'Category:', 'Estimated Cost:', 'Rating:']):
                if 'Vendor Name:' in line:
                    if current_vendor:
                        vendors_list.append(current_vendor)
                    current_vendor = {'name': line.replace('Vendor Name:', '').strip()}
                elif 'Category:' in line:
                    current_vendor['category'] = line.replace('Category:', '').strip()
                elif 'Estimated Cost:' in line:
                    current_vendor['cost'] = line.replace('Estimated Cost:', '').strip()
                elif 'Rating:' in line:
                    current_vendor['rating'] = line.replace('Rating:', '').strip()
        
        if current_vendor:
            vendors_list.append(current_vendor)
        
        # Display vendors in containers
        if vendors_list:
            for vendor in vendors_list:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"### {vendor.get('name', 'Vendor')}")
                        st.markdown(f"**Category:** {vendor.get('category', 'N/A')}")
                    
                    with col2:
                        rating_val = vendor.get('rating', 'N/A')
                        st.markdown(f"#### ⭐ {rating_val}")
                    
                    with col3:
                        cost_val = vendor.get('cost', 'N/A')
                        st.metric("Estimated Cost", cost_val)
        else:
            # Fallback: display as formatted text if parsing didn't work
            st.info(recommendations)
    else:
        st.info("No vendor recommendations available yet. Generate a plan to see recommendations.")
    
    st.divider()
    
    # =========================================================================
    # SECTION 5: RISK MITIGATION
    # =========================================================================
    st.markdown("## ⚠️ Risk Mitigation & Contingencies")
    
    contingency = int(plan['total_budget'] * 0.12)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Contingency Buffer (12%)", f"₹{contingency/100000:.2f}L")
    with col2:
        st.metric("Total Budget with Contingency", f"₹{(plan['total_budget'] + contingency)/100000:.2f}L")
    
    with st.expander("📋 Risk Scenarios & Mitigation", expanded=False):
        st.markdown(f"""
        ### Guest Count Fluctuation (±10%)
        - Keep catering flexible
        - Negotiate final headcount with caterer by Week 5
        - Budget buffer: ₹{int(plan['total_budget'] * 0.10)/100000:.2f}L
        
        ### Traffic Delays
        - For North Bengaluru venues (Hebbal), arrange shuttle services
        - Schedule event starts at 11:00 AM or 7:30 PM
        - Build in 30-min buffer for guest arrivals
        
        ### Weather Impact
        - Backup indoor spaces essential for outdoor venues
        - Check monsoon (June-Sept) policies
        - Weather contingency: ₹{int(contingency * 0.3)/100000:.2f}L
        
        ### Last-minute Changes
        - Allocate contingency for decor adjustments
        - Reserve budget for additional entertainment
        - AV upgrade buffer available
        """)
    
    st.divider()
    
    # =========================================================================
    # SECTION 6: NEXT STEPS
    # =========================================================================
    st.markdown("## 📞 Next Steps")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("""
        ### 1️⃣ Venue Confirmation
        Share shortlist of Bengaluru venues
        """)
    with col2:
        st.info("""
        ### 2️⃣ Vendor Connect
        Premium caterers (₹1,200-₹3,500/plate)
        """)
    with col3:
        st.info("""
        ### 3️⃣ Design Workshop
        Sustainable decor 2026 trends
        """)
    with col4:
        st.info("""
        ### 4️⃣ Timeline Lock
        Week 1-2 bookings finalized
        """)
    
    st.divider()
    
    # =========================================================================
    # EXPORT REPORT
    # =========================================================================
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📥 Export Report")
        if st.button("📄 Download as Markdown", use_container_width=True):
            st.download_button(
                label="Download Report",
                data=plan.get('recommendations', 'No report available'),
                file_name=f"event_plan_{event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
    
    with col2:
        st.markdown("### 📊 Export Data")
        if st.button("📋 Download as JSON", use_container_width=True):
            export_data = {
                "event_type": plan['event_type'],
                "guest_count": plan['guest_count'],
                "total_budget": plan['total_budget'],
                "budget_allocation": plan['budget_allocation'],
                "generated_at": plan['generated_at']
            }
            st.download_button(
                label="Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"event_plan_{event_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    st.divider()
    
    # =========================================================================
    # FOOTER
    # =========================================================================
    st.markdown("""
    ---
    **Festiva AI Dashboard** | Premium Event Planning for Bengaluru
    
    *Powered by Machine Learning | Built with ❤️ for Event Planners*
    """)

else:
    # =========================================================================
    # WELCOME STATE - BEFORE FIRST PLAN GENERATION
    # =========================================================================
    st.markdown("""
    ## 🎯 Welcome to Festiva AI Dashboard
    
    Your AI-powered event planning assistant for Bengaluru weddings, corporate events, and celebrations.
    
    ### How It Works:
    
    1. **Configure** your event in the sidebar (Event Type, Guests, Budget, Month)
    2. **Generate** a comprehensive event plan with AI-powered insights
    3. **Review** budget allocations, timelines, and venue recommendations
    4. **Export** your plan as Markdown or JSON for sharing
    
    ### Features:
    
    ✨ **Budget Intelligence** - ML-powered spending predictions based on Bengaluru market rates
    
    📊 **Visual Analytics** - Interactive pie charts and metrics for budget allocation
    
    📅 **6-Week Timeline** - Week-by-week implementation plan with milestone tracking
    
    📍 **Venue Intelligence** - AI-curated recommendations from knowledge base
    
    ⚠️ **Risk Management** - Contingency planning and scenario analysis
    
    💾 **Export Ready** - Download reports in Markdown or JSON format
    
    ---
    
    ### 📌 Event Budget Ranges
    
    | Event Type | Min Budget | Typical | Max Budget |
    |-----------|-----------|---------|----------|
    | 🎂 Birthday | ₹5L | ₹15L | ₹25L |
    | 💼 Corporate | ₹10L | ₹30L | ₹60L |
    | 💒 Wedding | ₹15L | ₹35L | ₹60L |
    
    ---
    
    **Start by selecting your event details in the sidebar and click "Generate Event Plan"**
    """)
    
    st.info("💡 **Tip:** Use the sidebar to configure your event details and generate a personalized plan!")
