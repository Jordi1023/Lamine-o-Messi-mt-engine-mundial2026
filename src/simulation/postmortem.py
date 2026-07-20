"""
postmortem.py
--------------
Herramientas de análisis retrospectivo ("post-mortem") para comparar la
predicción pre-partido del modelo contra el resultado real.

Dos piezas, ambas matemáticamente correctas para un modelo aditivo simple
Ojo: No es SHAP.

1. `player_contributions`: descompone el xG final en la contribución
   individual de cada titular. Para un modelo lineal/aditivo como este,
   el "valor SHAP" de cada variable es exactamente igual a su coeficiente
   -> no hace falta la librería shap, el desglose ya es la explicación
   completa y exacta.

2. `brier_score`: mide qué tan calibrada estuvo la probabilidad predicha
   contra el resultado real (binario). Es la métrica correcta para
   evaluar una predicción probabilística con una sola observación (n=1)
   -> a diferencia de MAE/RMSE o una matriz de confusión, que no tienen
   significado estadístico con un solo partido.
"""

from typing import Dict, List, Tuple

# Referencia para interpretar el Brier Score (rango 0=perfecto, 1=peor posible)
BRIER_REFERENCIA = {
    "perfecto": 0.0,
    "azar (50/50)": 0.25,
    "peor_posible": 1.0,
}


def player_contributions(jugadores: Dict[str, dict], titulares: List[str], clave: str = "of") -> List[Tuple[str, float]]:
    """
    Devuelve [(nombre, valor)] de cada titular para el coeficiente dado
    ('of' o 'def'), ordenado de mayor a menor contribución.
    """
    contribuciones = [(nombre, jugadores[nombre][clave]) for nombre in titulares]
    return sorted(contribuciones, key=lambda par: par[1], reverse=True)


def brier_score(prob_predicha_pct: float, ocurrio: bool) -> float:
    """
    Brier Score = (probabilidad predicha - resultado real)^2

    - probabilidad predicha: en escala 0-1 (se recibe en % y se normaliza acá)
    - resultado real: 1 si el evento ocurrió, 0 si no

    0.0 = predicción perfecta. 0.25 = equivalente a tirar una moneda (50/50).
    1.0 = predicción perfectamente equivocada.
    """
    prob = prob_predicha_pct / 100.0
    resultado = 1.0 if ocurrio else 0.0
    return round((prob - resultado) ** 2, 4)


def interpretar_brier(score: float) -> str:
    """Devuelve una interpretación honesta del Brier Score obtenido."""
    if score <= 0.05:
        return "Predicción muy bien calibrada — mucho más confiada de lo necesario y acertó."
    if score < 0.25:
        return "Mejor que adivinar al azar, pero sin gran margen de confianza."
    if abs(score - 0.25) < 0.01:
        return "Prácticamente equivalente a una moneda al aire (50/50), aunque acertó la dirección."
    return "Peor que adivinar al azar en esta observación — la dirección o la confianza no ayudaron."
