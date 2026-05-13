import streamlit as st
import pandas as pd

# Page Config für breites Layout
st.set_page_config(page_title="Behavioral Portfolio Tracker", layout="wide")

# --- CUSTOM CSS FÜR DEN "APP-LOOK" ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        border-radius: 10px;
    }
    .goal-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("MY BEHAVIORAL PORTFOLIO TRACKER")
st.write("Perspektive: Zielerreichung statt Tagesschwankung")

# --- DATEN (Hier später deine CSV/API anbinden) ---
current_value = 72000
goal_value = 100000
progress_pct = (current_value / goal_value)

# --- LAYOUT: ZWEI SPALTEN ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("System 1: Behavioral Goal Tracking")
    
    # Die große Goal-Card
    st.markdown(f"""
        <div class="goal-card">
            <h1 style='color: #1f3b4d; font-size: 2.5rem;'>FINANCIAL GOAL: RETIREMENT 2045</h1>
            <p style='font-size: 1.2rem; color: #666;'>Status: Dein Ziel ist auf Kurs. Bleib diszipliniert!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Der abgerundete Fortschrittsbalken
    st.write(f"### {int(progress_pct*100)}% ACHIEVED")
    st.progress(progress_pct)
    
    st.markdown("---")
    
    # Milestone Timeline
    st.write("### Milestone Timeline")
    milestones = {
        "Tier 1 (Emergency Fund)": "DONE ✅",
        "Tier 2 (Core Capital)": "DONE ✅",
        "Tier 3 (Growth)": "IN PROGRESS 🔵",
        "Tier 4 (Financial Freedom)": "FUTURE ⚪"
    }
    for m, status in milestones.items():
        st.write(f"**{m}**: {status}")

with col2:
    st.subheader("Asset Allocation")
    # Einfaches Donut-Chart (Beispieldaten)
    chart_data = pd.DataFrame({
        'Asset': ['Global ETFs', 'Emerging Markets', 'Bonds', 'Commodities'],
        'Value': [45, 20, 25, 10]
    })
    import plotly.express as px
    fig = px.pie(chart_data, values='Value', names='Asset', hole=0.5,
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

    # Actionable Insights (System 2 lite)
    st.info("""
    **Actionable Insights:**
    * Sparrate beibehalten.
    * Kein Rebalancing in diesem Quartal nötig.
    * Fokus auf das Zieljahr 2045 richten.
    """)
