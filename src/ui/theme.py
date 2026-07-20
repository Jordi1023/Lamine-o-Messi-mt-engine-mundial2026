"""
theme.py
--------
Estilo visual "dark premium" con fondo de estadio nocturno

Streamlit pinta el header, el contenedor principal y los
iframes de los gráficos Vega/Altair en blanco por defecto, sin importar
lo que se ponga en `.stApp`. El CSS de acá fuerza transparencia
en toda la cadena de contenedores reales (`stAppViewContainer`,
`stHeader`, `.block-container`, `stVegaLiteChart`, etc.), no solo en
`.stApp`.
"""

import streamlit as st

CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Rajdhani:wght@600;700&display=swap');

    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stBottomBlockContainer"],
    .main, .block-container {
        background: transparent !important;
        color: #F3F4F6 !important;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }

    .stApp {
        background:
            radial-gradient(ellipse at top, rgba(20, 40, 30, 0.55) 0%, rgba(8, 10, 12, 0.94) 55%),
            linear-gradient(180deg, rgba(6,8,10,0.92) 0%, rgba(10,12,14,0.97) 100%),
            url('https://images.unsplash.com/photo-1522778119026-d647f0596c20?auto=format&fit=crop&w=2000&q=80');
        background-size: cover;
        background-position: center top;
        background-attachment: fixed;
        color: #F3F4F6;
        font-family: 'Inter', sans-serif;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
        background-size: 42px 42px;
        pointer-events: none;
        z-index: 0;
    }

    [data-testid="stVegaLiteChart"], .vega-embed, .vega-embed canvas,
    [data-testid="stArrowVegaLiteChart"] {
        background: transparent !important;
    }

    p, span, label, .stMarkdown, .stCaption { color: #E5E5E5; }

    .dashboard-header {
        text-align: center;
        padding: 34px 10px;
        background: linear-gradient(135deg, rgba(20,22,26,0.85), rgba(12,14,17,0.85));
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 28px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.05);
        backdrop-filter: blur(6px);
    }
    .dashboard-header h1 {
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #F1BF00, #43A1D5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-card {
        background: linear-gradient(160deg, rgba(28,28,30,0.9), rgba(15,15,17,0.9));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 26px;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255,255,255,0.04);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        backdrop-filter: blur(8px);
    }
    .metric-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 22px 40px rgba(0, 0, 0, 0.6);
    }
    .spain-card { border-top: 5px solid #E10613 !important; }
    .argentina-card { border-top: 5px solid #43A1D5 !important; }

    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }

    .stSelectbox, .stMultiSelect, .stNumberInput, .stSlider { color: white !important; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10,12,14,0.97), rgba(6,7,9,0.98));
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    [data-baseweb="select"] > div,
    div[data-testid="stNumberInputContainer"],
    input[type="number"] {
        background-color: rgba(30, 32, 36, 0.9) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: #F3F4F6 !important;
        border-radius: 8px !important;
    }
    [data-baseweb="popover"] ul, [data-baseweb="menu"] {
        background-color: #1a1c20 !important;
        color: #F3F4F6 !important;
    }
    li[role="option"] { background-color: #1a1c20 !important; color: #F3F4F6 !important; }
    li[role="option"]:hover { background-color: #2a2d33 !important; }

    span[data-baseweb="tag"] {
        background-color: #2c3e50 !important;
        border: 1px solid #43A1D5 !important;
    }
    span[data-baseweb="tag"] span { color: #F3F4F6 !important; }

    .squad-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        background: rgba(67, 161, 213, 0.15);
        border: 1px solid rgba(67, 161, 213, 0.4);
        color: #8FD3FF;
        margin-bottom: 8px;
    }
</style>
"""


def inject_theme() -> None:
    """Inyecta el CSS del tema oscuro en la app de Streamlit."""
    st.markdown(CSS, unsafe_allow_html=True)
