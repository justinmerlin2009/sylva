"""
Sylva Drone Simulation Configuration
TamAir - Conrad Challenge 2026
"""

# =============================================================================
# DRONE SPECIFICATIONS
# =============================================================================

DRONE_SPECS = {
    "name": "Sylva-1",
    "type": "Fixed-wing",
    "wingspan_m": 2.5,
    "weight_kg": 4.2,
    "max_speed_ms": 31.3,  # 70 mph = ~31.3 m/s
    "cruise_speed_ms": 28,  # ~63 mph cruise
    "survey_speed_ms": 22,  # ~50 mph for detailed scanning
    "endurance_hours": 3.5,  # 3-4 hours flight time
    "max_altitude_m": 500,
    "camera_resolution_mp": 20,
    "range_km": 350,  # ~220 miles at cruise speed
}

# =============================================================================
# SURVEY LOCATIONS
# =============================================================================

LOCATIONS = {
    "stinson_beach": {
        "name": "Stinson Beach, California",
        "type": "beach",
        "center": {"lat": 37.8950, "lon": -122.6400},
        # Flight path follows the ENTIRE coastline from north to south (~3.5 miles)
        "waypoints": [
            # Northern section - Seadrift lagoon area
            {"lat": 37.9085, "lon": -122.6510, "name": "Seadrift North"},
            {"lat": 37.9060, "lon": -122.6495, "name": "Seadrift Lagoon"},
            {"lat": 37.9040, "lon": -122.6480, "name": "Seadrift Beach"},
            # Main Stinson Beach section
            {"lat": 37.9015, "lon": -122.6460, "name": "North Beach Access"},
            {"lat": 37.8990, "lon": -122.6435, "name": "Stinson Main Beach"},
            {"lat": 37.8965, "lon": -122.6415, "name": "Lifeguard Station"},
            {"lat": 37.8940, "lon": -122.6395, "name": "Central Beach"},
            {"lat": 37.8915, "lon": -122.6375, "name": "South Beach"},
            # Southern section - toward Bolinas
            {"lat": 37.8890, "lon": -122.6355, "name": "Easkoot Creek"},
            {"lat": 37.8865, "lon": -122.6330, "name": "Willow Camp"},
            {"lat": 37.8840, "lon": -122.6305, "name": "South Point"},
            {"lat": 37.8815, "lon": -122.6280, "name": "Bolinas Approach"},
        ],
        "survey_altitude_m": 80,  # Lower for better beach detection
        "survey_speed_ms": 20,  # ~45 mph for detailed beach scanning
        "flight_pattern": "corridor",
        "corridor_width_m": 100,  # Full beach width
        "population_density": 450,  # people per km² - rural beach area
    },
    "route_66": {
        "name": "Route 66 - Needles Corridor",
        "type": "highway",
        # 10-mile section (~16km) along historic Route 66 near Needles, CA
        "waypoints": [
            {"lat": 34.8480, "lon": -114.6147, "name": "Needles Downtown"},
            {"lat": 34.8520, "lon": -114.5950, "name": "East Needles"},
            {"lat": 34.8580, "lon": -114.5750, "name": "Desert View"},
            {"lat": 34.8650, "lon": -114.5550, "name": "Rest Stop"},
            {"lat": 34.8694, "lon": -114.5289, "name": "AZ State Line"},
            {"lat": 34.8750, "lon": -114.5050, "name": "Welcome Center"},
            {"lat": 34.8820, "lon": -114.4800, "name": "Historic Marker"},
            {"lat": 34.8900, "lon": -114.4550, "name": "Scenic Overlook"},
        ],
        "survey_altitude_m": 120,
        "survey_speed_ms": 28,  # ~63 mph cruise along highway
        "flight_pattern": "corridor",
        "corridor_width_m": 40,  # Highway shoulder scan
        "population_density": 85,  # people per km² - desert highway
    },
    "nasa_clear_lake": {
        "name": "NASA Clear Lake, Houston TX",
        "type": "urban_waterfront",
        "center": {"lat": 29.5519, "lon": -95.0920},
        # Survey along Clear Lake shoreline near NASA Johnson Space Center
        "waypoints": [
            # Starting near Space Center Houston
            {"lat": 29.5519, "lon": -95.0980, "name": "Space Center Houston"},
            {"lat": 29.5480, "lon": -95.0920, "name": "NASA Parkway East"},
            {"lat": 29.5450, "lon": -95.0850, "name": "Clear Lake Park"},
            # Along the bay shoreline
            {"lat": 29.5400, "lon": -95.0780, "name": "Lakeside Marina"},
            {"lat": 29.5350, "lon": -95.0720, "name": "Bay Area Blvd"},
            {"lat": 29.5300, "lon": -95.0650, "name": "Seabrook Channel"},
            {"lat": 29.5270, "lon": -95.0580, "name": "Kemah Approach"},
            # Kemah Boardwalk area
            {"lat": 29.5250, "lon": -95.0520, "name": "Kemah Boardwalk"},
            {"lat": 29.5220, "lon": -95.0450, "name": "Galveston Bay"},
        ],
        "survey_altitude_m": 100,
        "survey_speed_ms": 22,  # ~50 mph for urban waterfront
        "flight_pattern": "corridor",
        "corridor_width_m": 80,  # Waterfront scan width
        "population_density": 1850,  # people per km² - suburban Houston
    },
}

