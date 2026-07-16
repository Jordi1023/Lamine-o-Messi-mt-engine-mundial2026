"""
test_simulation.py
-------------------
Tests unitarios de la capa de simulación (src/simulation). Solo uso de Numpy, sin depender de Streamlit ... se puede testeardirectamente con pytest.

Correr con:
    pytest tests/ -v
"""

import sys
from pathlib import Path

# Permite correr `pytest` desde la raíz del proyecto sin instalar el paquete
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data.squads import JUGADORES_ARGENTINA, JUGADORES_ESPAÑA, XI_SUGERIDO_ARG, XI_SUGERIDO_ESP
from src.simulation.montecarlo import run_tactical_simulation
from src.simulation.xg_model import compute_match_xg


def test_compute_match_xg_devuelve_valores_positivos():
    xg_esp, xg_arg = compute_match_xg(
        JUGADORES_ESPAÑA, JUGADORES_ARGENTINA, XI_SUGERIDO_ESP, XI_SUGERIDO_ARG, clima="Normal"
    )
    assert xg_esp > 0
    assert xg_arg > 0


def test_compute_match_xg_respeta_minimo():
    # Con 0 titulares, el xG no debería bajar del piso definido (XG_MINIMO)
    xg_esp, xg_arg = compute_match_xg(
        JUGADORES_ESPAÑA, JUGADORES_ARGENTINA, [], [], clima="Normal"
    )
    assert xg_esp >= 0.4
    assert xg_arg >= 0.4


def test_clima_lluvia_reduce_el_xg_respecto_a_normal():
    xg_esp_normal, xg_arg_normal = compute_match_xg(
        JUGADORES_ESPAÑA, JUGADORES_ARGENTINA, XI_SUGERIDO_ESP, XI_SUGERIDO_ARG, clima="Normal"
    )
    xg_esp_lluvia, xg_arg_lluvia = compute_match_xg(
        JUGADORES_ESPAÑA, JUGADORES_ARGENTINA, XI_SUGERIDO_ESP, XI_SUGERIDO_ARG, clima="Pesada (Lluvia)"
    )
    assert xg_esp_lluvia < xg_esp_normal
    assert xg_arg_lluvia < xg_arg_normal


def test_run_tactical_simulation_probabilidades_suman_cien():
    prob_esp, prob_arg, _, _ = run_tactical_simulation(xg_esp=1.3, xg_arg=1.3, num_simulations=20_000)
    assert abs((prob_esp + prob_arg) - 100.0) < 0.5


def test_run_tactical_simulation_favorece_al_de_mayor_xg():
    prob_esp, prob_arg, _, _ = run_tactical_simulation(xg_esp=2.5, xg_arg=0.8, num_simulations=20_000)
    assert prob_esp > prob_arg


def test_tarjetas_rojas_penalizan_al_equipo_reducido():
    _, _, xg_sin_roja, _ = run_tactical_simulation(xg_esp=1.3, xg_arg=1.3, red_cards_esp=0, num_simulations=1_000)
    _, _, xg_con_roja, _ = run_tactical_simulation(xg_esp=1.3, xg_arg=1.3, red_cards_esp=1, num_simulations=1_000)
    assert xg_con_roja < xg_sin_roja


def test_squads_tienen_26_convocados():
    assert len(JUGADORES_ESPAÑA) == 26
    assert len(JUGADORES_ARGENTINA) == 26


def test_xi_sugerido_tiene_11_jugadores_convocados():
    assert len(XI_SUGERIDO_ESP) == 11
    assert len(XI_SUGERIDO_ARG) == 11
    assert all(nombre in JUGADORES_ESPAÑA for nombre in XI_SUGERIDO_ESP)
    assert all(nombre in JUGADORES_ARGENTINA for nombre in XI_SUGERIDO_ARG)
