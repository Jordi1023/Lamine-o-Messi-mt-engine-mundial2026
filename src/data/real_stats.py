"""
real_stats.py
-------------
Datos reales del camino a la final del Mundial 2026, compilados a mano
el 15 de julio de 2026 (día previo a la publicación de esta versión del
simulador) desde fuentes públicas: FIFA.com, Futbolred, CNN en Español,
ESPN y Yahoo Deportes.

IMPORTANTE: esto NO es un feed de datos en vivo. Es un snapshot fijo.
Si se usa después de jugarse la final del domingo 19 de julio, hay que
actualizar estos valores a mano con el resultado real.
"""

RESUMEN_REAL = {
    "España": {
        "PJ": 7, "V": 6, "E": 1, "D": 0, "GF": 13, "GC": 1,
        "camino": [
            "Cabo Verde 0-0", "Arabia Saudí 4-0", "Uruguay 1-0",
            "Austria 3-0 (16avos)", "Portugal 1-0 (8vos)",
            "Bélgica 2-1 (4tos)", "Francia 2-0 (semis)",
        ],
    },
    "Argentina": {
        "PJ": 7, "V": 7, "E": 0, "D": 0, "GF": 19, "GC": 7,
        "camino": [
            "Argelia 3-0", "Austria 2-0", "Jordania 3-1",
            "Cabo Verde 3-2 (16avos, prórroga)", "Egipto 3-2 (8vos)",
            "Suiza 3-1 (4tos, prórroga)", "Inglaterra 2-1 (semis, remontada)",
        ],
    },
}

GOLEADORES_REAL_ESP = {
    "Mikel Oyarzabal": 5,
    "Pedro Porro": 2,
    "Mikel Merino": 2,
    "Fabián Ruiz": 1,
}

GOLEADORES_REAL_ARG = {
    "Lionel Messi": 8,
    "Lautaro Martínez": 3,
    "Enzo Fernández": 2,
    "Julián Álvarez": 1,
    "Alexis Mac Allister": 1,
    "Giovani Lo Celso": 1,
    "Lisandro Martínez": 1,
    "Cristian Romero": 1,
}

FUENTES = [
    "FIFA.com",
    "Futbolred",
    "CNN en Español",
    "ESPN",
    "Yahoo Deportes",
]

FECHA_ACTUALIZACION = "15 de julio de 2026"
