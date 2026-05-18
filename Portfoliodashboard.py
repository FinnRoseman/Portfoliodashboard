import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import numpy as np
import plotly.graph_objects as go

# --- KONFIGURATION & CONFIG AREA ---
st.set_page_config(page_title="Behavioral Portfolio Tracker", layout="wide")

# Hier definierst du die Zielsummen (ohne monatliche Raten, wie gewünscht)
GOAL_RENTE = 500000
GOAL_HOCHZEIT = 20000
GOAL_HAUSBAU = 200000

@st.cache_data(ttl=3600)
def get_portfolio_data():
    # Dein echtes Altersvorsorge-Portfolio
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    } 
    .main { background-color: #0E1117; }
    
    /* Karte oben links */
    .metric-card {
        background: linear-gradient(135deg, #0B0840 20%, #270840 80%);
        padding: 2rem;
        border-radius: 1.2rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    /* Karte unten links */
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

# --- DROP-DOWN MENÜ GANZ OBEN ---
ziel = st.selectbox(
    "🎯 Ansicht wechseln:", 
    ["🌴 Altersvorsorge 2068", "💍 Hochzeit in 5 Jahren", "🧱 Hausbau in 12 Jahren"]
)

# --- DYNAMISCHE DATENLOGIK JE NACH ZIEL ---
current_value_rente, df_chart_rente = get_portfolio_data()

if ziel == "Rente 2068":
    # 1. Links Oben Card
    card_titel = "Rente 2068"
    progress_pct = min(current_value_rente / GOAL_RENTE, 1.0)
    
    # 2. Links Unten Card
    gesicherte_rente = (current_value_rente * 0.04) / 12
    card_unten_titel = "Rente nach aktuellem Stand"
    card_unten_wert = f"{gesicherte_rente:.2f} € <span style='font-size: 1rem; opacity:0.6;'>/ Monat</span>"
    card_unten_subtext = "Basierend auf 4% Entnahmerate"
    
    # 3. Donut Konfiguration
    df_active_chart = df_chart_rente
    donut_colors = px.colors.sequential.dense_r
    
    # 4. Zeit-Schutzschild-Kalkulation (Volles Risiko, flacht über 42 Jahre ab)
    x_max_jahre = 42
    basis_linie = 2
    amplitude_start = 18
    dämpfungs_faktor = 8
    frequenz = 3.5

elif ziel == "Hochzeit 2031":
    # Fiktive Daten für die Demonstration (Anpassbar)
    current_value_hochzeit = 7000 
    
    card_titel = "Hochzeit 2031"
    progress_pct = min(current_value_hochzeit / GOAL_HOCHZEIT, 1.0)
    
    card_unten_titel = "Zielbudget Hochzeit"
    card_unten_wert = f"{GOAL_HOCHZEIT:,} €".replace(",", ".")
    card_unten_subtext = "Dein kalkulierter Puffer für Feier & Reise"
    
    # Kühle, sichere Blau-Lila Farbstruktur für Geldmarkt/Tagesgeld
    df_active_chart = pd.DataFrame({
        "Asset": ["Geldmarkt-ETF (z.B. DBX0AN)", "Tagesgeldpuffer", "Staatsanleihen (AAA)", "Defensive ETFs"],
        "Wert": [4000, 1500, 1000, 500]
    })
    donut_colors = ['#0d0887', '#2a0593', '#41049d', '#5302a3']
    
    # 5 Jahre Horizont, sehr flache Kurve da defensiv investiert
    x_max_jahre = 5
    basis_linie = 1.5
    amplitude_start = 4  # Kaum Zittern durch Stoßdämpfer-Effekt
    dämpfungs_faktor = 3
    frequenz = 2.0
    behavioral_tipp = "Da das Hochzeitsgeld in 5 Jahren gebraucht wird, fängt dein hoher Geldmarkt-Anteil Marktschwankungen ab. Die Linie bleibt ruhig und sicher."

else: # 🧱 Hausbau in 12 Jahren
    current_value_haus = 15000
    
    card_titel = "Eigenkapital Haus"
    progress_pct = min(current_value_haus / GOAL_HAUSBAU, 1.0)
    
    card_unten_titel = "Ziel-Anzahlung"
    card_unten_wert = f"{GOAL_HAUSBAU:,} €".replace(",", ".")
    card_unten_subtext = "Dein Fundament für eine solide Bank-Finanzierung"
    
    # Misch-Portfolio aus ETFs und Festgeld
    df_active_chart = pd.DataFrame({
        "Asset": ["Welt-Aktien-ETF", "Einzelaktien (Core)", "Festgeld / Kündigungsgeld", "Anleihen-ETF"],
        "Wert": [7000, 3000, 3500, 1500]
    })
    donut_colors = px.colors.sequential.Purp_r
    
    # Hybrid-Verlauf über 12 Jahre
    x_max_jahre = 12
    basis_linie = 2
    amplitude_start = 12 # Mittleres Risiko am Anfang, flacht ab
    dämpfungs_faktor = 5
    frequenz = 3.0
    behavioral_tipp = "In den ersten Jahren nutzt du die Marktrendite für dein Eigenkapital. Zum Ende hin wird das Risiko kontrolliert in Richtung Nulllinie gedrosselt."


# --- LAYOUT: ZWEI SPALTEN ---
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("<p style='color: #6c757d !important; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;'>Fortschritt Übersicht</p>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="metric-card">
            <h1 style='margin: 0; font-size: 2.8rem;'>{card_titel}</h1>
            <p style='color: #4facfe !important; font-weight: 700; font-size: 1.1rem; margin-top: 10px;'>
                {int(progress_pct*100)}% GESCHAFFT
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.progress(progress_pct)
    st.write("") 
    st.markdown(f"""
        <div class="renten-info">
            <span style='font-size: 0.8rem; opacity: 0.7; text-transform: uppercase; letter-spacing: 1px;'>{card_unten_titel}</span>
            <h2 style='margin: 10px 0; font-size: 2.2rem;'>{card_unten_wert}</h2>
            <p style='font-size: 0.8rem; margin: 0; opacity: 0.8;'>{card_unten_subtext}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("<p style='color: #6c757d !important; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;'>Asset Verteilung</p>", unsafe_allow_html=True)   
    if not df_active_chart.empty:
        fig = px.pie(
            df_active_chart, 
            values='Wert', 
            names='Asset', 
            hole=0.6,
            color_discrete_sequence=donut_colors
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

# --- ZEITFAKTOR (DER BEHAVIORAL GRAPH) ---
st.write("---")
st.markdown("<p style='color: #6c757d !important; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;'>Zeitfaktor & Volatilitäts-Schutzschild</p>", unsafe_allow_html=True)

# Mathematische Generierung basierend auf den dynamischen Variablen von oben
x = np.linspace(0, x_max_jahre, 1000)
noise_amplitude = amplitude_start * np.exp(-x / dämpfungs_faktor) 
noise = noise_amplitude * np.sin(x * frequenz)
y_vals = basis_linie + noise

fig_shield = go.Figure()
fig_shield.add_trace(go.Scatter(
    x=x, 
    y=np.minimum(y_vals, 0), 
    fill='tozeroy',
    mode='lines',
    line=dict(width=0),
    fillcolor='rgba(255, 75, 75, 0.4)',
    name='Risiko-Zone',
    hoverinfo='skip'
))
fig_shield.add_trace(go.Scatter(
    x=x, 
    y=np.maximum(y_vals, 0), 
    fill='tozeroy',
    mode='lines',
    line=dict(width=0),
    fillcolor='rgba(49, 222, 18, 0.4)',
    name='Sicherheits-Zone',
    hoverinfo='skip'
))
fig_shield.add_trace(go.Scatter(
    x=x, 
    y=np.where(y_vals >= 0, y_vals, np.nan),
    mode='lines',
    line=dict(width=4, color='#31DE12'),
    name='Sicherheit'
))
fig_shield.add_trace(go.Scatter(
    x=x, 
    y=np.where(y_vals < 0, y_vals, np.nan), 
    mode='lines',
    line=dict(width=4, color='#ff4b4b'),
    name='Risiko'
))
fig_shield.add_hline(y=0, line_width=1, line_color="white", opacity=0.8) # Opacity leicht erhöht für bessere Sichtbarkeit
fig_shield.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    height=400,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(title="Haltedauer in Jahren", color="white", showgrid=False),
    yaxis=dict(title="Volatilität", color="white", showgrid=False, zeroline=True, showticklabels=False),
    showlegend=False
)
st.plotly_chart(fig_shield, use_container_width=True)

# Dynamischer psychologischer Tipp unter dem Graphen
st.markdown(f"> **Stoiker-Hinweis:** {behavioral_tipp}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #454A4F !important; font-size: 0.7rem;'>Stay focused ・ Stay invested ・ Keep investing ・ Never change a running system</p>", unsafe_allow_html=True)
