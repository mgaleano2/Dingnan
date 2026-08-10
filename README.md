# Dingnan United · Análisis (China League One)
Asistencia externa al cuerpo tecnico del Dingnan United. PF: Emanuel Bale - Transfermarkt: https://www.transfermarkt.com/emanuel-bale/profil/trainer/155367
Scraper + análisis del **Dingnan United** en la **China League One**, construido con datos de la API de [Sofascore](https://www.sofascore.com/).

```text
analisis.py  →  scrape partido a partido (stats por jugador)
scrape_liga.py  →  re-scrape resumible de toda la liga
consolidado.py  →  carga, limpieza y reportes (per-90, tablas, markdown)
```

### `analisis.py`
Entrada del scraping: define los partidos de Dingnan y guarda las stats por jugador de cada uno en `data/stats_{match_id}.csv`.
Voy introduciendo manualmente cada ID, en el codigo.

### `scrape_liga.py`
Scraper **resumible y tolerante a fallos**:
- Omite los partidos cuyo CSV ya existe (idempotente, se puede cortar y retomar).
- Cada partido envuelto en `try/except`: ante un error registra `ERROR <mid>: <tipo>: <mensaje>` y sigue con el siguiente.
- `time.sleep(1)` entre partidos para no saturar la API.
- Utilizacion de OpenCode + Claude Code, para mejoras del codigo.
### `consolidado.py`
Cálculo del análisis. Flujo `cargar → limpiar → tabla_partidos → tabla_jugadores → reporte → reporte_md`:

- Agregaciones con `groupby().agg()` (named aggregations) por partido y por jugador.
- Métricas normalizadas **por 90 minutos** con guarda de división por cero.
- Utilizacion de OpenCode + Claude Code, para mejoras del codigo.

## Salidas (`data/`)

| Archivo | Contenido |
|---|---|
| `stats_{match_id}.csv` | Stats por jugador de cada partido |
| `tabla_partidos.csv` | Resultados y datos por partido |
| `tabla_jugadores.csv` | Agregados por jugador (PJ, min, goles, rating, per-90) |
| `reporte.csv` | Tabla resumen |
| `reporte.md` | Reporte en Markdown listo para leer/compartir |

## Cómo correrlo

```bash
# Python 3.10+ con pandas y ScraperFC instalados
python analisis.py        # scrapea los partidos definidos
python scrape_liga.py     # opcional: completa partidos faltantes (resumible)
python consolidado.py     # genera tablas y reporte
```

## Dependencia

Se usa la librería [ScraperFC](https://github.com/oseymour/ScraperFC) (paquete Python para scraping de datos de fútbol); este proyecto se desarrolló sobre un **fork propio**: [mgaleano2/ScraperFC](https://github.com/mgaleano2/ScraperFC).

