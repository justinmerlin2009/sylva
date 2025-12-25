import React, { useState, useEffect } from 'react'

// Enhanced trash type icons with clearer, more recognizable designs
const TRASH_ICONS = {
  plastic_bottle: {
    icon: '🧴',
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <rect x="24" y="4" width="16" height="10" rx="3" fill="#3498db"/>
      <rect x="26" y="14" width="12" height="4" fill="#2980b9"/>
      <path d="M22 18 L42 18 L44 56 L20 56 Z" fill="#3498db"/>
      <rect x="26" y="24" width="4" height="28" rx="2" fill="#fff" opacity="0.4"/>
      <ellipse cx="32" cy="56" rx="12" ry="3" fill="#2980b9"/>
    </svg>`,
    label: 'PLASTIC',
    color: '#3498db'
  },
  food_packaging: {
    icon: '📦',
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <rect x="8" y="20" width="48" height="36" rx="4" fill="#e67e22"/>
      <rect x="12" y="24" width="40" height="28" rx="2" fill="#f39c12"/>
      <rect x="16" y="30" width="24" height="3" rx="1" fill="#fff" opacity="0.5"/>
      <rect x="16" y="36" width="18" height="3" rx="1" fill="#fff" opacity="0.5"/>
      <rect x="16" y="42" width="12" height="3" rx="1" fill="#fff" opacity="0.5"/>
      <path d="M8 20 L16 8 L48 8 L56 20" fill="#d35400"/>
    </svg>`,
    label: 'PACKAGING',
    color: '#e67e22'
  },
  tire: {
    icon: '⚫',
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <circle cx="32" cy="32" r="28" fill="#2c3e50"/>
      <circle cx="32" cy="32" r="22" fill="#34495e"/>
      <circle cx="32" cy="32" r="12" fill="#1a1a2e"/>
      <circle cx="32" cy="32" r="8" fill="#2c3e50"/>
      <rect x="30" y="4" width="4" height="10" fill="#1a1a2e"/>
      <rect x="30" y="50" width="4" height="10" fill="#1a1a2e"/>
      <rect x="4" y="30" width="10" height="4" fill="#1a1a2e"/>
      <rect x="50" y="30" width="10" height="4" fill="#1a1a2e"/>
    </svg>`,
    label: 'TIRE',
    color: '#2c3e50'
  },
  metal_debris: {
    icon: '🔩',
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <ellipse cx="32" cy="48" rx="26" ry="8" fill="#7f8c8d"/>
      <ellipse cx="32" cy="40" rx="26" ry="8" fill="#95a5a6"/>
      <ellipse cx="32" cy="32" rx="26" ry="8" fill="#bdc3c7"/>
      <ellipse cx="32" cy="24" rx="26" ry="8" fill="#95a5a6"/>
      <ellipse cx="32" cy="16" rx="26" ry="8" fill="#7f8c8d"/>
      <rect x="28" y="16" width="8" height="32" fill="#ecf0f1" opacity="0.3"/>
    </svg>`,
    label: 'METAL',
    color: '#95a5a6'
  },
  construction_waste: {
    icon: '🧱',
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <rect x="4" y="40" width="24" height="16" fill="#8e44ad"/>
      <rect x="20" y="40" width="24" height="16" fill="#9b59b6"/>
      <rect x="36" y="40" width="24" height="16" fill="#8e44ad"/>
      <rect x="12" y="24" width="24" height="16" fill="#9b59b6"/>
      <rect x="28" y="24" width="24" height="16" fill="#8e44ad"/>
      <rect x="20" y="8" width="24" height="16" fill="#9b59b6"/>
      <rect x="6" y="42" width="20" height="2" fill="#5b2c6f" opacity="0.5"/>
    </svg>`,
    label: 'DEBRIS',
    color: '#8e44ad'
  },
  organic_waste: {
    icon: '🍂',
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <ellipse cx="32" cy="44" rx="24" ry="16" fill="#27ae60"/>
      <ellipse cx="26" cy="40" rx="10" ry="8" fill="#2ecc71"/>
      <ellipse cx="40" cy="46" rx="8" ry="6" fill="#229954"/>
      <path d="M32 28c0-12 8-20 8-20s8 12 8 20c0 8-8 10-8 10s-8-2-8-10z" fill="#27ae60"/>
      <path d="M24 32c-6-8-16-10-16-10s6 12 12 16c4 4 8 2 8 2s2-4-4-8z" fill="#2ecc71"/>
    </svg>`,
    label: 'ORGANIC',
    color: '#27ae60'
  },
  glass: {
    icon: '🍾',
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <rect x="26" y="4" width="12" height="8" rx="2" fill="#16a085"/>
      <path d="M24 12 L40 12 L44 56 L20 56 Z" fill="#1abc9c" opacity="0.7"/>
      <rect x="28" y="16" width="4" height="36" rx="1" fill="#fff" opacity="0.5"/>
      <ellipse cx="32" cy="56" rx="12" ry="4" fill="#16a085"/>
    </svg>`,
    label: 'GLASS',
    color: '#1abc9c'
  },
  textile: {
    icon: '👕',
    svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <path d="M20 8 L44 8 L44 16 L52 16 L52 28 L44 28 L44 56 L20 56 L20 28 L12 28 L12 16 L20 16 Z" fill="#e74c3c"/>
      <path d="M20 8 L32 16 L44 8" fill="#c0392b"/>
      <rect x="28" y="24" width="8" height="4" rx="1" fill="#fff" opacity="0.3"/>
    </svg>`,
    label: 'TEXTILE',
    color: '#e74c3c'
  },
}

