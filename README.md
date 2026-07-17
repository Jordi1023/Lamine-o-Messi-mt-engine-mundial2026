# ⚡ MT-Engine — Simulador Táctico Mundial 2026

Simulador interactivo de la final del Mundial 2026 (**España vs Argentina**,
domingo 19 de julio, MetLife Stadium) construido con Streamlit. Permite armar
el once titular de cada selección **dentro de su convocatoria oficial de 26**,
y proyecta la probabilidad de victoria con una simulación de Monte Carlo.

## 🎯 Qué hace

- Arma tu XI titular eligiendo entre los **26 convocados reales** de cada
  selección (no jugadores genéricos ni retirados).
- Los coeficientes ofensivos/defensivos de cada jugador están calibrados con
  su **rendimiento real en este Mundial** (goles anotados, récord defensivo
  del equipo) — ver `src/data/real_stats.py`.
- Simula el resultado 10,000 veces con una distribución de Poisson (Monte
  Carlo) y devuelve la probabilidad de victoria de cada selección.
- Permite ajustar clima, tarjetas rojas y quién abre el marcador para ver
  cómo cambian las probabilidades en vivo.

## 🧠 Modelo estadístico 

- **Poisson + Monte Carlo**, no cadenas de Markov: los goles son eventos
  discretos y poco frecuentes, así que Poisson es el estándar en analítica
  deportiva para este tipo de conteo.
- El "ajuste in-play" cuando se rompe el marcador es una heurística
  multiplicativa simple, no una actualización bayesiana formal.
- Los coeficientes por jugador combinan datos reales (goles del torneo) con
  criterio experto sobre el rol táctico, porque no existe una métrica
  pública desagregada por jugador con la misma calidad que los goles.
- **No es un feed de datos en vivo.** Los datos reales del torneo están
  congelados al 15 de julio de 2026 (fuentes: FIFA.com, Futbolred, CNN en
  Español, ESPN, Yahoo Deportes). Si usas esto después de la final, actualiza
  `src/data/real_stats.py` a mano con el resultado real.

Detalle completo dentro de la app, en el expander "Ver sustento
metodológico".

## 🗂️ Estructura del proyecto

```
mt-engine-mundial2026/
├── app.py                      # Punto de entrada — orquesta todo
├── requirements.txt
├── .streamlit/
│   └── config.toml             # Tema base de Streamlit
├── src/
│   ├── data/
│   │   ├── squads.py           # Convocatoria oficial (26 + 26) y coeficientes
│   │   └── real_stats.py       # Estadísticas reales del camino a la final
│   ├── simulation/
│   │   ├── xg_model.py         # Cálculo de xG según titulares
│   │   └── montecarlo.py       # Simulación Monte Carlo (Poisson)
│   └── ui/
│       ├── theme.py            # CSS del tema oscuro
│       └── components.py       # Componentes de renderizado (header, cards, chart...)
└── tests/
    └── test_simulation.py      # Tests unitarios de la capa de simulación
```

La separación **datos / lógica / UI** permite testear `src/simulation` con
`pytest` sin necesidad de levantar Streamlit.

##  Cómo correrlo

```bash
# 1. Clonar el repo
git clone <tu-repo>
cd mt-engine-mundial2026

# 2. Crear entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Correr la app
streamlit run app.py
```

Esto te da una URL tipo `http://localhost:8501`, que **solo funciona en tu
propia PC**. Para compartirla con cualquiera, despliega en
[Streamlit Community Cloud](https://share.streamlit.io) conectando este repo.

##  Tests

```bash
pip install pytest
pytest tests/ -v
```


