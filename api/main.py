"""
Sylva API Server
FastAPI backend for the Sylva drone simulation
TamAir - Conrad Challenge 2026
"""

import sys
from pathlib import Path

# Add parent directory to path for simulation imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import json
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI(
    title="Sylva API",
    description="API for Sylva drone environmental monitoring simulation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory - resolve to absolute path for production
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filepath: Path) -> Dict:
    """Load JSON file safely."""
    if not filepath.exists():
        return {}
    with open(filepath) as f:
        return json.load(f)


def save_json(filepath: Path, data: Dict):
    """Save data to JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


# =============================================================================
# FLIGHT ENDPOINTS
# =============================================================================

@app.get("/api/flights")
async def list_flights() -> Dict:
    """List all available flight missions."""
    flights_dir = DATA_DIR / "flights"
    flights = []

    for geojson_file in flights_dir.glob("*_flight.geojson"):
        location_key = geojson_file.stem.replace("_flight", "")
        data = load_json(geojson_file)

        if data and "features" in data:
            line_feature = next(
                (f for f in data["features"] if f["geometry"]["type"] == "LineString"),
                None
            )
            if line_feature:
                flights.append({
                    "id": location_key,
                    "flight_id": line_feature["properties"]["flight_id"],
                    "location": line_feature["properties"]["location"],
                    "distance_m": line_feature["properties"]["total_distance_m"],
                    "duration_seconds": line_feature["properties"]["duration_seconds"],
                })

    return {"flights": flights, "count": len(flights)}


@app.get("/api/flights/{flight_id}")
async def get_flight(flight_id: str) -> Dict:
    """Get flight path GeoJSON by ID."""
    flight_file = DATA_DIR / "flights" / f"{flight_id}_flight.geojson"

    if not flight_file.exists():
        raise HTTPException(status_code=404, detail=f"Flight {flight_id} not found")

    return load_json(flight_file)


@app.get("/api/flights/{flight_id}/animation")
async def get_flight_animation(flight_id: str) -> List[Dict]:
    """Get flight animation data for live demo."""
    animation_file = DATA_DIR / "flights" / f"{flight_id}_animation.json"

    if not animation_file.exists():
        raise HTTPException(status_code=404, detail=f"Animation data for {flight_id} not found")

    return load_json(animation_file)


@app.get("/api/flights/{flight_id}/waypoints")
async def get_flight_waypoints(flight_id: str) -> Dict:
    """Get flight waypoints for a location."""
    from simulation.config import LOCATIONS

    if flight_id not in LOCATIONS:
        raise HTTPException(status_code=404, detail=f"Location {flight_id} not found")

    location = LOCATIONS[flight_id]

    if location["flight_pattern"] == "corridor":
        waypoints = location.get("waypoints", [])
    else:
        # For lawnmower pattern, generate waypoints from bounds
        bounds = location.get("bounds", {})
        waypoints = [
            {"lat": bounds.get("south", 0), "lon": bounds.get("west", 0), "name": "Start"},
            {"lat": bounds.get("north", 0), "lon": bounds.get("west", 0), "name": "NW Corner"},
            {"lat": bounds.get("north", 0), "lon": bounds.get("east", 0), "name": "NE Corner"},
            {"lat": bounds.get("south", 0), "lon": bounds.get("east", 0), "name": "SE Corner"},
        ]

    return {
        "location": flight_id,
        "waypoints": waypoints,
        "altitude_m": location.get("survey_altitude_m", 120),
        "speed_ms": location.get("survey_speed_ms", 15),
    }


# =============================================================================
# DETECTION ENDPOINTS
# =============================================================================

@app.get("/api/detections")
async def get_detections(
    location: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    min_confidence: Optional[float] = Query(None, ge=0, le=1),
    limit: Optional[int] = Query(None, ge=1, le=10000),
) -> Dict:
    """Get trash detections with optional filtering."""
    all_detections_file = DATA_DIR / "detections" / "all_detections.geojson"
    data = load_json(all_detections_file)

    if not data or "features" not in data:
        return {"type": "FeatureCollection", "features": [], "count": 0}

    features = data["features"]

    if location:
        features = [f for f in features if location in f["properties"].get("location", "").lower().replace(" ", "_")]

    if category:
        features = [f for f in features if f["properties"].get("category") == category]

    if priority:
        features = [f for f in features if f["properties"].get("priority") == priority]

    if min_confidence:
        features = [f for f in features if f["properties"].get("confidence", 0) >= min_confidence]

    if limit:
        features = features[:limit]

    return {
        "type": "FeatureCollection",
        "features": features,
        "count": len(features),
        "filters_applied": {
            "location": location,
            "category": category,
            "priority": priority,
            "min_confidence": min_confidence,
        },
    }


@app.get("/api/detections/geojson")
async def get_detections_geojson(location: Optional[str] = None) -> Dict:
    """Get detections as pure GeoJSON FeatureCollection."""
    if location:
        detection_file = DATA_DIR / "detections" / f"{location}_detections.geojson"
    else:
        detection_file = DATA_DIR / "detections" / "all_detections.geojson"

    if not detection_file.exists():
        raise HTTPException(status_code=404, detail="Detection data not found")

    return load_json(detection_file)


@app.get("/api/detections/categories")
async def get_categories() -> Dict:
    """Get list of all trash categories with metadata."""
    from simulation.config import TRASH_CATEGORIES

    categories = []
    for key, data in TRASH_CATEGORIES.items():
        categories.append({
            "id": key,
            "name": data["name"],
            "color": data["color"],
            "avg_size_m2": data["avg_size_m2"],
            "weight_range_kg": data["weight_range_kg"],
        })

    return {"categories": categories}


# =============================================================================
# STATISTICS ENDPOINTS
# =============================================================================

@app.get("/api/stats")
async def get_stats(location: Optional[str] = None) -> Dict:
    """Get summary statistics."""
    if location:
        stats_file = DATA_DIR / "summary" / f"{location}_stats.json"
    else:
        stats_file = DATA_DIR / "summary" / "combined_stats.json"

    if not stats_file.exists():
        raise HTTPException(status_code=404, detail="Statistics not found")

    return load_json(stats_file)


@app.get("/api/heatmap")
async def get_heatmap() -> List[List]:
    """Get heatmap data for density visualization."""
    heatmap_file = DATA_DIR / "summary" / "heatmap_data.json"

    if not heatmap_file.exists():
        all_detections = load_json(DATA_DIR / "detections" / "all_detections.geojson")
        heatmap_data = []

        if all_detections and "features" in all_detections:
            for feature in all_detections["features"]:
                coords = feature["geometry"]["coordinates"]
                weight = feature["properties"]["estimated_weight_kg"]
                intensity = min(1.0, weight / 10.0)
                heatmap_data.append([coords[1], coords[0], intensity])

        return heatmap_data

    return load_json(heatmap_file)


# =============================================================================
# CLUSTER ENDPOINTS
# =============================================================================

@app.get("/api/clusters")
async def get_clusters(location: Optional[str] = None) -> Dict:
    """Get high-density trash clusters."""
    if location:
        clusters_file = DATA_DIR / "detections" / f"{location}_clusters.geojson"
    else:
        clusters_file = DATA_DIR / "detections" / "all_clusters.geojson"

    if not clusters_file.exists():
        return {"type": "FeatureCollection", "features": []}

    return load_json(clusters_file)


# =============================================================================
# LIVE DEMO WEBSOCKET - Enhanced with waypoint support
# =============================================================================

class ConnectionManager:
    """Manage WebSocket connections for live demo."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.demo_state = {
            "is_running": False,
            "current_frame": 0,
            "speed_multiplier": 1.0,
            "location": "stinson_beach",
            "start_waypoint": 0,
        }

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass


manager = ConnectionManager()


@app.websocket("/ws/live")
async def websocket_live_demo(websocket: WebSocket):
    """
    WebSocket endpoint for live demo mode with enhanced features.

    Supports commands:
    - start: Start demo for location with optional start_waypoint
    - pause: Pause demo
    - resume: Resume demo
    - reset: Reset to beginning
    - speed: Set speed multiplier
    - jump_to_waypoint: Jump to specific waypoint
    """
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            command = data.get("command")

            if command == "start":
                location = data.get("location", "stinson_beach")
                speed = data.get("speed", 1.0)
                start_waypoint = data.get("start_waypoint", 0)
                custom_path_id = data.get("custom_path_id")  # For custom paths

                if custom_path_id:
                    await start_custom_path_demo(websocket, custom_path_id, speed)
                else:
                    await start_enhanced_demo(websocket, location, speed, start_waypoint)

            elif command == "pause":
                manager.demo_state["is_running"] = False

            elif command == "resume":
                manager.demo_state["is_running"] = True

            elif command == "reset":
                manager.demo_state["current_frame"] = 0

            elif command == "speed":
                manager.demo_state["speed_multiplier"] = data.get("speed", 1.0)

            elif command == "get_state":
                await websocket.send_json({
                    "type": "state",
                    "data": manager.demo_state,
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def start_enhanced_demo(websocket: WebSocket, location: str, speed: float, start_waypoint: int = 0):
    """
    Run enhanced live demo simulation with individual detection streaming.

    Features:
    - Individual detection events (one at a time for CV visualization)
    - Waypoint-based navigation info
    - Altitude and speed data per frame
    """
    from simulation.config import LOCATIONS

    # Load animation and detection data
    animation_file = DATA_DIR / "flights" / f"{location}_animation.json"
    detections_file = DATA_DIR / "detections" / f"{location}_detections.geojson"

    if not animation_file.exists() or not detections_file.exists():
        await websocket.send_json({
            "type": "error",
            "message": f"Data for location {location} not found",
        })
        return

    animation_data = load_json(animation_file)
    detections_data = load_json(detections_file)
    all_detections = detections_data.get("features", [])

    # Sort detections along the flight path based on proximity to waypoints
    # This ensures detections appear in order as the drone flies
    def get_detection_path_position(detection):
        det_lon, det_lat = detection["geometry"]["coordinates"]
        min_dist = float('inf')
        best_idx = 0
        # Find which animation frame this detection is closest to
        for idx, frame in enumerate(animation_data):
            dist = ((frame["lat"] - det_lat) ** 2 + (frame["lon"] - det_lon) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                best_idx = idx
        return best_idx

    all_detections = sorted(all_detections, key=get_detection_path_position)

    # Get location config for waypoints
    location_config = LOCATIONS.get(location, {})
    waypoints = location_config.get("waypoints", [])
    altitude = location_config.get("survey_altitude_m", 120)
    survey_speed = location_config.get("survey_speed_ms", 15)

    # Calculate start frame based on waypoint
    total_frames = len(animation_data)
    if start_waypoint > 0 and len(waypoints) > 0:
        start_frame = int((start_waypoint / len(waypoints)) * total_frames)
    else:
        start_frame = 0

    # Update state
    manager.demo_state.update({
        "is_running": True,
        "current_frame": start_frame,
        "speed_multiplier": speed,
        "location": location,
        "total_frames": total_frames,
        "start_waypoint": start_waypoint,
    })

    # Send initial state with waypoints
    await websocket.send_json({
        "type": "demo_start",
        "location": location,
        "location_name": location_config.get("name", location),
        "total_frames": total_frames,
        "total_detections": len(all_detections),
        "waypoints": waypoints,
        "altitude": altitude,
        "speed": survey_speed,
        "start_frame": start_frame,
    })

    # POSITION-BASED DETECTION SYNC
    # Detections appear based on drone position, not time delays
    # Only show detections whose timestamp <= current drone timestamp

    shown_detection_ids = set()  # Track which detections have been shown
    last_cv_detection_idx = 0

    for frame_idx in range(start_frame, total_frames):
        if not manager.demo_state["is_running"]:
            while not manager.demo_state["is_running"]:
                await asyncio.sleep(0.1)
                if manager.demo_state.get("stop_requested"):
                    manager.demo_state["stop_requested"] = False
                    return

        manager.demo_state["current_frame"] = frame_idx
        frame = animation_data[frame_idx]

        # Calculate progress (0.0 to 1.0)
        progress = (frame_idx - start_frame) / (total_frames - start_frame) if total_frames > start_frame else 0

        # Determine current waypoint
        current_waypoint_idx = 0
        current_waypoint_name = ""
        if waypoints:
            current_waypoint_idx = min(int(progress * len(waypoints)), len(waypoints) - 1)
            current_waypoint_name = waypoints[current_waypoint_idx].get("name", f"Waypoint {current_waypoint_idx + 1}")

        # POSITION-BASED: Only show detections the drone has ACTUALLY passed
        # Compare drone position to each detection's position
        current_lat = frame["lat"]
        current_lon = frame["lon"]

        # Get current frame timestamp for comparison
        current_timestamp = frame.get("timestamp", "")

        # Find all detections that are BEHIND the drone (already scanned)
        new_detections = []
        for det in all_detections:
            det_timestamp = det["properties"].get("timestamp", "")
            # Only show if detection timestamp <= current frame timestamp
            if det_timestamp and current_timestamp and det_timestamp <= current_timestamp:
                det_id = det["properties"]["id"]
                if det_id not in shown_detection_ids:
                    shown_detection_ids.add(det_id)
                    new_detections.append(det)

        current_detection_count = len(shown_detection_ids)

        # For CV panel: only send one detection periodically (every 5th detection)
        # This keeps CV panel updating without overwhelming it
        cv_detection = None
        if current_detection_count > last_cv_detection_idx:
            # Check if we crossed a "5th detection" boundary
            if current_detection_count // 5 > last_cv_detection_idx // 5:
                # Send the most recent detection for CV display
                if new_detections:
                    cv_detection = new_detections[-1]
                last_cv_detection_idx = current_detection_count

        # Send frame update
        frame_data = {
            "type": "frame",
            "frame_index": frame_idx,
            "position": {
                "lat": frame["lat"],
                "lon": frame["lon"],
                "altitude": frame.get("altitude", altitude),
            },
            "elapsed_seconds": frame.get("elapsed_seconds", 0),
            "progress": progress,
            "total_shown": current_detection_count,
            "current_waypoint": current_waypoint_idx,
            "current_waypoint_name": current_waypoint_name,
            "altitude": altitude,
            "speed": survey_speed,
            # Send ALL new detections for this frame so map can show them immediately
            "new_detections": new_detections,
        }

        # Send CV detection as separate event for CV panel animation
        if cv_detection:
            frame_data["new_detection"] = cv_detection
            frame_data["detection_event"] = True

        await websocket.send_json(frame_data)

        # Delay based on speed - ultra smooth movement
        # With 15m interpolation we have very granular frames
        base_delay = 0.12  # Slower, smoother animation
        delay = base_delay / manager.demo_state["speed_multiplier"]
        await asyncio.sleep(delay)

    # Demo complete
    manager.demo_state["is_running"] = False
    await websocket.send_json({
        "type": "demo_complete",
        "total_detections": len(all_detections),
        "location": location,
    })


async def start_custom_path_demo(websocket: WebSocket, path_id: str, speed: float):
    """
    Run live demo simulation for a user-created custom path.
    """
    if path_id not in custom_paths:
        await websocket.send_json({
            "type": "error",
            "message": f"Custom path {path_id} not found"
        })
        return

    path_data = custom_paths[path_id]
    animation_frames = path_data.get("animation_data", [])
    all_detections = path_data.get("detections", {}).get("features", [])

    if not animation_frames:
        await websocket.send_json({
            "type": "error",
            "message": "No animation data for this path"
        })
        return

    # Initialize demo state
    manager.demo_state["is_running"] = True
    manager.demo_state["location"] = "custom"
    manager.demo_state["current_frame"] = 0
    manager.demo_state["speed_multiplier"] = speed

    total_frames = len(animation_frames)
    base_interval = 0.08  # 80ms per frame

    # Send start event
    await websocket.send_json({
        "type": "demo_start",
        "location": path_data["name"],
        "total_frames": total_frames,
        "total_detections": len(all_detections),
    })

    # Timestamp-based detection sync - only show detections drone has passed
    shown_detection_ids = set()
    last_cv_detection_idx = 0

    for frame_idx in range(total_frames):
        if not manager.demo_state["is_running"]:
            await asyncio.sleep(0.1)
            continue

        frame = animation_frames[frame_idx]
        current_speed = manager.demo_state["speed_multiplier"]
        progress = frame_idx / total_frames
        current_timestamp = frame.get("timestamp", "")

        # Find detections the drone has passed (by timestamp comparison)
        new_detections = []
        for det in all_detections:
            det_timestamp = det["properties"].get("timestamp", "")
            if det_timestamp and current_timestamp and det_timestamp <= current_timestamp:
                det_id = det["properties"]["id"]
                if det_id not in shown_detection_ids:
                    shown_detection_ids.add(det_id)
                    new_detections.append(det)

        current_detection_count = len(shown_detection_ids)

        # CV panel detection (every 5th)
        cv_detection = None
        if current_detection_count > last_cv_detection_idx:
            if current_detection_count // 5 > last_cv_detection_idx // 5 and new_detections:
                cv_detection = new_detections[-1]
                last_cv_detection_idx = current_detection_count

        frame_data = {
            "type": "frame",
            "frame_index": frame_idx,
            "total_frames": total_frames,
            "progress": progress,
            "position": {
                "lat": frame["lat"],
                "lon": frame["lon"],
            },
            "altitude": frame.get("altitude", 120),
            "elapsed_seconds": frame.get("elapsed_seconds", 0),
            "timestamp": frame.get("timestamp", ""),
            "speed_ms": 25,
            "detections_shown": current_detection_count,
            "new_detections": new_detections,
        }

        if cv_detection:
            frame_data["new_detection"] = cv_detection
            frame_data["detection_event"] = True

        await websocket.send_json(frame_data)
        await asyncio.sleep(base_interval / current_speed)

    # Demo complete
    manager.demo_state["is_running"] = False
    await websocket.send_json({
        "type": "demo_complete",
        "total_detections": len(all_detections),
        "location": path_data["name"],
    })


# =============================================================================
# UTILITY ENDPOINTS
# =============================================================================

@app.get("/api/locations")
async def get_locations() -> Dict:
    """Get available survey locations with waypoints."""
    from simulation.config import LOCATIONS

    locations = []
    for key, data in LOCATIONS.items():
        loc_data = {
            "id": key,
            "name": data["name"],
            "type": data["type"],
            "center": data.get("center", data.get("waypoints", [{}])[0]),
            "altitude_m": data.get("survey_altitude_m", 120),
            "speed_ms": data.get("survey_speed_ms", 15),
        }

        # Include waypoints for route-based locations
        if "waypoints" in data:
            loc_data["waypoints"] = data["waypoints"]
        elif "bounds" in data:
            # Generate waypoints from bounds for area surveys
            bounds = data["bounds"]
            loc_data["waypoints"] = [
                {"lat": bounds["south"], "lon": bounds["west"], "name": "SW Start"},
                {"lat": bounds["north"], "lon": bounds["west"], "name": "NW Corner"},
                {"lat": bounds["north"], "lon": bounds["east"], "name": "NE Corner"},
                {"lat": bounds["south"], "lon": bounds["east"], "name": "SE End"},
            ]

        locations.append(loc_data)

    return {"locations": locations}


@app.get("/api/population-density")
async def get_population_density(location: Optional[str] = None) -> Dict:
    """Get population density data for visualization overlay."""
    from simulation.config import LOCATIONS, POPULATION_DENSITY_ZONES

    result = {
        "zones": [],
        "location_densities": {},
    }

    # Get density zones for specific location or all
    if location and location in POPULATION_DENSITY_ZONES:
        zones = POPULATION_DENSITY_ZONES[location]
        for zone in zones:
            result["zones"].append({
                "lat": zone["lat"],
                "lon": zone["lon"],
                "radius_m": zone["radius_m"],
                "density": zone["density"],
                "name": zone["name"],
                "location": location,
                # Intensity for heatmap (normalized 0-1)
                "intensity": min(1.0, zone["density"] / 3500),
            })
    else:
        # Return all zones
        for loc_key, zones in POPULATION_DENSITY_ZONES.items():
            for zone in zones:
                result["zones"].append({
                    "lat": zone["lat"],
                    "lon": zone["lon"],
                    "radius_m": zone["radius_m"],
                    "density": zone["density"],
                    "name": zone["name"],
                    "location": loc_key,
                    "intensity": min(1.0, zone["density"] / 3500),
                })

    # Add overall location densities
    for loc_key, loc_data in LOCATIONS.items():
        result["location_densities"][loc_key] = {
            "name": loc_data["name"],
            "density": loc_data.get("population_density", 0),
            "type": loc_data["type"],
        }

    return result


# =============================================================================
# CUSTOM PATH ENDPOINTS
# =============================================================================

# In-memory storage for custom paths (in production, use a database)
custom_paths = {}
custom_path_results = {}


@app.post("/api/custom-path")
async def create_custom_path(data: Dict) -> Dict:
    """
    Create a custom flight path from user-drawn waypoints.

    Expected data:
    {
        "name": "My Highway Survey",
        "waypoints": [{"lat": 34.5, "lon": -114.5}, ...],
        "survey_altitude_m": 120,
        "survey_speed_ms": 25
    }
    """
    import uuid
    from simulation.flight_paths import FlightPathGenerator
    from simulation.trash_detector import TrashDetector

    path_id = str(uuid.uuid4())[:8]
    name = data.get("name", f"Custom Path {path_id}")
    waypoints = data.get("waypoints", [])
    altitude = data.get("survey_altitude_m", 120)
    speed = data.get("survey_speed_ms", 25)

    if len(waypoints) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 waypoints")

    # Create custom location config
    custom_config = {
        "name": name,
        "type": "custom",
        "waypoints": [{"lat": wp["lat"], "lon": wp["lon"], "name": f"Point {i+1}"}
                      for i, wp in enumerate(waypoints)],
        "survey_altitude_m": altitude,
        "survey_speed_ms": speed,
        "flight_pattern": "corridor",
        "corridor_width_m": 50,
        "population_density": 100,
    }

    # Generate flight path using custom config
    generator = FlightPathGenerator(custom_config=custom_config)
    path_waypoints = generator.generate_path()

    # Convert to GeoJSON
    flight_path = generator.to_geojson()

    # Generate detections using the trash detector
    detector = TrashDetector("stinson_beach")
    detections = detector.simulate_detections(flight_path, custom_config)

    # Generate animation data
    animation_data = generator.to_animation_data()

    # Store in memory
    custom_paths[path_id] = {
        "id": path_id,
        "name": name,
        "config": custom_config,
        "flight_path": flight_path,
        "detections": detections,
        "animation_data": animation_data,
        "created_at": datetime.now().isoformat(),
    }

    return {
        "id": path_id,
        "name": name,
        "waypoint_count": len(waypoints),
        "detection_count": len(detections.get("features", [])),
        "message": "Custom path created successfully",
    }


@app.get("/api/custom-path/{path_id}")
async def get_custom_path(path_id: str) -> Dict:
    """Get custom path details."""
    if path_id not in custom_paths:
        raise HTTPException(status_code=404, detail="Custom path not found")

    path = custom_paths[path_id]
    return {
        "id": path_id,
        "name": path["name"],
        "config": path["config"],
        "detection_count": len(path["detections"].get("features", [])),
        "created_at": path["created_at"],
    }


@app.get("/api/custom-path/{path_id}/detections")
async def get_custom_path_detections(path_id: str) -> Dict:
    """Get detections for a custom path."""
    if path_id not in custom_paths:
        raise HTTPException(status_code=404, detail="Custom path not found")

    return custom_paths[path_id]["detections"]


@app.get("/api/custom-path/{path_id}/flight")
async def get_custom_path_flight(path_id: str) -> Dict:
    """Get flight path GeoJSON for a custom path."""
    if path_id not in custom_paths:
        raise HTTPException(status_code=404, detail="Custom path not found")

    return custom_paths[path_id]["flight_path"]


@app.get("/api/custom-paths")
async def list_custom_paths() -> Dict:
    """List all custom paths."""
    paths = []
    for path_id, path in custom_paths.items():
        paths.append({
            "id": path_id,
            "name": path["name"],
            "waypoint_count": len(path["config"]["waypoints"]),
            "detection_count": len(path["detections"].get("features", [])),
            "created_at": path["created_at"],
        })
    return {"paths": paths}


@app.delete("/api/custom-path/{path_id}")
async def delete_custom_path(path_id: str) -> Dict:
    """Delete a custom path."""
    if path_id not in custom_paths:
        raise HTTPException(status_code=404, detail="Custom path not found")

    del custom_paths[path_id]
    return {"message": "Custom path deleted"}


@app.post("/api/custom-path/{path_id}/save-results")
async def save_custom_path_results(path_id: str) -> Dict:
    """Save custom path results to disk for export."""
    if path_id not in custom_paths:
        raise HTTPException(status_code=404, detail="Custom path not found")

    path = custom_paths[path_id]

    # Create custom paths directory
    custom_dir = DATA_DIR / "custom_paths"
    custom_dir.mkdir(exist_ok=True)

    # Save flight path
    flight_file = custom_dir / f"{path_id}_flight.geojson"
    with open(flight_file, "w") as f:
        json.dump(path["flight_path"], f, indent=2)

    # Save detections
    detections_file = custom_dir / f"{path_id}_detections.geojson"
    with open(detections_file, "w") as f:
        json.dump(path["detections"], f, indent=2)

    # Save animation data
    animation_file = custom_dir / f"{path_id}_animation.json"
    with open(animation_file, "w") as f:
        json.dump(path["animation_data"], f, indent=2)

    # Generate stats
    detections = path["detections"].get("features", [])
    total_weight = sum(d["properties"]["estimated_weight_kg"] for d in detections)
    categories = {}
    for d in detections:
        cat = d["properties"]["category_name"]
        if cat not in categories:
            categories[cat] = {"count": 0, "weight": 0}
        categories[cat]["count"] += 1
        categories[cat]["weight"] += d["properties"]["estimated_weight_kg"]

    stats = {
        "path_id": path_id,
        "name": path["name"],
        "total_detections": len(detections),
        "total_weight_kg": round(total_weight, 2),
        "categories": categories,
        "waypoints": path["config"]["waypoints"],
        "created_at": path["created_at"],
        "saved_at": datetime.now().isoformat(),
    }

    stats_file = custom_dir / f"{path_id}_stats.json"
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)

    return {
        "message": "Results saved successfully",
        "files": {
            "flight_path": str(flight_file),
            "detections": str(detections_file),
            "animation": str(animation_file),
            "stats": str(stats_file),
        },
        "stats": stats,
    }


@app.get("/api/custom-path/{path_id}/export")
async def export_custom_path(path_id: str, format: str = "geojson") -> Dict:
    """Export custom path data in various formats."""
    if path_id not in custom_paths:
        raise HTTPException(status_code=404, detail="Custom path not found")

    path = custom_paths[path_id]
    detections = path["detections"].get("features", [])

    if format == "geojson":
        return path["detections"]

    elif format == "csv":
        # Return CSV-ready data
        rows = []
        for d in detections:
            props = d["properties"]
            coords = d["geometry"]["coordinates"]
            rows.append({
                "id": props["id"],
                "latitude": coords[1],
                "longitude": coords[0],
                "category": props["category_name"],
                "confidence": props["confidence"],
                "weight_kg": props["estimated_weight_kg"],
                "size_m2": props["size_m2"],
                "priority": props["priority"],
            })
        return {"format": "csv", "data": rows}

    elif format == "summary":
        total_weight = sum(d["properties"]["estimated_weight_kg"] for d in detections)
        categories = {}
        priorities = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        for d in detections:
            cat = d["properties"]["category_name"]
            categories[cat] = categories.get(cat, 0) + 1
            priorities[d["properties"]["priority"]] += 1

        return {
            "name": path["name"],
            "total_detections": len(detections),
            "total_weight_kg": round(total_weight, 2),
            "categories": categories,
            "priorities": priorities,
            "waypoints": len(path["config"]["waypoints"]),
        }

    else:
        raise HTTPException(status_code=400, detail=f"Unknown format: {format}")


# =============================================================================
# GEOGRAPHY ENDPOINTS
# =============================================================================

GEOGRAPHY_DIR = DATA_DIR / "geography"


@app.get("/api/geography/{location}")
async def get_geography(location: str) -> Dict:
    """
    Get geographic features (water bodies, highways, shorelines) for a location.

    Returns GeoJSON FeatureCollection with:
    - Water polygons (oceans, lakes, lagoons)
    - Highway/road linestrings
    - Shoreline linestrings
    """
    features = []

    # Map location keys to geography files
    file_mappings = {
        "stinson_beach": ["stinson_beach_water.geojson", "stinson_beach_shoreline.geojson"],
        "route_66": ["route_66_highway.geojson"],
        "nasa_clear_lake": ["nasa_clear_lake.geojson"],
    }

    if location not in file_mappings:
        raise HTTPException(status_code=404, detail=f"Geography data for {location} not found")

    for filename in file_mappings[location]:
        filepath = GEOGRAPHY_DIR / filename
        if filepath.exists():
            data = load_json(filepath)
            if data and "features" in data:
                features.extend(data["features"])

    return {
        "type": "FeatureCollection",
        "location": location,
        "features": features,
    }


@app.get("/api/geography")
async def list_geography() -> Dict:
    """List all available geography data."""
    available = []

    if GEOGRAPHY_DIR.exists():
        for f in GEOGRAPHY_DIR.glob("*.geojson"):
            data = load_json(f)
            available.append({
                "filename": f.name,
                "name": data.get("name", f.stem),
                "feature_count": len(data.get("features", [])),
            })

    return {"geography_files": available}


@app.get("/api/health")
async def health_check() -> Dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
    }


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Sylva API",
        "description": "Drone environmental monitoring simulation API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "flights": "/api/flights",
            "detections": "/api/detections",
            "stats": "/api/stats",
            "clusters": "/api/clusters",
            "heatmap": "/api/heatmap",
            "locations": "/api/locations",
            "live_demo": "ws://localhost:8000/ws/live",
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
