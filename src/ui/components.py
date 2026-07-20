"""
components.py
--------------
Componentes de renderizado de la app: header, panel de datos reales,
controles de la barra lateral, tarjetas de resultado, gráfico de
probabilidades y bloques informativos (convocatoria completa y
metodología).

Mantener la UI separada de la lógica de datos/simulación permite testear
`src/simulation` sin depender de Streamlit.
"""

from typing import Dict, List, Tuple

import altair as alt
import pandas as pd
import streamlit as st

from src.data.real_stats import (
    FUENTES,
    FECHA_ACTUALIZACION,
    GOLEADORES_REAL_ARG,
    GOLEADORES_REAL_ESP,
    RESULTADO_FINAL,
    RESUMEN_REAL,
)


def render_final_result_banner() -> None:
    """Banner con el resultado real de la final, si ya se jugó."""
    if not RESULTADO_FINAL.get("jugado"):
        return
    st.markdown(
        f"""
        <div class="metric-card" style="border-top: 5px solid #F1BF00; text-align:center; margin-bottom:24px;">
            <h2 style="margin:0;">🏆 {RESULTADO_FINAL['campeon']} es Campeona del Mundo 2026</h2>
            <p style="margin:6px 0 0; font-size:1.1rem;"><b>{RESULTADO_FINAL['marcador']}</b></p>
            <p style="margin:4px 0 0; color:#CCCCCC; font-size:14px;">
                Gol: {RESULTADO_FINAL['goleador']} · {RESULTADO_FINAL['detalle']}
            </p>
            <p style="margin:2px 0 0; color:#888; font-size:12px;">{RESULTADO_FINAL['fecha']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("🔍 ¿Acertó el modelo? — análisis post-partido", expanded=False):
        st.markdown(
            """
            **Lo que acertó:** el modelo daba a España como favorita en la mayoría de configuraciones
            de titulares (por su récord defensivo real de 1 gol recibido en 7 partidos previos), y España
            efectivamente ganó. También calculaba un partido de **pocos goles** (xG cercano a 1 por equipo),
            coherente con un 1-0.

            **Lo que NO acertó / no podía acertar:**
            - No predijo el marcador exacto ni que se necesitaría prórroga.
            - No predijo que Ferrán Torres sería el goleador (el modelo lo tenía como aporte ofensivo
              moderado, no como principal candidato — eso lo tenía Oyarzabal).
            - No predijo la expulsión de Enzo Fernández. Eso solo se puede *simular* manualmente con el
              contador de Tarjetas Rojas después de que pasa, no anticiparlo.

            **Conclusión :** un modelo de Poisson + Monte Carlo con datos reales del torneo puede
            orientar razonablemente hacia quién es favorito y si el partido será cerrado o no — pero
            **no predice eventos puntuales** (goleador, expulsiones, tiempo exacto del gol). Eso requeriría
            un modelo completamente distinto (simulación evento a evento, no agregada). 
            """
        )


def render_header() -> None:
    st.markdown(
        """
        <div class="dashboard-header">
            <h1 style='margin:0; font-size: 2.7rem;'>⚡ MT-ENGINE: Simulador Táctico Avanzado</h1>
            <p style='margin:5px 0 0 0; color:#AAAAAA; font-size:1.1rem;'>
                Mundial 2026 | España vs Argentina — Final jugada el 19 de julio en el MetLife Stadium (Nueva Jersey)
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_real_data_panel() -> None:
    with st.expander("📡 Datos reales del torneo (fuente y actualización)", expanded=False):
        st.markdown(
            "La final **ya se jugó**: España se coronó campeona del Mundo 2026 tras vencer a Argentina "
            "en la final del domingo 19 de julio. Los coeficientes de cada jugador en este simulador están "
            "calibrados con el rendimiento **real** de cada selección durante todo el torneo — no son datos "
            "históricos genéricos ni una proyección de preferencias. El simulador sigue activo para explorar "
            "escenarios hipotéticos ('¿y si...'), pero ya no es una predicción — es una herramienta retrospectiva."
        )
        col_real1, col_real2 = st.columns(2)
        for pais, col in [("España", col_real1), ("Argentina", col_real2)]:
            r = RESUMEN_REAL[pais]
            with col:
                st.markdown(f"**{pais}** — {r['PJ']} PJ · {r['V']}V {r['E']}E {r['D']}D · **{r['GF']} GF / {r['GC']} GC**")
                st.caption(" → ".join(r["camino"]))

        st.markdown("**Goleadores reales de este Mundial :**")
        col_gol1, col_gol2 = st.columns(2)
        with col_gol1:
            st.caption("🇪🇸 " + ", ".join(f"{n} ({g})" for n, g in GOLEADORES_REAL_ESP.items()))
        with col_gol2:
            st.caption("🇦🇷 " + ", ".join(f"{n} ({g})" for n, g in GOLEADORES_REAL_ARG.items()))

        fuentes_txt = ", ".join(FUENTES)
        st.markdown(
            f"<span style='font-size:12px; color:#888;'>Fuentes: {fuentes_txt} "
            f"(consultadas el {FECHA_ACTUALIZACION}). Datos compilados manualmente para esta app; "
            "no es un feed en tiempo real, así que si simulas después del domingo 19 de julio, actualiza tú "
            "los números con el resultado real. Esto es una herramienta ilustrativa/analítica — no la uses como "
            "base para apostar dinero real.</span>",
            unsafe_allow_html=True,
        )


def render_sidebar_controls(
    jugadores_esp: Dict[str, dict],
    jugadores_arg: Dict[str, dict],
    xi_sugerido_esp: List[str],
    xi_sugerido_arg: List[str],
) -> dict:
    """Renderiza la barra lateral completa y devuelve todas las selecciones del usuario."""
    st.sidebar.header("📋 Gestión de Plantillas (Arma tu 11)")
    st.sidebar.caption("Todos los jugadores listados pertenecen a la convocatoria final de 26 confirmada para el Mundial 2026.")

    tactica_esp = st.sidebar.selectbox("📐 Sistema España", ["4-3-3", "4-2-3-1", "3-5-2"])
    tactica_arg = st.sidebar.selectbox("📐 Sistema Argentina", ["4-3-3", "4-4-2", "3-5-2"])

    st.sidebar.subheader("🇪🇸 Convocados España (26)")
    titulares_esp = st.sidebar.multiselect(
        "Selecciona los 11 titulares de España:",
        options=list(jugadores_esp.keys()),
        default=xi_sugerido_esp,
        help=(
            "Solo aparecen los 26 futbolistas realmente convocados por Luis de la Fuente. "
            "El 11 titular se mantiene fijo durante todo el partido: para simular una "
            "expulsión NO quites jugadores de acá, usa el contador de Tarjetas Rojas más abajo."
        ),
        key="titulares_esp",
    )

    st.sidebar.subheader("🇦🇷 Convocados Argentina (26)")
    titulares_arg = st.sidebar.multiselect(
        "Selecciona los 11 titulares de Argentina:",
        options=list(jugadores_arg.keys()),
        default=xi_sugerido_arg,
        help=(
            "Solo aparecen los 26 futbolistas realmente convocados por Lionel Scaloni. "
            "El 11 titular se mantiene fijo durante todo el partido: para simular una "
            "expulsión NO quites jugadores de acá, usa el contador de Tarjetas Rojas más abajo."
        ),
        key="titulares_arg",
    )

    st.sidebar.header("⚠️ Eventos de Partido In-Play")
    st.sidebar.caption("Para simular una expulsión, sube el contador de tarjetas rojas — no edites el 11 titular de arriba.")
    clima = st.sidebar.select_slider("🌦️ Estado de la Cancha / Clima", options=["Rápida (Seca)", "Normal", "Pesada (Lluvia)"])
    expulsados_esp = st.sidebar.number_input("🔴 Tarjetas Rojas España", min_value=0, max_value=4, value=0, step=1)
    expulsados_arg = st.sidebar.number_input("🔴 Tarjetas Rojas Argentina", min_value=0, max_value=4, value=0, step=1)

    return {
        "tactica_esp": tactica_esp,
        "tactica_arg": tactica_arg,
        "titulares_esp": titulares_esp,
        "titulares_arg": titulares_arg,
        "clima": clima,
        "expulsados_esp": expulsados_esp,
        "expulsados_arg": expulsados_arg,
    }


def render_live_status(
    tactica_esp: str,
    tactica_arg: str,
    titulares_esp: List[str],
    titulares_arg: List[str],
    total_esp: int,
    total_arg: int,
) -> str:
    """Renderiza el estado del partido (radio de marcador) y el resumen de titulares. Devuelve la opción de marcador elegida."""
    col_live1, col_live2 = st.columns([2, 1])

    with col_live2:
        st.markdown("### 🏟️ Estado del Partido")
        marcador = st.radio(
            "Modificar Marcador Real-Time:",
            ["Empate / Inicio", "España abre el marcador", "Argentina abre el marcador"],
        )

    with col_live1:
        st.markdown("### 📋 Análisis de los 11 elegidos")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown('<span class="squad-badge">CONVOCADOS OFICIALES</span>', unsafe_allow_html=True)
            st.markdown(f"**🇪🇸 España ({tactica_esp}):**")
            st.caption(f"Titulares seleccionados: {len(titulares_esp)} de 11 recomendados · {total_esp} convocados disponibles.")
            if len(titulares_esp) != 11:
                st.warning("Selecciona exactamente 11 titulares para España.")
        with col_t2:
            st.markdown('<span class="squad-badge">CONVOCADOS OFICIALES</span>', unsafe_allow_html=True)
            st.markdown(f"**🇦🇷 Argentina ({tactica_arg}):**")
            st.caption(f"Titulares seleccionados: {len(titulares_arg)} de 11 recomendados · {total_arg} convocados disponibles.")
            if len(titulares_arg) != 11:
                st.warning("Selecciona exactamente 11 titulares para Argentina.")

    return marcador


def render_result_cards(tactica_esp: str, tactica_arg: str, xg_esp: float, xg_arg: float, prob_esp: float, prob_arg: float) -> None:
    col_res1, col_res2 = st.columns(2)

    with col_res1:
        st.markdown(
            f"""
            <div class="metric-card spain-card">
                <h2 style='margin:0; color:#FF4B4B;'>🇪🇸 ESPAÑA</h2>
                <p style='margin:0; font-size:14px; color:#CCCCCC;'>Esquema: {tactica_esp} | xG Esperado: <b>{xg_esp:.2f}</b></p>
                <h1 style='margin:10px 0 0 0; font-size:4.2rem; color:#F1BF00;'>{prob_esp:.1f}%</h1>
                <p style='margin:0; font-size:13px; color:#888;'>Suma de impactos individuales de los convocados titulares.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_res2:
        st.markdown(
            f"""
            <div class="metric-card argentina-card">
                <h2 style='margin:0; color:#43A1D5;'>🇦🇷 ARGENTINA</h2>
                <p style='margin:0; font-size:14px; color:#CCCCCC;'>Esquema: {tactica_arg} | xG Esperado: <b>{xg_arg:.2f}</b></p>
                <h1 style='margin:10px 0 0 0; font-size:4.2rem; color:#43A1D5;'>{prob_arg:.1f}%</h1>
                <p style='margin:0; font-size:13px; color:#888;'>Suma de impactos individuales de los convocados titulares.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_probability_chart(prob_esp: float, prob_arg: float) -> None:
    st.subheader("📊 Probabilidades Proyectadas en Tiempo Real")

    df_chart = pd.DataFrame({
        "Selección": ["España 🇪🇸", "Argentina 🇦🇷"],
        "Porcentaje": [prob_esp, prob_arg],
    })

    barras = alt.Chart(df_chart).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=90).encode(
        x=alt.X("Selección:N", sort=None, axis=alt.Axis(labelColor="#F3F4F6", titleColor="#F3F4F6", labelFontSize=13, domain=False, ticks=False)),
        y=alt.Y("Porcentaje:Q", title="Probabilidad de victoria (%)",
                axis=alt.Axis(labelColor="#CCCCCC", titleColor="#CCCCCC", gridColor="rgba(255,255,255,0.08)", domain=False)),
        color=alt.Color("Selección:N",
                         scale=alt.Scale(domain=["España 🇪🇸", "Argentina 🇦🇷"], range=["#F1BF00", "#43A1D5"]),
                         legend=None),
        tooltip=[alt.Tooltip("Selección:N"), alt.Tooltip("Porcentaje:Q", format=".1f")],
    )

    etiquetas = alt.Chart(df_chart).mark_text(dy=-12, fontSize=16, fontWeight="bold", color="#FFFFFF").encode(
        x=alt.X("Selección:N", sort=None),
        y=alt.Y("Porcentaje:Q"),
        text=alt.Text("Porcentaje:Q", format=".1f"),
    )

    chart_final = (barras + etiquetas).properties(height=380, background="transparent").configure_view(strokeWidth=0)
    st.altair_chart(chart_final, use_container_width=True)


def render_squad_reference(jugadores_esp: Dict[str, dict], jugadores_arg: Dict[str, dict]) -> None:
    with st.expander("📜 Ver convocatoria completa (26 + 26)"):
        col_ref1, col_ref2 = st.columns(2)
        for pais_nombre, jugadores, col in [("🇪🇸 España", jugadores_esp, col_ref1), ("🇦🇷 Argentina", jugadores_arg, col_ref2)]:
            with col:
                st.markdown(f"**{pais_nombre}**")
                df_squad = pd.DataFrame([
                    {"Jugador": nombre, "Posición": datos["pos"]}
                    for nombre, datos in jugadores.items()
                ])
                for pos in ["Portero", "Defensa", "Mediocampista", "Delantero"]:
                    nombres = df_squad[df_squad["Posición"] == pos]["Jugador"].tolist()
                    st.caption(f"**{pos}s:** " + ", ".join(nombres))


def render_methodology() -> None:
    with st.expander("🛠️ Ver Sustento Metodológico de Impacto de Plantillas: "):
        st.markdown(
            """
            ### Arquitectura del Simulador de Plantillas

            Este motor no utiliza valores planos de xG estáticos, sino un modelo aditivo de **Sinergia Colectiva**
            calculado exclusivamente sobre los **26 jugadores convocados oficialmente** por cada selección.

            **De dónde salen los números? :**
            Los coeficientes ofensivos ($of$) están calibrados con el **rendimiento real** de cada jugador en este
            Mundial 2026 — goles anotados en el torneo, minutos disputados y contexto de cada gol (ver panel de
            "Datos reales" arriba) — recopilados manualmente de fuentes públicas (FIFA.com, Futbolred, CNN, ESPN).
            Los coeficientes defensivos ($def$) combinan el récord defensivo real del equipo (España recibió solo 1
            gol en 7 partidos; Argentina recibió 7).
            **Esto NO es un feed de datos en vivo**: es un snapshot construido a mano el 15 de julio de 2026, antes
            de la final. Si algo cambia (lesiones, decisiones técnicas de última hora), el modelo no se entera solo.

            1. **Suma de Impactos Individuales ($I_i$):**
               Cada jugador titular tiene un coeficiente $I_i = (of_i, def_i)$. El xG de ataque del equipo aumenta con su ofensiva,
               mientras que el xG en contra disminuye según la capacidad defensiva combinada de los titulares rivales.

            2. **Impacto de Expulsiones Dinámicas:**
               Si simulas una tarjeta roja, se activa una penalización del $20\\%$ de poder ofensivo por cada jugador menos,
               además de conceder un bono del $12\\%$ de generación de espacios al ataque rival.

            3. **Ajuste heurístico por marcador in-play:**
               La probabilidad cambia una vez que se rompe el marcador, escalando un factor multiplicativo simple.
               *(Nota honesta: no es una actualización bayesiana formal con prior/posterior, es una heurística.)*

            4. **Por qué Monte Carlo + Poisson y no una cadena de Markov?:**
               Los goles en un partido son eventos discretos y poco frecuentes: Poisson es el estándar en analítica
               deportiva para este tipo de conteo. Una cadena de Markov tendría sentido para modelar transiciones de
               estado minuto a minuto (posesión → tiro → gol), que no es el alcance de esta versión.

            **Límite del modelo:** ningún simulador estático predice sorpresas — y este Mundial ya nos enseñó
            esa lección con el 0-0 de España ante Cabo Verde en fase de grupos. Úsalo como herramienta analítica y de
            portafolio, no como garantía de resultado.
            """,
            unsafe_allow_html=True,
        )
