"""
Sylva API Data Models
Pydantic models for request/response validation
TamAir - Conrad Challenge 2026
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# =============================================================================
# RESPONSE MODELS WITH EXAMPLES
# =============================================================================

class FlightSummary(BaseModel):
    """Summary of a flight mission."""
    id: str = Field(..., example="stinson_beach")
    flight_id: str = Field(..., example="stinson_beach_survey_001")
    location: str = Field(..., example="Stinson Beach")
    distance_m: float = Field(..., example=12500.5)
    duration_seconds: float = Field(..., example=2100.0)

class FlightListResponse(BaseModel):
    """Response for listing flights."""
    flights: List[FlightSummary] = Field(..., example=[
        {"id": "stinson_beach", "flight_id": "stinson_beach_survey_001", "location": "Stinson Beach", "distance_m": 12500.5, "duration_seconds": 2100.0},
        {"id": "lake_erie", "flight_id": "lake_erie_corridor_001", "location": "Lake Erie Highway", "distance_m": 430000.0, "duration_seconds": 17200.0}
    ])
    count: int = Field(..., example=3)

class DetectionFeature(BaseModel):
    """A single detection in GeoJSON format."""
    type: str = Field(default="Feature", example="Feature")
    geometry: Dict[str, Any] = Field(..., example={"type": "Point", "coordinates": [-122.6432, 37.8965]})
    properties: Dict[str, Any] = Field(..., example={
        "id": "det_001",
        "category": "plastic_bottles",
        "category_name": "Plastic Bottles",
        "confidence": 0.92,
        "priority": "medium",
        "estimated_weight_kg": 0.35,
        "timestamp": "2026-03-15T10:23:45Z",
        "location": "stinson_beach"
    })

class DetectionResponse(BaseModel):
    """Response for detection queries."""
    type: str = Field(default="FeatureCollection", example="FeatureCollection")
    features: List[DetectionFeature]
    count: int = Field(..., example=247)
    filters_applied: Optional[Dict[str, Any]] = Field(None, example={"location": "stinson_beach", "priority": "high"})

class CategoryInfo(BaseModel):
    """Information about a trash category."""
    id: str = Field(..., example="plastic_bottles")
    name: str = Field(..., example="Plastic Bottles")
    color: str = Field(..., example="#3498db")
    avg_size_m2: float = Field(..., example=0.015)
    weight_range_kg: List[float] = Field(..., example=[0.01, 0.5])

class CategoriesResponse(BaseModel):
    """Response for category list."""
    categories: List[CategoryInfo]

class StatsResponse(BaseModel):
    """Response for statistics endpoint."""
    total_detections: int = Field(..., example=1247)
    total_weight_kg: float = Field(..., example=523.7)
    by_priority: Dict[str, int] = Field(..., example={"critical": 23, "high": 156, "medium": 687, "low": 381})
    by_category: List[Dict[str, Any]] = Field(..., example=[
        {"category": "plastic_bottles", "count": 342, "percentage": 27.4},
        {"category": "tires", "count": 89, "percentage": 7.1}
    ])

class LocationInfo(BaseModel):
    """Information about a survey location."""
    id: str = Field(..., example="stinson_beach")
    name: str = Field(..., example="Stinson Beach")
    type: str = Field(..., example="coastal")
    center: Dict[str, float] = Field(..., example={"lat": 37.8967, "lon": -122.6437})
    altitude_m: float = Field(..., example=120)
    speed_ms: float = Field(..., example=15)
    waypoints: Optional[List[Dict[str, Any]]] = Field(None, example=[
        {"lat": 37.8967, "lon": -122.6437, "name": "Start Point"},
        {"lat": 37.9012, "lon": -122.6398, "name": "Beach North"}
    ])

class LocationsResponse(BaseModel):
    """Response for locations endpoint."""
    locations: List[LocationInfo]

class AnnualSummaryResponse(BaseModel):
    """Response for annual analytics."""
    year: int = Field(..., example=2026)
    total_detections: int = Field(..., example=15847)
    total_weight_kg: float = Field(..., example=6234.5)
    total_flights: int = Field(..., example=312)
    total_area_surveyed_km2: float = Field(..., example=847.3)
    by_month: List[Dict[str, Any]] = Field(..., example=[
        {"month": 1, "month_name": "January", "detections": 1023, "weight_kg": 412.3}
    ])
    water_risk_summary: Dict[str, Any] = Field(..., example={
        "critical_near_water": 234,
        "estimated_water_pollution_prevented_kg": 156.7
    })

class WaterRiskResponse(BaseModel):
    """Response for water risk analysis."""
    year: int = Field(..., example=2026)
    critical_count: int = Field(..., example=234)
    high_count: int = Field(..., example=567)
    medium_count: int = Field(..., example=1234)
    low_count: int = Field(..., example=2456)
    estimated_water_pollution_prevented_kg: float = Field(..., example=156.7)
    risk_levels: Dict[str, str] = Field(..., example={
        "critical": "Within 25m of water body",
        "high": "25-100m from water body",
        "medium": "100-500m from water body",
        "low": "Over 500m from water body"
    })

class ExecutiveSummaryResponse(BaseModel):
    """Response for executive summary report."""
    report_type: str = Field(default="Executive Summary", example="Executive Summary")
    year: int = Field(..., example=2026)
    generated_at: str = Field(..., example="2026-12-29T15:30:00Z")
    key_findings: Dict[str, Any] = Field(..., example={
        "total_debris_detected_kg": 6234.5,
        "total_items_detected": 15847,
        "critical_water_risk_items": 234,
        "pollution_prevented_kg": 156.7
    })
    operational_efficiency: Dict[str, Any] = Field(..., example={
        "total_flights": 312,
        "cost_per_detection_usd": 2.34,
        "estimated_savings_pct": 67.5
    })
    recommendations: List[str] = Field(..., example=[
        "Focus cleanup resources on 5 critical water-risk hotspots",
        "Continue weekly surveys at beach locations during summer months"
    ])

class HealthResponse(BaseModel):
    """Response for health check."""
    status: str = Field(..., example="healthy")
    timestamp: str = Field(..., example="2026-12-29T15:30:00Z")
    version: str = Field(..., example="1.2.0")


# =============================================================================
# ORIGINAL MODELS
# =============================================================================

class Coordinates(BaseModel):
    """Geographic coordinates."""
    lat: float = Field(..., ge=-90, le=90, example=37.8967)
    lon: float = Field(..., ge=-180, le=180, example=-122.6437)


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
