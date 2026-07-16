"""
xg_model.py
-----------
Cálculo del xG (goles esperados) de cada selección a partir de los
titulares elegidos, usando un modelo aditivo de "Sinergia Colectiva":

    xG_equipo = xg_base + suma(aporte_ofensivo_propio)
                        - 0.8 * suma(aporte_defensivo_rival)

Después se aplica un ajuste multiplicativo por condición climática.
"""

from typing import Dict, List, Tuple

XG_BASE = 0.8
FACTOR_DEF_RIVAL = 0.8
XG_MINIMO = 0.4

AJUSTE_CLIMA = {
    "Pesada (Lluvia)": {"España": 0.86, "Argentina": 0.91},
    "Normal": {"España": 1.00, "Argentina": 1.00},
    "Rápida (Seca)": {"España": 1.05, "Argentina": 1.02},
}


def _suma_aporte(jugadores: Dict[str, dict], titulares: List[str], clave: str) -> float:
    """Suma el coeficiente `clave` ('of' o 'def') de una lista de titulares."""
    return sum(jugadores[nombre][clave] for nombre in titulares)


def compute_match_xg(
    jugadores_esp: Dict[str, dict],
    jugadores_arg: Dict[str, dict],
    titulares_esp: List[str],
    titulares_arg: List[str],
    clima: str,
) -> Tuple[float, float]:
    """
    Calcula el xG esperado de España y Argentina según los titulares
    seleccionados y la condición climática.

    Retorna (xg_esp, xg_arg).
    """
    aporte_of_esp = _suma_aporte(jugadores_esp, titulares_esp, "of")
    aporte_def_esp = _suma_aporte(jugadores_esp, titulares_esp, "def")
    aporte_of_arg = _suma_aporte(jugadores_arg, titulares_arg, "of")
    aporte_def_arg = _suma_aporte(jugadores_arg, titulares_arg, "def")

    xg_esp = max(XG_MINIMO, XG_BASE + aporte_of_esp - (aporte_def_arg * FACTOR_DEF_RIVAL))
    xg_arg = max(XG_MINIMO, XG_BASE + aporte_of_arg - (aporte_def_esp * FACTOR_DEF_RIVAL))

    ajuste = AJUSTE_CLIMA.get(clima, AJUSTE_CLIMA["Normal"])
    xg_esp *= ajuste["España"]
    xg_arg *= ajuste["Argentina"]

    return xg_esp, xg_arg
