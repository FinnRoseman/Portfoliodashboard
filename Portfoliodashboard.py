import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

st.set_page_config(page_title="Behavioral Portfolio Tracker", layout="wide")

def get_portfolio_value():
    euro_portfolio = {
        "5MVL.DE": 6.58, "XD9U.DE": 9.83, "BRYN.DE": 1.88, "IOC.F": 24.26, "IVSD.F": 14.70, "V3PA.DE": 31.05, "IBC0.DE": 82.12   
    }
    total_val = 0
    try:
        for ticker, shares in euro_portfolio.items():
            data = yf.Ticker(ticker)
            price = data.fast_info['last_price']
            total_val += (price * shares)
    except Exception as e:
        st.error(f"Fehler beim Laden der Live-Kurse: {e}")
        return 0      
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
st.title("Behavioral Finance Dashboard")

# --- DATEN BERECHNUNG ---
goal_value = 500000 
current_value = get_portfolio_value()
progress_pct = min(current_value / goal_value, 1.0) 
st.markdown(f"""
    <div class="goal-card">
        <h1 style='color: #1f3b4d; font-size: 2.5rem;'>Rente 2068</h1>
    </div>
    """, unsafe_allow_html=True)
    
# Der abgerundete Fortschrittsbalken
st.write(f"### {int(progress_pct*100)}% Geschafft")
st.progress(progress_pct)  
st.markdown("---")

for ticker in euro_portfolio.keys():
    try:
        asset = yf.Ticker(ticker)
        full_name = asset.info.get('longName', ticker) 
        st.write(f"* **{full_name}** ({ticker})")
    except:
        st.write(f"* **Unbekanntes Asset** ({ticker})")
