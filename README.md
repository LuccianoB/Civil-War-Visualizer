# Civil War Visualizer

 [Github Pages Link](luccianob.github.io/Civil-War-Visualizer/)

An interactive historical map that shows major American Civil War battles over time.

This project combines a Python data pipeline (Wikipedia + Wikidata enrichment) with a Svelte + MapLibre frontend to let users scrub through war dates and see which battles were active on any given day.

## Features

- Interactive map built with MapLibre
- Timeline-driven filtering of battles by `start_date` and `end_date`
- Marker color by battle outcome:
  - Union: blue
  - Confederate: gray
  - Draw: yellow
- Battle popups with key details (name, victor, date, location)
- Offline data pipeline to produce enriched, frontend-ready JSON

## Tech Stack

### Frontend

- Svelte 5
- Vite
- MapLibre GL
- svelte-maplibre-gl
- Tailwind CSS (v4 tooling in place)

### Data Pipeline

- Python
- requests
- BeautifulSoup4
- Wikidata API + SPARQL endpoint

## Project Structure

```text
Civil War Visualizer/
├── data-pipeline/
│   ├── requirements.txt
│   ├── raw_data/
│   │   └── baseline_battles.json
│   ├── processed_data/
│   │   └── enriched_battles.json
│   └── scripts/
│       ├── scrape_battles.py
│       ├── enrich_battles.py
│       ├── wikidata_queries.py
│       ├── wikipedia_battles.py
│       ├── debug_partials.py
│       └── test_enrich_single_battle.py
├── frontend/
│   ├── package.json
│   ├── index.html
│   └── src/
│       ├── App.svelte
│       └── lib/
│           ├── components/
│           ├── data/
│           │   └── enriched_battles.json
│           ├── store.js
│           └── utils/
└── development-notes/
```

## How It Works

### 1) Build baseline battle list from Wikipedia

`scrape_battles.py`:

- fetches the Wikipedia list of Civil War battles
- parses the CWSAC table
- cleans text fields and date ranges
- filters to high-significance classes (`A` and `B`)
- writes `data-pipeline/raw_data/baseline_battles.json`

### 2) Enrich each battle with Wikidata

`enrich_battles.py`:

- attempts to resolve a Wikidata Q-ID per battle
- fetches coordinates via SPARQL (`P625`)
- marks records as complete/partial
- writes `data-pipeline/processed_data/enriched_battles.json`

### 3) Visualize in the frontend

The Svelte app loads `frontend/src/lib/data/enriched_battles.json`, then filters battles reactively using:

- `battle.start_date <= currentDate`
- `battle.end_date >= currentDate`

Only matching battles render as map markers.

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm

### A) Data Pipeline

```bash
cd data-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Step 1: scrape + baseline filter
python scripts/scrape_battles.py

# Step 2: Wikidata enrichment
python scripts/enrich_battles.py
```

Useful debugging scripts:

```bash
# Test enrichment logic on one known battle
python scripts/test_enrich_single_battle.py

# Inspect incomplete or partial records
python scripts/debug_partials.py
```

### B) Sync data into frontend

```bash
cp data-pipeline/processed_data/enriched_battles.json frontend/src/lib/data/enriched_battles.json
```

### C) Run frontend

```bash
cd frontend
npm install
npm run dev
```

Then open the local Vite URL (usually `http://localhost:5173`).

## Frontend Commands

From `frontend/`:

```bash
npm run dev      # start local dev server
npm run build    # production build
npm run preview  # preview production build
npm run lint     # lint source files
```

## Data Schema (Enriched Battle)

Representative fields in `enriched_battles.json`:

```json
{
  "Battle": "Battle of Gettysburg",
  "Date": "July 1-3, 1863",
  "State": "Pennsylvania",
  "CWSAC": "A",
  "Wikipedia_Link": "Battle_of_Gettysburg",
  "start_date": "1863-07-01",
  "end_date": "1863-07-03",
  "Victory": "Union",
  "qid": "Q8676",
  "wikidata_coordinates": "Point(-77.235 39.830)",
  "data_complete": true,
  "data_source": "wikipedia_and_wikidata"
}
```

## Known Limitations

- Some battles do not resolve to a reliable Wikidata entry
- Some records are partial (for example, Q-ID found but no coordinates)
- Historical naming inconsistencies can affect matching accuracy

## Roadmap

### Next Up

- Make the site mobile friendly across common phone and tablet breakpoints
- Add marker types to distinguish land battles, naval battles, and sieges
- Add richer battle metadata in popups and data model: troop counts, casualty counts, commanders, and parent campaigns
- Add playback controls (play/pause + variable speed) wired to timeline progression

### Mid-Term

- Add advanced filtering options (for example: by campaign and commander)
- Add advanced icon scaling options (for example: by CWSAC ranking, troop counts, or casualty counts)
- Add geographically anchored non-battle events (for example: riots, major speeches, key law passages, diplomatic incidents)
- Extend the timeline to include pre-war escalation events

### Long-Term

- Add an optional period-appropriate historical map layer
- Add richer statistical summaries and comparative views
- Add battle detail map overlays on zoom for key engagements, including overlays already available through Wikidata where possible

### Platform Vision

- Refactor the project into reusable, modular timeline-map components so other conflicts or event timelines can be added with minimal code changes

## Notes for Contributors

- Keep data pipeline outputs deterministic and JSON-formatted
- Avoid hardcoding paths outside `data-pipeline/` and `frontend/`
- If you change enrichment fields, update frontend marker/popup logic accordingly

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Data Attribution

- **Battle metadata & coordinates** sourced from Wikidata ([CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/))
- **Battle list & baseline data** sourced from Wikipedia's [List of American Civil War battles](https://en.wikipedia.org/wiki/List_of_American_Civil_War_battles)
