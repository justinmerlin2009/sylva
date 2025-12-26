"""
Sylva Drone Flight Path Generator
Generates realistic GPS waypoints for drone survey missions
TamAir - Conrad Challenge 2026
"""

import json
import math
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import numpy as np

from .config import LOCATIONS, DRONE_SPECS, SIMULATION


class FlightPathGenerator:
    """Generate realistic drone flight paths for survey missions."""

    def __init__(self, location_key: str = None, custom_config: Dict = None):
        """
        Initialize flight path generator for a specific location or custom config.

        Args:
            location_key: Key from LOCATIONS config (e.g., 'stinson_beach', 'lake_erie')
            custom_config: Custom configuration dict for user-drawn paths
        """
        if custom_config:
            # Use custom config
            self.location = custom_config
            self.location_key = "custom"
        elif location_key:
            if location_key not in LOCATIONS:
                raise ValueError(f"Unknown location: {location_key}")
            self.location = LOCATIONS[location_key]
            self.location_key = location_key
        else:
            raise ValueError("Must provide either location_key or custom_config")

        self.waypoints = []
        self.flight_data = []

    def generate_path(self) -> List[Dict]:
        """
        Generate flight path based on location configuration.

        Returns:
            List of waypoint dictionaries with GPS coordinates and metadata
        """
        if self.location["flight_pattern"] == "lawnmower":
            return self._generate_lawnmower_pattern()
        elif self.location["flight_pattern"] == "corridor":
            return self._generate_corridor_pattern()
        else:
            raise ValueError(f"Unknown flight pattern: {self.location['flight_pattern']}")

    def _generate_lawnmower_pattern(self) -> List[Dict]:
        """Generate a lawnmower (parallel sweeps) flight pattern for area coverage."""
        bounds = self.location["bounds"]
        swath_width = self.location["swath_width_m"]
        altitude = self.location["survey_altitude_m"]
        speed = self.location["survey_speed_ms"]

        # Calculate the number of passes needed
        lat_range = bounds["north"] - bounds["south"]
        lon_range = bounds["east"] - bounds["west"]

        # Convert swath width to degrees (approximate)
        swath_deg = swath_width / 111320  # ~111km per degree latitude

        num_passes = int(lat_range / swath_deg) + 1

        waypoints = []
        start_time = datetime.fromisoformat(f"{SIMULATION['start_date']}T09:00:00")
        current_time = start_time

        for i in range(num_passes):
            lat = bounds["south"] + (i * swath_deg)
            lat = min(lat, bounds["north"])

            # Alternate direction for each pass
            if i % 2 == 0:
                start_lon, end_lon = bounds["west"], bounds["east"]
            else:
                start_lon, end_lon = bounds["east"], bounds["west"]

            # Start of pass
            waypoints.append({
                "lat": lat,
                "lon": start_lon,
                "altitude_m": altitude,
                "speed_ms": speed,
                "timestamp": current_time.isoformat(),
                "waypoint_type": "survey",
                "pass_number": i + 1,
            })

            # Calculate time to traverse
            distance = self._haversine_distance(lat, start_lon, lat, end_lon)
            travel_time = distance / speed
            current_time += timedelta(seconds=travel_time)

            # End of pass
            waypoints.append({
                "lat": lat,
                "lon": end_lon,
                "altitude_m": altitude,
                "speed_ms": speed,
                "timestamp": current_time.isoformat(),
                "waypoint_type": "survey",
                "pass_number": i + 1,
            })

            # Add turn time between passes
            current_time += timedelta(seconds=5)

        self.waypoints = waypoints
        return waypoints

    def _generate_corridor_pattern(self) -> List[Dict]:
        """Generate a corridor-following flight pattern for linear features (highways)."""
        base_waypoints = self.location["waypoints"]
        altitude = self.location["survey_altitude_m"]
        speed = self.location["survey_speed_ms"]

        waypoints = []
        start_time = datetime.fromisoformat(f"{SIMULATION['start_date']}T10:00:00")
        current_time = start_time

        for i, wp in enumerate(base_waypoints):
            waypoints.append({
                "lat": wp["lat"],
                "lon": wp["lon"],
                "altitude_m": altitude,
                "speed_ms": speed,
                "timestamp": current_time.isoformat(),
                "waypoint_type": "survey",
                "waypoint_name": wp["name"],
                "segment": i + 1,
            })

            # Calculate time to next waypoint
            if i < len(base_waypoints) - 1:
                next_wp = base_waypoints[i + 1]
                distance = self._haversine_distance(
                    wp["lat"], wp["lon"],
                    next_wp["lat"], next_wp["lon"]
                )
                travel_time = distance / speed
                current_time += timedelta(seconds=travel_time)

        # Interpolate intermediate points for ultra-smooth visualization
        # Use very small interval for buttery smooth drone animation
        detailed_waypoints = self._interpolate_waypoints(waypoints, interval_m=15)

        self.waypoints = detailed_waypoints
        return detailed_waypoints

    def _interpolate_waypoints(self, waypoints: List[Dict], interval_m: float) -> List[Dict]:
        """
        Interpolate additional waypoints between existing ones for smoother paths.

        Args:
            waypoints: Original waypoints
            interval_m: Distance between interpolated points in meters

        Returns:
            List of interpolated waypoints
        """
        if len(waypoints) < 2:
            return waypoints

        detailed = []

        for i in range(len(waypoints) - 1):
            wp1 = waypoints[i]
            wp2 = waypoints[i + 1]

            distance = self._haversine_distance(
                wp1["lat"], wp1["lon"],
                wp2["lat"], wp2["lon"]
            )

            num_points = max(2, int(distance / interval_m))

            for j in range(num_points):
                t = j / num_points
                lat = wp1["lat"] + t * (wp2["lat"] - wp1["lat"])
                lon = wp1["lon"] + t * (wp2["lon"] - wp1["lon"])

                # Interpolate timestamp
                t1 = datetime.fromisoformat(wp1["timestamp"])
                t2 = datetime.fromisoformat(wp2["timestamp"])
                interp_time = t1 + timedelta(seconds=(t2 - t1).total_seconds() * t)

                detailed.append({
                    "lat": lat,
                    "lon": lon,
                    "altitude_m": wp1["altitude_m"],
                    "speed_ms": wp1["speed_ms"],
                    "timestamp": interp_time.isoformat(),
                    "waypoint_type": "interpolated",
                    "segment": wp1.get("segment", i + 1),
                })

        # Add the last waypoint
        detailed.append(waypoints[-1])

        return detailed

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great-circle distance between two points in meters.

        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates

        Returns:
            Distance in meters
        """
        R = 6371000  # Earth's radius in meters

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def get_total_distance(self) -> float:
        """Calculate total flight path distance in meters."""
        if len(self.waypoints) < 2:
            return 0

        total = 0
        for i in range(len(self.waypoints) - 1):
            total += self._haversine_distance(
                self.waypoints[i]["lat"], self.waypoints[i]["lon"],
                self.waypoints[i + 1]["lat"], self.waypoints[i + 1]["lon"]
            )
        return total

    def get_flight_duration(self) -> float:
        """Calculate total flight duration in seconds."""
        if len(self.waypoints) < 2:
            return 0

        start = datetime.fromisoformat(self.waypoints[0]["timestamp"])
        end = datetime.fromisoformat(self.waypoints[-1]["timestamp"])
        return (end - start).total_seconds()

    def to_geojson(self) -> Dict:
        """
        Export flight path as GeoJSON.

        Returns:
            GeoJSON FeatureCollection with LineString and Point features
        """
        if not self.waypoints:
            self.generate_path()

        # Create LineString for the path
        coordinates = [[wp["lon"], wp["lat"]] for wp in self.waypoints]

        line_feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates,
            },
            "properties": {
                "flight_id": f"SYLVA-{self.location_key.upper()[:3]}-001",
                "location": self.location["name"],
                "type": self.location["type"],
                "altitude_m": self.location["survey_altitude_m"],
                "total_distance_m": self.get_total_distance(),
                "duration_seconds": self.get_flight_duration(),
                "start_time": self.waypoints[0]["timestamp"],
                "end_time": self.waypoints[-1]["timestamp"],
            },
        }

        # Create Point features for key waypoints
        point_features = []
        for i, wp in enumerate(self.waypoints):
            if wp.get("waypoint_type") != "interpolated" or i == 0 or i == len(self.waypoints) - 1:
                point_features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [wp["lon"], wp["lat"]],
                    },
                    "properties": {
                        "timestamp": wp["timestamp"],
                        "altitude_m": wp["altitude_m"],
                        "waypoint_name": wp.get("waypoint_name", f"WP-{i+1}"),
                        "waypoint_type": wp.get("waypoint_type", "unknown"),
                    },
                })

        return {
            "type": "FeatureCollection",
            "features": [line_feature] + point_features,
        }

    def to_animation_data(self) -> List[Dict]:
        """
        Export flight path as animation-friendly data.

        Returns:
            List of frame data for animation
        """
        if not self.waypoints:
            self.generate_path()

        frames = []
        start_time = datetime.fromisoformat(self.waypoints[0]["timestamp"])

        for wp in self.waypoints:
            wp_time = datetime.fromisoformat(wp["timestamp"])
            elapsed = (wp_time - start_time).total_seconds()

            frames.append({
                "lat": wp["lat"],
                "lon": wp["lon"],
                "altitude": wp["altitude_m"],
                "elapsed_seconds": elapsed,
                "timestamp": wp["timestamp"],
            })

        return frames


def generate_all_flight_paths() -> Dict[str, Dict]:
    """Generate flight paths for all configured locations."""
    paths = {}

    for location_key in LOCATIONS:
        generator = FlightPathGenerator(location_key)
        generator.generate_path()
        paths[location_key] = {
            "geojson": generator.to_geojson(),
            "animation": generator.to_animation_data(),
            "stats": {
                "total_distance_m": generator.get_total_distance(),
                "duration_seconds": generator.get_flight_duration(),
                "waypoint_count": len(generator.waypoints),
            },
        }

    return paths


if __name__ == "__main__":
    # Test flight path generation
    for location in LOCATIONS:
        print(f"\n{'='*50}")
        print(f"Generating flight path for: {LOCATIONS[location]['name']}")
        print('='*50)

        generator = FlightPathGenerator(location)
        waypoints = generator.generate_path()

        print(f"Waypoints generated: {len(waypoints)}")
        print(f"Total distance: {generator.get_total_distance()/1000:.2f} km")
        print(f"Flight duration: {generator.get_flight_duration()/60:.1f} minutes")

        geojson = generator.to_geojson()
        print(f"GeoJSON features: {len(geojson['features'])}")
