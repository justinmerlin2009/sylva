"""
Sylva Annual Data Generator
Generates 1 year of multi-drone environmental monitoring data
TamAir - Conrad Challenge 2026
"""

import json
import math
import random
import uuid
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path
import numpy as np

from .config import LOCATIONS, TRASH_CATEGORIES, DRONE_SPECS, SIMULATION
from .trash_detector import TrashDetector
from .flight_paths import FlightPathGenerator


# Drone fleet configuration
DRONE_FLEET = [
    {"id": "SYLVA-1-ALPHA", "name": "Alpha", "status": "active"},
    {"id": "SYLVA-1-BRAVO", "name": "Bravo", "status": "active"},
    {"id": "SYLVA-1-CHARLIE", "name": "Charlie", "status": "active"},
    {"id": "SYLVA-1-DELTA", "name": "Delta", "status": "active"},
    {"id": "SYLVA-1-ECHO", "name": "Echo", "status": "active"},
]

# Seasonal multipliers for detection rates
SEASONAL_PATTERNS = {
    1: 0.85,   # January - winter low
    2: 0.80,   # February - winter low
    3: 0.95,   # March - early spring
    4: 1.05,   # April - spring increase
    5: 1.15,   # May - late spring
    6: 1.30,   # June - summer begins
    7: 1.45,   # July - summer peak
    8: 1.40,   # August - summer high
    9: 1.15,   # September - fall begins
    10: 1.00,  # October - fall
    11: 0.90,  # November - late fall
    12: 0.85,  # December - winter
}

# Holiday spikes (day of year -> multiplier)
HOLIDAY_SPIKES = {
    1: 1.30,    # New Year's Day aftermath
    2: 1.25,    # Jan 2
    3: 1.20,    # Jan 3
    20: 1.15,   # MLK Day weekend
    46: 1.20,   # Valentine's Day aftermath
    90: 1.15,   # Spring break period
    121: 1.25,  # May long weekend
    152: 1.20,  # Early June
    185: 1.50,  # July 4th aftermath
    186: 1.40,  # July 5
    187: 1.30,  # July 6
    247: 1.35,  # Labor Day aftermath
    248: 1.25,  # Day after
    305: 1.10,  # Halloween aftermath
    329: 1.25,  # Thanksgiving aftermath
    330: 1.20,  # Black Friday
    359: 1.15,  # Christmas aftermath
    360: 1.20,
    361: 1.25,
}

# Weather conditions distribution
WEATHER_CONDITIONS = [
    {"condition": "clear", "probability": 0.45, "detection_mult": 1.0},
    {"condition": "partly_cloudy", "probability": 0.25, "detection_mult": 0.95},
    {"condition": "overcast", "probability": 0.15, "detection_mult": 0.90},
    {"condition": "light_rain", "probability": 0.10, "detection_mult": 0.70},
    {"condition": "post_storm", "probability": 0.05, "detection_mult": 1.50},
]

# Water bodies for proximity calculation - positioned along survey paths
WATER_BODIES = {
    "stinson_beach": [
        # Ocean edge runs along the beach - multiple points to create a "shoreline"
        {"name": "Pacific Ocean", "type": "ocean", "lat": 37.910, "lon": -122.652, "radius_m": 50},
        {"name": "Pacific Ocean", "type": "ocean", "lat": 37.905, "lon": -122.648, "radius_m": 50},
        {"name": "Pacific Ocean", "type": "ocean", "lat": 37.900, "lon": -122.645, "radius_m": 50},
        {"name": "Pacific Ocean", "type": "ocean", "lat": 37.895, "lon": -122.642, "radius_m": 50},
        {"name": "Pacific Ocean", "type": "ocean", "lat": 37.890, "lon": -122.640, "radius_m": 50},
        {"name": "Pacific Ocean", "type": "ocean", "lat": 37.885, "lon": -122.638, "radius_m": 50},
        {"name": "Bolinas Lagoon", "type": "lagoon", "lat": 37.908, "lon": -122.650, "radius_m": 100},
    ],
    "route_66": [
        # Colorado River runs near the highway
        {"name": "Colorado River", "type": "river", "lat": 34.848, "lon": -114.625, "radius_m": 200},
        {"name": "Colorado River", "type": "river", "lat": 34.852, "lon": -114.590, "radius_m": 200},
        {"name": "Colorado River", "type": "river", "lat": 34.858, "lon": -114.555, "radius_m": 200},
    ],
    "nasa_clear_lake": [
        # Clear Lake and surrounding waterways along the survey path
        {"name": "Clear Lake", "type": "lake", "lat": 29.555, "lon": -95.095, "radius_m": 100},
        {"name": "Clear Lake", "type": "lake", "lat": 29.545, "lon": -95.075, "radius_m": 100},
        {"name": "Clear Lake", "type": "lake", "lat": 29.535, "lon": -95.055, "radius_m": 100},
        {"name": "Taylor Lake", "type": "lake", "lat": 29.550, "lon": -95.085, "radius_m": 80},
        {"name": "Galveston Bay", "type": "bay", "lat": 29.525, "lon": -95.030, "radius_m": 150},
        {"name": "Galveston Bay", "type": "bay", "lat": 29.520, "lon": -95.020, "radius_m": 150},
    ],
}

