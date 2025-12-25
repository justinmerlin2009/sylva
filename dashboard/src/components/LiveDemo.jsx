import React, { useState } from 'react'

function LiveDemo({
  locations,
  selectedLocation,
  demoActive,
  demoProgress,
  demoDetectionCount,
  onStart,
  onStop,
  waypoints,
  selectedWaypoint,
  onWaypointSelect,
  currentWaypointName,
  droneAltitude,
  droneSpeed,
}) {
  const [speed, setSpeed] = useState('1')
  const [startWaypoint, setStartWaypoint] = useState(0)

  const handleStart = () => {
    const location = selectedLocation === 'all' ? 'stinson_beach' : selectedLocation
    onStart(location, parseFloat(speed), startWaypoint)
  }

  const getLocationName = (id) => {
    if (id === 'stinson_beach') return 'Stinson Beach'
    if (id === 'route_66') return 'Route 66'
    return id
  }

  const demoLocation = selectedLocation === 'all' ? 'stinson_beach' : selectedLocation

  // Get waypoints for current location
  const locationWaypoints = waypoints || []

  return (
    <div className="demo-controls">
      <h3>
        {demoActive ? 'Live Scanning' : 'Live Demo Mode'}
      </h3>

      {!demoActive ? (
        <>
          <p style={{ fontSize: '12px', color: '#64748b', marginBottom: '12px' }}>
            Simulate a low-altitude drone survey with real-time AI trash detection over{' '}
            <strong>{getLocationName(demoLocation)}</strong>
          </p>

          {/* Waypoint selector */}
          {locationWaypoints.length > 0 && (
            <div className="waypoint-selector">
              <label>Start from waypoint:</label>
              <select
                value={startWaypoint}
                onChange={(e) => setStartWaypoint(parseInt(e.target.value))}
              >
                {locationWaypoints.map((wp, idx) => (
                  <option key={idx} value={idx}>
                    {wp.name || `Waypoint ${idx + 1}`}
                  </option>
                ))}
              </select>
            </div>
          )}

          <div className="speed-control" style={{ marginBottom: '12px' }}>
            <label>Animation Speed:</label>
            <select
              value={speed}
              onChange={(e) => setSpeed(e.target.value)}
            >
              <option value="0.5">0.5x (Slow - Best for demos)</option>
              <option value="1">1x (Normal)</option>
              <option value="2">2x (Fast)</option>
              <option value="5">5x (Very Fast)</option>
            </select>
          </div>

          <div className="demo-buttons">
            <button
              className="demo-btn primary"
              onClick={handleStart}
            >
              Start Survey
            </button>
          </div>

          <div className="demo-features">
            <h4>Demo Features:</h4>
            <ul>
              <li>Close-up drone following</li>
              <li>Real-time CV detection</li>
              <li>Individual trash identification</li>
              <li>Geo-tagging visualization</li>
            </ul>
          </div>
        </>
      ) : (
        <>
          {/* Flight info */}
          <div className="flight-info">
            <div className="flight-stat">
              <span className="flight-stat-label">Location</span>
              <span className="flight-stat-value">{getLocationName(demoLocation)}</span>
            </div>
            <div className="flight-stat">
              <span className="flight-stat-label">Waypoint</span>
              <span className="flight-stat-value">{currentWaypointName || 'En route'}</span>
            </div>
            <div className="flight-stat">
              <span className="flight-stat-label">Altitude</span>
              <span className="flight-stat-value">{droneAltitude || 120}m AGL</span>
            </div>
            <div className="flight-stat">
              <span className="flight-stat-label">Speed</span>
              <span className="flight-stat-value">{droneSpeed || 15} m/s</span>
            </div>
          </div>

          {/* Progress */}
          <div style={{ marginBottom: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
              <span>Survey Progress</span>
              <span>{demoProgress.toFixed(0)}%</span>
            </div>
            <div className="progress-bar">
              <div
                className="progress-bar-fill"
                style={{ width: `${demoProgress}%` }}
              />
            </div>
          </div>

          {/* Detection counter */}
          <div className="detection-counter">
            <div className="detection-counter-icon">📷</div>
            <div className="detection-counter-info">
              <span className="detection-counter-value">{demoDetectionCount}</span>
              <span className="detection-counter-label">Objects Detected</span>
            </div>
          </div>

          <div className="demo-buttons">
            <button
              className="demo-btn secondary"
              onClick={onStop}
            >
              Stop Survey
            </button>
          </div>
        </>
      )}
    </div>
  )
}

export default LiveDemo
