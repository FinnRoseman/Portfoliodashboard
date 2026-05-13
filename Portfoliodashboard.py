import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

st.set_page_config(page_title="Behavioral Portfolio Tracker", layout="wide")

# --- FUNKTION: LIVE-KURSE LADEN (EURO-TICKER) ---
def get_portfolio_value():
    euro_portfolio = {
        "5MVL.DE": 6.58, "XD9U.DE": 9.83, "BRYN.DE": 1.88, 
        "I0C.F": 24.26, "IVSD.F": 14.70, "V3PA.DE": 31.05, "IBC0.DE": 82.12
    }
    total_val = 0
    for ticker, shares in euro_portfolio.items():
        data = yf.Ticker(ticker)
        hist = data.history(period="1mo")
        avg_price = hist['Close'].mean() 
        total_val += (avg_price * shares)
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
st.title("Portfoliodashboard")

# --- DATEN BERECHNUNG ---
goal_value = 500000
current_value = get_portfolio_value() 
progress_pct = min(current_value / goal_value, 1.0)
st.markdown(f"""
    <div class="goal-card">
        <h1 style='color: #1f3b4d; font-size: 2.5rem;'>Rente 2068</h1>
    </div>
    """, unsafe_allow_html=True)
st.write(f"### {int(progress_pct*100)}% Erreicht")
st.progress(progress_pct)    
st.markdown("---")
