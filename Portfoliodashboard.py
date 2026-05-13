import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

st.set_page_config(page_title="Behavioral Portfolio Tracker", layout="wide")

# --- FUNKTION: LIVE-KURSE LADEN (EURO-TICKER) ---
def get_portfolio_value():
    euro_portfolio = {
        "5MVL.DE": 6.58,  
        "XD9U.DE": 9.83,   
        "BRYN.DE": 1.88,  
        "IOC.F": 24.26,   
        "IVSD.F": 14.70,   
        "V3PA.DE": 31.05,  
        "IBC0.DE": 82.12   
    }
    
    total_val = 0
    try:
        for ticker, shares in euro_portfolio.items():
            data = yf.Ticker(ticker)
            price = data.fast_info['last_price']
            total_val += (price * shares)
    except Exception as e:
        st.error(f"Fehler beim Laden der Live-Kurse: {e}")
        return 72000
        
    return total_val

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
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("MY BEHAVIORAL PORTFOLIO TRACKER")
st.write("Perspektive: Zielerreichung statt Tagesschwankung")

# --- DATEN BERECHNUNG ---
goal_value = 100000 # Dein Ziel aus dem Sheet
current_value = get_portfolio_value()
progress_pct = min(current_value / goal_value, 1.0) # Begrenzt auf max 100%

# --- LAYOUT: ZWEI SPALTEN ---
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
