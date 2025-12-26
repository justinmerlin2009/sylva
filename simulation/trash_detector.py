"""
Sylva Trash Detection Simulator
Generates realistic trash detection data based on environmental factors
TamAir - Conrad Challenge 2026
"""

import json
import math
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import numpy as np

from .config import (
    TRASH_CATEGORIES,
    DETECTION_PARAMS,
    PRIORITY_THRESHOLDS,
    LOCATIONS,
    SIMULATION,
)


class TrashDetector:
    """Simulate trash detection from drone imagery."""

    def __init__(self, location_key: str, seed: Optional[int] = None):
        """
        Initialize trash detector for a specific location.

        Args:
            location_key: Key from LOCATIONS config
            seed: Random seed for reproducibility
        """
        if location_key not in LOCATIONS:
            raise ValueError(f"Unknown location: {location_key}")

        self.location = LOCATIONS[location_key]
        self.location_key = location_key
        self.env_type = self.location["type"]

        # Set random seed for reproducibility
        self.seed = seed or SIMULATION["random_seed"]
        random.seed(self.seed)
        np.random.seed(self.seed)

        self.detections = []

        # Define hotspot areas (areas with higher trash density)
        self._define_hotspots()

    def _define_hotspots(self):
        """Define areas with elevated trash density based on location type."""
        if self.env_type == "beach":
            # Beach hotspots along entire Stinson Beach coastline (3.5 miles)
            # Creating heterogeneous density with major and minor hotspots
            self.hotspots = [
                # NORTHERN SECTION - Seadrift
                {
                    "lat": 37.9070,
                    "lon": -122.6500,
                    "radius_m": 150,
                    "multiplier": 3.5,
                    "name": "Seadrift Lagoon Debris",
                    "primary_trash": ["organic_waste", "plastic_bottle"],
                },
                {
                    "lat": 37.9045,
                    "lon": -122.6485,
                    "radius_m": 100,
                    "multiplier": 4.0,
                    "name": "Seadrift Party Beach",
                    "primary_trash": ["glass", "plastic_bottle", "food_packaging"],
                },
                # MAIN BEACH SECTION - highest activity
                {
                    "lat": 37.9015,
                    "lon": -122.6460,
                    "radius_m": 180,
                    "multiplier": 6.0,
                    "name": "North Beach Parking",
                    "primary_trash": ["food_packaging", "plastic_bottle"],
                },
                {
                    "lat": 37.8990,
                    "lon": -122.6435,
                    "radius_m": 220,
                    "multiplier": 7.0,
                    "name": "Main Beach - Heavy Use",
                    "primary_trash": ["plastic_bottle", "food_packaging", "textile"],
                },
                {
                    "lat": 37.8965,
                    "lon": -122.6415,
                    "radius_m": 120,
                    "multiplier": 5.0,
                    "name": "Lifeguard Station Area",
                    "primary_trash": ["plastic_bottle", "food_packaging"],
                },
                # CENTRAL SECTION
                {
                    "lat": 37.8940,
                    "lon": -122.6395,
                    "radius_m": 100,
                    "multiplier": 3.0,
                    "name": "Central Beach Access",
                    "primary_trash": ["plastic_bottle", "textile"],
                },
                {
                    "lat": 37.8915,
                    "lon": -122.6375,
                    "radius_m": 90,
                    "multiplier": 3.5,
                    "name": "South Beach Picnic",
                    "primary_trash": ["food_packaging", "glass"],
                },
                # SOUTHERN SECTION - Easkoot Creek and beyond
                {
                    "lat": 37.8890,
                    "lon": -122.6355,
                    "radius_m": 200,
                    "multiplier": 5.5,
                    "name": "Easkoot Creek Dumping",
                    "primary_trash": ["tire", "construction_waste", "metal_debris"],
                },
                {
                    "lat": 37.8865,
                    "lon": -122.6330,
                    "radius_m": 80,
                    "multiplier": 2.5,
                    "name": "Willow Camp Debris",
                    "primary_trash": ["organic_waste", "textile"],
                },
                {
                    "lat": 37.8830,
                    "lon": -122.6295,
                    "radius_m": 150,
                    "multiplier": 4.0,
                    "name": "South Point Illegal Dump",
                    "primary_trash": ["construction_waste", "tire", "metal_debris"],
                },
            ]
        elif self.env_type == "urban_waterfront":
            # NASA Clear Lake / Houston urban waterfront hotspots
            self.hotspots = [
                {
                    "lat": 29.5480,
                    "lon": -95.0920,
                    "radius_m": 200,
                    "multiplier": 4.0,
                    "name": "NASA Parkway Roadside",
                    "primary_trash": ["plastic_bottle", "food_packaging", "metal_debris"],
                },
                {
                    "lat": 29.5450,
                    "lon": -95.0850,
                    "radius_m": 250,
                    "multiplier": 5.0,
                    "name": "Clear Lake Park",
                    "primary_trash": ["food_packaging", "plastic_bottle", "glass"],
                },
                {
                    "lat": 29.5400,
                    "lon": -95.0780,
                    "radius_m": 300,
                    "multiplier": 6.0,
                    "name": "Marina Dumping",
                    "primary_trash": ["tire", "metal_debris", "construction_waste"],
                },
                {
                    "lat": 29.5300,
                    "lon": -95.0650,
                    "radius_m": 200,
                    "multiplier": 3.5,
                    "name": "Seabrook Waterfront",
                    "primary_trash": ["plastic_bottle", "organic_waste"],
                },
                {
                    "lat": 29.5250,
                    "lon": -95.0520,
                    "radius_m": 350,
                    "multiplier": 7.0,
                    "name": "Kemah Boardwalk Area",
                    "primary_trash": ["food_packaging", "plastic_bottle", "glass", "textile"],
                },
                {
                    "lat": 29.5220,
                    "lon": -95.0450,
                    "radius_m": 250,
                    "multiplier": 4.5,
                    "name": "Bay Shoreline",
                    "primary_trash": ["plastic_bottle", "organic_waste", "tire"],
                },
            ]
        else:
            # Highway hotspots for 10-mile Route 66 section near Needles
            self.hotspots = [
                {
                    "lat": 34.8480,
                    "lon": -114.6147,
                    "radius_m": 250,
                    "multiplier": 4.5,
                    "name": "Needles Downtown Exit",
                    "primary_trash": ["food_packaging", "plastic_bottle", "tire"],
                },
                {
                    "lat": 34.8550,
                    "lon": -114.5850,
                    "radius_m": 180,
                    "multiplier": 3.0,
                    "name": "East Needles Pullout",
                    "primary_trash": ["plastic_bottle", "metal_debris"],
                },
                {
                    "lat": 34.8650,
                    "lon": -114.5550,
                    "radius_m": 300,
                    "multiplier": 5.0,
                    "name": "Desert Rest Stop",
                    "primary_trash": ["food_packaging", "plastic_bottle", "tire"],
                },
                {
                    "lat": 34.8694,
                    "lon": -114.5289,
                    "radius_m": 200,
                    "multiplier": 4.0,
                    "name": "AZ State Line Welcome",
                    "primary_trash": ["plastic_bottle", "food_packaging"],
                },
                {
                    "lat": 34.8820,
                    "lon": -114.4800,
                    "radius_m": 350,
                    "multiplier": 6.0,
                    "name": "Historic Marker Dumping",
                    "primary_trash": ["tire", "construction_waste", "metal_debris"],
                },
            ]

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in meters."""
        R = 6371000
        lat1_rad, lat2_rad = math.radians(lat1), math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def _get_density_multiplier(self, lat: float, lon: float) -> float:
        """Get detection density multiplier based on proximity to hotspots."""
        max_multiplier = 1.0

        for hotspot in self.hotspots:
            distance = self._haversine_distance(lat, lon, hotspot["lat"], hotspot["lon"])
            if distance < hotspot["radius_m"]:
                # Linear falloff from center
                factor = 1 - (distance / hotspot["radius_m"])
                multiplier = 1 + (hotspot["multiplier"] - 1) * factor
                max_multiplier = max(max_multiplier, multiplier)

        return max_multiplier

    def _select_category(self, lat: float = None, lon: float = None) -> str:
        """Select a trash category based on environment and hotspot-specific probabilities."""
        prob_key = f"{self.env_type}_probability"
        categories = list(TRASH_CATEGORIES.keys())
        probabilities = [TRASH_CATEGORIES[cat][prob_key] for cat in categories]

        # Check if we're in a hotspot with specific trash types
        if lat is not None and lon is not None:
            for hotspot in self.hotspots:
                distance = self._haversine_distance(lat, lon, hotspot["lat"], hotspot["lon"])
                if distance < hotspot["radius_m"] and "primary_trash" in hotspot:
                    # Boost probabilities for primary trash types in this hotspot
                    for i, cat in enumerate(categories):
                        if cat in hotspot["primary_trash"]:
                            probabilities[i] *= 3.0  # Triple probability for primary types

        # Normalize probabilities
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]

        return np.random.choice(categories, p=probabilities)

    def _generate_detection(self, lat: float, lon: float, timestamp: str, flight_id: str) -> Dict:
        """Generate a single trash detection with all metadata."""
        category = self._select_category(lat, lon)
        cat_data = TRASH_CATEGORIES[category]

        # Generate size with some variation
        base_size = cat_data["avg_size_m2"]
        size = base_size * np.random.uniform(0.5, 2.0)

        # Generate weight within range
        weight_min, weight_max = cat_data["weight_range_kg"]
        weight = np.random.uniform(weight_min, weight_max)

        # Generate confidence score
        conf_min, conf_max = DETECTION_PARAMS["confidence_range"]
        confidence = np.random.uniform(conf_min, conf_max)

        # Calculate priority based on various factors
        priority = self._calculate_priority(lat, lon, weight, size)

        # Add small random offset to exact position (simulating detection uncertainty)
        lat_offset = np.random.uniform(-0.00005, 0.00005)
        lon_offset = np.random.uniform(-0.00005, 0.00005)

        detection_id = f"DET-{datetime.now().strftime('%Y')}-{uuid.uuid4().hex[:8].upper()}"

        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon + lon_offset, lat + lat_offset],
            },
            "properties": {
                "id": detection_id,
                "timestamp": timestamp,
                "category": category,
                "category_name": cat_data["name"],
                "confidence": round(confidence, 3),
                "size_m2": round(size, 4),
                "estimated_weight_kg": round(weight, 3),
                "priority": priority,
                "color": cat_data["color"],
                "flight_id": flight_id,
                "environment": self.env_type,
                "location": self.location["name"],
            },
        }

    def _calculate_priority(self, lat: float, lon: float, weight: float, size: float) -> str:
        """Calculate priority level based on weight, size, and location sensitivity."""
        # Base score from weight
        score = 0

        if weight > 10:
            score += 40
        elif weight > 5:
            score += 30
        elif weight > 1:
            score += 20
        else:
            score += 10

        # Add score from size
        if size > 0.3:
            score += 30
        elif size > 0.1:
            score += 20
        elif size > 0.05:
            score += 10

        # Add score from location sensitivity
        density_mult = self._get_density_multiplier(lat, lon)
        if density_mult > 3:
            score += 20  # In a major hotspot
        elif density_mult > 2:
            score += 10

        # Beach environments are more sensitive
        if self.env_type == "beach":
            score += 10

        # Determine priority level
        if score >= 70:
            return "critical"
        elif score >= 50:
            return "high"
        elif score >= 30:
            return "medium"
        else:
            return "low"

    def generate_detections_for_path(self, waypoints: List[Dict], flight_id: str) -> List[Dict]:
        """
        Generate SPARSE, realistic trash detections along a flight path.

        Creates a small number of discrete detections (50-80 total) that
        represent individual trash items found during the survey.

        Args:
            waypoints: List of waypoint dictionaries from flight path
            flight_id: Unique identifier for this flight

        Returns:
            List of detection features in GeoJSON format
        """
        detections = []

        # Target: 75-95 detections total (20% increase for better coverage)
        target_detections = random.randint(75, 95)

        # Calculate total path length and spacing
        total_waypoints = len(waypoints)
        if total_waypoints == 0:
            return detections

        # Distribute detections across the path, weighted by hotspots
        # First, calculate detection probability at each waypoint
        detection_weights = []
        for wp in waypoints:
            weight = 0.1  # Base probability (very low outside hotspots)

            # Check proximity to hotspots
            for hotspot in self.hotspots:
                distance = self._haversine_distance(wp["lat"], wp["lon"],
                                                    hotspot["lat"], hotspot["lon"])
                if distance < hotspot["radius_m"]:
                    # Higher weight near hotspot centers
                    factor = 1 - (distance / hotspot["radius_m"])
                    weight = max(weight, factor * hotspot["multiplier"])

            detection_weights.append(weight)

        # Normalize weights to probabilities
        total_weight = sum(detection_weights)
        if total_weight > 0:
            probs = [w / total_weight for w in detection_weights]
        else:
            probs = [1 / total_waypoints] * total_waypoints

        # Select waypoint indices for detections
        selected_indices = np.random.choice(
            total_waypoints,
            size=min(target_detections, total_waypoints),
            replace=False,
            p=probs
        )

        # Generate detections at selected positions
        altitude = self.location.get("survey_altitude_m", 120)
        footprint_width = altitude * 0.5  # Smaller scatter for cleaner look

        for idx in sorted(selected_indices):
            wp = waypoints[idx]
            lat, lon = wp["lat"], wp["lon"]
            timestamp = wp["timestamp"]

            # Small random offset
            offset_lat = np.random.uniform(-footprint_width/2, footprint_width/2) / 111320
            offset_lon = np.random.uniform(-footprint_width/2, footprint_width/2) / (111320 * math.cos(math.radians(lat)))

            detection = self._generate_detection(
                lat + offset_lat,
                lon + offset_lon,
                timestamp,
                flight_id
            )
            detections.append(detection)

        self.detections = detections
        return detections

    def generate_analysis_zones(self) -> List[Dict]:
        """
        Generate analysis zones that summarize trash density areas.

        These are larger markers that appear after scanning an area,
        showing where dangerous trash concentrations were found.

        Returns:
            List of analysis zone features in GeoJSON format
        """
        zones = []

        # Create analysis zones from hotspots that have detections nearby
        for hotspot in self.hotspots:
            # Count detections near this hotspot
            nearby_detections = []
            total_weight = 0

            for det in self.detections:
                coords = det["geometry"]["coordinates"]
                det_lat, det_lon = coords[1], coords[0]
                distance = self._haversine_distance(
                    det_lat, det_lon,
                    hotspot["lat"], hotspot["lon"]
                )
                if distance < hotspot["radius_m"] * 1.5:
                    nearby_detections.append(det)
                    total_weight += det["properties"]["estimated_weight_kg"]

            if len(nearby_detections) >= 3:  # Minimum to create a zone
                # Calculate danger level based on count and weight
                if len(nearby_detections) >= 10 or total_weight >= 20:
                    danger_level = "critical"
                    color = "#e74c3c"
                elif len(nearby_detections) >= 6 or total_weight >= 10:
                    danger_level = "high"
                    color = "#e67e22"
                elif len(nearby_detections) >= 3 or total_weight >= 5:
                    danger_level = "medium"
                    color = "#f39c12"
                else:
                    danger_level = "low"
                    color = "#27ae60"

                zones.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [hotspot["lon"], hotspot["lat"]],
                    },
                    "properties": {
                        "zone_id": f"ZONE-{len(zones)+1:02d}",
                        "name": hotspot.get("name", f"Analysis Zone {len(zones)+1}"),
                        "detection_count": len(nearby_detections),
                        "total_weight_kg": round(total_weight, 2),
                        "danger_level": danger_level,
                        "color": color,
                        "radius_m": hotspot["radius_m"],
                        "recommendation": self._get_zone_recommendation(danger_level, total_weight),
                    },
                })

        return zones

    def _get_zone_recommendation(self, danger_level: str, weight: float) -> str:
        """Generate a recommendation for an analysis zone."""
        if danger_level == "critical":
            return f"URGENT: Heavy debris concentration ({weight:.1f}kg). Immediate cleanup recommended."
        elif danger_level == "high":
            return f"High priority cleanup area. Estimated {weight:.1f}kg of waste."
        elif danger_level == "medium":
            return f"Moderate debris. Schedule routine cleanup."
        else:
            return f"Light debris detected. Monitor during next survey."

    def _generate_micro_clusters(self, waypoints: List[Dict]) -> List[Dict]:
        """
        Generate random micro-clusters along the path to create
        realistic scattered trash pockets between major hotspots.
        """
        if not waypoints:
            return []

        micro_clusters = []
        total_waypoints = len(waypoints)

        # Create 3-8 random micro-clusters along the path
        num_clusters = random.randint(3, 8)

        for _ in range(num_clusters):
            # Pick a random waypoint
            idx = random.randint(0, total_waypoints - 1)
            wp = waypoints[idx]

            # Don't place micro-cluster too close to existing hotspots
            too_close = False
            for hotspot in self.hotspots:
                dist = self._haversine_distance(wp["lat"], wp["lon"],
                                                hotspot["lat"], hotspot["lon"])
                if dist < hotspot["radius_m"] * 1.5:
                    too_close = True
                    break

            if not too_close:
                micro_clusters.append({
                    "lat": wp["lat"] + random.uniform(-0.001, 0.001),
                    "lon": wp["lon"] + random.uniform(-0.001, 0.001),
                    "radius_m": random.randint(30, 80),
                    "multiplier": random.uniform(1.5, 3.0),
                })

        return micro_clusters

    def get_statistics(self) -> Dict:
        """Calculate summary statistics for detections."""
        if not self.detections:
            return {}

        categories_count = {}
        priorities_count = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        total_weight = 0
        total_size = 0

        for det in self.detections:
            props = det["properties"]

            # Count by category
            cat = props["category"]
            categories_count[cat] = categories_count.get(cat, 0) + 1

            # Count by priority
            priorities_count[props["priority"]] += 1

            # Sum totals
            total_weight += props["estimated_weight_kg"]
            total_size += props["size_m2"]

        # Calculate category breakdown with percentages
        category_breakdown = []
        for cat, count in sorted(categories_count.items(), key=lambda x: -x[1]):
            cat_data = TRASH_CATEGORIES[cat]
            category_breakdown.append({
                "category": cat,
                "name": cat_data["name"],
                "count": count,
                "percentage": round(100 * count / len(self.detections), 1),
                "color": cat_data["color"],
            })

        return {
            "total_detections": len(self.detections),
            "total_estimated_weight_kg": round(total_weight, 2),
            "total_area_m2": round(total_size, 2),
            "by_category": category_breakdown,
            "by_priority": priorities_count,
            "location": self.location["name"],
            "environment_type": self.env_type,
        }

    def get_clusters(self, eps_meters: float = 50, min_samples: int = 5) -> List[Dict]:
        """
        Identify high-density trash clusters using a simple clustering approach.

        Args:
            eps_meters: Maximum distance between points in a cluster
            min_samples: Minimum points to form a cluster

        Returns:
            List of cluster centers with statistics
        """
        if len(self.detections) < min_samples:
            return []

        # Simple grid-based clustering
        grid_size = eps_meters / 111320  # Convert meters to degrees (approximate)
        grid_cells = {}

        for det in self.detections:
            coords = det["geometry"]["coordinates"]
            lon, lat = coords[0], coords[1]

            # Assign to grid cell
            cell_x = int(lon / grid_size)
            cell_y = int(lat / grid_size)
            cell_key = (cell_x, cell_y)

            if cell_key not in grid_cells:
                grid_cells[cell_key] = []
            grid_cells[cell_key].append(det)

        # Find significant clusters
        clusters = []
        for cell_key, cell_detections in grid_cells.items():
            if len(cell_detections) >= min_samples:
                # Calculate cluster center and stats
                lats = [d["geometry"]["coordinates"][1] for d in cell_detections]
                lons = [d["geometry"]["coordinates"][0] for d in cell_detections]
                weights = [d["properties"]["estimated_weight_kg"] for d in cell_detections]

                center_lat = sum(lats) / len(lats)
                center_lon = sum(lons) / len(lons)

                # Determine cluster priority
                total_weight = sum(weights)
                density = len(cell_detections) / (grid_size * grid_size * 111320 * 111320 / 10000)  # per 100m²

                if density > PRIORITY_THRESHOLDS["critical"]["min_density"]:
                    priority = "critical"
                elif density > PRIORITY_THRESHOLDS["high"]["min_density"]:
                    priority = "high"
                elif density > PRIORITY_THRESHOLDS["medium"]["min_density"]:
                    priority = "medium"
                else:
                    priority = "low"

                clusters.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [center_lon, center_lat],
                    },
                    "properties": {
                        "cluster_id": f"CLU-{len(clusters)+1:03d}",
                        "detection_count": len(cell_detections),
                        "total_weight_kg": round(total_weight, 2),
                        "density_per_100m2": round(density, 2),
                        "priority": priority,
                        "radius_m": eps_meters,
                    },
                })

        # Sort by detection count
        clusters.sort(key=lambda x: -x["properties"]["detection_count"])

        return clusters

    def to_geojson(self) -> Dict:
        """Export detections as GeoJSON FeatureCollection."""
        return {
            "type": "FeatureCollection",
            "features": self.detections,
            "properties": {
                "location": self.location["name"],
                "total_detections": len(self.detections),
                "generated_at": datetime.now().isoformat(),
            },
        }

    def simulate_detections(self, flight_path: Dict, config: Dict) -> Dict:
        """
        Generate detections for a custom flight path.
        Used for user-drawn custom paths.

        Args:
            flight_path: GeoJSON flight path with LineString
            config: Custom configuration dict

        Returns:
            GeoJSON FeatureCollection of detections
        """
        # Extract waypoints from flight path with proper timestamps
        waypoints = []
        speed = config.get("survey_speed_ms", 25)  # meters per second
        start_time = datetime.now()
        elapsed_seconds = 0

        if flight_path.get("features"):
            for feature in flight_path["features"]:
                if feature["geometry"]["type"] == "LineString":
                    coords = feature["geometry"]["coordinates"]
                    for i, coord in enumerate(coords):
                        # Calculate elapsed time based on distance from previous point
                        if i > 0:
                            prev_coord = coords[i - 1]
                            distance = self._haversine_distance(
                                prev_coord[1], prev_coord[0],
                                coord[1], coord[0]
                            )
                            elapsed_seconds += distance / speed

                        timestamp = start_time + timedelta(seconds=elapsed_seconds)

                        waypoints.append({
                            "lat": coord[1],
                            "lon": coord[0],
                            "timestamp": timestamp.isoformat(),
                        })

        if not waypoints:
            return {"type": "FeatureCollection", "features": []}

        # Generate micro-clusters for custom path (no predefined hotspots)
        self.hotspots = []  # Clear hotspots for custom paths

        # Create random trash pockets along the custom path
        num_clusters = random.randint(2, 5)
        for _ in range(num_clusters):
            idx = random.randint(0, len(waypoints) - 1)
            wp = waypoints[idx]
            self.hotspots.append({
                "lat": wp["lat"],
                "lon": wp["lon"],
                "radius_m": random.randint(50, 150),
                "multiplier": random.uniform(3.0, 6.0),
                "name": f"Trash Pocket",
                "primary_trash": random.sample(list(TRASH_CATEGORIES.keys()), 3),
            })

        # Generate detections
        flight_id = f"CUSTOM-{uuid.uuid4().hex[:6].upper()}"
        detections = self.generate_detections_for_path(waypoints, flight_id)

        return {
            "type": "FeatureCollection",
            "features": detections,
            "properties": {
                "location": config.get("name", "Custom Path"),
                "total_detections": len(detections),
                "generated_at": datetime.now().isoformat(),
            },
        }


if __name__ == "__main__":
    # Test trash detection simulation
    from .flight_paths import FlightPathGenerator

    for location in LOCATIONS:
        print(f"\n{'='*50}")
        print(f"Simulating trash detection for: {LOCATIONS[location]['name']}")
        print('='*50)

        # Generate flight path
        flight_gen = FlightPathGenerator(location)
        waypoints = flight_gen.generate_path()

        # Generate detections
        detector = TrashDetector(location)
        flight_id = f"SYLVA-{location.upper()[:3]}-001"
        detections = detector.generate_detections_for_path(waypoints, flight_id)

        print(f"Detections generated: {len(detections)}")

        stats = detector.get_statistics()
        print(f"Total estimated weight: {stats['total_estimated_weight_kg']} kg")
        print(f"\nBy category:")
        for cat in stats['by_category'][:5]:
            print(f"  {cat['name']}: {cat['count']} ({cat['percentage']}%)")

        print(f"\nBy priority:")
        for priority, count in stats['by_priority'].items():
            print(f"  {priority}: {count}")

        clusters = detector.get_clusters()
        print(f"\nHigh-density clusters found: {len(clusters)}")