# Cleanup simulation - monthly cleanup effectiveness
CLEANUP_SCHEDULE = {
    "stinson_beach": {
        "frequency": "weekly",
        "effectiveness": 0.65,  # 65% of critical items removed
        "target_hotspots": ["Main Beach - Heavy Use", "Easkoot Creek Dumping"],
    },
    "route_66": {
        "frequency": "monthly",
        "effectiveness": 0.45,
        "target_hotspots": ["Needles Downtown Exit", "Historic Marker Dumping"],
    },
    "nasa_clear_lake": {
        "frequency": "biweekly",
        "effectiveness": 0.55,
        "target_hotspots": ["Clear Lake Park", "Marina Dumping", "Kemah Boardwalk Area"],
    },
}


class AnnualDataGenerator:
    """Generate comprehensive annual environmental monitoring data."""

    def __init__(self, year: int = 2026, seed: int = 42):
        self.year = year
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)

        self.detections = []
        self.flights = []
        self.monthly_stats = {}
        self.hotspot_evolution = {}
        self.cleanup_events = []

        # Data output directory
        self.output_dir = Path(__file__).parent.parent / "data" / "annual"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "monthly").mkdir(exist_ok=True)

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

    def _get_water_proximity(self, lat: float, lon: float, location: str) -> Dict:
        """Calculate distance to nearest water body and risk level."""
        water_bodies = WATER_BODIES.get(location, [])

        min_distance = float('inf')
        nearest_water = None

        for water in water_bodies:
            distance = self._haversine_distance(lat, lon, water["lat"], water["lon"])
            if distance < min_distance:
                min_distance = distance
                nearest_water = water

        # Determine risk level
        if min_distance < 25:
            risk_level = "critical"
        elif min_distance < 100:
            risk_level = "high"
        elif min_distance < 500:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "water_proximity_m": round(min_distance, 1),
            "water_risk_level": risk_level,
            "nearest_water_body": nearest_water["name"] if nearest_water else None,
            "water_body_type": nearest_water["type"] if nearest_water else None,
        }

    def _get_weather(self, date: datetime) -> Dict:
        """Generate weather conditions for a given date."""
        # Select weather based on probability
        r = random.random()
        cumulative = 0
        selected = WEATHER_CONDITIONS[0]

        for weather in WEATHER_CONDITIONS:
            cumulative += weather["probability"]
            if r <= cumulative:
                selected = weather
                break

        # Generate wind speed (higher in coastal areas, varies by season)
        base_wind = random.uniform(2, 8)
        if date.month in [11, 12, 1, 2, 3]:  # Windier months
            base_wind *= 1.3

        return {
            "weather_conditions": selected["condition"],
            "detection_multiplier": selected["detection_mult"],
            "wind_speed_ms": round(base_wind, 1),
        }

    def _get_seasonal_multiplier(self, date: datetime) -> float:
        """Get detection rate multiplier based on season and holidays."""
        month_mult = SEASONAL_PATTERNS.get(date.month, 1.0)
        day_of_year = date.timetuple().tm_yday
        holiday_mult = HOLIDAY_SPIKES.get(day_of_year, 1.0)

        return month_mult * holiday_mult

    def _generate_flight(self, location: str, date: datetime, drone: Dict, flight_num: int) -> Dict:
        """Generate a single flight record."""
        location_data = LOCATIONS[location]

        flight_id = f"SYLVA-{location[:3].upper()}-{self.year}-{flight_num:03d}"

        # Generate waypoints using existing generator
        generator = FlightPathGenerator(location)
        waypoints = generator.generate_path()

        weather = self._get_weather(date)

        return {
            "flight_id": flight_id,
            "drone_id": drone["id"],
            "drone_name": drone["name"],
            "location": location,
            "location_name": location_data["name"],
            "date": date.strftime("%Y-%m-%d"),
            "start_time": date.strftime("%Y-%m-%dT10:00:00"),
            "end_time": (date + timedelta(minutes=random.randint(35, 55))).strftime("%Y-%m-%dT%H:%M:%S"),
            "altitude_m": location_data["survey_altitude_m"],
            "distance_km": round(generator.get_total_distance() / 1000, 2),
            "waypoint_count": len(waypoints),
            "weather": weather["weather_conditions"],
            "wind_speed_ms": weather["wind_speed_ms"],
            "status": "completed",
            "month": date.month,
            "week": date.isocalendar()[1],
            "quarter": f"Q{(date.month - 1) // 3 + 1}",
        }

    def _generate_detections_for_flight(self, flight: Dict, waypoints: List[Dict]) -> List[Dict]:
        """Generate detections for a single flight with enhanced metadata."""
        location = flight["location"]
        date = datetime.fromisoformat(flight["start_time"])

        # Get multipliers
        seasonal_mult = self._get_seasonal_multiplier(date)
        weather = self._get_weather(date)

        # Use existing trash detector
        detector = TrashDetector(location, seed=random.randint(1, 100000))
        base_detections = detector.generate_detections_for_path(waypoints, flight["flight_id"])

        # Adjust detection count based on season and weather
        target_count = int(len(base_detections) * seasonal_mult * weather["detection_multiplier"])

        # Sample or extend detections to match target
        if target_count < len(base_detections):
            base_detections = random.sample(base_detections, target_count)
        elif target_count > len(base_detections):
            # Add more detections by duplicating and slightly modifying existing ones
            additional = target_count - len(base_detections)
            for _ in range(additional):
                if base_detections:
                    original = random.choice(base_detections).copy()
                    # Slightly modify position
                    coords = original["geometry"]["coordinates"]
                    original["geometry"]["coordinates"] = [
                        coords[0] + random.uniform(-0.0003, 0.0003),
                        coords[1] + random.uniform(-0.0003, 0.0003),
                    ]
                    original["properties"]["id"] = f"DET-{self.year}-{uuid.uuid4().hex[:8].upper()}"
                    base_detections.append(original)

        # Enhance detections with additional metadata
        enhanced_detections = []
        for det in base_detections:
            props = det["properties"]
            coords = det["geometry"]["coordinates"]

            # Add water proximity
            water_info = self._get_water_proximity(coords[1], coords[0], location)

            # Escalate priority if near water
            if water_info["water_risk_level"] == "critical" and props["priority"] != "critical":
                if props["priority"] == "high":
                    props["priority"] = "critical"
                elif props["priority"] == "medium":
                    props["priority"] = "high"

            # Update ID format
            props["id"] = f"DET-{self.year}-{uuid.uuid4().hex[:8].upper()}"

            # Add enhanced properties
            props.update({
                "flight_id": flight["flight_id"],
                "drone_id": flight["drone_id"],
                "weather_conditions": weather["weather_conditions"],
                "wind_speed_ms": weather["wind_speed_ms"],
                "month": date.month,
                "week": date.isocalendar()[1],
                "quarter": f"Q{(date.month - 1) // 3 + 1}",
                "year": self.year,
                **water_info,
            })

            # Update timestamp to match flight date
            base_time = date + timedelta(seconds=random.randint(0, 2400))
            props["timestamp"] = base_time.isoformat()

            enhanced_detections.append(det)

        return enhanced_detections

    def _simulate_cleanup(self, month: int, location: str) -> Dict:
        """Simulate cleanup event and calculate impact."""
        cleanup_config = CLEANUP_SCHEDULE.get(location, {})
        if not cleanup_config:
            return None

        # Calculate items to be "cleaned"
        location_detections = [d for d in self.detections
                               if d["properties"]["location"] == LOCATIONS[location]["name"]
                               and d["properties"]["month"] == month]

        # Focus on critical and high priority near water
        critical_items = [d for d in location_detections
                         if d["properties"]["water_risk_level"] in ["critical", "high"]
                         and d["properties"]["priority"] in ["critical", "high"]]

        items_cleaned = int(len(critical_items) * cleanup_config["effectiveness"])
        weight_cleaned = sum(d["properties"]["estimated_weight_kg"]
                            for d in random.sample(critical_items, min(items_cleaned, len(critical_items))))

        cleanup_date = datetime(self.year, month, random.randint(15, 28))

        return {
            "cleanup_id": f"CLN-{location[:3].upper()}-{self.year}-{month:02d}",
            "location": location,
            "location_name": LOCATIONS[location]["name"],
            "date": cleanup_date.strftime("%Y-%m-%d"),
            "month": month,
            "items_removed": items_cleaned,
            "weight_removed_kg": round(weight_cleaned, 2),
            "target_hotspots": cleanup_config["target_hotspots"],
            "crew_size": random.randint(4, 12),
            "hours_worked": random.randint(4, 8),
            "effectiveness_rate": cleanup_config["effectiveness"],
        }

    def _calculate_hotspot_evolution(self) -> List[Dict]:
        """Calculate how hotspots change over the year."""
        hotspots = []

        # Get unique hotspot areas from trash detector
        for location in LOCATIONS:
            detector = TrashDetector(location)

            for i, hotspot in enumerate(detector.hotspots):
                hotspot_id = f"HS-{location[:3].upper()}-{i+1:03d}"

                # Count monthly detections near this hotspot
                monthly_counts = []
                monthly_weights = []

                for month in range(1, 13):
                    month_detections = [d for d in self.detections
                                       if d["properties"]["month"] == month
                                       and d["properties"]["location"] == LOCATIONS[location]["name"]]

                    # Count detections within hotspot radius
                    nearby = 0
                    weight = 0
                    for det in month_detections:
                        coords = det["geometry"]["coordinates"]
                        dist = self._haversine_distance(
                            coords[1], coords[0],
                            hotspot["lat"], hotspot["lon"]
                        )
                        if dist < hotspot["radius_m"] * 1.5:
                            nearby += 1
                            weight += det["properties"]["estimated_weight_kg"]

                    monthly_counts.append(nearby)
                    monthly_weights.append(round(weight, 2))

                # Determine trend
                first_half_avg = sum(monthly_counts[:6]) / 6
                second_half_avg = sum(monthly_counts[6:]) / 6

                if second_half_avg < first_half_avg * 0.8:
                    trend = "improving"
                elif second_half_avg > first_half_avg * 1.2:
                    trend = "worsening"
                elif max(monthly_counts[5:8]) > max(monthly_counts[:3] + monthly_counts[9:]) * 1.3:
                    trend = "seasonal_peak_summer"
                else:
                    trend = "stable"

                # Water risk for hotspot
                water_info = self._get_water_proximity(hotspot["lat"], hotspot["lon"], location)

                hotspots.append({
                    "hotspot_id": hotspot_id,
                    "name": hotspot.get("name", f"Hotspot {i+1}"),
                    "location": location,
                    "location_name": LOCATIONS[location]["name"],
                    "coordinates": {"lat": hotspot["lat"], "lon": hotspot["lon"]},
                    "radius_m": hotspot["radius_m"],
                    "first_detected": f"{self.year}-01-15",
                    "monthly_detections": monthly_counts,
                    "monthly_weight_kg": monthly_weights,
                    "total_annual_detections": sum(monthly_counts),
                    "total_annual_weight_kg": round(sum(monthly_weights), 2),
                    "trend": trend,
                    "water_risk": water_info["water_risk_level"],
                    "nearest_water": water_info["nearest_water_body"],
                    "recommended_action": self._get_hotspot_recommendation(trend, water_info["water_risk_level"]),
                })

        return hotspots

    def _get_hotspot_recommendation(self, trend: str, water_risk: str) -> str:
        """Generate cleanup recommendation based on trend and risk."""
        if water_risk == "critical":
            if trend == "worsening":
                return "URGENT: Install barriers, weekly cleanup, public signage, enforcement patrols"
            elif trend == "improving":
                return "Continue current cleanup schedule, monitor for regression"
            else:
                return "Priority cleanup twice weekly, install trash receptacles"
        elif water_risk == "high":
            if trend == "worsening":
                return "Increase cleanup frequency, add collection points, community outreach"
            else:
                return "Weekly cleanup, seasonal signage during peak months"
        else:
            if trend == "worsening":
                return "Monthly cleanup, investigate illegal dumping sources"
            else:
                return "Routine monitoring, quarterly cleanup sufficient"

    def generate_annual_data(self) -> Dict:
        """Generate complete annual dataset."""
        print(f"Generating annual data for {self.year}...")

        flight_counter = 0

        # Generate data for each month
        for month in range(1, 13):
            print(f"  Processing month {month}/12...")

            # 4 flights per location per month
            for week in range(1, 5):
                flight_date = datetime(self.year, month, min(7 * week, 28))

                for location in LOCATIONS:
                    # Rotate through drone fleet
                    drone = DRONE_FLEET[flight_counter % len(DRONE_FLEET)]
                    flight_counter += 1

                    # Generate flight
                    generator = FlightPathGenerator(location)
                    waypoints = generator.generate_path()

                    flight = self._generate_flight(location, flight_date, drone, flight_counter)
                    self.flights.append(flight)

                    # Generate detections for this flight
                    detections = self._generate_detections_for_flight(flight, waypoints)
                    self.detections.extend(detections)

            # Simulate cleanup events at end of month
            for location in LOCATIONS:
                cleanup = self._simulate_cleanup(month, location)
                if cleanup:
                    self.cleanup_events.append(cleanup)

        # Calculate hotspot evolution
        hotspots = self._calculate_hotspot_evolution()

        # Calculate summary statistics
        summary = self._calculate_annual_summary(hotspots)

        # Generate monthly reports
        monthly_reports = self._generate_monthly_reports()

        return {
            "summary": summary,
            "monthly_reports": monthly_reports,
            "hotspots": hotspots,
            "cleanup_events": self.cleanup_events,
        }

    def _calculate_annual_summary(self, hotspots: List[Dict]) -> Dict:
        """Calculate comprehensive annual statistics."""
        total_detections = len(self.detections)
        total_weight = sum(d["properties"]["estimated_weight_kg"] for d in self.detections)

        # By location
        by_location = {}
        for location in LOCATIONS:
            loc_name = LOCATIONS[location]["name"]
            loc_detections = [d for d in self.detections if d["properties"]["location"] == loc_name]

            by_location[location] = {
                "total_detections": len(loc_detections),
                "total_weight_kg": round(sum(d["properties"]["estimated_weight_kg"] for d in loc_detections), 2),
                "flights_completed": len([f for f in self.flights if f["location"] == location]),
                "by_priority": {
                    "critical": len([d for d in loc_detections if d["properties"]["priority"] == "critical"]),
                    "high": len([d for d in loc_detections if d["properties"]["priority"] == "high"]),
                    "medium": len([d for d in loc_detections if d["properties"]["priority"] == "medium"]),
                    "low": len([d for d in loc_detections if d["properties"]["priority"] == "low"]),
                },
            }

        # By month
        by_month = {}
        for month in range(1, 13):
            month_detections = [d for d in self.detections if d["properties"]["month"] == month]
            by_month[month] = {
                "detections": len(month_detections),
                "weight_kg": round(sum(d["properties"]["estimated_weight_kg"] for d in month_detections), 2),
                "flights": len([f for f in self.flights if f["month"] == month]),
            }

        # By category
        by_category = {}
        for category in TRASH_CATEGORIES:
            cat_detections = [d for d in self.detections if d["properties"]["category"] == category]
            by_category[category] = {
                "name": TRASH_CATEGORIES[category]["name"],
                "count": len(cat_detections),
                "percentage": round(100 * len(cat_detections) / total_detections, 1) if total_detections > 0 else 0,
                "weight_kg": round(sum(d["properties"]["estimated_weight_kg"] for d in cat_detections), 2),
                "color": TRASH_CATEGORIES[category]["color"],
            }

        # Water risk summary
        critical_water = [d for d in self.detections if d["properties"]["water_risk_level"] == "critical"]
        high_water = [d for d in self.detections if d["properties"]["water_risk_level"] == "high"]

        total_cleaned_weight = sum(c["weight_removed_kg"] for c in self.cleanup_events)

        water_risk_summary = {
            "critical_near_water": len(critical_water),
            "high_risk_near_water": len(high_water),
            "critical_weight_kg": round(sum(d["properties"]["estimated_weight_kg"] for d in critical_water), 2),
            "items_cleaned": sum(c["items_removed"] for c in self.cleanup_events),
            "weight_cleaned_kg": round(total_cleaned_weight, 2),
            "estimated_water_pollution_prevented_kg": round(total_cleaned_weight * 0.7, 2),  # 70% would have reached water
        }

        # Calculate total area surveyed
        total_distance_km = sum(f["distance_km"] for f in self.flights)
        avg_swath_km = 0.1  # 100m average swath width
        area_surveyed_km2 = round(total_distance_km * avg_swath_km, 2)

        return {
            "year": self.year,
            "generated_at": datetime.now().isoformat(),
            "total_flights": len(self.flights),
            "total_detections": total_detections,
            "total_weight_kg": round(total_weight, 2),
            "total_area_surveyed_km2": area_surveyed_km2,
            "total_distance_flown_km": round(total_distance_km, 2),
            "drones_deployed": len(DRONE_FLEET),
            "drone_fleet": [d["id"] for d in DRONE_FLEET],
            "locations_monitored": len(LOCATIONS),
            "by_location": by_location,
            "by_month": by_month,
            "by_category": list(by_category.values()),
            "by_priority": {
                "critical": len([d for d in self.detections if d["properties"]["priority"] == "critical"]),
                "high": len([d for d in self.detections if d["properties"]["priority"] == "high"]),
                "medium": len([d for d in self.detections if d["properties"]["priority"] == "medium"]),
                "low": len([d for d in self.detections if d["properties"]["priority"] == "low"]),
            },
            "water_risk_summary": water_risk_summary,
            "cleanup_summary": {
                "total_cleanup_events": len(self.cleanup_events),
                "total_items_removed": sum(c["items_removed"] for c in self.cleanup_events),
                "total_weight_removed_kg": round(total_cleaned_weight, 2),
                "total_crew_hours": sum(c["hours_worked"] * c["crew_size"] for c in self.cleanup_events),
            },
            "operational_metrics": {
                "avg_detections_per_flight": round(total_detections / len(self.flights), 1) if self.flights else 0,
                "avg_weight_per_detection_kg": round(total_weight / total_detections, 3) if total_detections > 0 else 0,
                "flight_completion_rate": 1.0,  # 100% in simulation
                "cost_per_detection_usd": 0.87,  # Estimated
                "manual_equivalent_cost_usd": 15.50,  # Industry average
            },
        }

    def _generate_monthly_reports(self) -> List[Dict]:
        """Generate detailed monthly reports."""
        reports = []

        for month in range(1, 13):
            month_name = datetime(self.year, month, 1).strftime("%B %Y")
            month_detections = [d for d in self.detections if d["properties"]["month"] == month]
            month_flights = [f for f in self.flights if f["month"] == month]
            month_cleanups = [c for c in self.cleanup_events if c["month"] == month]

            # Previous month comparison
            prev_month = month - 1 if month > 1 else 12
            prev_detections = [d for d in self.detections if d["properties"]["month"] == prev_month]

            detection_change = 0
            if prev_detections:
                detection_change = round(100 * (len(month_detections) - len(prev_detections)) / len(prev_detections), 1)

            # Top categories this month
            category_counts = {}
            for det in month_detections:
                cat = det["properties"]["category"]
                category_counts[cat] = category_counts.get(cat, 0) + 1

            top_categories = sorted(category_counts.items(), key=lambda x: -x[1])[:5]

            # Water risk detections
            water_critical = len([d for d in month_detections if d["properties"]["water_risk_level"] == "critical"])

            reports.append({
                "month": month,
                "month_name": month_name,
                "flights_completed": len(month_flights),
                "total_detections": len(month_detections),
                "total_weight_kg": round(sum(d["properties"]["estimated_weight_kg"] for d in month_detections), 2),
                "comparison_to_previous": {
                    "detection_change_pct": detection_change,
                    "previous_month_detections": len(prev_detections),
                },
                "top_categories": [
                    {"category": cat, "name": TRASH_CATEGORIES[cat]["name"], "count": count}
                    for cat, count in top_categories
                ],
                "water_risk_detections": water_critical,
                "cleanup_events": len(month_cleanups),
                "items_cleaned": sum(c["items_removed"] for c in month_cleanups),
                "by_priority": {
                    "critical": len([d for d in month_detections if d["properties"]["priority"] == "critical"]),
                    "high": len([d for d in month_detections if d["properties"]["priority"] == "high"]),
                    "medium": len([d for d in month_detections if d["properties"]["priority"] == "medium"]),
                    "low": len([d for d in month_detections if d["properties"]["priority"] == "low"]),
                },
            })

        return reports

    def save_data(self, data: Dict):
        """Save all generated data to files."""
        print("Saving data files...")

        # Save annual summary
        with open(self.output_dir / f"{self.year}_summary.json", "w") as f:
            json.dump(data["summary"], f, indent=2)
        print(f"  Saved {self.year}_summary.json")

        # Save monthly reports
        for report in data["monthly_reports"]:
            month = report["month"]
            with open(self.output_dir / "monthly" / f"{self.year}_{month:02d}_report.json", "w") as f:
                json.dump(report, f, indent=2)
        print(f"  Saved 12 monthly reports")

        # Save hotspot evolution
        with open(self.output_dir / f"hotspots_{self.year}.json", "w") as f:
            json.dump(data["hotspots"], f, indent=2)
        print(f"  Saved hotspots_{self.year}.json")

        # Save cleanup events
        with open(self.output_dir / f"cleanups_{self.year}.json", "w") as f:
            json.dump(data["cleanup_events"], f, indent=2)
        print(f"  Saved cleanups_{self.year}.json")

        # Save all detections as GeoJSON
        detections_geojson = {
            "type": "FeatureCollection",
            "features": self.detections,
            "properties": {
                "year": self.year,
                "total_detections": len(self.detections),
                "generated_at": datetime.now().isoformat(),
            },
        }
        with open(self.output_dir / f"detections_{self.year}.geojson", "w") as f:
            json.dump(detections_geojson, f)
        print(f"  Saved detections_{self.year}.geojson ({len(self.detections)} features)")

        # Save flights log
        with open(self.output_dir / f"flights_{self.year}.json", "w") as f:
            json.dump(self.flights, f, indent=2)
        print(f"  Saved flights_{self.year}.json ({len(self.flights)} flights)")

        print(f"\nAll data saved to {self.output_dir}")


def generate_annual_data(year: int = 2026):
    """Main function to generate annual data."""
    generator = AnnualDataGenerator(year=year)
    data = generator.generate_annual_data()
    generator.save_data(data)

    # Print summary
    summary = data["summary"]
    print("\n" + "=" * 60)
    print(f"ANNUAL DATA GENERATION COMPLETE - {year}")
    print("=" * 60)
    print(f"Total Flights: {summary['total_flights']}")
    print(f"Total Detections: {summary['total_detections']}")
    print(f"Total Weight: {summary['total_weight_kg']} kg")
    print(f"Area Surveyed: {summary['total_area_surveyed_km2']} km²")
    print(f"Critical Water Risk Items: {summary['water_risk_summary']['critical_near_water']}")
    print(f"Pollution Prevented: {summary['water_risk_summary']['estimated_water_pollution_prevented_kg']} kg")
    print("=" * 60)

    return data


if __name__ == "__main__":
    generate_annual_data(2026)
