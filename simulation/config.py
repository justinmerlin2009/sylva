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
        "name": "Stinson Beach Shoreline, California",
        "type": "beach",
        "center": {"lat": 37.8965, "lon": -122.6400},
        # Flight path follows the ENTIRE shoreline from Seadrift to Bolinas (~4 miles)
        "waypoints": [
            # Northern section - Seadrift
            {"lat": 37.9100, "lon": -122.6520, "name": "Seadrift Beach Start"},
            {"lat": 37.9070, "lon": -122.6500, "name": "Seadrift South"},
            {"lat": 37.9045, "lon": -122.6485, "name": "North Stinson"},
            # Main Stinson Beach shoreline
            {"lat": 37.9015, "lon": -122.6460, "name": "Stinson North Beach"},
            {"lat": 37.9000, "lon": -122.6445, "name": "Stinson Beach Center"},
            {"lat": 37.8975, "lon": -122.6420, "name": "Lifeguard Station"},
            {"lat": 37.8950, "lon": -122.6400, "name": "Central Beach"},
            {"lat": 37.8920, "lon": -122.6380, "name": "South Stinson"},
            # Southern section - toward Bolinas
            {"lat": 37.8895, "lon": -122.6360, "name": "Easkoot Creek"},
            {"lat": 37.8870, "lon": -122.6340, "name": "Willow Camp"},
            {"lat": 37.8845, "lon": -122.6310, "name": "Rocky Point"},
            {"lat": 37.8830, "lon": -122.6295, "name": "Bolinas Approach"},
        ],
        "survey_altitude_m": 80,  # Lower for better beach detection
        "survey_speed_ms": 20,  # ~45 mph for detailed beach scanning
        "flight_pattern": "shoreline",
        "corridor_width_m": 100,  # Full beach width
        "population_density": 450,  # people per km² - rural beach area
    },
    "route_66": {
        "name": "Historic Route 66, Needles to Topock",
        "type": "highway",
        # 14-mile section (~22km) along historic Route 66 from Needles, CA to Topock, AZ
        "waypoints": [
            {"lat": 34.8450, "lon": -114.6200, "name": "Needles, CA"},
            {"lat": 34.8500, "lon": -114.6100, "name": "East Needles"},
            {"lat": 34.8540, "lon": -114.5950, "name": "Desert View"},
            {"lat": 34.8580, "lon": -114.5750, "name": "Route 66 Sign"},
            {"lat": 34.8625, "lon": -114.5600, "name": "Midpoint Vista"},
            {"lat": 34.8650, "lon": -114.5550, "name": "Route 66 Midpoint"},
            {"lat": 34.8694, "lon": -114.5289, "name": "Historic Marker"},
            {"lat": 34.8770, "lon": -114.5000, "name": "Colorado River Approach"},
            {"lat": 34.8820, "lon": -114.4800, "name": "River View"},
            {"lat": 34.8855, "lon": -114.4400, "name": "Topock, AZ Border"},
        ],
        "survey_altitude_m": 100,
        "survey_speed_ms": 28,  # ~63 mph cruise along highway
        "flight_pattern": "highway",
        "corridor_width_m": 40,  # Highway shoulder scan
        "population_density": 85,  # people per km² - desert highway
    },
    "nasa_clear_lake": {
        "name": "NASA Clear Lake Area, Houston TX",
        "type": "urban_waterfront",
        "center": {"lat": 29.5400, "lon": -95.0700},
        # 350-mile concentric circle survey around Clear Lake
        "waypoints": [
            # Expanding concentric circles - 7 rings totaling 350 miles
            {"lat": 29.5580, "lon": -95.0700, "name": "Clear Lake Center - Start"},
            {"lat": 29.5625, "lon": -95.0700, "name": "Circle 1 Complete"},
            {"lat": 29.5670, "lon": -95.0700, "name": "Circle 2 Complete"},
            {"lat": 29.5760, "lon": -95.0700, "name": "Circle 3 Complete"},
            {"lat": 29.5830, "lon": -95.0700, "name": "Circle 4 Complete"},
            {"lat": 29.5940, "lon": -95.0700, "name": "Circle 5 Complete"},
            {"lat": 29.6080, "lon": -95.0700, "name": "Circle 6 Complete"},
            {"lat": 29.6300, "lon": -95.0700, "name": "Circle 7 - 350 Miles Complete"},
        ],
        "survey_altitude_m": 120,
        "survey_speed_ms": 22,  # ~50 mph for urban waterfront
        "flight_pattern": "concentric_circles",
        "corridor_width_m": 150,  # Wide scan for concentric pattern
        "population_density": 1850,  # people per km² - suburban Houston
        "total_distance_miles": 350,
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
