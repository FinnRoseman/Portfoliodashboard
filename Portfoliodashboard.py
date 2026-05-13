import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# Page Config für breites Layout
st.set_page_config(page_title="Behavioral Portfolio Tracker", layout="wide")

# --- FUNKTION: LIVE-KURSE LADEN (EURO-TICKER) ---
def get_portfolio_value():
    # Deine Positionen mit deutschen Tickern (.DE = Xetra, .F = Frankfurt, .SG = Stuttgart)
    # So umgehen wir die Währungsumrechnung, da diese Kurse direkt in EUR kommen.
    euro_portfolio = {
        "EMVL.DE": 6.58,   # iShares MSCI EM Value (Xetra)
        "XD9U.DE": 9.83,   # Xtrackers MSCI USA (Xetra)
        "BRYN.DE": 1.88,   # Berkshire Hathaway B (Xetra)
        "ITC.F": 24.26,    # Itochu Corp (Frankfurt)
        "IVS.F": 14.70,    # Investor AB (Frankfurt)
        "VDPX.DE": 31.05,  # Vanguard ESG Developed Asia (Xetra)
        "EUMF.DE": 82.12   # iShares MSCI Europe Multi-Factor (Xetra)
    }
    
    total_val = 0
    try:
        for ticker, shares in euro_portfolio.items():
            data = yf.Ticker(ticker)
            # Nutzt den aktuellsten verfügbaren Preis (Last Price)
            price = data.fast_info['last_price']
            total_val += (price * shares)
    except Exception as e:
        # Falls Yahoo Finance mal hakt, wird eine Fehlermeldung im Dashboard angezeigt
        st.error(f"Fehler beim Laden der Live-Kurse: {e}")
        return 72000 # Fallback-Wert
        
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
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("System 1: Behavioral Goal Tracking")
    
    # Die große Goal-Card
    st.markdown(f"""
        <div class="goal-card">
            <h1 style='color: #1f3b4d; font-size: 2.5rem;'>FINANCIAL GOAL: RETIREMENT 2045</h1>
            <p style='font-size: 1.2rem; color: #666;'>Status: Dein Ziel ist auf Kurs. Bleib diszipliniert!</p>
            <h2 style='color: #2ecc71;'>Aktueller Stand: {current_value:,.2f} €</h2>
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
    
    # Donut-Chart (Beispieldaten basierend auf deinem Portfolio)
    chart_data = pd.DataFrame({
        'Asset': ['Global ETFs', 'USA', 'Japan', 'Sweden', 'Asia/Europe'],
        'Value': [45, 15, 10, 10, 20]
    })
    
    fig = px.pie(chart_data, values='Value', names='Asset', hole=0.5,
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

    # Actionable Insights
    st.info("""
    **Actionable Insights:**
    * Sparrate beibehalten.
    * Kein Rebalancing in diesem Quartal nötig.
    * Fokus auf das Zieljahr 2045 richten.
    """)
