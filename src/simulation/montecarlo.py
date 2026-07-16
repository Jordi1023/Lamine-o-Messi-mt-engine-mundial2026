"""
montecarlo.py
-------------
Simulación de Monte Carlo del resultado del partido, usando una
distribución de Poisson para el número de goles de cada equipo.

Por qué Poisson y no una cadena de Markov:
Los goles en un partido de fútbol son eventos discretos, relativamente
poco frecuentes y aproximadamente independientes entre sí dentro del
mismo partido -> Poisson es el modelo estándar en analítica deportiva
para este tipo de conteo (es la base de modelos públicos como el de
Opta/FiveThirtyEight). Una cadena de Markov tendría sentido si se
modelaran transiciones de estado minuto a minuto (posesión -> tiro ->
gol), pero eso no es lo que hace este simulador.

El "ajuste bayesiano" que se aplica en la capa de UI cuando se rompe el
marcador es, honestamente, una heurística multiplicativa simple —no una
actualización bayesiana formal con prior/posterior.
"""

from typing import Tuple

import numpy as np


def run_tactical_simulation(
    xg_esp: float,
    xg_arg: float,
    red_cards_esp: int = 0,
    red_cards_arg: int = 0,
    num_simulations: int = 10_000,
) -> Tuple[float, float, float, float]:
    """
    Corre `num_simulations` partidos aleatorios con goles ~ Poisson(xG)
    y devuelve las probabilidades de victoria de cada selección.

    Retorna (prob_esp, prob_arg, xg_esp_final, xg_arg_final).
    """
    xg_esp_final = max(0.2, xg_esp * (1 - 0.20 * red_cards_esp))
    xg_arg_final = max(0.2, xg_arg * (1 - 0.20 * red_cards_arg))

    # Si el rival tiene expulsados, el propio ataque se beneficia del espacio libre
    if red_cards_esp > 0:
        xg_arg_final *= (1 + 0.12 * red_cards_esp)
    if red_cards_arg > 0:
        xg_esp_final *= (1 + 0.12 * red_cards_arg)

    goals_esp = np.random.poisson(xg_esp_final, num_simulations)
    goals_arg = np.random.poisson(xg_arg_final, num_simulations)

    esp_wins = goals_esp > goals_arg
    arg_wins = goals_arg > goals_esp
    draws = goals_esp == goals_arg

    # Resolución estocástica de empates (penales / muerte súbita, 50/50)
    tie_breaker_esp = np.random.choice([True, False], size=num_simulations, p=[0.5, 0.5])

    final_esp_wins = esp_wins | (draws & tie_breaker_esp)
    final_arg_wins = arg_wins | (draws & ~tie_breaker_esp)

    prob_esp = (np.sum(final_esp_wins) / num_simulations) * 100
    prob_arg = (np.sum(final_arg_wins) / num_simulations) * 100

    return round(float(prob_esp), 2), round(float(prob_arg), 2), xg_esp_final, xg_arg_final
