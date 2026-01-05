import React, { useEffect, useRef, useState, useCallback } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Polyline, CircleMarker, Circle, Polygon, useMap, useMapEvents } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Tile loading tracker component
function TileLoadingTracker({ onLoadingChange }) {
  const map = useMap()

  useEffect(() => {
    let loadingCount = 0

    const handleTileLoadStart = () => {
      loadingCount++
      if (loadingCount === 1) {
        onLoadingChange(true)
      }
    }

    const handleTileLoad = () => {
      loadingCount = Math.max(0, loadingCount - 1)
      if (loadingCount === 0) {
        // Small delay to batch tile loads
        setTimeout(() => {
          if (loadingCount === 0) {
            onLoadingChange(false)
          }
        }, 100)
      }
    }

    const handleTileError = () => {
      loadingCount = Math.max(0, loadingCount - 1)
      if (loadingCount === 0) {
        onLoadingChange(false)
      }
    }

    map.on('tileloadstart', handleTileLoadStart)
    map.on('tileload', handleTileLoad)
    map.on('tileerror', handleTileError)

    return () => {
      map.off('tileloadstart', handleTileLoadStart)
      map.off('tileload', handleTileLoad)
      map.off('tileerror', handleTileError)
    }
  }, [map, onLoadingChange])

  return null
}

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

