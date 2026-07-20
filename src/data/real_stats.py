"""

Datos reales del Mundial 2026, incluyendo el resultado final ya jugado
(España campeona, 19 de julio de 2026), compilados a mano desde fuentes
públicas: FIFA.com, CNN en Español, ESPN y Yahoo
Deportes. Última actualización: 19 de julio de 2026, post-final.

IMPORTANTE: esto NO es un feed de datos en vivo. Es un snapshot fijo.
"""

RESULTADO_FINAL = {
    "jugado": True,
    "marcador": "España 1-0 Argentina (tras prórroga)",
    "campeon": "España",
    "goleador": "Ferrán Torres (tiempo extra)",
    "detalle": "Argentina terminó el partido con 10 jugadores por la expulsión de Enzo Fernández.",
    "fecha": "19 de julio de 2026",
}

RESUMEN_REAL = {
    "España": {
        "PJ": 8, "V": 7, "E": 1, "D": 0, "GF": 14, "GC": 1,
        "camino": [
            "Cabo Verde 0-0", "Arabia Saudí 4-0", "Uruguay 1-0",
            "Austria 3-0 (16avos)", "Portugal 1-0 (8vos)",
            "Bélgica 2-1 (4tos)", "Francia 2-0 (semis)",
            "Argentina 1-0 (FINAL, prórroga) 🏆",
        ],
    },
    "Argentina": {
        "PJ": 8, "V": 7, "E": 0, "D": 1, "GF": 19, "GC": 8,
        "camino": [
            "Argelia 3-0", "Austria 2-0", "Jordania 3-1",
            "Cabo Verde 3-2 (16avos, prórroga)", "Egipto 3-2 (8vos)",
            "Suiza 3-1 (4tos, prórroga)", "Inglaterra 2-1 (semis, remontada)",
            "España 0-1 (FINAL, prórroga)",
        ],
    },
}

GOLEADORES_REAL_ESP = {
    "Mikel Oyarzabal": 5,
    "Pedro Porro": 2,
    "Mikel Merino": 2,
    "Fabián Ruiz": 1,
    "Ferrán Torres": 1,  # gol del título en la final
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
    "Depor",
    "ESPN",
    "Yahoo Deportes",
]

FECHA_ACTUALIZACION = "19 de julio de 2026 (post-final)"

