"""
Tests del módulo de análisis post-mortem (contribuciones y Brier Score).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data.squads import JUGADORES_ESPAÑA, XI_SUGERIDO_ESP
from src.simulation.postmortem import brier_score, interpretar_brier, player_contributions


def test_player_contributions_devuelve_11_jugadores_ordenados():
    contribuciones = player_contributions(JUGADORES_ESPAÑA, XI_SUGERIDO_ESP, clave="of")
    assert len(contribuciones) == 11
    valores = [v for _, v in contribuciones]
    assert valores == sorted(valores, reverse=True)


def test_player_contributions_suma_igual_al_aporte_total():
    contribuciones = player_contributions(JUGADORES_ESPAÑA, XI_SUGERIDO_ESP, clave="of")
    suma_manual = sum(JUGADORES_ESPAÑA[nombre]["of"] for nombre in XI_SUGERIDO_ESP)
    suma_contribuciones = sum(v for _, v in contribuciones)
    assert abs(suma_manual - suma_contribuciones) < 1e-9


def test_brier_score_prediccion_perfecta_es_cero():
    assert brier_score(100.0, ocurrio=True) == 0.0
    assert brier_score(0.0, ocurrio=False) == 0.0


def test_brier_score_prediccion_totalmente_equivocada_es_uno():
    assert brier_score(0.0, ocurrio=True) == 1.0
    assert brier_score(100.0, ocurrio=False) == 1.0


def test_brier_score_moneda_al_aire_es_cuarto():
    assert brier_score(50.0, ocurrio=True) == 0.25
    assert brier_score(50.0, ocurrio=False) == 0.25


def test_interpretar_brier_devuelve_texto_para_cada_rango():
    assert isinstance(interpretar_brier(0.01), str)
    assert isinstance(interpretar_brier(0.25), str)
    assert isinstance(interpretar_brier(0.9), str)