# Population density zones for overlay visualization
POPULATION_DENSITY_ZONES = {
    "stinson_beach": [
        {"lat": 37.8990, "lon": -122.6435, "radius_m": 500, "density": 1200, "name": "Main Beach Area"},
        {"lat": 37.9060, "lon": -122.6495, "radius_m": 400, "density": 800, "name": "Seadrift Residential"},
        {"lat": 37.8865, "lon": -122.6330, "radius_m": 300, "density": 200, "name": "South Rural"},
    ],
    "route_66": [
        {"lat": 34.8480, "lon": -114.6147, "radius_m": 1000, "density": 350, "name": "Needles Town"},
        {"lat": 34.8694, "lon": -114.5289, "radius_m": 500, "density": 50, "name": "Border Area"},
        {"lat": 34.8820, "lon": -114.4800, "radius_m": 300, "density": 20, "name": "Desert"},
    ],
    "nasa_clear_lake": [
        {"lat": 29.5519, "lon": -95.0920, "radius_m": 800, "density": 2500, "name": "NASA Complex"},
        {"lat": 29.5400, "lon": -95.0780, "radius_m": 600, "density": 3200, "name": "Clear Lake City"},
        {"lat": 29.5300, "lon": -95.0650, "radius_m": 500, "density": 2800, "name": "Seabrook"},
        {"lat": 29.5250, "lon": -95.0520, "radius_m": 700, "density": 1500, "name": "Kemah"},
    ],
}

# =============================================================================
# TRASH DETECTION CATEGORIES
# =============================================================================

TRASH_CATEGORIES = {
    "plastic_bottle": {
        "name": "Plastic Bottles",
        "avg_size_m2": 0.002,
        "weight_range_kg": (0.01, 0.05),
        "color": "#3498db",
        "icon": "bottle",
        "beach_probability": 0.25,
        "highway_probability": 0.15,
        "urban_waterfront_probability": 0.22,
    },
    "food_packaging": {
        "name": "Food Packaging",
        "avg_size_m2": 0.01,
        "weight_range_kg": (0.02, 0.1),
        "color": "#e67e22",
        "icon": "package",
        "beach_probability": 0.20,
        "highway_probability": 0.20,
        "urban_waterfront_probability": 0.25,
    },
    "tire": {
        "name": "Tires",
        "avg_size_m2": 0.25,
        "weight_range_kg": (8, 15),
        "color": "#2c3e50",
        "icon": "tire",
        "beach_probability": 0.02,
        "highway_probability": 0.15,
        "urban_waterfront_probability": 0.08,
    },
    "metal_debris": {
        "name": "Metal Debris",
        "avg_size_m2": 0.05,
        "weight_range_kg": (0.5, 5),
        "color": "#95a5a6",
        "icon": "metal",
        "beach_probability": 0.05,
        "highway_probability": 0.18,
        "urban_waterfront_probability": 0.12,
    },
    "construction_waste": {
        "name": "Construction Waste",
        "avg_size_m2": 0.5,
        "weight_range_kg": (10, 50),
        "color": "#8e44ad",
        "icon": "construction",
        "beach_probability": 0.03,
        "highway_probability": 0.12,
        "urban_waterfront_probability": 0.10,
    },
    "organic_waste": {
        "name": "Organic Waste",
        "avg_size_m2": 0.03,
        "weight_range_kg": (0.1, 1),
        "color": "#27ae60",
        "icon": "leaf",
        "beach_probability": 0.15,
        "highway_probability": 0.08,
        "urban_waterfront_probability": 0.08,
    },
    "glass": {
        "name": "Glass",
        "avg_size_m2": 0.005,
        "weight_range_kg": (0.2, 0.5),
        "color": "#1abc9c",
        "icon": "glass",
        "beach_probability": 0.18,
        "highway_probability": 0.07,
        "urban_waterfront_probability": 0.10,
    },
    "textile": {
        "name": "Textile/Fabric",
        "avg_size_m2": 0.1,
        "weight_range_kg": (0.2, 2),
        "color": "#e74c3c",
        "icon": "fabric",
        "beach_probability": 0.12,
        "highway_probability": 0.05,
        "urban_waterfront_probability": 0.05,
    },
}

# =============================================================================
# DETECTION PARAMETERS
# =============================================================================

DETECTION_PARAMS = {
    "base_detection_rate_per_km2": {
        "beach": 400,  # items per km² - higher for realistic beach survey
        "highway": 80,  # items per km²
        "urban_waterfront": 350,  # items per km² - urban area near water
    },
    "hotspot_multiplier": 3.0,  # multiplier for high-density areas
    "rest_stop_multiplier": 2.5,
    "confidence_range": (0.75, 0.99),
    "min_confidence_threshold": 0.70,
}

# =============================================================================
# PRIORITY SCORING
# =============================================================================

PRIORITY_THRESHOLDS = {
    "critical": {"min_density": 50, "min_weight": 100},  # items/100m², kg
    "high": {"min_density": 25, "min_weight": 50},
    "medium": {"min_density": 10, "min_weight": 20},
    "low": {"min_density": 0, "min_weight": 0},
}

# =============================================================================
# SIMULATION PARAMETERS
# =============================================================================

SIMULATION = {
    "random_seed": 42,  # for reproducibility
    "time_step_seconds": 1,
    "start_date": "2026-01-15",
    "camera_frame_rate_hz": 2,  # frames per second
}
