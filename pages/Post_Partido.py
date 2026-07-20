import altair as alt
import pandas as pd
import streamlit as st

from src.data.real_stats import RESULTADO_FINAL
from src.data.squads import JUGADORES_ARGENTINA, JUGADORES_ESPAÑA, XI_SUGERIDO_ARG, XI_SUGERIDO_ESP
from src.simulation.montecarlo import run_tactical_simulation
from src.simulation.postmortem import brier_score, interpretar_brier, player_contributions
from src.simulation.xg_model import XG_BASE, FACTOR_DEF_RIVAL, compute_match_xg
from src.ui.theme import inject_theme

st.set_page_config(page_title="Post-Mortem — MT-Engine", page_icon="📊", layout="wide")
inject_theme()

st.markdown(
    """
    <div class="dashboard-header">
        <h1 style='margin:0; font-size: 2.4rem;'>📊 Post-Mortem: ¿Acertó el Modelo?</h1>
        <p style='margin:5px 0 0 0; color:#AAAAAA; font-size:1.05rem;'>
            Predicción pre-partido (XI sugerido, sin ajustes in-play) vs. resultado real de la final
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "En esta página nos saltamos librerías como SHAP o las matrices de confusión a propósito: el modelo es una "
"fórmula aditiva que escribimos nosotros mismos, así que es 100% transparente — no es ninguna caja negra "
"que necesite herramientas extra para entenderse. Para un modelo lineal como este, calcular el "
"\"valor SHAP\" de cada variable sería redundante, porque matemáticamente es igual a su coeficiente directo. Lo que sí "
"aporta valor real es desmenuzar el cálculo paso a paso y medir la calibración con el **Brier Score**, "
"que es la métrica correcta cuando analizamos **una** sola observación real (n=1) — no el MAE o una matriz de "
"confusión, que no tienen ningún sentido estadístico si lo único que estás evaluando es un solo partido."
)


# Predicción pre-partido de referencia 

xg_esp, xg_arg = compute_match_xg(JUGADORES_ESPAÑA, JUGADORES_ARGENTINA, XI_SUGERIDO_ESP, XI_SUGERIDO_ARG, clima="Normal")
prob_esp, prob_arg, _, _ = run_tactical_simulation(xg_esp, xg_arg, num_simulations=50_000)

gano_esp = RESULTADO_FINAL["campeon"] == "España"
score = brier_score(prob_esp, ocurrio=gano_esp)

st.markdown("---")
st.subheader("🎯 Predicción vs. Realidad")

col_pred, col_real, col_brier = st.columns(3)
with col_pred:
    st.markdown(
        f"""
        <div class="metric-card" style="text-align:center;">
            <p style="margin:0; color:#CCCCCC; font-size:13px;">PREDICCIÓN PRE-PARTIDO</p>
            <h1 style="margin:6px 0 0; font-size:2.6rem; color:#F1BF00;">{prob_esp:.1f}%</h1>
            <p style="margin:0; font-size:13px; color:#888;">España (XI sugerido, sin ajustes live)</p>
        </div>
        """, unsafe_allow_html=True,
    )
with col_real:
    st.markdown(
        f"""
        <div class="metric-card" style="text-align:center;">
            <p style="margin:0; color:#CCCCCC; font-size:13px;">RESULTADO REAL</p>
            <h1 style="margin:6px 0 0; font-size:2.6rem; color:#43A1D5;">{RESULTADO_FINAL['marcador']}</h1>
            <p style="margin:0; font-size:13px; color:#888;">Campeón: {RESULTADO_FINAL['campeon']}</p>
        </div>
        """, unsafe_allow_html=True,
    )
with col_brier:
    st.markdown(
        f"""
        <div class="metric-card" style="text-align:center;">
            <p style="margin:0; color:#CCCCCC; font-size:13px;">BRIER SCORE</p>
            <h1 style="margin:6px 0 0; font-size:2.6rem; color:#FFFFFF;">{score}</h1>
            <p style="margin:0; font-size:13px; color:#888;">0 = perfecto · 0.25 = moneda al aire · 1 = pésimo</p>
        </div>
        """, unsafe_allow_html=True,
    )

st.info(f"**Interpretación honesta:** {interpretar_brier(score)}")

st.markdown(
    """
    **Por qué esto importa más que solo "acertó o no" ? :** el modelo dio a España **apenas por encima del 50%**
    con la alineación sugerida por defecto — no fue una predicción confiada, fue prácticamente un lanzamiento
    de moneda que se inclinó levemente hacia España. Acertó la dirección, pero el Brier Score cercano a 0.25
    lo confirma: la certeza real del modelo fue baja. 
    """
)


# Waterfall de la contribución ofensiva de cada titular

st.markdown("---")
st.subheader("🧩 Descomposición del xG — contribución de cada titular")

equipo_sel = st.radio("Selecciona la selección a descomponer:", ["España 🇪🇸", "Argentina 🇦🇷"], horizontal=True)

if equipo_sel.startswith("España"):
    jugadores, titulares, rivales, titulares_rival = JUGADORES_ESPAÑA, XI_SUGERIDO_ESP, JUGADORES_ARGENTINA, XI_SUGERIDO_ARG
    color_positivo, xg_final = "#F1BF00", xg_esp
else:
    jugadores, titulares, rivales, titulares_rival = JUGADORES_ARGENTINA, XI_SUGERIDO_ARG, JUGADORES_ESPAÑA, XI_SUGERIDO_ESP
    color_positivo, xg_final = "#43A1D5", xg_arg

contribuciones_of = player_contributions(jugadores, titulares, clave="of")
defensa_rival_total = sum(rivales[nombre]["def"] for nombre in titulares_rival) * FACTOR_DEF_RIVAL

pasos = [("Base (estructura mínima)", XG_BASE)]
pasos += contribuciones_of
pasos.append(("Defensa rival (agregada)", -defensa_rival_total))

df_waterfall = pd.DataFrame(pasos, columns=["Concepto", "Valor"])
df_waterfall["Acumulado_fin"] = df_waterfall["Valor"].cumsum()
df_waterfall["Acumulado_inicio"] = df_waterfall["Acumulado_fin"] - df_waterfall["Valor"]
df_waterfall["Color"] = df_waterfall["Valor"].apply(lambda v: color_positivo if v >= 0 else "#E10613")
orden = df_waterfall["Concepto"].tolist()

waterfall_chart = alt.Chart(df_waterfall).mark_bar(size=28, cornerRadius=4).encode(
    x=alt.X("Concepto:N", sort=orden, axis=alt.Axis(labelColor="#F3F4F6", titleColor="#F3F4F6", labelAngle=-40, domain=False)),
    y=alt.Y("Acumulado_inicio:Q", title="xG acumulado", axis=alt.Axis(labelColor="#CCCCCC", titleColor="#CCCCCC", gridColor="rgba(255,255,255,0.08)")),
    y2="Acumulado_fin:Q",
    color=alt.Color("Color:N", scale=None, legend=None),
    tooltip=[alt.Tooltip("Concepto:N"), alt.Tooltip("Valor:Q", format="+.2f"), alt.Tooltip("Acumulado_fin:Q", title="Acumulado", format=".2f")],
).properties(height=420, background="transparent").configure_view(strokeWidth=0)

st.altair_chart(waterfall_chart, use_container_width=True)
st.caption(
    f"xG final resultante: **{xg_final:.2f}**. Cada barra dorada/celeste suma según el aporte ofensivo real del "
    f"jugador en este Mundial; la barra roja resta el aporte defensivo agregado del XI rival "
    f"(ponderado × {FACTOR_DEF_RIVAL}, el mismo factor que usa el modelo principal)."
)

st.markdown("---")
st.page_link("app.py", label="⬅️ Volver al simulador principal", icon="⚡")
