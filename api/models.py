"""
Sylva API Data Models
Pydantic models for request/response validation
TamAir - Conrad Challenge 2026
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    """Geographic coordinates."""
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)


class DetectionProperties(BaseModel):
    """Properties of a trash detection."""
    id: str
    timestamp: str
    category: str
    category_name: str
    confidence: float = Field(..., ge=0, le=1)
    size_m2: float
    estimated_weight_kg: float
    priority: str
    color: str
    flight_id: str
    environment: str
    location: str


class Detection(BaseModel):
    """A single trash detection."""
    type: str = "Feature"
    geometry: Dict[str, Any]
    properties: DetectionProperties


class DetectionCollection(BaseModel):
    """Collection of detections (GeoJSON FeatureCollection)."""
    type: str = "FeatureCollection"
    features: List[Detection]
    properties: Optional[Dict[str, Any]] = None


class FlightProperties(BaseModel):
    """Properties of a flight path."""
    flight_id: str
    location: str
    type: str
    altitude_m: float
    total_distance_m: float
    duration_seconds: float
    start_time: str
    end_time: str


class Flight(BaseModel):
    """A flight path feature."""
    type: str = "Feature"
    geometry: Dict[str, Any]
    properties: FlightProperties


class FlightCollection(BaseModel):
    """Collection of flight paths."""
    type: str = "FeatureCollection"
    features: List[Dict[str, Any]]


class CategoryStats(BaseModel):
    """Statistics for a single trash category."""
    category: str
    name: str
    count: int
    percentage: float
    color: str


class PriorityStats(BaseModel):
    """Statistics by priority level."""
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0


class LocationStats(BaseModel):
    """Statistics for a location."""
    total_detections: int
    total_estimated_weight_kg: float
    total_area_m2: float
    by_category: List[CategoryStats]
    by_priority: Dict[str, int]
    location: str
    environment_type: str


class CombinedStats(BaseModel):
    """Combined statistics across all locations."""
    total_detections: int
    total_weight_kg: float
    total_clusters: int
    by_location: Dict[str, LocationStats]
    generated_at: str


class ClusterProperties(BaseModel):
    """Properties of a high-density cluster."""
    cluster_id: str
    detection_count: int
    total_weight_kg: float
    density_per_100m2: float
    priority: str
    radius_m: float


class Cluster(BaseModel):
    """A high-density trash cluster."""
    type: str = "Feature"
    geometry: Dict[str, Any]
    properties: ClusterProperties


class ClusterCollection(BaseModel):
    """Collection of clusters."""
    type: str = "FeatureCollection"
    features: List[Cluster]


class AnimationFrame(BaseModel):
    """A single frame in the flight animation."""
    lat: float
    lon: float
    altitude: float
    elapsed_seconds: float
    timestamp: str


class LiveDemoState(BaseModel):
    """State of the live demo simulation."""
    is_running: bool = False
    current_frame: int = 0
    total_frames: int = 0
    speed_multiplier: float = 1.0
    detections_shown: int = 0
    location: str = ""


class FilterParams(BaseModel):
    """Parameters for filtering detections."""
    categories: Optional[List[str]] = None
    priorities: Optional[List[str]] = None
    min_confidence: Optional[float] = None
    flight_id: Optional[str] = None
    location: Optional[str] = None
    bbox: Optional[List[float]] = None  # [min_lon, min_lat, max_lon, max_lat]