// Calculate bearing between two points (in degrees, 0 = north, 90 = east)
function calculateBearing(lat1, lon1, lat2, lon2) {
  const toRad = (deg) => deg * Math.PI / 180
  const toDeg = (rad) => rad * 180 / Math.PI

  const dLon = toRad(lon2 - lon1)
  const y = Math.sin(dLon) * Math.cos(toRad(lat2))
  const x = Math.cos(toRad(lat1)) * Math.sin(toRad(lat2)) -
            Math.sin(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.cos(dLon)

  let bearing = toDeg(Math.atan2(y, x))
  return (bearing + 360) % 360
}

// Create drone icon with rotation (heading in degrees)
const createDroneIcon = (heading = 0) => {
  // The plane emoji points right (east = 90°), so we subtract 90 to correct
  const rotation = heading - 90
  return L.divIcon({
    className: 'drone-marker',
    html: `<div class="drone-icon-wrapper">
      <div class="drone-icon-pulse"></div>
      <div class="drone-icon" style="transform: rotate(${rotation}deg);">✈</div>
    </div>`,
    iconSize: [48, 48],
    iconAnchor: [24, 24],
  })
}

// Default drone icon (pointing east/right)
const droneIcon = createDroneIcon(90)

// Waypoint icon
const waypointIcon = L.divIcon({
  className: 'waypoint-marker',
  html: '<div class="waypoint-icon"></div>',
  iconSize: [16, 16],
  iconAnchor: [8, 8],
})

// Drawn point icon (for custom path drawing)
const drawnPointIcon = L.divIcon({
  className: 'drawn-point-marker',
  html: '<div class="drawn-point-icon"></div>',
  iconSize: [20, 20],
  iconAnchor: [10, 10],
})

// Map click handler for drawing mode
function MapClickHandler({ isDrawing, onMapClick }) {
  useMapEvents({
    click: (e) => {
      if (isDrawing) {
        onMapClick({ lat: e.latlng.lat, lon: e.latlng.lng })
      }
    },
  })
  return null
}

// Heatmap Layer Component
function HeatmapLayer({ data }) {
  const map = useMap()
  const heatLayerRef = useRef(null)

  useEffect(() => {
    if (!window.L.heatLayer) {
      const script = document.createElement('script')
      script.src = 'https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js'
      script.onload = () => {
        if (data.length > 0) {
          createHeatLayer()
        }
      }
      document.head.appendChild(script)
    } else if (data.length > 0) {
      createHeatLayer()
    }

    function createHeatLayer() {
      if (heatLayerRef.current) {
        map.removeLayer(heatLayerRef.current)
      }

      if (data.length > 0 && window.L.heatLayer) {
        heatLayerRef.current = window.L.heatLayer(data, {
          radius: 35,         // Larger radius for better visibility
          blur: 20,           // More blur for smoother gradients
          maxZoom: 18,
          max: 1.0,
          minOpacity: 0.4,    // Ensure heatmap is always visible
          gradient: {
            0.0: '#22c55e',   // Green - low density (start visible)
            0.2: '#84cc16',   // Yellow-green - moderate low
            0.35: '#eab308',  // Yellow - moderate
            0.5: '#f59e0b',   // Amber - medium
            0.65: '#f97316',  // Orange - high density
            0.8: '#ef4444',   // Red - very high
            0.9: '#dc2626',   // Dark red - critical
            1.0: '#991b1b',   // Deep red - maximum intensity
          },
        }).addTo(map)
      }
    }

    return () => {
      if (heatLayerRef.current) {
        map.removeLayer(heatLayerRef.current)
      }
    }
  }, [map, data])

  return null
}

// Map view controller with smooth animation and user interaction detection
function MapController({ center, zoom, shouldFollowDrone, disableAutoUpdate, onUserInteraction, forceRecenter }) {
  const map = useMap()
  const prevCenterRef = useRef(center)

  // Detect user interaction (drag/zoom) to disable auto-follow
  useMapEvents({
    dragstart: () => {
      if (onUserInteraction) onUserInteraction()
    },
    zoomstart: (e) => {
      // Only trigger if user initiated (not programmatic)
      if (e.originalEvent && onUserInteraction) onUserInteraction()
    },
  })

  useEffect(() => {
    // Don't auto-update view when user is drawing custom paths
    if (disableAutoUpdate) {
      return
    }

    if (shouldFollowDrone) {
      // Smooth pan to keep drone in view - use shorter duration for smoother following
      map.panTo(center, { animate: true, duration: 0.15 })
    } else if (forceRecenter) {
      // Location changed - fly to new location
      const prevCenter = prevCenterRef.current
      const centerChanged = Math.abs(prevCenter[0] - center[0]) > 0.01 || Math.abs(prevCenter[1] - center[1]) > 0.01
      if (centerChanged) {
        map.flyTo(center, zoom, { duration: 1.0 })
      }
    }
    prevCenterRef.current = center
  }, [map, center, zoom, shouldFollowDrone, disableAutoUpdate, forceRecenter])

  return null
}

// Scan area visualization - two concentric circles around the plane
function ScanArea({ position, altitude, heading }) {
  if (!position) return null

  // Circle radii in meters - outer and inner scan circles
  const outerRadius = 250  // ~250m outer circle
  const innerRadius = 150  // ~150m inner circle

  return (
    <>
      {/* Outer scan circle */}
      <Circle
        center={[position.lat, position.lon]}
        radius={outerRadius}
        pathOptions={{
          color: '#374151',
          weight: 3,
          fillColor: '#1f2937',
          fillOpacity: 0.25,
        }}
      />
      {/* Inner scan circle */}
      <Circle
        center={[position.lat, position.lon]}
        radius={innerRadius}
        pathOptions={{
          color: '#22c55e',
          weight: 2,
          fillColor: '#22c55e',
          fillOpacity: 0.1,
          dashArray: '8, 6',
        }}
      />
      {/* Center crosshair - vertical */}
      <Polyline
        positions={[
          [position.lat - 0.0008, position.lon],
          [position.lat + 0.0008, position.lon]
        ]}
        pathOptions={{
          color: '#ef4444',
          weight: 2,
          opacity: 0.8,
        }}
      />
      {/* Center crosshair - horizontal */}
      <Polyline
        positions={[
          [position.lat, position.lon - 0.001],
          [position.lat, position.lon + 0.001]
        ]}
        pathOptions={{
          color: '#ef4444',
          weight: 2,
          opacity: 0.8,
        }}
      />
    </>
  )
}

// Detection trail summary markers - shows stats at intervals along scanned path
function DetectionTrailMarker({ detection, index }) {
  const coords = detection.geometry.coordinates
  const props = detection.properties

  // Only show summary markers every few detections
  if (index % 8 !== 0) return null

  return (
    <CircleMarker
      center={[coords[1], coords[0]]}
      radius={4}
      fillColor={props.color}
      color="#fff"
      weight={1}
      fillOpacity={0.9}
    >
      <Popup>
        <div className="trail-popup">
          <strong>{props.category_name}</strong>
          <br />
          <small>{props.priority} priority</small>
        </div>
      </Popup>
    </CircleMarker>
  )
}

function Map({
  center,
  zoom,
  detections,
  flights,
  heatmapData,
  dronePosition,
  categories,
  satelliteView,
  demoActive,
  scanningDetection,
  waypoints,
  currentWaypointIndex,
  onWaypointClick,
  droneAltitude,
  populationDensityData,
  dronePathHistory,
  demoDetections,
  // Drawing mode props
  isDrawing,
  drawnPoints,
  onMapClick,
  customPathFlight,
  customPathDetections,
  // Geography data
  geographyData,
  // Follow drone controls
  followDrone = true,
  onFollowDroneChange,
}) {
  // Only follow drone during demo when followDrone is true
  const shouldFollowDrone = demoActive && dronePosition && followDrone

  // Track tile loading state
  const [tilesLoading, setTilesLoading] = useState(false)
  const handleLoadingChange = useCallback((loading) => {
    setTilesLoading(loading)
  }, [])

  // Get category color by id
  const getCategoryColor = (categoryId) => {
    const category = categories.find(c => c.id === categoryId)
    return category ? category.color : '#666'
  }

  // Get priority class
  const getPriorityClass = (priority) => {
    return `priority-badge ${priority}`
  }

  // Render geography features (water bodies, highways, shorelines)
  const renderGeography = () => {
    if (!geographyData || !geographyData.features) return null

    return geographyData.features.map((feature, idx) => {
      const props = feature.properties
      const geometry = feature.geometry

      // Water polygons (ocean, lake, lagoon)
      if (geometry.type === 'Polygon' && props.natural === 'water') {
        const positions = geometry.coordinates[0].map(coord => [coord[1], coord[0]])
        return (
          <Polygon
            key={`water-${idx}`}
            positions={positions}
            pathOptions={{
              color: '#1e40af',
              weight: 1,
              fillColor: '#3b82f6',
              fillOpacity: 0.3,
            }}
          >
            <Popup>
              <strong>{props.name}</strong>
              <br />
              <small>{props.type}</small>
            </Popup>
          </Polygon>
        )
      }

      // Highway/road linestrings
      if (geometry.type === 'LineString' && props.highway) {
        const positions = geometry.coordinates.map(coord => [coord[1], coord[0]])
        const isMotorway = props.highway === 'motorway'
        return (
          <Polyline
            key={`highway-${idx}`}
            positions={positions}
            pathOptions={{
              color: isMotorway ? '#dc2626' : '#f59e0b',
              weight: isMotorway ? 5 : 4,
              opacity: 0.8,
            }}
          >
            <Popup>
              <strong>{props.name}</strong>
              {props.ref && <><br /><small>{props.ref}</small></>}
            </Popup>
          </Polyline>
        )
      }

      // Shoreline linestrings
      if (geometry.type === 'LineString' && props.type === 'shoreline') {
        const positions = geometry.coordinates.map(coord => [coord[1], coord[0]])
        return (
          <Polyline
            key={`shoreline-${idx}`}
            positions={positions}
            pathOptions={{
              color: '#0ea5e9',
              weight: 3,
              opacity: 0.7,
              dashArray: '8, 4',
            }}
          >
            <Popup>
              <strong>{props.name}</strong>
              <br />
              <small>Shoreline - {props.trash_density} trash density</small>
            </Popup>
          </Polyline>
        )
      }

      // Stream/creek linestrings
      if (geometry.type === 'LineString' && props.type === 'stream') {
        const positions = geometry.coordinates.map(coord => [coord[1], coord[0]])
        return (
          <Polyline
            key={`stream-${idx}`}
            positions={positions}
            pathOptions={{
              color: '#3b82f6',
              weight: 2,
              opacity: 0.6,
            }}
          />
        )
      }

      return null
    })
  }

  // Render flight paths
  const renderFlightPaths = () => {
    const paths = []

    Object.entries(flights).forEach(([locationId, flightData]) => {
      if (!flightData || !flightData.features) return

      flightData.features.forEach((feature, idx) => {
        if (feature.geometry.type === 'LineString') {
          const positions = feature.geometry.coordinates.map(coord => [coord[1], coord[0]])
          paths.push(
            <Polyline
              key={`flight-${locationId}-${idx}`}
              positions={positions}
              color="#2563eb"
              weight={3}
              opacity={0.7}
              dashArray="10, 5"
            />
          )
        }
      })
    })

    return paths
  }

  // Render waypoint markers
  const renderWaypoints = () => {
    if (!waypoints || waypoints.length === 0) return null

    return waypoints.map((wp, idx) => (
      <Marker
        key={`wp-${idx}`}
        position={[wp.lat, wp.lon]}
        icon={waypointIcon}
        eventHandlers={{
          click: () => onWaypointClick && onWaypointClick(idx),
        }}
      >
        <Popup>
          <div className="waypoint-popup">
            <strong>{wp.name || `Waypoint ${idx + 1}`}</strong>
            <br />
            <small>{wp.lat.toFixed(4)}, {wp.lon.toFixed(4)}</small>
            {onWaypointClick && (
              <>
                <br />
                <button
                  className="waypoint-start-btn"
                  onClick={() => onWaypointClick(idx)}
                >
                  Start from here
                </button>
              </>
            )}
          </div>
        </Popup>
      </Marker>
    ))
  }

  // Render detection markers - size based on priority
  const renderDetections = () => {
    // Get radius based on priority level - larger for critical/high visibility
    const getPriorityRadius = (priority) => {
      switch (priority) {
        case 'critical': return 12  // Very large for critical
        case 'high': return 10      // Large for high priority
        case 'medium': return 6
        case 'low': return 4
        default: return 5
      }
    }

    // Get border color for better contrast based on priority
    const getPriorityBorderColor = (priority) => {
      switch (priority) {
        case 'critical': return '#dc2626'  // Dark red border
        case 'high': return '#ea580c'       // Dark orange border
        case 'medium': return '#ffffff'     // White border
        case 'low': return '#ffffff'        // White border
        default: return '#ffffff'
      }
    }

    // Get border weight based on priority
    const getPriorityWeight = (priority) => {
      switch (priority) {
        case 'critical': return 3
        case 'high': return 2.5
        case 'medium': return 1.5
        case 'low': return 1
        default: return 1.5
      }
    }

    return detections.map((detection, idx) => {
      const coords = detection.geometry.coordinates
      const props = detection.properties
      const color = getCategoryColor(props.category)
      const isScanning = scanningDetection && scanningDetection.properties.id === props.id
      const baseRadius = getPriorityRadius(props.priority)
      const borderColor = getPriorityBorderColor(props.priority)
      const borderWeight = getPriorityWeight(props.priority)

      return (
        <CircleMarker
          key={`det-${props.id || idx}`}
          center={[coords[1], coords[0]]}
          radius={isScanning ? baseRadius + 4 : baseRadius}
          fillColor={color}
          color={isScanning ? '#fff' : borderColor}
          weight={isScanning ? 3 : borderWeight}
          opacity={1}
          fillOpacity={isScanning ? 0.95 : 0.85}
          className={isScanning ? 'detection-scanning' : ''}
        >
          <Popup>
            <div className="detection-popup">
              <h4>
                {props.category_name}
                <span className={getPriorityClass(props.priority)}>
                  {props.priority}
                </span>
              </h4>
              <table>
                <tbody>
                  <tr>
                    <td>Confidence</td>
                    <td>{(props.confidence * 100).toFixed(1)}%</td>
                  </tr>
                  <tr>
                    <td>Est. Weight</td>
                    <td>{props.estimated_weight_kg.toFixed(2)} kg</td>
                  </tr>
                  <tr>
                    <td>Size</td>
                    <td>{(props.size_m2 * 10000).toFixed(1)} cm²</td>
                  </tr>
                  <tr>
                    <td>Location</td>
                    <td>{props.location}</td>
                  </tr>
                  <tr>
                    <td>Coordinates</td>
                    <td>{coords[1].toFixed(5)}, {coords[0].toFixed(5)}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </Popup>
        </CircleMarker>
      )
    })
  }

  // Render population density zones
  const renderPopulationDensity = () => {
    if (!populationDensityData || populationDensityData.length === 0) return null

    return populationDensityData.map((zone, idx) => {
      // Color based on density: low=green, medium=yellow, high=red
      const density = zone.density
      let color
      if (density < 500) {
        color = '#22c55e' // green - low density
      } else if (density < 1500) {
        color = '#eab308' // yellow - medium density
      } else if (density < 2500) {
        color = '#f97316' // orange - high density
      } else {
        color = '#ef4444' // red - very high density
      }

      return (
        <Circle
          key={`pop-${idx}`}
          center={[zone.lat, zone.lon]}
          radius={zone.radius_m}
          pathOptions={{
            color: color,
            weight: 2,
            fillColor: color,
            fillOpacity: 0.25,
            dashArray: '4, 4',
          }}
        >
          <Popup>
            <div className="density-popup">
              <strong>{zone.name}</strong>
              <br />
              <span className="density-value">{zone.density.toLocaleString()} people/km²</span>
            </div>
          </Popup>
        </Circle>
      )
    })
  }

  // Calculate map center - follow drone when enabled
  const mapCenter = shouldFollowDrone ? [dronePosition.lat, dronePosition.lon] : center
  const mapZoom = zoom // Use the zoom from props, don't override

  // Handle user interaction to disable auto-follow
  const handleUserInteraction = () => {
    if (demoActive && followDrone && onFollowDroneChange) {
      onFollowDroneChange(false)
    }
  }

  return (
    <>
    <MapContainer
      center={center}
      zoom={zoom}
      style={{ height: '100%', width: '100%' }}
      zoomControl={true}
    >
      <MapController
        center={mapCenter}
        zoom={mapZoom}
        shouldFollowDrone={shouldFollowDrone}
        disableAutoUpdate={isDrawing}
        onUserInteraction={handleUserInteraction}
        forceRecenter={!demoActive && !isDrawing}
      />

      {/* Tile loading tracker */}
      <TileLoadingTracker onLoadingChange={handleLoadingChange} />

      {/* Base map layer - CartoDB Voyager (always mounted, opacity controlled) */}
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        subdomains="abcd"
        opacity={satelliteView ? 0 : 1}
        className={satelliteView ? 'tile-layer-hidden' : ''}
      />

      {/* Satellite layer - ESRI World Imagery (always mounted for preloading) */}
      <TileLayer
        attribution='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        opacity={satelliteView ? 1 : 0}
        className={satelliteView ? '' : 'tile-layer-hidden'}
      />

      {/* Roads and labels overlay for satellite view */}
      <TileLayer
        attribution=''
        url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}"
        opacity={satelliteView ? 0.7 : 0}
        className={satelliteView ? '' : 'tile-layer-hidden'}
      />

      {/* Place names overlay for satellite view */}
      <TileLayer
        attribution=''
        url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}"
        opacity={satelliteView ? 0.8 : 0}
        className={satelliteView ? '' : 'tile-layer-hidden'}
      />

      {/* Geography features (water, highways, shorelines) */}
      {renderGeography()}

      {/* Heatmap layer */}
      {heatmapData.length > 0 && <HeatmapLayer data={heatmapData} />}

      {/* Population density overlay */}
      {renderPopulationDensity()}

      {/* Scanned path trail (shows where drone has been) */}
      {demoActive && dronePathHistory && dronePathHistory.length > 1 && (
        <Polyline
          positions={dronePathHistory}
          pathOptions={{
            color: '#22c55e',
            weight: 4,
            opacity: 0.8,
          }}
        />
      )}

      {/* Detection summary markers along the trail */}
      {demoActive && demoDetections && demoDetections.map((det, idx) => {
        // Show summary marker every 10 detections
        if (idx % 10 !== 0 || idx === 0) return null
        const coords = det.geometry.coordinates
        const props = det.properties

        // Calculate summary for last 10 detections
        const recentDets = demoDetections.slice(Math.max(0, idx - 10), idx)
        const totalWeight = recentDets.reduce((sum, d) => sum + d.properties.estimated_weight_kg, 0)
        const categories = [...new Set(recentDets.map(d => d.properties.category_name))]

        return (
          <CircleMarker
            key={`trail-sum-${idx}`}
            center={[coords[1], coords[0]]}
            radius={6}
            fillColor="#22c55e"
            color="#fff"
            weight={2}
            fillOpacity={0.9}
          >
            <Popup>
              <div className="trail-summary-popup">
                <strong>Scan Summary</strong>
                <div className="trail-stats">
                  <div><span className="stat-label">Items:</span> {recentDets.length}</div>
                  <div><span className="stat-label">Weight:</span> {totalWeight.toFixed(1)} kg</div>
                  <div><span className="stat-label">Types:</span> {categories.slice(0, 3).join(', ')}</div>
                </div>
              </div>
            </Popup>
          </CircleMarker>
        )
      })}

      {/* Flight paths */}
      {renderFlightPaths()}

      {/* Waypoint markers */}
      {renderWaypoints()}

      {/* Detection markers */}
      {renderDetections()}

      {/* Calculate drone heading from path history */}
      {(() => {
        let droneHeading = 90 // Default east
        if (dronePathHistory && dronePathHistory.length >= 2) {
          const prevPos = dronePathHistory[dronePathHistory.length - 2]
          const currPos = dronePathHistory[dronePathHistory.length - 1]
          droneHeading = calculateBearing(prevPos[0], prevPos[1], currPos[0], currPos[1])
        }

        return (
          <>
            {/* Drone scan area visualization */}
            {demoActive && dronePosition && (
              <ScanArea position={dronePosition} altitude={droneAltitude} heading={droneHeading} />
            )}

            {/* Drone position marker with rotation */}
            {dronePosition && (
              <Marker
                position={[dronePosition.lat, dronePosition.lon]}
                icon={createDroneIcon(droneHeading)}
              >
                <Popup>
                  <div className="drone-popup">
                    <strong>Sylva-1 Drone</strong>
                    <table>
                      <tbody>
                        <tr>
                          <td>Status</td>
                          <td><span className="status-active">Scanning</span></td>
                        </tr>
                        <tr>
                          <td>Altitude</td>
                          <td>{droneAltitude || 120}m AGL</td>
                        </tr>
                        <tr>
                          <td>Heading</td>
                          <td>{droneHeading.toFixed(0)}°</td>
                        </tr>
                        <tr>
                          <td>Position</td>
                          <td>{dronePosition.lat.toFixed(5)}, {dronePosition.lon.toFixed(5)}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </Popup>
              </Marker>
            )}
          </>
        )
      })()}

      {/* Drawing mode click handler */}
      <MapClickHandler isDrawing={isDrawing} onMapClick={onMapClick} />

      {/* Drawn points for custom path */}
      {drawnPoints && drawnPoints.length > 0 && drawnPoints.map((point, idx) => (
        <Marker
          key={`drawn-${idx}`}
          position={[point.lat, point.lon]}
          icon={drawnPointIcon}
        >
          <Popup>
            <div className="drawn-point-popup">
              <strong>Point {idx + 1}</strong>
              <br />
              <small>{point.lat.toFixed(5)}, {point.lon.toFixed(5)}</small>
            </div>
          </Popup>
        </Marker>
      ))}

      {/* Drawn path preview line */}
      {drawnPoints && drawnPoints.length > 1 && (
        <Polyline
          positions={drawnPoints.map(p => [p.lat, p.lon])}
          pathOptions={{
            color: '#f97316',
            weight: 3,
            opacity: 0.8,
            dashArray: '8, 8',
          }}
        />
      )}

      {/* Custom path flight line */}
      {customPathFlight && customPathFlight.features && customPathFlight.features.map((feature, idx) => {
        if (feature.geometry.type === 'LineString') {
          const positions = feature.geometry.coordinates.map(coord => [coord[1], coord[0]])
          return (
            <Polyline
              key={`custom-flight-${idx}`}
              positions={positions}
              pathOptions={{
                color: '#8b5cf6',
                weight: 4,
                opacity: 0.9,
              }}
            />
          )
        }
        return null
      })}

      {/* Custom path detections - size based on priority */}
      {customPathDetections && customPathDetections.features && customPathDetections.features.map((detection, idx) => {
        const coords = detection.geometry.coordinates
        const props = detection.properties
        // Size based on priority - larger for critical/high visibility
        const radius = props.priority === 'critical' ? 12
          : props.priority === 'high' ? 10
          : props.priority === 'medium' ? 6
          : 4
        // Border color for better contrast
        const borderColor = props.priority === 'critical' ? '#dc2626'
          : props.priority === 'high' ? '#ea580c'
          : '#ffffff'
        const borderWeight = props.priority === 'critical' ? 3
          : props.priority === 'high' ? 2.5
          : 1.5
        return (
          <CircleMarker
            key={`custom-det-${idx}`}
            center={[coords[1], coords[0]]}
            radius={radius}
            fillColor={props.color}
            color={borderColor}
            weight={borderWeight}
            fillOpacity={0.85}
          >
            <Popup>
              <div className="detection-popup">
                <h4>{props.category_name}</h4>
                <p>Confidence: {(props.confidence * 100).toFixed(1)}%</p>
                <p>Weight: {props.estimated_weight_kg.toFixed(2)} kg</p>
              </div>
            </Popup>
          </CircleMarker>
        )
      })}

    </MapContainer>

    {/* Loading indicator for tiles */}
    {tilesLoading && (
      <div className="map-loading-indicator">
        <div className="map-loading-spinner"></div>
        <span>Loading map...</span>
      </div>
    )}

    {/* Recenter button - shown when user has panned away during demo */}
    {demoActive && dronePosition && !followDrone && (
      <button
        className="recenter-button"
        onClick={() => onFollowDroneChange && onFollowDroneChange(true)}
        title="Re-center on drone"
      >
        Re-center
      </button>
    )}
    </>
  )
}

export default Map