// Get trash icon data
const getTrashIcon = (category) => {
  return TRASH_ICONS[category] || TRASH_ICONS.plastic_bottle
}

// Simulated CV processing stages - slower for detailed visualization
const CV_STAGES = [
  { id: 'capture', label: '4K Frame Capture', duration: 800 },
  { id: 'multispectral', label: 'Multi-spectral Analysis', duration: 600 },
  { id: 'preprocess', label: 'Image Enhancement', duration: 500 },
  { id: 'detect', label: 'Object Detection (YOLOv8)', duration: 900 },
  { id: 'classify', label: 'Waste Classification CNN', duration: 800 },
  { id: 'estimate', label: 'Size/Weight Estimation', duration: 500 },
  { id: 'geotag', label: 'GPS Geo-tagging', duration: 400 },
]

// Camera system info
const CAMERA_SPECS = {
  primary: '4K RGB (3840x2160)',
  secondary: '4K Wide-angle',
  spectral: 'Multi-spectral (NIR/NDVI)',
  snapshot: '20MP High-res Capture',
}

function DetectionPanel({
  detection,
  isProcessing,
  dronePosition,
  droneAltitude,
  totalDetections,
  onClose,
}) {
  const [currentStage, setCurrentStage] = useState(0)
  const [stageProgress, setStageProgress] = useState(0)
  const [processingComplete, setProcessingComplete] = useState(false)
  const [displayedDetection, setDisplayedDetection] = useState(null)

  // Only show every Nth detection in the CV panel to reduce animation frequency
  // This shows "1 of X" style - not every single detection
  useEffect(() => {
    if (detection && isProcessing) {
      // Only animate CV panel for every 5th detection (or first one)
      if (totalDetections === 1 || totalDetections % 5 === 0) {
        setDisplayedDetection(detection)
        setCurrentStage(0)
        setStageProgress(0)
        setProcessingComplete(false)
      }
    }
  }, [detection, isProcessing, totalDetections])

  // Simulate CV processing stages - runs independently
  useEffect(() => {
    if (!displayedDetection) {
      return
    }

    let stageIndex = 0
    let progress = 0

    const interval = setInterval(() => {
      progress += 5  // Faster progress since we show fewer

      if (progress >= 100) {
        stageIndex++
        progress = 0

        if (stageIndex >= CV_STAGES.length) {
          setProcessingComplete(true)
          clearInterval(interval)
          return
        }
      }

      setCurrentStage(stageIndex)
      setStageProgress(progress)
    }, 60)

    return () => clearInterval(interval)
  }, [displayedDetection])

  if (!detection) {
    return (
      <div className="detection-panel">
        <div className="detection-panel-header">
          <h3>CV Detection Analysis</h3>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>
        <div className="camera-view">
          <div className="camera-frame">
            <div className="camera-overlay">
              <div className="scan-line"></div>
              <div className="waiting-message">
                <span>Scanning...</span>
                <small>Waiting for detection</small>
              </div>
            </div>
            <div className="camera-info">
              <span>ALT: {droneAltitude || 120}m</span>
              <span>{CAMERA_SPECS.primary}</span>
            </div>
          </div>
        </div>
        {/* Camera system specs */}
        <div className="camera-specs">
          <h4>Camera System</h4>
          <div className="spec-grid">
            <div className="spec-item">
              <span className="spec-label">Primary</span>
              <span className="spec-value">{CAMERA_SPECS.primary}</span>
            </div>
            <div className="spec-item">
              <span className="spec-label">Wide-angle</span>
              <span className="spec-value">{CAMERA_SPECS.secondary}</span>
            </div>
            <div className="spec-item">
              <span className="spec-label">Spectral</span>
              <span className="spec-value">{CAMERA_SPECS.spectral}</span>
            </div>
            <div className="spec-item">
              <span className="spec-label">Snapshot</span>
              <span className="spec-value">{CAMERA_SPECS.snapshot}</span>
            </div>
          </div>
        </div>
        <div className="detection-panel-footer">
          <span>Total Detections: <strong>{totalDetections}</strong></span>
        </div>
      </div>
    )
  }

  // Use displayed detection (every 5th) for CV animation
  const activeDetection = displayedDetection || detection
  const props = activeDetection.properties
  const coords = activeDetection.geometry.coordinates
  const trashData = getTrashIcon(props.category)
  const trashSvgUrl = `data:image/svg+xml,${encodeURIComponent(trashData.svg)}`

  return (
    <div className="detection-panel">
      <div className="detection-panel-header">
        <h3>CV Detection Analysis</h3>
        <span className="detection-counter">#{totalDetections}</span>
        <button className="close-btn" onClick={onClose}>×</button>
      </div>

      {/* Large prominent trash type indicator */}
      <div className="trash-type-banner" style={{ backgroundColor: trashData.color }}>
        <span className="trash-emoji">{trashData.icon}</span>
        <span className="trash-type-label">{trashData.label} DETECTED</span>
      </div>

      {/* Simulated camera view with trash icon */}
      <div className="camera-view">
        <div className="camera-frame">
          <div className="camera-overlay">
            <div className="scan-line"></div>

            {/* Trash icon in detection box */}
            <div className="detection-box" style={{ borderColor: trashData.color }}>
              <img
                src={trashSvgUrl}
                alt={props.category_name}
                className="trash-image"
              />
              <span className="detection-label" style={{ backgroundColor: trashData.color }}>
                {processingComplete ? props.category_name : 'Analyzing...'}
              </span>
              {processingComplete && (
                <span className="confidence-badge">
                  {(props.confidence * 100).toFixed(0)}%
                </span>
              )}
            </div>

            <div className="camera-info">
              <span>ALT: {droneAltitude || 120}m</span>
              <span>4K + NIR</span>
              <span className="live-indicator">● LIVE</span>
            </div>
          </div>
          <div className="camera-coords">
            {coords[1].toFixed(6)}, {coords[0].toFixed(6)}
          </div>
        </div>
      </div>

      {/* Processing stages */}
      <div className="cv-stages">
        <h4>AI Processing Pipeline</h4>
        {CV_STAGES.map((stage, idx) => (
          <div
            key={stage.id}
            className={`cv-stage ${idx < currentStage ? 'complete' : ''} ${idx === currentStage ? 'active' : ''}`}
          >
            <div className="stage-indicator">
              {idx < currentStage ? '✓' : idx === currentStage ? '●' : '○'}
            </div>
            <div className="stage-info">
              <span className="stage-label">{stage.label}</span>
              {idx === currentStage && (
                <div className="stage-progress">
                  <div
                    className="stage-progress-bar"
                    style={{ width: `${stageProgress}%` }}
                  ></div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Detection result */}
      {processingComplete && (
        <div className="detection-result">
          <h4>Detection Result</h4>
          <div className="result-header">
            <div className="result-icon-wrapper" style={{ backgroundColor: trashData.color }}>
              <span className="result-emoji">{trashData.icon}</span>
            </div>
            <div className="result-title">
              <span className="result-type" style={{ color: trashData.color }}>
                {props.category_name}
              </span>
              <span className={`result-priority priority-${props.priority}`}>
                {props.priority.toUpperCase()} PRIORITY
              </span>
            </div>
          </div>
          <div className="result-grid">
            <div className="result-item">
              <span className="result-label">Confidence</span>
              <span className="result-value">{(props.confidence * 100).toFixed(1)}%</span>
            </div>
            <div className="result-item">
              <span className="result-label">Est. Size</span>
              <span className="result-value">{(props.size_m2 * 10000).toFixed(0)} cm²</span>
            </div>
            <div className="result-item">
              <span className="result-label">Est. Weight</span>
              <span className="result-value">{props.estimated_weight_kg.toFixed(2)} kg</span>
            </div>
            <div className="result-item">
              <span className="result-label">Detection ID</span>
              <span className="result-value id">{props.id.slice(-8)}</span>
            </div>
          </div>
        </div>
      )}

      {/* Stats footer */}
      <div className="detection-panel-footer">
        <span>Total Detections: <strong>{totalDetections}</strong></span>
      </div>
    </div>
  )
}

export default DetectionPanel
