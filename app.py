"""
app.py
------
MT-ENGINE: Simulador Táctico Avanzado — Final del Mundial 2026
España vs Argentina | Domingo 19 de julio, MetLife Stadium.


    1. Configuración de página + tema visual   -> src/ui
    2. Datos de convocatoria y estadísticas reales -> src/data
    3. Cálculo de xG y simulación Monte Carlo   -> src/simulation
    4. Renderizado de la interfaz               -> src/ui/components

Correr con:
    streamlit run app.py
"""

import streamlit as st

from src.data.squads import (
    JUGADORES_ARGENTINA,
    JUGADORES_ESPAÑA,
    XI_SUGERIDO_ARG,
    XI_SUGERIDO_ESP,
)
from src.simulation.montecarlo import run_tactical_simulation
from src.simulation.xg_model import compute_match_xg
from src.ui.components import (
    render_header,
    render_live_status,
    render_methodology,
    render_probability_chart,
    render_real_data_panel,
    render_result_cards,
    render_sidebar_controls,
    render_squad_reference,
)
from src.ui.theme import inject_theme


def main() -> None:
    st.set_page_config(
        page_title="Mundial 2026 - Tactical Simulator",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_theme()

    render_header()
    render_real_data_panel()

    controles = render_sidebar_controls(
        JUGADORES_ESPAÑA, JUGADORES_ARGENTINA, XI_SUGERIDO_ESP, XI_SUGERIDO_ARG
    )

    marcador = render_live_status(
        controles["tactica_esp"],
        controles["tactica_arg"],
        controles["titulares_esp"],
        controles["titulares_arg"],
        len(JUGADORES_ESPAÑA),
        len(JUGADORES_ARGENTINA),
    )

   
    equipos_completos = len(controles["titulares_esp"]) == 11 and len(controles["titulares_arg"]) == 11
    if not equipos_completos:
        st.info(
            "⏳ **Simulación en pausa.** Selecciona exactamente 11 titulares en cada "
            "selección (en la barra lateral) para calcular el xG y las probabilidades. "
            "Un equipo incompleto no tiene una plantilla real que evaluar."
        )
        st.stop()


    xg_esp, xg_arg = compute_match_xg(
        JUGADORES_ESPAÑA,
        JUGADORES_ARGENTINA,
        controles["titulares_esp"],
        controles["titulares_arg"],
        controles["clima"],
    )

    prob_esp_calc, prob_arg_calc, xg_esp_final, xg_arg_final = run_tactical_simulation(
        xg_esp, xg_arg, controles["expulsados_esp"], controles["expulsados_arg"]
    )

    if marcador == "España abre el marcador":
        prob_esp_final = min(98.0, prob_esp_calc * 1.45)
        prob_arg_final = max(2.0, 100.0 - prob_esp_final)
    elif marcador == "Argentina abre el marcador":
        prob_arg_final = min(98.0, prob_arg_calc * 1.45)
        prob_esp_final = max(2.0, 100.0 - prob_arg_final)
    else:
        prob_esp_final = prob_esp_calc
        prob_arg_final = prob_arg_calc

    render_result_cards(
        controles["tactica_esp"], controles["tactica_arg"],
        xg_esp_final, xg_arg_final, prob_esp_final, prob_arg_final,
    )

    st.markdown("---")
    render_probability_chart(prob_esp_final, prob_arg_final)
    render_squad_reference(JUGADORES_ESPAÑA, JUGADORES_ARGENTINA)
    render_methodology()


if __name__ == "__main__":
    main()
