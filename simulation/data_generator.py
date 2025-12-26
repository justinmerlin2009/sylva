"""
Sylva Data Generator
Main entry point for generating simulation datasets
TamAir - Conrad Challenge 2026
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .config import LOCATIONS, SIMULATION
from .flight_paths import FlightPathGenerator
from .trash_detector import TrashDetector


class DataGenerator:
    """Generate complete simulation datasets for all locations."""

    def __init__(self, output_dir: str = "data"):
        """
        Initialize data generator.

        Args:
            output_dir: Directory to save generated data
        """
        self.output_dir = Path(output_dir)
        self.flights_dir = self.output_dir / "flights"
        self.detections_dir = self.output_dir / "detections"
        self.summary_dir = self.output_dir / "summary"

        # Create directories if they don't exist
        for dir_path in [self.flights_dir, self.detections_dir, self.summary_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        self.all_flights = {}
        self.all_detections = {}
        self.all_stats = {}
        self.all_clusters = {}

    def generate_all(self, seed: Optional[int] = None) -> Dict:
        """
        Generate data for all configured locations.

        Args:
            seed: Random seed for reproducibility

        Returns:
            Summary of all generated data
        """
        seed = seed or SIMULATION["random_seed"]
        summary = {
            "generated_at": datetime.now().isoformat(),
            "seed": seed,
            "locations": {},
        }

        for location_key in LOCATIONS:
            print(f"\nGenerating data for: {LOCATIONS[location_key]['name']}")
            location_data = self.generate_location(location_key, seed)
            summary["locations"][location_key] = location_data

        # Generate combined datasets
        self._generate_combined_data()

        # Save summary
        summary_path = self.summary_dir / "generation_summary.json"
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"\nData generation complete!")
        print(f"Files saved to: {self.output_dir}")

        return summary

    def generate_location(self, location_key: str, seed: Optional[int] = None) -> Dict:
        """
        Generate data for a single location.

        Args:
            location_key: Key from LOCATIONS config
            seed: Random seed for reproducibility

        Returns:
            Summary of generated data for this location
        """
        flight_id = f"SYLVA-{location_key.upper()[:3]}-001"

        # Check for existing animation file (custom paths)
        animation_path = self.flights_dir / f"{location_key}_animation.json"
        flight_path_file = self.flights_dir / f"{location_key}_flight.geojson"

        if animation_path.exists() and flight_path_file.exists():
            # Use existing custom flight paths
            print(f"  Loading existing flight path...")
            with open(animation_path, "r") as f:
                animation_data = json.load(f)
            with open(flight_path_file, "r") as f:
                flight_geojson = json.load(f)

            # Convert animation frames to waypoints format for detection generation
            env_type = LOCATIONS[location_key].get("type", "beach")
            if env_type == "urban_waterfront":
                target_waypoints = 130
            else:
                target_waypoints = 110
            sample_rate = max(1, len(animation_data) // target_waypoints)

            waypoints = []
            for i in range(0, len(animation_data), sample_rate):
                frame = animation_data[i]
                waypoints.append({
                    "lat": frame["lat"],
                    "lon": frame["lon"],
                    "timestamp": frame.get("timestamp", "2026-01-15T10:00:00"),
                    "name": f"WP-{len(waypoints)+1}"
                })
        else:
            # Generate new flight path from config
            print(f"  Generating flight path...")
            flight_gen = FlightPathGenerator(location_key)
            waypoints = flight_gen.generate_path()

            flight_geojson = flight_gen.to_geojson()
            animation_data = flight_gen.to_animation_data()

            # Save flight data
            with open(flight_path_file, "w") as f:
                json.dump(flight_geojson, f, indent=2)

            with open(animation_path, "w") as f:
                json.dump(animation_data, f, indent=2)

        self.all_flights[location_key] = {
            "geojson": flight_geojson,
            "animation": animation_data,
        }

        # Generate detections
        print(f"  Generating trash detections...")
        detector = TrashDetector(location_key, seed=seed)
        detections = detector.generate_detections_for_path(waypoints, flight_id)

        detections_geojson = detector.to_geojson()
        stats = detector.get_statistics()
        clusters = detector.get_clusters()

        # Save detection data
        detections_path = self.detections_dir / f"{location_key}_detections.geojson"
        with open(detections_path, "w") as f:
            json.dump(detections_geojson, f, indent=2)

        clusters_path = self.detections_dir / f"{location_key}_clusters.geojson"
        clusters_geojson = {
            "type": "FeatureCollection",
            "features": clusters,
        }
        with open(clusters_path, "w") as f:
            json.dump(clusters_geojson, f, indent=2)

        stats_path = self.summary_dir / f"{location_key}_stats.json"
        with open(stats_path, "w") as f:
            json.dump(stats, f, indent=2)

        self.all_detections[location_key] = detections_geojson
        self.all_stats[location_key] = stats
        self.all_clusters[location_key] = clusters_geojson

        # Get distance and duration from flight data
        if flight_geojson.get("features"):
            props = flight_geojson["features"][0].get("properties", {})
            distance_km = round(props.get("total_distance_m", 0) / 1000, 2)
            duration_minutes = round(props.get("duration_seconds", 0) / 60, 1)
        else:
            distance_km = 0
            duration_minutes = 0

        location_summary = {
            "flight_id": flight_id,
            "waypoints": len(waypoints),
            "distance_km": distance_km,
            "duration_minutes": duration_minutes,
            "detections": len(detections),
            "estimated_weight_kg": stats.get("total_estimated_weight_kg", 0),
            "clusters": len(clusters),
        }

        print(f"  Generated {len(detections)} detections, {len(clusters)} clusters")

        return location_summary

    def _generate_combined_data(self):
        """Generate combined datasets from all locations."""
        # Combine all detections
        all_features = []
        for location_key, geojson in self.all_detections.items():
            all_features.extend(geojson["features"])

        combined_detections = {
            "type": "FeatureCollection",
            "features": all_features,
            "properties": {
                "total_detections": len(all_features),
                "locations": list(self.all_detections.keys()),
                "generated_at": datetime.now().isoformat(),
            },
        }

        combined_path = self.detections_dir / "all_detections.geojson"
        with open(combined_path, "w") as f:
            json.dump(combined_detections, f, indent=2)

        # Combine all flights
        all_flight_features = []
        for location_key, flight_data in self.all_flights.items():
            all_flight_features.extend(flight_data["geojson"]["features"])

        combined_flights = {
            "type": "FeatureCollection",
            "features": all_flight_features,
        }

        combined_flights_path = self.flights_dir / "all_flights.geojson"
        with open(combined_flights_path, "w") as f:
            json.dump(combined_flights, f, indent=2)

        # Combine all clusters
        all_cluster_features = []
        for location_key, clusters in self.all_clusters.items():
            all_cluster_features.extend(clusters["features"])

        combined_clusters = {
            "type": "FeatureCollection",
            "features": all_cluster_features,
        }

        combined_clusters_path = self.detections_dir / "all_clusters.geojson"
        with open(combined_clusters_path, "w") as f:
            json.dump(combined_clusters, f, indent=2)

        # Generate combined statistics
        combined_stats = {
            "total_detections": sum(s.get("total_detections", 0) for s in self.all_stats.values()),
            "total_weight_kg": round(sum(s.get("total_estimated_weight_kg", 0) for s in self.all_stats.values()), 2),
            "total_clusters": len(all_cluster_features),
            "by_location": self.all_stats,
            "generated_at": datetime.now().isoformat(),
        }

        combined_stats_path = self.summary_dir / "combined_stats.json"
        with open(combined_stats_path, "w") as f:
            json.dump(combined_stats, f, indent=2)

        # Generate heatmap data
        self.get_heatmap_data()

    def get_heatmap_data(self) -> List[List]:
        """
        Generate heatmap data for visualization.
        Uses weight and priority to create varied intensity distribution.
        Blue/green = low trash, yellow/orange/red = high density.

        Returns:
            List of [lat, lon, intensity] values
        """
        import math
        heatmap_data = []

        # Priority multipliers for intensity
        priority_mult = {
            "critical": 1.0,
            "high": 0.75,
            "medium": 0.5,
            "low": 0.25
        }

        for location_key, geojson in self.all_detections.items():
            for feature in geojson["features"]:
                coords = feature["geometry"]["coordinates"]
                weight = feature["properties"]["estimated_weight_kg"]
                priority = feature["properties"].get("priority", "low")

                # Base intensity from weight - spread across full gradient range
                # Lightweight items (0-0.5kg): 0.05-0.3 intensity (blue/cyan)
                # Medium items (0.5-2kg): 0.3-0.5 intensity (green/yellow-green)
                # Large items (2-10kg): 0.5-0.75 intensity (yellow/orange)
                # Heavy items (10+kg): 0.75-1.0 intensity (red)
                if weight < 0.5:
                    base_intensity = 0.05 + (weight / 0.5) * 0.25
                elif weight < 2.0:
                    base_intensity = 0.3 + ((weight - 0.5) / 1.5) * 0.2
                elif weight < 10.0:
                    base_intensity = 0.5 + ((weight - 2.0) / 8.0) * 0.25
                else:
                    base_intensity = 0.75 + min(0.25, (weight - 10.0) / 40.0)

                # Adjust by priority - critical items bump up, low items stay low
                priority_boost = priority_mult.get(priority, 0.25)
                intensity = min(1.0, base_intensity * (0.6 + 0.4 * priority_boost))
                heatmap_data.append([coords[1], coords[0], round(intensity, 3)])

        heatmap_path = self.output_dir / "heatmap_data.json"
        with open(heatmap_path, "w") as f:
            json.dump(heatmap_data, f)

        return heatmap_data


def main():
    """Run data generation from command line."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate Sylva simulation data")
    parser.add_argument(
        "--output", "-o",
        default="data",
        help="Output directory (default: data)"
    )
    parser.add_argument(
        "--seed", "-s",
        type=int,
        default=None,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--location", "-l",
        choices=list(LOCATIONS.keys()),
        help="Generate data for specific location only"
    )

    args = parser.parse_args()

    generator = DataGenerator(output_dir=args.output)

    if args.location:
        summary = generator.generate_location(args.location, seed=args.seed)
        print(f"\nGenerated data for {LOCATIONS[args.location]['name']}:")
        print(json.dumps(summary, indent=2))
    else:
        summary = generator.generate_all(seed=args.seed)
        print("\nGeneration Summary:")
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
