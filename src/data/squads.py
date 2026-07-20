"""
squads.py
---------
Convocatoria oficial de 26 jugadores por selección para la final del
Mundial 2026 (España vs Argentina, domingo 19 de julio, MetLife Stadium).

Cada jugador tiene dos coeficientes:
    of  -> aporte ofensivo estimado (impacto en el xG propio)
    def -> aporte defensivo estimado (impacto en el xG que recibe el equipo)

Los coeficientes están calibrados con el rendimiento REAL de cada jugador
en este Mundial (ver src/data/real_stats.py para el detalle de goles y
resultados que sustentan estos números). No son valores genéricos de
"reputación" del jugador.
"""

JUGADORES_ESPAÑA = {
    # Porteros
    "Unai Simón":        {"of": 0.00, "def": 0.15, "pos": "Portero"},
    "David Raya":         {"of": 0.00, "def": 0.14, "pos": "Portero"},
    "Joan García":        {"of": 0.00, "def": 0.12, "pos": "Portero"},
    # Defensas — récord real: mejor defensa del torneo (1 gol recibido en 7 partidos)
    "Marc Cucurella":     {"of": 0.05, "def": 0.17, "pos": "Defensa"},
    "Alejandro Grimaldo": {"of": 0.08, "def": 0.12, "pos": "Defensa"},
    "Marc Pubill":        {"of": 0.06, "def": 0.13, "pos": "Defensa"},
    "Eric García":        {"of": 0.03, "def": 0.18, "pos": "Defensa"},
    "Aymeric Laporte":    {"of": 0.03, "def": 0.23, "pos": "Defensa"},
    "Pau Cubarsí":        {"of": 0.02, "def": 0.22, "pos": "Defensa"},
    "Marcos Llorente":    {"of": 0.10, "def": 0.13, "pos": "Defensa"},
    "Pedro Porro":        {"of": 0.16, "def": 0.11, "pos": "Defensa"},  # 2 goles 
    # Centrocampistas
    "Pedri":              {"of": 0.20, "def": 0.06, "pos": "Mediocampista"},
    "Fabián Ruiz":        {"of": 0.16, "def": 0.09, "pos": "Mediocampista"},  # 1 gol 
    "Martín Zubimendi":   {"of": 0.08, "def": 0.22, "pos": "Mediocampista"},
    "Gavi":               {"of": 0.16, "def": 0.10, "pos": "Mediocampista"},
    "Rodri Hernández":    {"of": 0.12, "def": 0.25, "pos": "Mediocampista"},
    "Mikel Merino":       {"of": 0.21, "def": 0.12, "pos": "Mediocampista"},  # 2 goles 
    "Álex Baena":         {"of": 0.17, "def": 0.04, "pos": "Mediocampista"},
    # Delanteros
    "Mikel Oyarzabal":    {"of": 0.34, "def": 0.02, "pos": "Delantero"},  # 5 goles 
    "Dani Olmo":          {"of": 0.23, "def": 0.03, "pos": "Delantero"},
    "Nico Williams":      {"of": 0.26, "def": 0.01, "pos": "Delantero"},
    "Yeremy Pino":        {"of": 0.18, "def": 0.00, "pos": "Delantero"},
    "Ferran Torres":      {"of": 0.19, "def": -0.01, "pos": "Delantero"},
    "Borja Iglesias":     {"of": 0.16, "def": -0.02, "pos": "Delantero"},
    "Víctor Muñoz":       {"of": 0.13, "def": 0.02, "pos": "Delantero"},
    "Lamine Yamal":       {"of": 0.35, "def": 0.00, "pos": "Delantero"},
}

JUGADORES_ARGENTINA = {
    # Porteros
    "Emiliano Martínez":  {"of": 0.00, "def": 0.16, "pos": "Portero"},
    "Gerónimo Rulli":     {"of": 0.00, "def": 0.12, "pos": "Portero"},
    "Juan Musso":         {"of": 0.00, "def": 0.11, "pos": "Portero"},
    # Defensas — récord real: 7 goles recibidos en 7 partidos (defensa más permeable que la de España)
    "Gonzalo Montiel":    {"of": 0.08, "def": 0.13, "pos": "Defensa"},
    "Nahuel Molina":      {"of": 0.09, "def": 0.10, "pos": "Defensa"},
    "Lisandro Martínez":  {"of": 0.06, "def": 0.20, "pos": "Defensa"},  # 1 gol 
    "Nicolás Otamendi":   {"of": 0.03, "def": 0.20, "pos": "Defensa"},
    "Leonardo Balerdi":   {"of": 0.02, "def": 0.15, "pos": "Defensa"},
    "Cristian Romero":    {"of": 0.06, "def": 0.23, "pos": "Defensa"},  # 1 gol 
    "Nicolás Tagliafico": {"of": 0.05, "def": 0.13, "pos": "Defensa"},
    "Facundo Medina":     {"of": 0.04, "def": 0.14, "pos": "Defensa"},
    # Mediocampistas
    "Leandro Paredes":    {"of": 0.10, "def": 0.17, "pos": "Mediocampista"},
    "Alexis Mac Allister": {"of": 0.19, "def": 0.13, "pos": "Mediocampista"},  # 1 gol 
    "Rodrigo De Paul":    {"of": 0.11, "def": 0.20, "pos": "Mediocampista"},
    "Giovani Lo Celso":   {"of": 0.19, "def": 0.06, "pos": "Mediocampista"},  # 1 gol 
    "Exequiel Palacios":  {"of": 0.13, "def": 0.15, "pos": "Mediocampista"},
    "Enzo Fernández":     {"of": 0.19, "def": 0.16, "pos": "Mediocampista"},  # 2 goles 
    "Valentín Barco":     {"of": 0.09, "def": 0.10, "pos": "Mediocampista"},
    # Delanteros
    "Lionel Messi":       {"of": 0.42, "def": -0.03, "pos": "Delantero"},  # 8 goles reales, mejor jugador de la historia
    "Julián Álvarez":     {"of": 0.20, "def": 0.05, "pos": "Delantero"},  # solo 1 gol 
    "Lautaro Martínez":   {"of": 0.27, "def": 0.02, "pos": "Delantero"},  # 3 goles 
    "Thiago Almada":      {"of": 0.17, "def": 0.01, "pos": "Delantero"},
    "Nicolás Paz":        {"of": 0.16, "def": 0.03, "pos": "Delantero"},
    "Nicolás González":   {"of": 0.18, "def": 0.06, "pos": "Delantero"},
    "Giuliano Simeone":   {"of": 0.14, "def": 0.05, "pos": "Delantero"},
    "José Manuel López":  {"of": 0.15, "def": -0.01, "pos": "Delantero"},
}

# XI titular sugerido por defecto (4-3-3), dentro de la convocatoria oficial
XI_SUGERIDO_ESP = [
    "Unai Simón", "Pedro Porro", "Aymeric Laporte", "Pau Cubarsí", "Marc Cucurella",
    "Rodri Hernández", "Dani Olmo", "Fabián Ruiz",
    "Lamine Yamal", "Mikel Oyarzabal", "Álex Baena",
]

XI_SUGERIDO_ARG = [
    "Emiliano Martínez", "Gonzalo Montiel", "Cristian Romero", "Lisandro Martínez", "Nicolás Tagliafico",
    "Rodrigo De Paul", "Enzo Fernández", "Alexis Mac Allister",
    "Lionel Messi", "Julián Álvarez", "Nicolás González",
]
