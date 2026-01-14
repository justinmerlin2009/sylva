# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sylva is an environmental monitoring drone simulation system developed for the Conrad Challenge 2026 by the TamAir team. It demonstrates autonomous drone surveys for detecting and mapping pollution across US locations (Stinson Beach CA, NASA Space Center TX, Lake Erie OH).

## Git Commit Attribution

All commits to this repository should be attributed to:
- **Author:** Justin Merlin <justin.merlin2009@gmail.com>
- Always include: `Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>`

## Development Commands

### Run Everything (Recommended)
```bash
./run.sh  # Starts API (port 8000) + Dashboard (port 3000)
```

### Run Components Separately

**API Server:**
```bash
source venv/bin/activate
python -m uvicorn api.main:app --reload --port 8000
```

**Dashboard:**
```bash
cd dashboard && npm run dev
```

**Build Dashboard:**
```bash
cd dashboard && npm run build
```

**Regenerate Simulation Data:**
```bash
source venv/bin/activate
python -m simulation.data_generator
```

## Architecture

### Backend (Python/FastAPI)
- `api/main.py` - FastAPI server with REST endpoints and WebSocket support for live demos
- `api/models.py` - Pydantic response models
- `simulation/` - Data generation engine:
  - `config.py` - Survey locations, drone specs, waypoint definitions
  - `flight_paths.py` - Flight path generation
  - `trash_detector.py` - Trash detection simulation with 8 waste categories
  - `data_generator.py` - Main entry point for regenerating data
  - `annual_generator.py` - Annual analytics data

### Frontend (React/Vite)
- `dashboard/src/App.jsx` - Simulation page with map, live demo, showcase mode
- `dashboard/src/pages/` - Page components:
  - `Home.jsx` - Landing page with project overview, sensor fusion chart, team info
  - `Technology.jsx` - Technical specs, 3D drone viewer, sensor payload details
  - `DetectionDemo.jsx` - TACO + SAM 2 detection pipeline demo with video
- `dashboard/src/components/`:
  - `Map.jsx` - Leaflet map with flight paths, detection markers, heatmap overlay
  - `LiveDemo.jsx` - Real-time drone animation controls (default 0.5x speed)
  - `DetectionPanel.jsx` - AI detection display with confidence scores
  - `Sidebar.jsx` - Filters and statistics
  - `PathDrawer.jsx` - Custom survey path drawing
  - `AnnualData.jsx` - Annual analytics visualization
  - `DroneViewer3D.jsx` - Three.js 3D drone viewer
- `dashboard/src/utils/`:
  - `SimulationPreloader.js` - Background preloading for faster simulation load

### Performance Optimizations

**Simulation Preloading (`SimulationPreloader.js`):**
- When users visit the Home page, simulation data preloads in the background
- Preloads API data: locations, detections, heatmap, flights, categories, stats
- Preloads map tiles for ALL 3 locations at zoom levels 12-16:
  - Stinson Beach (37.8985, -122.6352)
  - NASA Space Center (29.5589, -95.0899)
  - Lake Erie (41.5, -81.5)
- Starts 2 seconds after Home page renders
- Uses preconnect hints in `index.html` for CARTO and ESRI tile CDNs

**Showcase Demo Animation Settings (`App.jsx`):**
- `DEMO_SPEED = 3.5` (3.5x real-time for smooth animation)
- Per-location durations based on frame counts:
  - `STINSON_DURATION = 15000` (847 frames, ~12s at 3.5x)
  - `NASA_DURATION = 35000` (2234 frames, ~32s at 3.5x)
- `FLY_DURATION = 2500` (transition between locations)
- Total showcase: ~55 seconds

**Map Camera Following (`Map.jsx`):**
- `panTo duration = 0.08s` (matches frame rate at 3.5x speed)
- Frames arrive every ~14ms at 3.5x speed (50ms base / 3.5)
- Short duration prevents animation stacking/jerkiness

**Manual Demo (`LiveDemo.jsx`):**
- Default speed: 0.5x (Recommended - Smooth)
- Speed options: 0.5x, 1x, 2x, 3x

### Flight Path Frame Counts
Important for calculating demo durations:
- Stinson Beach: 847 frames
- NASA Space Center: 2,234 frames
- Lake Erie: 28,581 frames (very long path)

Formula: `duration = frames * 0.05 / speed`

### Data Flow
1. `simulation/` generates GeoJSON files in `data/` (flights, detections, heatmaps, stats)
2. `api/` serves this data via REST endpoints
3. `dashboard/` fetches from API and renders on Leaflet map
4. WebSocket endpoints stream live demo animations at 50ms base interval

### Data Directory
- `data/flights/` - Flight path GeoJSON per location + `{location}_animation.json`
- `data/detections/` - Detection GeoJSON per location + aggregated
- `data/annual/` - Monthly/yearly analytics
- `data/geography/` - Water bodies, roads, shorelines
- `data/summary/` - Statistics JSON

## Key Terminology

- **Sylva Hybrid Camera** - The multi-sensor fusion system (RGB + Hyperspectral + LiDAR)
- **Sensor Fusion Accuracy** - Chart showing ~90% accuracy with full fusion vs ~70% single sensor
- Labels should use: "RGB only", "Hyper-spectral only", "Sylva Hybrid Camera"

## Key Patterns

- API proxy configured in `vite.config.js` - `/api` and `/ws` routes proxy to backend
- All geographic data uses GeoJSON format (RFC 7946)
- Detection categories: plastic_bottle, food_packaging, tires, metal_debris, construction_waste, organic_waste, glass, textile_fabric
- Priority levels: critical, high, medium, low
- Live demo uses WebSocket at `/ws/live`
- Showcase mode runs automated demo across 2 locations (Stinson Beach, NASA Space Center)

## Deployment

Production deployed on Render:
- Dashboard: Static site from `dashboard/dist/` at `https://sylva-dashboard.onrender.com`
- API: Separate Python service at `https://sylva-api.onrender.com`
- API docs: `https://sylva-api.onrender.com/docs`

## TODO - Next Session

1. **Add picture of all plane prototypes** to website
2. **Review AI fusion pipeline SVG** - located at `dashboard/public/images/ai-fusion-pipeline.svg`
   - Shows: 3 sensor inputs (RGB, Multispectral, LiDAR) → SYLVA AI model → 4 outputs (Detection, Triangulation, Priority, Heatmap)
   - After approval, integrate into website as a new section
3. **Integrate AI diagram into website** after review approval

## Recent Changes (Jan 2026)

- Updated terminology: "Sylva Full Fusion" → "Sylva Hybrid Camera"
- Added background preloading system for faster simulation load (all 3 locations)
- Fixed NASA demo completing full flight path (was cutting off at 45%)
- Optimized demo animation:
  - Speed: 6x → 2.5x → 3.5x (current)
  - Per-location durations instead of fixed 20s
  - panTo duration: 0.3s → 0.08s for smoother camera
- Manual demo default speed: 1x → 0.5x (smoother)
- Fixed copyright year to 2026
- Updated system diagram image
- Fixed text: "actionable intelligence" → "actionable intelligence from the air"
- Updated Fixed-Wing Surveillance description with hybrid camera details
- Added API/GIS integration mention to Data Analytics section
