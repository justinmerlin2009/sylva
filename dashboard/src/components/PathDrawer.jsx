import React, { useState, useEffect } from 'react'

function PathDrawer({
  isDrawing,
  onStartDrawing,
  onCancelDrawing,
  drawnPoints,
  onAddPoint,
  onRemovePoint,
  onCreatePath,
  onSaveResults,
  customPaths,
  selectedCustomPath,
  onSelectCustomPath,
  onDeleteCustomPath,
  onRunCustomDemo,
}) {
  const [pathName, setPathName] = useState('')
  const [altitude, setAltitude] = useState(120)
  const [speed, setSpeed] = useState(25)
  const [isCreating, setIsCreating] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [isCollapsed, setIsCollapsed] = useState(true) // Collapsed by default

  const handleCreate = async () => {
    if (drawnPoints.length < 2) {
      alert('Please add at least 2 points to create a path')
      return
    }

    setIsCreating(true)
    try {
      await onCreatePath({
        name: pathName || `Custom Path ${new Date().toLocaleDateString()}`,
        waypoints: drawnPoints,
        survey_altitude_m: altitude,
        survey_speed_ms: speed,
      })
      setPathName('')
    } catch (error) {
      console.error('Failed to create path:', error)
      alert('Failed to create path')
    }
    setIsCreating(false)
  }

  const handleSave = async (pathId) => {
    setIsSaving(true)
    try {
      await onSaveResults(pathId)
    } catch (error) {
      console.error('Failed to save results:', error)
      alert('Failed to save results. The path may have been lost after a server restart. Please create a new path.')
    }
    setIsSaving(false)
  }

  return (
    <div className={`path-drawer ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="path-drawer-header" onClick={() => setIsCollapsed(!isCollapsed)}>
        <h3>Custom Flight Path</h3>
        <button
          className="collapse-btn"
          onClick={(e) => {
            e.stopPropagation()
            setIsCollapsed(!isCollapsed)
          }}
          title={isCollapsed ? 'Expand' : 'Collapse'}
        >
          {isCollapsed ? '▲' : '▼'}
        </button>
      </div>

      {/* Content - only show when not collapsed */}
      {!isCollapsed && (
        <>
          {/* Drawing Mode */}
          {!isDrawing ? (
            <div className="path-drawer-actions">
              <button className="btn btn-primary" onClick={onStartDrawing}>
                Draw New Path
              </button>
              <p className="helper-text">
                Click points on the map to create a custom flight path for highway or area surveys.
              </p>
            </div>
          ) : (
            <div className="path-drawing-mode">
              <div className="drawing-status">
                <span className="status-indicator active"></span>
                <span>Drawing Mode Active</span>
              </div>

              <div className="form-group">
                <label>Path Name</label>
                <input
                  type="text"
                  value={pathName}
                  onChange={(e) => setPathName(e.target.value)}
                  placeholder="e.g., Highway 66 Survey"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Altitude (m)</label>
                  <input
                    type="number"
                    value={altitude}
                    onChange={(e) => setAltitude(Number(e.target.value))}
                    min={50}
                    max={500}
                  />
                </div>
                <div className="form-group">
                  <label>Speed (m/s)</label>
                  <input
                    type="number"
                    value={speed}
                    onChange={(e) => setSpeed(Number(e.target.value))}
                    min={10}
                    max={35}
                  />
                </div>
              </div>

              <div className="drawn-points">
                <h4>Waypoints ({drawnPoints.length})</h4>
                <div className="points-list">
                  {drawnPoints.map((point, idx) => (
                    <div key={idx} className="point-item">
                      <span className="point-num">{idx + 1}</span>
                      <span className="point-coords">
                        {point.lat.toFixed(5)}, {point.lon.toFixed(5)}
                      </span>
                      <button
                        className="btn-remove"
                        onClick={() => onRemovePoint(idx)}
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
                {drawnPoints.length === 0 && (
                  <p className="helper-text">Click on the map to add waypoints</p>
                )}
              </div>

              <div className="drawing-buttons">
                <button
                  className="btn btn-success"
                  onClick={handleCreate}
                  disabled={drawnPoints.length < 2 || isCreating}
                >
                  {isCreating ? 'Creating...' : 'Create Path'}
                </button>
                <button className="btn btn-secondary" onClick={onCancelDrawing}>
                  Cancel
                </button>
              </div>
            </div>
          )}

          {/* Saved Custom Paths */}
          {customPaths.length > 0 && (
            <div className="custom-paths-list">
              <h4>Saved Paths</h4>
              {customPaths.map((path) => (
                <div
                  key={path.id}
                  className={`custom-path-item ${selectedCustomPath?.id === path.id ? 'selected' : ''}`}
                  onClick={() => onSelectCustomPath(path)}
                >
                  <div className="path-info">
                    <span className="path-name">{path.name}</span>
                    <span className="path-stats">
                      {path.waypoint_count} points · {path.detection_count} detections
                    </span>
                  </div>
                  <div className="path-actions">
                    <button
                      className="btn-icon"
                      onClick={(e) => {
                        e.stopPropagation()
                        onRunCustomDemo(path.id)
                      }}
                      title="Run Demo"
                    >
                      ▶
                    </button>
                    <button
                      className="btn-icon"
                      onClick={(e) => {
                        e.stopPropagation()
                        handleSave(path.id)
                      }}
                      title="Save Results"
                      disabled={isSaving}
                    >
                      💾
                    </button>
                    <button
                      className="btn-icon delete"
                      onClick={(e) => {
                        e.stopPropagation()
                        onDeleteCustomPath(path.id)
                      }}
                      title="Delete"
                    >
                      🗑
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Selected Path Details */}
          {selectedCustomPath && (
            <div className="selected-path-details">
              <h4>Path Details</h4>
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="detail-label">Detections</span>
                  <span className="detail-value">{selectedCustomPath.detection_count}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Waypoints</span>
                  <span className="detail-value">{selectedCustomPath.waypoint_count}</span>
                </div>
              </div>
              <div className="export-buttons">
                <button
                  className="btn btn-sm"
                  onClick={async () => {
                    try {
                      // Fetch full flight path and animation data from API
                      const [flightRes, animRes] = await Promise.all([
                        fetch(`http://localhost:8000/api/custom-path/${selectedCustomPath.id}/flight`),
                        fetch(`http://localhost:8000/api/custom-path/${selectedCustomPath.id}/animation`)
                      ])
                      const flightPath = await flightRes.json()
                      const animation = await animRes.json()

                      // Combine all data for export
                      const exportData = {
                        ...selectedCustomPath,
                        flight_path: flightPath,
                        animation_data: animation
                      }

                      const data = JSON.stringify(exportData, null, 2)
                      const blob = new Blob([data], { type: 'application/json' })
                      const url = URL.createObjectURL(blob)
                      const a = document.createElement('a')
                      a.href = url
                      a.download = `${selectedCustomPath.name.replace(/\s+/g, '_')}_full_export.json`
                      a.click()
                    } catch (error) {
                      console.error('Export error:', error)
                      // Fallback to basic export
                      const data = JSON.stringify(selectedCustomPath, null, 2)
                      const blob = new Blob([data], { type: 'application/json' })
                      const url = URL.createObjectURL(blob)
                      const a = document.createElement('a')
                      a.href = url
                      a.download = `${selectedCustomPath.name.replace(/\s+/g, '_')}_export.json`
                      a.click()
                    }
                  }}
                >
                  Export Full Data
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default PathDrawer
