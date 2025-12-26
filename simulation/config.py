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
        "name": "Stinson Beach Coastline, California",
        "type": "beach",
        "center": {"lat": 37.907, "lon": -122.676},
        # Flight path follows the coastline from northwest to southeast
        "waypoints": [
            {"lat": 37.9021, "lon": -122.7185, "name": "Northwest Start"},
            {"lat": 37.8947, "lon": -122.7030, "name": "Stinson North"},
            {"lat": 37.9037, "lon": -122.6889, "name": "Main Beach Area"},
            {"lat": 37.9066, "lon": -122.6756, "name": "Stinson Beach Center"},
            {"lat": 37.9044, "lon": -122.6573, "name": "South Beach"},
            {"lat": 37.8968, "lon": -122.6410, "name": "Rocky Point South"},
            {"lat": 37.8858, "lon": -122.6285, "name": "Southeast End"},
        ],
        "survey_altitude_m": 120,
        "survey_speed_ms": 20,
        "flight_pattern": "corridor",
        "corridor_width_m": 100,
        "population_density": 450,
    },
    "route_66": {
        "name": "Historic Route 66, Needles CA",
        "type": "highway",
        "center": {"lat": 34.850, "lon": -114.585},
        # Flight path follows Historic Route 66 highway
        "waypoints": [
            {"lat": 34.843, "lon": -114.630, "name": "Needles, CA - Start"},
            {"lat": 34.848, "lon": -114.610, "name": "East Needles"},
            {"lat": 34.853, "lon": -114.585, "name": "Route 66 Midpoint"},
            {"lat": 34.858, "lon": -114.560, "name": "Desert View"},
            {"lat": 34.862, "lon": -114.540, "name": "East End"},
        ],
        "survey_altitude_m": 100,
        "survey_speed_ms": 28,
        "flight_pattern": "corridor",
        "corridor_width_m": 40,
        "population_density": 85,
    },
    "nasa_clear_lake": {
        "name": "NASA - Space Center Houston, Texas",
        "type": "urban_waterfront",
        "center": {"lat": 29.548, "lon": -95.100},
        # Flight path from Space Center Houston along Clear Lake to Galveston Bay
        "waypoints": [
            {"lat": 29.4813, "lon": -95.1014, "name": "Space Center Start"},
            {"lat": 29.5065, "lon": -95.1160, "name": "NASA Road 1"},
            {"lat": 29.5279, "lon": -95.1138, "name": "Clear Lake North"},
            {"lat": 29.5482, "lon": -95.1001, "name": "Clear Lake Center"},
            {"lat": 29.5616, "lon": -95.0729, "name": "Seabrook Marina"},
            {"lat": 29.5637, "lon": -95.0430, "name": "Kemah Boardwalk"},
            {"lat": 29.5749, "lon": -95.0277, "name": "Galveston Bay End"},
        ],
        "survey_altitude_m": 120,
        "survey_speed_ms": 20,
        "flight_pattern": "corridor",
        "corridor_width_m": 150,
        "population_density": 1850,
    },
}

# Population density zones for overlay visualization
POPULATION_DENSITY_ZONES = {
    "stinson_beach": [
        {"lat": 37.907, "lon": -122.676, "radius_m": 500, "density": 1200, "name": "Main Beach Area"},
        {"lat": 37.895, "lon": -122.710, "radius_m": 400, "density": 800, "name": "North Stinson"},
        {"lat": 37.890, "lon": -122.640, "radius_m": 300, "density": 200, "name": "South Rural"},
    ],
    "route_66": [
        {"lat": 34.848, "lon": -114.615, "radius_m": 1000, "density": 350, "name": "Needles Town"},
        {"lat": 34.855, "lon": -114.575, "radius_m": 500, "density": 50, "name": "Desert Highway"},
        {"lat": 34.860, "lon": -114.550, "radius_m": 300, "density": 20, "name": "East Desert"},
    ],
    "nasa_clear_lake": [
        {"lat": 29.485, "lon": -95.100, "radius_m": 800, "density": 2500, "name": "Space Center Houston"},
        {"lat": 29.520, "lon": -95.115, "radius_m": 600, "density": 3200, "name": "Clear Lake City"},
        {"lat": 29.550, "lon": -95.100, "radius_m": 500, "density": 2800, "name": "Clear Lake Shore"},
        {"lat": 29.565, "lon": -95.045, "radius_m": 700, "density": 1500, "name": "Kemah Boardwalk"},
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
        "urban_waterfront_probability": 0.25,  # increased for NASA
    },
    "food_packaging": {
        "name": "Food Packaging/Cardboard",
        "avg_size_m2": 0.01,
        "weight_range_kg": (0.02, 0.1),
        "color": "#e67e22",
        "icon": "package",
        "beach_probability": 0.20,
        "highway_probability": 0.20,
        "urban_waterfront_probability": 0.18,
    },
    "tire": {
        "name": "Tires",
        "avg_size_m2": 0.25,
        "weight_range_kg": (8, 15),
        "color": "#2c3e50",
        "icon": "tire",
        "beach_probability": 0.02,
        "highway_probability": 0.15,
        "urban_waterfront_probability": 0.12,  # increased for NASA - hazardous
    },
    "metal_debris": {
        "name": "Metal Debris",
        "avg_size_m2": 0.05,
        "weight_range_kg": (0.5, 5),
        "color": "#95a5a6",
        "icon": "metal",
        "beach_probability": 0.05,
        "highway_probability": 0.18,
        "urban_waterfront_probability": 0.15,  # increased for NASA - hazardous
    },
    "construction_waste": {
        "name": "Construction Waste",
        "avg_size_m2": 0.5,
        "weight_range_kg": (10, 50),
        "color": "#8e44ad",
        "icon": "construction",
        "beach_probability": 0.03,
        "highway_probability": 0.12,
        "urban_waterfront_probability": 0.15,  # increased for NASA - cardboard/debris
    },
    "organic_waste": {
        "name": "Organic Waste",
        "avg_size_m2": 0.03,
        "weight_range_kg": (0.1, 1),
        "color": "#27ae60",
        "icon": "leaf",
        "beach_probability": 0.15,
        "highway_probability": 0.08,
        "urban_waterfront_probability": 0.05,  # reduced
    },
    "glass": {
        "name": "Glass",
        "avg_size_m2": 0.005,
        "weight_range_kg": (0.2, 0.5),
        "color": "#1abc9c",
        "icon": "glass",
        "beach_probability": 0.18,
        "highway_probability": 0.07,
        "urban_waterfront_probability": 0.05,  # reduced
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
        "urban_waterfront": 420,  # items per km² - 20% increase for NASA Space Center
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
