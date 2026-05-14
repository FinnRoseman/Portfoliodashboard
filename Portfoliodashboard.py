import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Behavioral Portfolio Tracker", layout="centered")

# --- DATA LOGIC ---
@st.cache_data(ttl=3600) # Cache für 1 Stunde, um Ladezeit zu sparen
def get_portfolio_data():
    portfolio_config = {
        "5MVL.DE": 6.58, "XD9U.DE": 9.83, "BRYN.DE": 1.88, 
        "IOC.F": 24.26, "IVSD.F": 14.70, "V3PA.DE": 31.05, "IBC0.DE": 82.12   
    }
    total_val = 0
    names = []
    
    for ticker, shares in portfolio_config.items():
        data = yf.Ticker(ticker)
        # Schnellerer Preisabruf
        price = data.fast_info['last_price']
        total_val += (price * shares)
        # Namen für die Liste unten sammeln
        names.append(f"{data.info.get('longName', ticker)} ({ticker})")
        
    return total_val, names

# --- STYLING (MODERN APP LOOK) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main { background-color: #f0f2f6; }
    
    /* Card Design */
    .metric-card {
        background-color: #454A4F;
        border-radius: 1.2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 1.5rem
    }
    
    .renten-info {
        background: linear-gradient(135deg, #1f3b4d 0%, #345a72 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        margin-top: 1rem;
    }
    
    /* Progress Bar Styling */
    .stProgress > div > div > div > div {
        background-color: #4facfe;
        background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        border-radius: 10px;
        height: 12px;
    }
    
    h1, h2, h3 { color: #1f3b4d; }
    </style>
    """, unsafe_allow_html=True)

# --- APP START ---
goal_value = 500000 
current_value, asset_names = get_portfolio_data()
progress_pct = min(current_value / goal_value, 1.0) 

# Header
st.markdown("<h4 style='text-align: center; color: #6c757d; margin-bottom: 0;'>Finanzielle Freiheit im Alter</h4>", unsafe_allow_html=True)

# Central Goal Card
st.markdown(f"""
    <div class="metric-card">
        <h1 style='margin: 0; color: white; font-size: 3rem;'>Rente 2068</h1>
        <p style='color: #7df66a; font-weight: 700; font-size: 1.2rem; margin-top: 10px;'>
            {int(progress_pct*100)}% GESCHAFFT
        </p>
    </div>
    """, unsafe_allow_html=True)

# Progress Bar
st.progress(progress_pct)

# Behavioral Reframing Card
gesicherte_rente = (current_value * 0.04) / 12

st.markdown(f"""
    <div class="renten-info">
        <span style='font-size: 0.9rem; opacity: 0.8; text-transform: uppercase; letter-spacing: 1px;'>Monatliches Budget in der Rente nach aktuellem Stand</span>
        <h2 style='color: white; margin: 10px 0; font-size: 2.2rem;'>{gesicherte_rente:.2f} €</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Asset List (System 2 - Details)
with st.expander("Portfolio Details anzeigen"):
    st.markdown("### Deine Strategie-Bausteine")
    for name in asset_names:
        st.markdown(f"<div style='padding: 5px 0; border-bottom: 1px solid #f0f2f6; font-size: 0.9rem;'>{name}</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #ced4da; font-size: 0.7rem; margin-top: 50px;'>Stay focused</p>", unsafe_allow_html=True)
