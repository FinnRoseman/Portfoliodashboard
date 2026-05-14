import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# --- KONFIGURATION & DATA ---
st.set_page_config(page_title="Behavioral Portfolio Tracker", layout="wide")
@st.cache_data(ttl=3600)
def get_portfolio_data():
    portfolio_config = {
        "5MVL.DE": 6.58,
        "XD9U.DE": 9.83,
        "BRYN.DE": 1.88, 
        "IOC.F": 24.26,
        "IVSD.F": 14.70,
        "V3PA.DE": 31.05,
        "IBC0.DE": 82.12   
    }
    total_val = 0
    chart_list = []    
    for ticker, shares in portfolio_config.items():
        try:
            asset = yf.Ticker(ticker)
            price = asset.fast_info['last_price']
            full_name = asset.info.get('longName', ticker)
            wert = price * shares
            total_val += wert
            chart_list.append({"Asset": full_name, "Wert": round(wert, 2)})
        except:
            continue      
    return total_val, pd.DataFrame(chart_list)

# --- CUSTOM CSS FÜR MODERNES DESIGN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    } 
    .main { background-color: #0E1117; } /* Dunkler Hintergrund für App-Look */
    /* Karte oben links (Rente 2068) */
    .metric-card {
        background: linear-gradient(135deg, #0B0840 20%, #270840 80%);
        padding: 2rem;
        border-radius: 1.2rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    /* Karte unten links (Monatsrente) */
    .renten-info {
        background: linear-gradient(135deg, #0B0840 20%, #270840 80%);
        color: white;
        padding: 1.5rem;
        border-radius: 1.2rem;
        text-align: center;
    }
    /* Fortschrittsbalken Styling */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        border-radius: 10px;
        height: 12px;
    }  
    h1, h2, h3, p { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATEN LADEN ---
goal_value = 500000 
current_value, df_chart = get_portfolio_data()
progress_pct = min(current_value / goal_value, 1.0) 
gesicherte_rente = (current_value * 0.04) / 12

# --- LAYOUT: ZWEI SPALTEN ---
col1, col2 = st.columns([1, 1.2], gap="large")
with col1:
    st.markdown("<p style='color: #6c757d !important; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;'>Fortschritt Übersicht</p>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="metric-card">
            <h1 style='margin: 0; font-size: 2.8rem;'>Rente 2068</h1>
            <p style='color: #4facfe !important; font-weight: 700; font-size: 1.1rem; margin-top: 10px;'>
                {int(progress_pct*100)}% GESCHAFFT
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.progress(progress_pct)
    st.write("") 
    st.markdown(f"""
        <div class="renten-info">
            <span style='font-size: 0.8rem; opacity: 0.7; text-transform: uppercase; letter-spacing: 1px;'>Rente nach aktuellem Stand</span>
            <h2 style='margin: 10px 0; font-size: 2.2rem;'>{gesicherte_rente:.2f} € <span style='font-size: 1rem; opacity:0.6;'>/ Monat</span></h2>
            <p style='font-size: 0.8rem; margin: 0; opacity: 0.8;'>Basierend auf 4% Entnahmerate</p>
        </div>
        """, unsafe_allow_html=True)
with col2:
    st.markdown("<p style='color: #6c757d !important; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;'>Asset Verteilung</p>", unsafe_allow_html=True)   
    if not df_chart.empty:
        fig = px.pie(
            df_chart, 
            values='Wert', 
            names='Asset', 
            hole=0.6,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )     
        fig.update_layout(
            margin=dict(t=30, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white", size=12),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle", y=0.5,
                xanchor="left", x=1.1 
            )
        )
        fig.update_traces(textinfo='none', hovertemplate="<b>%{label}</b><br>%{value:,.2f} €<br>%{percent}")     
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Fehler beim Laden der Chart-Daten.")
st.markdown("---")
st.markdown("<p style='text-align: center; color: #454A4F !important; font-size: 0.7rem;'>Stay focused ・ Stay invested ・ Keep investing ・ Never change a running system</p>", unsafe_allow_html=True)
