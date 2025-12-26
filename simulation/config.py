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
        "center": {"lat": 37.893, "lon": -122.670},
        # Flight path follows the coastline - New Stinson path (29 waypoints, 847 frames)
        "waypoints": [
            {"lat": 37.9069, "lon": -122.7276, "name": "WP-01"},
            {"lat": 37.9034, "lon": -122.7253, "name": "WP-02"},
            {"lat": 37.9023, "lon": -122.7202, "name": "WP-03"},
            {"lat": 37.9012, "lon": -122.715, "name": "WP-04"},
            {"lat": 37.8983, "lon": -122.7112, "name": "WP-05"},
            {"lat": 37.8956, "lon": -122.707, "name": "WP-06"},
            {"lat": 37.8944, "lon": -122.7019, "name": "WP-07"},
            {"lat": 37.8981, "lon": -122.6993, "name": "WP-08"},
            {"lat": 37.9008, "lon": -122.6951, "name": "WP-09"},
            {"lat": 37.903, "lon": -122.6904, "name": "WP-10"},
            {"lat": 37.9049, "lon": -122.6852, "name": "WP-11"},
            {"lat": 37.908, "lon": -122.6824, "name": "WP-12"},
            {"lat": 37.9069, "lon": -122.6802, "name": "WP-13"},
            {"lat": 37.9067, "lon": -122.6749, "name": "WP-14"},
            {"lat": 37.9065, "lon": -122.6696, "name": "WP-15"},
            {"lat": 37.906, "lon": -122.6642, "name": "WP-16"},
            {"lat": 37.9047, "lon": -122.6589, "name": "WP-17"},
            {"lat": 37.903, "lon": -122.654, "name": "WP-18"},
            {"lat": 37.9009, "lon": -122.6493, "name": "WP-19"},
            {"lat": 37.8986, "lon": -122.6446, "name": "WP-20"},
            {"lat": 37.8959, "lon": -122.6402, "name": "WP-21"},
            {"lat": 37.8929, "lon": -122.6363, "name": "WP-22"},
            {"lat": 37.8896, "lon": -122.6329, "name": "WP-23"},
            {"lat": 37.8862, "lon": -122.6295, "name": "WP-24"},
            {"lat": 37.8821, "lon": -122.628, "name": "WP-25"},
            {"lat": 37.8811, "lon": -122.623, "name": "WP-26"},
            {"lat": 37.878, "lon": -122.62, "name": "WP-27"},
            {"lat": 37.8785, "lon": -122.6149, "name": "WP-28"},
            {"lat": 37.8791, "lon": -122.6135, "name": "WP-29"},
        ],
        "survey_altitude_m": 120,
        "survey_speed_ms": 20,
        "flight_pattern": "corridor",
        "corridor_width_m": 100,
        "population_density": 450,
    },
    "route_66": {
        "name": "Lake Erie - Highway & Waterfront, Ohio",
        "type": "highway",
        "center": {"lat": 41.526, "lon": -82.930},
        # Flight path along Lake Erie shoreline (27 waypoints)
        "waypoints": [
            {"lat": 41.8941, "lon": -80.7880, "name": "WP-01"},
            {"lat": 41.8275, "lon": -80.9398, "name": "WP-02"},
            {"lat": 41.7609, "lon": -81.0915, "name": "WP-03"},
            {"lat": 41.6943, "lon": -81.2433, "name": "WP-04"},
            {"lat": 41.6277, "lon": -81.3951, "name": "WP-05"},
            {"lat": 41.5611, "lon": -81.5468, "name": "WP-06"},
            {"lat": 41.5144, "lon": -81.7088, "name": "WP-07"},
            {"lat": 41.4849, "lon": -81.8796, "name": "WP-08"},
            {"lat": 41.4554, "lon": -82.0505, "name": "WP-09"},
            {"lat": 41.4258, "lon": -82.2213, "name": "WP-10"},
            {"lat": 41.3963, "lon": -82.3921, "name": "WP-11"},
            {"lat": 41.3831, "lon": -82.5606, "name": "WP-12"},
            {"lat": 41.4388, "lon": -82.7196, "name": "WP-13"},
            {"lat": 41.4945, "lon": -82.8785, "name": "WP-14"},
            {"lat": 41.5501, "lon": -83.0375, "name": "WP-15"},
            {"lat": 41.6058, "lon": -83.1964, "name": "WP-16"},
            {"lat": 41.6658, "lon": -83.3434, "name": "WP-17"},
            {"lat": 41.7933, "lon": -83.3008, "name": "WP-18"},
            {"lat": 41.9209, "lon": -83.2583, "name": "WP-19"},
            {"lat": 42.0484, "lon": -83.2158, "name": "WP-20"},
            {"lat": 42.1760, "lon": -83.1733, "name": "WP-21"},
            {"lat": 42.2823, "lon": -83.0725, "name": "WP-22"},
            {"lat": 42.3847, "lon": -82.9609, "name": "WP-23"},
            {"lat": 42.4871, "lon": -82.8493, "name": "WP-24"},
            {"lat": 42.5895, "lon": -82.7377, "name": "WP-25"},
            {"lat": 42.6919, "lon": -82.6261, "name": "WP-26"},
            {"lat": 42.6925, "lon": -82.6254, "name": "WP-27"},
        ],
        "survey_altitude_m": 120,
        "survey_speed_ms": 25,
        "flight_pattern": "corridor",
        "corridor_width_m": 80,
        "population_density": 450,
    },
    "nasa_clear_lake": {
        "name": "NASA - Space Center Houston, Texas",
        "type": "urban_waterfront",
        "center": {"lat": 29.548, "lon": -95.100},
        # Flight path from Space Center Houston to Galveston Bay (27 waypoints)
        "waypoints": [
            {"lat": 29.4813, "lon": -95.1014, "name": "WP-01"},
            {"lat": 29.4864, "lon": -95.1043, "name": "WP-02"},
            {"lat": 29.4914, "lon": -95.1073, "name": "WP-03"},
            {"lat": 29.4965, "lon": -95.1102, "name": "WP-04"},
            {"lat": 29.5016, "lon": -95.1131, "name": "WP-05"},
            {"lat": 29.5066, "lon": -95.1160, "name": "WP-06"},
            {"lat": 29.5123, "lon": -95.1154, "name": "WP-07"},
            {"lat": 29.5179, "lon": -95.1148, "name": "WP-08"},
            {"lat": 29.5236, "lon": -95.1142, "name": "WP-09"},
            {"lat": 29.5291, "lon": -95.1130, "name": "WP-10"},
            {"lat": 29.5340, "lon": -95.1097, "name": "WP-11"},
            {"lat": 29.5389, "lon": -95.1064, "name": "WP-12"},
            {"lat": 29.5438, "lon": -95.1031, "name": "WP-13"},
            {"lat": 29.5485, "lon": -95.0996, "name": "WP-14"},
            {"lat": 29.5513, "lon": -95.0939, "name": "WP-15"},
            {"lat": 29.5541, "lon": -95.0882, "name": "WP-16"},
            {"lat": 29.5569, "lon": -95.0825, "name": "WP-17"},
            {"lat": 29.5597, "lon": -95.0768, "name": "WP-18"},
            {"lat": 29.5617, "lon": -95.0709, "name": "WP-19"},
            {"lat": 29.5622, "lon": -95.0644, "name": "WP-20"},
            {"lat": 29.5627, "lon": -95.0579, "name": "WP-21"},
            {"lat": 29.5631, "lon": -95.0514, "name": "WP-22"},
            {"lat": 29.5636, "lon": -95.0449, "name": "WP-23"},
            {"lat": 29.5663, "lon": -95.0394, "name": "WP-24"},
            {"lat": 29.5700, "lon": -95.0344, "name": "WP-25"},
            {"lat": 29.5737, "lon": -95.0294, "name": "WP-26"},
            {"lat": 29.5749, "lon": -95.0277, "name": "WP-27"},
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
        {"lat": 41.89, "lon": -80.79, "radius_m": 1000, "density": 800, "name": "Conneaut Harbor"},
        {"lat": 41.53, "lon": -81.62, "radius_m": 1500, "density": 1200, "name": "Cleveland Metro"},
        {"lat": 41.37, "lon": -82.53, "radius_m": 800, "density": 600, "name": "Sandusky Bay"},
        {"lat": 41.66, "lon": -83.35, "radius_m": 1200, "density": 900, "name": "Toledo Waterfront"},
        {"lat": 42.20, "lon": -83.17, "radius_m": 1000, "density": 1100, "name": "Detroit River"},
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
