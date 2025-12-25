# SYLVA - Environmental Monitoring Drone Simulation

**TamAir Team - Conrad Challenge 2026**

Sylva is a system of autonomous fixed-wing drones designed to detect and map environmental pollution across highways, coastlines, and natural habitats. This repository contains a **realistic simulation** of the Sylva system for demonstration purposes.

## Overview

The simulation demonstrates:
- Drone flight path generation over real geographic locations
- AI-powered trash detection and classification
- Geo-tagged waste mapping with GPS coordinates
- Density analysis for identifying pollution hotspots
- Interactive dashboard for agency coordination

### Survey Locations

1. **Stinson Beach, California** - Coastal environment monitoring
2. **Route 66 (Needles, CA to Kingman, AZ)** - Historic highway corridor

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm

### Run the Simulation

```bash
# Clone or navigate to the project directory
cd sylva_simulation

# Run everything with a single command
./run.sh
```

This will:
1. Install Python dependencies
2. Install Node.js dependencies
3. Generate simulation data (if not already generated)
4. Start the API server (port 8000)
5. Start the dashboard (port 3000)

### Access the Dashboard

- **Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Root**: http://localhost:8000

## Features

### Dashboard Capabilities

- **Interactive Map**: View detections on a Leaflet map with OpenStreetMap tiles
- **Heatmap Overlay**: Toggle density visualization to identify hotspots
- **Flight Path Display**: View simulated drone flight paths
- **Live Demo Mode**: Watch an animated drone flight with real-time detections appearing
- **Filtering**: Filter by waste category, priority level
- **Statistics**: View detection counts, estimated weights, category breakdown

### Waste Categories Detected

| Category | Description |
|----------|-------------|
| Plastic Bottles | Water bottles, beverage containers |
| Food Packaging | Wrappers, containers, bags |
| Tires | Vehicle tires, tire fragments |
| Metal Debris | Cans, automotive parts, scrap |
| Construction Waste | Concrete, lumber, materials |
| Organic Waste | Food waste, vegetation |
| Glass | Bottles, broken glass |
| Textile/Fabric | Clothing, fabric scraps |

### Priority Levels

- **Critical**: Large debris, high-density areas, near sensitive ecosystems
- **High**: Significant accumulation, moderate environmental risk
- **Medium**: Standard detection, routine cleanup recommended
- **Low**: Minor debris, low environmental impact

## Project Structure

```
sylva_simulation/
├── run.sh                  # Single command launcher
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── simulation/            # Python simulation engine
│   ├── config.py          # Configuration and parameters
│   ├── flight_paths.py    # Flight path generation
│   ├── trash_detector.py  # Trash detection simulation
│   └── data_generator.py  # Main data generation
│
├── api/                   # FastAPI backend
│   ├── main.py           # API endpoints + WebSocket
│   └── models.py         # Pydantic data models
│
├── data/                  # Generated simulation data
│   ├── flights/          # Flight path GeoJSON files
│   ├── detections/       # Detection GeoJSON files
│   └── summary/          # Statistics and summaries
│
└── dashboard/             # React frontend
    ├── src/
    │   ├── App.jsx       # Main application
    │   ├── components/
    │   │   ├── Map.jsx      # Leaflet map
    │   │   ├── Sidebar.jsx  # Filters and stats
    │   │   └── LiveDemo.jsx # Animation controls
    │   └── styles.css    # Styling
    └── package.json
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/flights` | GET | List all flight missions |
| `/api/flights/{id}` | GET | Get flight path GeoJSON |
| `/api/detections` | GET | Get detections (with filters) |
| `/api/detections/geojson` | GET | Raw GeoJSON FeatureCollection |
| `/api/stats` | GET | Summary statistics |
| `/api/heatmap` | GET | Heatmap data points |
| `/api/clusters` | GET | High-density clusters |
| `/api/locations` | GET | Available survey locations |
| `/ws/live` | WebSocket | Live demo data stream |

### Query Parameters for `/api/detections`

- `location`: Filter by location ID
- `category`: Filter by waste category
- `priority`: Filter by priority level
- `min_confidence`: Minimum confidence threshold
- `limit`: Maximum results to return

## Technical Details

### Simulation Parameters

**Drone Specifications:**
- Fixed-wing design, 2.5m wingspan
- Survey altitude: 120-150m AGL
- Survey speed: 15-20 m/s
- Camera: 20MP RGB + multispectral

**Detection Algorithm:**
- Probabilistic detection based on environment type
- Poisson-distributed detection counts
- Confidence scores: 0.75-0.99
- Size and weight estimation

**Density Analysis:**
- Grid-based clustering (50m cells)
- Priority scoring based on density + weight + sensitivity

### Data Formats

All geographic data uses **GeoJSON** format (RFC 7946), compatible with:
- QGIS
- ArcGIS
- Mapbox
- Google Earth

## Development

### Running Components Separately

**API Server:**
```bash
source venv/bin/activate
python -m uvicorn api.main:app --reload --port 8000
```

**Dashboard:**
```bash
cd dashboard
npm run dev
```

**Regenerate Simulation Data:**
```bash
source venv/bin/activate
python -m simulation.data_generator
```

### Customization

Edit `simulation/config.py` to modify:
- Survey locations and coordinates
- Trash categories and probabilities
- Detection parameters
- Drone specifications

## Conrad Challenge 2026

This project was developed by **TamAir**, a team of four high school students, for the **Conrad Challenge 2026** organized in partnership with NASA.

**Mission**: Optimize environmental cleanup operations by providing agencies with accurate, actionable data on pollution locations and severity.

**Target Users**:
- Caltrans (California Department of Transportation)
- National Park Service
- EPA Regional Offices
- Local environmental agencies
- Cleanup coordination organizations

## License

This project is for educational and competition purposes.

---

*Developed with environmental stewardship in mind.*
