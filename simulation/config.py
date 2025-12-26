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
        # Flight path follows the coastline - New Stinson path (86 waypoints, 847 frames)
        "waypoints": [
            {"lat": 37.9069, "lon": -122.7276, "name": "WP-01"},
            {"lat": 37.9055, "lon": -122.7274, "name": "WP-02"},
            {"lat": 37.9042, "lon": -122.7268, "name": "WP-03"},
            {"lat": 37.9035, "lon": -122.7254, "name": "WP-04"},
            {"lat": 37.9029, "lon": -122.7239, "name": "WP-05"},
            {"lat": 37.9024, "lon": -122.7223, "name": "WP-06"},
            {"lat": 37.9023, "lon": -122.7205, "name": "WP-07"},
            {"lat": 37.9021, "lon": -122.7188, "name": "WP-08"},
            {"lat": 37.9018, "lon": -122.7172, "name": "WP-09"},
            {"lat": 37.9013, "lon": -122.7155, "name": "WP-10"},
            {"lat": 37.9009, "lon": -122.7139, "name": "WP-11"},
            {"lat": 37.9, "lon": -122.7125, "name": "WP-12"},
            {"lat": 37.8989, "lon": -122.7115, "name": "WP-13"},
            {"lat": 37.8977, "lon": -122.7105, "name": "WP-14"},
            {"lat": 37.8968, "lon": -122.7091, "name": "WP-15"},
            {"lat": 37.896, "lon": -122.7077, "name": "WP-16"},
            {"lat": 37.8953, "lon": -122.7062, "name": "WP-17"},
            {"lat": 37.8948, "lon": -122.7045, "name": "WP-18"},
            {"lat": 37.8944, "lon": -122.7028, "name": "WP-19"},
            {"lat": 37.8948, "lon": -122.7015, "name": "WP-20"},
            {"lat": 37.8961, "lon": -122.7009, "name": "WP-21"},
            {"lat": 37.8974, "lon": -122.7002, "name": "WP-22"},
            {"lat": 37.8984, "lon": -122.699, "name": "WP-23"},
            {"lat": 37.8993, "lon": -122.6977, "name": "WP-24"},
            {"lat": 37.9002, "lon": -122.6962, "name": "WP-25"},
            {"lat": 37.901, "lon": -122.6948, "name": "WP-26"},
            {"lat": 37.9018, "lon": -122.6933, "name": "WP-27"},
            {"lat": 37.9025, "lon": -122.6918, "name": "WP-28"},
            {"lat": 37.903, "lon": -122.6902, "name": "WP-29"},
            {"lat": 37.9036, "lon": -122.6885, "name": "WP-30"},
            {"lat": 37.9044, "lon": -122.6869, "name": "WP-31"},
            {"lat": 37.9049, "lon": -122.6852, "name": "WP-32"},
            {"lat": 37.9054, "lon": -122.6836, "name": "WP-33"},
            {"lat": 37.9066, "lon": -122.683, "name": "WP-34"},
            {"lat": 37.9079, "lon": -122.6825, "name": "WP-35"},
            {"lat": 37.909, "lon": -122.6819, "name": "WP-36"},
            {"lat": 37.9085, "lon": -122.6809, "name": "WP-37"},
            {"lat": 37.9071, "lon": -122.6804, "name": "WP-38"},
            {"lat": 37.9067, "lon": -122.679, "name": "WP-39"},
            {"lat": 37.9067, "lon": -122.6772, "name": "WP-40"},
            {"lat": 37.9067, "lon": -122.6754, "name": "WP-41"},
            {"lat": 37.9067, "lon": -122.6737, "name": "WP-42"},
            {"lat": 37.9066, "lon": -122.672, "name": "WP-43"},
            {"lat": 37.9066, "lon": -122.6702, "name": "WP-44"},
            {"lat": 37.9064, "lon": -122.6685, "name": "WP-45"},
            {"lat": 37.9064, "lon": -122.6668, "name": "WP-46"},
            {"lat": 37.9061, "lon": -122.6651, "name": "WP-47"},
            {"lat": 37.9058, "lon": -122.6633, "name": "WP-48"},
            {"lat": 37.9054, "lon": -122.6615, "name": "WP-49"},
            {"lat": 37.905, "lon": -122.6599, "name": "WP-50"},
            {"lat": 37.9045, "lon": -122.6582, "name": "WP-51"},
            {"lat": 37.904, "lon": -122.6566, "name": "WP-52"},
            {"lat": 37.9035, "lon": -122.655, "name": "WP-53"},
            {"lat": 37.9028, "lon": -122.6535, "name": "WP-54"},
            {"lat": 37.9021, "lon": -122.652, "name": "WP-55"},
            {"lat": 37.9014, "lon": -122.6505, "name": "WP-56"},
            {"lat": 37.9007, "lon": -122.649, "name": "WP-57"},
            {"lat": 37.9, "lon": -122.6475, "name": "WP-58"},
            {"lat": 37.8993, "lon": -122.646, "name": "WP-59"},
            {"lat": 37.8986, "lon": -122.6444, "name": "WP-60"},
            {"lat": 37.8977, "lon": -122.643, "name": "WP-61"},
            {"lat": 37.8968, "lon": -122.6416, "name": "WP-62"},
            {"lat": 37.8959, "lon": -122.6402, "name": "WP-63"},
            {"lat": 37.895, "lon": -122.6388, "name": "WP-64"},
            {"lat": 37.8941, "lon": -122.6375, "name": "WP-65"},
            {"lat": 37.893, "lon": -122.6364, "name": "WP-66"},
            {"lat": 37.892, "lon": -122.6353, "name": "WP-67"},
            {"lat": 37.8909, "lon": -122.6343, "name": "WP-68"},
            {"lat": 37.8898, "lon": -122.6331, "name": "WP-69"},
            {"lat": 37.8887, "lon": -122.632, "name": "WP-70"},
            {"lat": 37.8876, "lon": -122.631, "name": "WP-71"},
            {"lat": 37.8865, "lon": -122.6298, "name": "WP-72"},
            {"lat": 37.8854, "lon": -122.6287, "name": "WP-73"},
            {"lat": 37.8841, "lon": -122.6281, "name": "WP-74"},
            {"lat": 37.8826, "lon": -122.6282, "name": "WP-75"},
            {"lat": 37.8815, "lon": -122.6273, "name": "WP-76"},
            {"lat": 37.8815, "lon": -122.6256, "name": "WP-77"},
            {"lat": 37.8814, "lon": -122.6239, "name": "WP-78"},
            {"lat": 37.8807, "lon": -122.6224, "name": "WP-79"},
            {"lat": 37.8798, "lon": -122.6211, "name": "WP-80"},
            {"lat": 37.8784, "lon": -122.6208, "name": "WP-81"},
            {"lat": 37.8778, "lon": -122.6193, "name": "WP-82"},
            {"lat": 37.8779, "lon": -122.6177, "name": "WP-83"},
            {"lat": 37.8781, "lon": -122.616, "name": "WP-84"},
            {"lat": 37.8787, "lon": -122.6144, "name": "WP-85"},
            {"lat": 37.8791, "lon": -122.6135, "name": "WP-86"},
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
        "center": {"lat": 41.75, "lon": -82.05},
        # New Lake Erie path (97 waypoints, 957 frames, 429.9 km)
        "waypoints": [
            {"lat": 41.9248, "lon": -80.6644, "name": "WP-01"},
            {"lat": 41.9116, "lon": -80.7158, "name": "WP-02"},
            {"lat": 41.8985, "lon": -80.7673, "name": "WP-03"},
            {"lat": 41.8854, "lon": -80.8187, "name": "WP-04"},
            {"lat": 41.8724, "lon": -80.8702, "name": "WP-05"},
            {"lat": 41.8603, "lon": -80.9221, "name": "WP-06"},
            {"lat": 41.8482, "lon": -80.974, "name": "WP-07"},
            {"lat": 41.833, "lon": -81.0243, "name": "WP-08"},
            {"lat": 41.8153, "lon": -81.0732, "name": "WP-09"},
            {"lat": 41.7963, "lon": -81.1211, "name": "WP-10"},
            {"lat": 41.7767, "lon": -81.1686, "name": "WP-11"},
            {"lat": 41.7566, "lon": -81.2157, "name": "WP-12"},
            {"lat": 41.7359, "lon": -81.2623, "name": "WP-13"},
            {"lat": 41.7169, "lon": -81.3102, "name": "WP-14"},
            {"lat": 41.6987, "lon": -81.3588, "name": "WP-15"},
            {"lat": 41.6742, "lon": -81.4018, "name": "WP-16"},
            {"lat": 41.6465, "lon": -81.4409, "name": "WP-17"},
            {"lat": 41.6154, "lon": -81.4756, "name": "WP-18"},
            {"lat": 41.5885, "lon": -81.5153, "name": "WP-19"},
            {"lat": 41.5664, "lon": -81.5606, "name": "WP-20"},
            {"lat": 41.5442, "lon": -81.6059, "name": "WP-21"},
            {"lat": 41.52, "lon": -81.6489, "name": "WP-22"},
            {"lat": 41.4913, "lon": -81.6871, "name": "WP-23"},
            {"lat": 41.48, "lon": -81.7382, "name": "WP-24"},
            {"lat": 41.4711, "lon": -81.7909, "name": "WP-25"},
            {"lat": 41.4641, "lon": -81.8442, "name": "WP-26"},
            {"lat": 41.4572, "lon": -81.8974, "name": "WP-27"},
            {"lat": 41.4795, "lon": -81.9424, "name": "WP-28"},
            {"lat": 41.4951, "lon": -81.9904, "name": "WP-29"},
            {"lat": 41.4979, "lon": -82.0444, "name": "WP-30"},
            {"lat": 41.486, "lon": -82.0955, "name": "WP-31"},
            {"lat": 41.4719, "lon": -82.1462, "name": "WP-32"},
            {"lat": 41.4556, "lon": -82.1956, "name": "WP-33"},
            {"lat": 41.4375, "lon": -82.2439, "name": "WP-34"},
            {"lat": 41.4194, "lon": -82.2922, "name": "WP-35"},
            {"lat": 41.4072, "lon": -82.3434, "name": "WP-36"},
            {"lat": 41.3976, "lon": -82.3958, "name": "WP-37"},
            {"lat": 41.3866, "lon": -82.4475, "name": "WP-38"},
            {"lat": 41.3667, "lon": -82.4946, "name": "WP-39"},
            {"lat": 41.3571, "lon": -82.5418, "name": "WP-40"},
            {"lat": 41.3763, "lon": -82.5894, "name": "WP-41"},
            {"lat": 41.3954, "lon": -82.637, "name": "WP-42"},
            {"lat": 41.4284, "lon": -82.6671, "name": "WP-43"},
            {"lat": 41.4635, "lon": -82.694, "name": "WP-44"},
            {"lat": 41.4988, "lon": -82.7205, "name": "WP-45"},
            {"lat": 41.5244, "lon": -82.7591, "name": "WP-46"},
            {"lat": 41.5421, "lon": -82.8078, "name": "WP-47"},
            {"lat": 41.5386, "lon": -82.8557, "name": "WP-48"},
            {"lat": 41.5191, "lon": -82.9032, "name": "WP-49"},
            {"lat": 41.5057, "lon": -82.9502, "name": "WP-50"},
            {"lat": 41.5291, "lon": -82.9943, "name": "WP-51"},
            {"lat": 41.5525, "lon": -83.0385, "name": "WP-52"},
            {"lat": 41.5759, "lon": -83.0826, "name": "WP-53"},
            {"lat": 41.592, "lon": -83.1318, "name": "WP-54"},
            {"lat": 41.6052, "lon": -83.1829, "name": "WP-55"},
            {"lat": 41.6184, "lon": -83.2341, "name": "WP-56"},
            {"lat": 41.6315, "lon": -83.2854, "name": "WP-57"},
            {"lat": 41.6445, "lon": -83.3367, "name": "WP-58"},
            {"lat": 41.6575, "lon": -83.388, "name": "WP-59"},
            {"lat": 41.6679, "lon": -83.4403, "name": "WP-60"},
            {"lat": 41.6766, "lon": -83.4933, "name": "WP-61"},
            {"lat": 41.7153, "lon": -83.4934, "name": "WP-62"},
            {"lat": 41.7557, "lon": -83.4902, "name": "WP-63"},
            {"lat": 41.7936, "lon": -83.4713, "name": "WP-64"},
            {"lat": 41.8316, "lon": -83.4523, "name": "WP-65"},
            {"lat": 41.8661, "lon": -83.4246, "name": "WP-66"},
            {"lat": 41.8991, "lon": -83.393, "name": "WP-67"},
            {"lat": 41.9321, "lon": -83.3615, "name": "WP-68"},
            {"lat": 41.9611, "lon": -83.3236, "name": "WP-69"},
            {"lat": 41.9898, "lon": -83.2851, "name": "WP-70"},
            {"lat": 42.0238, "lon": -83.2567, "name": "WP-71"},
            {"lat": 42.0602, "lon": -83.2327, "name": "WP-72"},
            {"lat": 42.0965, "lon": -83.2087, "name": "WP-73"},
            {"lat": 42.1353, "lon": -83.1965, "name": "WP-74"},
            {"lat": 42.1757, "lon": -83.1917, "name": "WP-75"},
            {"lat": 42.216, "lon": -83.187, "name": "WP-76"},
            {"lat": 42.2511, "lon": -83.1626, "name": "WP-77"},
            {"lat": 42.2844, "lon": -83.1314, "name": "WP-78"},
            {"lat": 42.313, "lon": -83.0936, "name": "WP-79"},
            {"lat": 42.3376, "lon": -83.0502, "name": "WP-80"},
            {"lat": 42.3591, "lon": -83.0039, "name": "WP-81"},
            {"lat": 42.3788, "lon": -82.956, "name": "WP-82"},
            {"lat": 42.4012, "lon": -82.9116, "name": "WP-83"},
            {"lat": 42.4361, "lon": -82.8837, "name": "WP-84"},
            {"lat": 42.4747, "lon": -82.8938, "name": "WP-85"},
            {"lat": 42.5131, "lon": -82.9006, "name": "WP-86"},
            {"lat": 42.5486, "lon": -82.874, "name": "WP-87"},
            {"lat": 42.5841, "lon": -82.8476, "name": "WP-88"},
            {"lat": 42.623, "lon": -82.8323, "name": "WP-89"},
            {"lat": 42.6561, "lon": -82.8054, "name": "WP-90"},
            {"lat": 42.6808, "lon": -82.7616, "name": "WP-91"},
            {"lat": 42.6985, "lon": -82.7131, "name": "WP-92"},
            {"lat": 42.7004, "lon": -82.6623, "name": "WP-93"},
            {"lat": 42.6776, "lon": -82.6167, "name": "WP-94"},
            {"lat": 42.6446, "lon": -82.6015, "name": "WP-95"},
            {"lat": 42.6056, "lon": -82.6154, "name": "WP-96"},
            {"lat": 42.5834, "lon": -82.6254, "name": "WP-97"},
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
