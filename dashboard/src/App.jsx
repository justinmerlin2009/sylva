import React, { useState, useEffect, useCallback, useRef } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import Map from './components/Map'
import Sidebar from './components/Sidebar'
import LiveDemo from './components/LiveDemo'
import DetectionPanel from './components/DetectionPanel'
import PathDrawer from './components/PathDrawer'
import AnnualData from './components/AnnualData'
import { getPreloadedData, isPreloadComplete } from './utils/SimulationPreloader'

const API_BASE = 'https://sylva-api.onrender.com/api'
const WS_BASE = 'wss://sylva-api.onrender.com'

// Instructions popup component
function InstructionsPopup({ onClose, onDontShowAgain }) {
  const [dontShow, setDontShow] = useState(false)

  const handleClose = () => {
    if (dontShow) {
      onDontShowAgain()
    }
    onClose()
  }

  return (
    <div className="instructions-overlay">
      <div className="instructions-popup">
        <h2>Welcome to Sylva Simulation</h2>
        <div className="instructions-content">
          <div className="instruction-item">
            <span className="instruction-icon">▶️</span>
            <div>
              <strong>Start Demo Survey</strong>
              <p>Select a location from the sidebar, then click "Start Demo" to watch a live drone survey simulation.</p>
            </div>
          </div>
          <div className="instruction-item">
            <span className="instruction-icon">🗺️</span>
            <div>
              <strong>Navigate the Map</strong>
              <p>Drag to pan, scroll to zoom. Click waypoint markers to start survey from that point.</p>
            </div>
          </div>
          <div className="instruction-item">
            <span className="instruction-icon">🛰️</span>
            <div>
              <strong>Satellite View</strong>
              <p>Toggle between map and satellite view using the button in the top-right corner.</p>
            </div>
          </div>
          <div className="instruction-item">
            <span className="instruction-icon">🔥</span>
            <div>
              <strong>Show Heatmap</strong>
              <p>Enable the heatmap toggle in the sidebar to see pollution density patterns.</p>
            </div>
          </div>
          <div className="instruction-item">
            <span className="instruction-icon">📊</span>
            <div>
              <strong>Annual Data 2026</strong>
              <p>Click "Annual Data 2026" button to view yearly analytics, trends, and reports.</p>
            </div>
          </div>
        </div>
        <div className="instructions-footer">
          <label className="dont-show-label">
            <input
              type="checkbox"
              checked={dontShow}
              onChange={(e) => setDontShow(e.target.checked)}
            />
            Don't show again for 24 hours
          </label>
          <button className="btn btn-primary" onClick={handleClose}>Got it!</button>
        </div>
      </div>
    </div>
  )
}

// Showcase overlay component - minimal and unobtrusive
function ShowcaseOverlay({ step, message, progress, onClose }) {
  // Location info based on step (2 locations: Stinson Beach, NASA)
  const getLocationInfo = () => {
    if (step === 1 || step === 2) return { icon: '🏖️', name: 'Stinson Beach, CA', type: 'Coastal Survey' }
    if (step === 3 || step === 4) return { icon: '🚀', name: 'NASA Space Center, TX', type: 'Urban Waterfront' }
    if (step === 5) return { icon: '✓', name: 'Demo Complete', type: 'Explore on your own!' }
    return { icon: '▶', name: 'Starting Demo...', type: '' }
  }

  const location = getLocationInfo()

  return (
    <div className="showcase-overlay">
      <button className="showcase-close" onClick={onClose}>✕ Exit</button>

      <div className="showcase-header-minimal">
        <div className="showcase-location-badge">
          <span className="location-icon-large">{location.icon}</span>
          <div className="location-info">
            <div className="location-name">{location.name}</div>
            <div className="location-type">{location.type}</div>
          </div>
        </div>
        {message && <div className="showcase-status">{message}</div>}
      </div>

      <div className="showcase-progress-minimal">
        <div className="showcase-progress-bar">
          <div className="showcase-progress-fill" style={{ width: `${progress}%` }}></div>
        </div>
        <div className="showcase-locations-dots">
          <span className={`dot ${step >= 1 ? 'active' : ''} ${step >= 3 ? 'done' : ''}`}>1</span>
          <span className={`dot ${step >= 3 ? 'active' : ''} ${step >= 5 ? 'done' : ''}`}>2</span>
        </div>
      </div>
    </div>
  )
}

function App() {
  // Instructions popup state
  const [showInstructions, setShowInstructions] = useState(false)

  // Check if we should show instructions on mount
  useEffect(() => {
    const dismissedUntil = localStorage.getItem('sylva_instructions_dismissed')
    if (dismissedUntil) {
      const dismissedTime = parseInt(dismissedUntil, 10)
      if (Date.now() < dismissedTime) {
        return // Still within "don't show" period
      }
    }
    setShowInstructions(true)
  }, [])

  const handleDontShowAgain = () => {
    const oneDayFromNow = Date.now() + (24 * 60 * 60 * 1000)
    localStorage.setItem('sylva_instructions_dismissed', oneDayFromNow.toString())
  }

  // Data state
  const [locations, setLocations] = useState([])
  const [flights, setFlights] = useState({})
  const [detections, setDetections] = useState([])
  const [stats, setStats] = useState(null)
  const [categories, setCategories] = useState([])
  const [heatmapData, setHeatmapData] = useState([])
  const [loading, setLoading] = useState(true)

  // UI state
  const [selectedLocation, setSelectedLocation] = useState('all')
  const [activeFilters, setActiveFilters] = useState({
    categories: [],
    priorities: [],
  })
  const [showHeatmap, setShowHeatmap] = useState(false)
  const [showFlightPath, setShowFlightPath] = useState(true)
  const [satelliteView, setSatelliteView] = useState(false)
  const [showPopulationDensity, setShowPopulationDensity] = useState(false)
  const [populationDensityData, setPopulationDensityData] = useState([])

  // Live demo state
  const [demoActive, setDemoActive] = useState(false)
  const [demoProgress, setDemoProgress] = useState(0)
  const [demoDetections, setDemoDetections] = useState([])
  const [dronePosition, setDronePosition] = useState(null)
  const [droneAltitude, setDroneAltitude] = useState(120)
  const [droneSpeed, setDroneSpeed] = useState(15)
  const [currentWaypointName, setCurrentWaypointName] = useState('')
  const [waypoints, setWaypoints] = useState([])
  const [dronePathHistory, setDronePathHistory] = useState([]) // Track scanned path
  const [followDrone, setFollowDrone] = useState(true) // Toggle for following drone during demo

  // Computer Vision AI panel state
  const [scanningDetection, setScanningDetection] = useState(null)
  const [showDetectionPanel, setShowDetectionPanel] = useState(false)

  // Custom path drawing state
  const [isDrawing, setIsDrawing] = useState(false)
  const [drawnPoints, setDrawnPoints] = useState([])
  const [customPaths, setCustomPaths] = useState([])
  const [selectedCustomPath, setSelectedCustomPath] = useState(null)
  const [customPathFlight, setCustomPathFlight] = useState(null)
  const [customPathDetections, setCustomPathDetections] = useState(null)

  // Annual data panel state
  const [showAnnualData, setShowAnnualData] = useState(false)

  // Map loading state - for impressive initial load experience
  const [mapReady, setMapReady] = useState(false)

  // Force map ready after 6 seconds max (fallback if tiles don't trigger callback)
  useEffect(() => {
    const timeout = setTimeout(() => {
      if (!mapReady) {
        setMapReady(true)
      }
    }, 6000) // 6 second max
    return () => clearTimeout(timeout)
  }, [mapReady])

  // Showcase mode state
  const [showcaseMode, setShowcaseMode] = useState(false)
  const [showcaseStep, setShowcaseStep] = useState(0)
  const [showcaseMessage, setShowcaseMessage] = useState('')
  const [forceMapRecenter, setForceMapRecenter] = useState(false)
  const showcaseTimerRef = useRef(null)
  const showcaseActiveRef = useRef(false) // Ref to avoid stale closure

  const wsRef = useRef(null)

  // Load initial data
  useEffect(() => {
    loadInitialData()
  }, [])

  // Load data when location changes
  useEffect(() => {
    if (!loading) {
      loadDetections()
      loadStats()
      loadWaypoints()
      loadPopulationDensity()
    }
  }, [selectedLocation, activeFilters])

  const loadInitialData = async () => {
    try {
      setLoading(true)

      // Check if data was preloaded from Home page
      const preloaded = getPreloadedData()
      const hasPreloadedData = isPreloadComplete() && preloaded.locations && preloaded.categories

      if (hasPreloadedData) {
        // Use preloaded data for instant load
        console.log('Using preloaded simulation data')
        setLocations(preloaded.locations.locations)
        setCategories(preloaded.categories.categories)
        setHeatmapData(preloaded.heatmap)
        setFlights(preloaded.flights)

        if (preloaded.detections) {
          setDetections(preloaded.detections.features || [])
        }
        if (preloaded.stats) {
          setStats(preloaded.stats)
        }

        setLoading(false)
        return
      }

      // Fallback: fetch data from API if not preloaded
      const [locationsRes, categoriesRes, heatmapRes] = await Promise.all([
        axios.get(`${API_BASE}/locations`),
        axios.get(`${API_BASE}/detections/categories`),
        axios.get(`${API_BASE}/heatmap`),
      ])

      setLocations(locationsRes.data.locations)
      setCategories(categoriesRes.data.categories)
      setHeatmapData(heatmapRes.data)

      // Load flights for each location
      const flightsData = {}
      for (const loc of locationsRes.data.locations) {
        try {
          const flightRes = await axios.get(`${API_BASE}/flights/${loc.id}`)
          flightsData[loc.id] = flightRes.data
        } catch (e) {
          console.warn(`Could not load flight for ${loc.id}`)
        }
      }
      setFlights(flightsData)

      await loadDetections()
      await loadStats()

      setLoading(false)
    } catch (error) {
      console.error('Error loading data:', error)
      setLoading(false)
    }
  }

  const loadWaypoints = async () => {
    const location = selectedLocation === 'all' ? 'stinson_beach' : selectedLocation
    const loc = locations.find(l => l.id === location)
    if (loc && loc.waypoints) {
      setWaypoints(loc.waypoints)
    }
  }

  const loadDetections = async () => {
    try {
      const params = new URLSearchParams()

      if (selectedLocation !== 'all') {
        params.append('location', selectedLocation)
      }

      const response = await axios.get(`${API_BASE}/detections?${params}`)
      let features = response.data.features || []

      if (activeFilters.categories.length > 0) {
        features = features.filter(f =>
          activeFilters.categories.includes(f.properties.category)
        )
      }

      if (activeFilters.priorities.length > 0) {
        features = features.filter(f =>
          activeFilters.priorities.includes(f.properties.priority)
        )
      }

      setDetections(features)
    } catch (error) {
      console.error('Error loading detections:', error)
    }
  }

  const loadStats = async () => {
    try {
      const location = selectedLocation !== 'all' ? selectedLocation : null
      const url = location
        ? `${API_BASE}/stats?location=${location}`
        : `${API_BASE}/stats`

      const response = await axios.get(url)
      setStats(response.data)
    } catch (error) {
      console.error('Error loading stats:', error)
    }
  }

  const loadPopulationDensity = async () => {
    try {
      const location = selectedLocation !== 'all' ? selectedLocation : null
      const url = location
        ? `${API_BASE}/population-density?location=${location}`
        : `${API_BASE}/population-density`

      const response = await axios.get(url)
      setPopulationDensityData(response.data.zones || [])
    } catch (error) {
      console.error('Error loading population density:', error)
    }
  }

  const toggleCategoryFilter = (category) => {
    setActiveFilters(prev => {
      const categories = prev.categories.includes(category)
        ? prev.categories.filter(c => c !== category)
        : [...prev.categories, category]
      return { ...prev, categories }
    })
  }

  const togglePriorityFilter = (priority) => {
    setActiveFilters(prev => {
      const priorities = prev.priorities.includes(priority)
        ? prev.priorities.filter(p => p !== priority)
        : [...prev.priorities, priority]
      return { ...prev, priorities }
    })
  }

  const clearFilters = () => {
    setActiveFilters({ categories: [], priorities: [] })
  }

  // Live Demo Functions
  const startDemo = useCallback((location, speed = 1.0, startWaypoint = 0) => {
    if (wsRef.current) {
      wsRef.current.close()
    }

    const ws = new WebSocket(`${WS_BASE}/ws/live`)
    wsRef.current = ws

    ws.onopen = () => {
      setDemoActive(true)
      setDemoDetections([])
      setDemoProgress(0)
      setScanningDetection(null)
      setShowDetectionPanel(true)
      setDronePathHistory([]) // Reset path history
      setFollowDrone(true) // Start following drone

      ws.send(JSON.stringify({
        command: 'start',
        location: location,
        speed: speed,
        start_waypoint: startWaypoint,
      }))
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.type === 'demo_start') {
        setDroneAltitude(data.altitude || 120)
        setDroneSpeed(data.speed || 15)
        if (data.waypoints) {
          setWaypoints(data.waypoints)
        }
      } else if (data.type === 'frame') {
        const newPos = {
          lat: data.position.lat,
          lon: data.position.lon,
        }
        setDronePosition(newPos)
        // Track path history for trail visualization (every 3rd point for performance)
        if (data.frame_index % 3 === 0) {
          setDronePathHistory(prev => [...prev, [newPos.lat, newPos.lon]])
        }
        setDemoProgress(data.progress * 100)
        setDroneAltitude(data.altitude || 120)
        setDroneSpeed(data.speed || 15)
        setCurrentWaypointName(data.current_waypoint_name || '')

        // POSITION-BASED SYNC: Add ALL new detections to the map immediately
        // This keeps detection dots synchronized with drone position
        if (data.new_detections && data.new_detections.length > 0) {
          setDemoDetections(prev => [...prev, ...data.new_detections])
        }

        // Handle Computer Vision AI panel detection (sampled - every 5th detection)
        // This is separate from map dots - only for the AI panel animation
        if (data.detection_event && data.new_detection) {
          setScanningDetection(data.new_detection)

          // Clear scanning state after animation
          setTimeout(() => {
            setScanningDetection(null)
          }, 1200)
        }
      } else if (data.type === 'demo_complete') {
        setDemoActive(false)
        setDronePosition(null)
        setScanningDetection(null)
      }
    }

    ws.onclose = () => {
      setDemoActive(false)
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      setDemoActive(false)
    }
  }, [])

  const stopDemo = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close()
    }
    setDemoActive(false)
    setDronePosition(null)
    setDemoDetections([])
    setDemoProgress(0)
    setScanningDetection(null)
    setShowDetectionPanel(false)
    setDronePathHistory([]) // Reset path history
  }, [])

  // Showcase mode functions - fully hands-off automated demo
  // Order: Stinson Beach → NASA Space Center (2 locations only)

  const startShowcase = useCallback(() => {
    // Set ref immediately to avoid stale closure issues
    showcaseActiveRef.current = true
    setShowcaseMode(true)
    setShowcaseStep(0)
    setShowcaseMessage('Starting Sylva Demo...')
    setSatelliteView(false)  // Start with map view (faster tile loading)
    setShowHeatmap(false)
    setShowInstructions(false)
    setFollowDrone(true)

    // Go straight to first location - no intro delay
    setTimeout(() => {
      if (showcaseActiveRef.current) {
        runShowcaseStep(1)
      }
    }, 500)
  }, [])

  const runShowcaseStep = (step) => {
    // Use ref to check if still active (avoids stale closure)
    if (!showcaseActiveRef.current) return

    setShowcaseStep(step)

    const DEMO_SPEED = 2.5  // 2.5x speed for smooth showcase (allows tiles to load)
    const DEMO_DURATION = 20000  // 20 seconds per location for smooth experience
    const FLY_DURATION = 2500  // 2.5 seconds to fly to new location

    // Helper to trigger map recenter
    const flyToLocation = (locationId, satellite, heatmap) => {
      stopDemo()
      setForceMapRecenter(true)
      setSelectedLocation(locationId)
      setSatelliteView(satellite)
      setShowHeatmap(heatmap)
      // Reset force recenter after map has time to respond
      setTimeout(() => setForceMapRecenter(false), 100)
    }

    if (step === 1) {
      // Fly to Stinson Beach
      flyToLocation('stinson_beach', false, false)  // Start with map view (faster tiles)
      setShowcaseMessage('Flying to Stinson Beach, California...')
      showcaseTimerRef.current = setTimeout(() => {
        if (showcaseActiveRef.current) runShowcaseStep(2)
      }, FLY_DURATION)
    } else if (step === 2) {
      // Run demo at Stinson Beach
      setShowcaseMessage('Coastal Survey — Detecting marine debris')
      startDemo('stinson_beach', DEMO_SPEED, 0)
      // Dynamic view changes during flight (adjusted for 20s duration)
      setTimeout(() => { if (showcaseActiveRef.current) setSatelliteView(true) }, 5000)   // Switch to satellite at 5s
      setTimeout(() => { if (showcaseActiveRef.current) setShowHeatmap(true) }, 12000)   // Show heatmap at 12s
      setTimeout(() => { if (showcaseActiveRef.current) setSatelliteView(false) }, 16000) // Back to map at 16s
      showcaseTimerRef.current = setTimeout(() => {
        if (showcaseActiveRef.current) runShowcaseStep(3)
      }, DEMO_DURATION)
    } else if (step === 3) {
      // Fly to NASA Space Center
      flyToLocation('nasa_space_center', false, false)  // Start with map view
      setShowcaseMessage('Flying to NASA Space Center, Texas...')
      showcaseTimerRef.current = setTimeout(() => {
        if (showcaseActiveRef.current) runShowcaseStep(4)
      }, FLY_DURATION)
    } else if (step === 4) {
      // Run demo at NASA
      setShowcaseMessage('Urban Waterfront — Detecting debris')
      startDemo('nasa_space_center', DEMO_SPEED, 0)
      // Dynamic view changes (adjusted for 20s duration)
      setTimeout(() => { if (showcaseActiveRef.current) setSatelliteView(true) }, 5000)    // Switch to satellite at 5s
      setTimeout(() => { if (showcaseActiveRef.current) setShowHeatmap(true) }, 10000)    // Show heatmap at 10s
      setTimeout(() => { if (showcaseActiveRef.current) setSatelliteView(false) }, 15000) // Back to map at 15s
      showcaseTimerRef.current = setTimeout(() => {
        if (showcaseActiveRef.current) runShowcaseStep(5)
      }, DEMO_DURATION)
    } else if (step === 5) {
      // Demo complete
      stopDemo()
      setShowHeatmap(true)
      setShowcaseMessage('Demo complete — Click anywhere to explore!')
      showcaseTimerRef.current = setTimeout(() => {
        showcaseActiveRef.current = false
        setShowcaseMode(false)
        setShowcaseStep(0)
      }, 4000)
    }
  }

  const stopShowcase = useCallback(() => {
    showcaseActiveRef.current = false
    if (showcaseTimerRef.current) {
      clearTimeout(showcaseTimerRef.current)
    }
    stopDemo()
    setShowcaseMode(false)
    setShowcaseStep(0)
    setForceMapRecenter(false)
  }, [stopDemo])

  // Calculate showcase progress (5 steps total for 2 locations)
  const getShowcaseProgress = () => {
    const baseProgress = (showcaseStep / 5) * 100
    if (showcaseStep % 2 === 0 && showcaseStep > 0 && showcaseStep < 5) {
      // During demo steps, add demo progress
      return baseProgress + (demoProgress / 5)
    }
    return baseProgress
  }

  const handleWaypointClick = (waypointIndex) => {
    if (!demoActive) {
      const location = selectedLocation === 'all' ? 'stinson_beach' : selectedLocation
      startDemo(location, 1.0, waypointIndex)
    }
  }

  // Custom Path Drawing Functions
  const handleStartDrawing = () => {
    setIsDrawing(true)
    setDrawnPoints([])
    setSelectedCustomPath(null)
    setCustomPathFlight(null)
    setCustomPathDetections(null)
  }

  const handleCancelDrawing = () => {
    setIsDrawing(false)
    setDrawnPoints([])
  }

  const handleMapClick = (point) => {
    if (isDrawing) {
      setDrawnPoints(prev => [...prev, point])
    }
  }

  const handleRemovePoint = (index) => {
    setDrawnPoints(prev => prev.filter((_, i) => i !== index))
  }

  const handleCreatePath = async (pathData) => {
    try {
      const response = await axios.post(`${API_BASE}/custom-path`, pathData)
      const newPath = response.data
      setCustomPaths(prev => [...prev, newPath])
      setIsDrawing(false)
      setDrawnPoints([])

      // Load the created path details
      await handleSelectCustomPath(newPath)

      return newPath
    } catch (error) {
      console.error('Failed to create custom path:', error)
      throw error
    }
  }

  const handleSelectCustomPath = async (path) => {
    setSelectedCustomPath(path)

    try {
      // Load flight path and detections
      const [flightRes, detectionsRes] = await Promise.all([
        axios.get(`${API_BASE}/custom-path/${path.id}/flight`),
        axios.get(`${API_BASE}/custom-path/${path.id}/detections`),
      ])

      setCustomPathFlight(flightRes.data)
      setCustomPathDetections(detectionsRes.data)

      // Center map on the custom path
      if (flightRes.data.features && flightRes.data.features.length > 0) {
        const coords = flightRes.data.features[0].geometry.coordinates
        if (coords.length > 0) {
          const midIdx = Math.floor(coords.length / 2)
          setSelectedLocation('all') // Reset to show custom path
        }
      }
    } catch (error) {
      console.error('Failed to load custom path details:', error)
    }
  }

  const handleDeleteCustomPath = async (pathId) => {
    try {
      await axios.delete(`${API_BASE}/custom-path/${pathId}`)
      setCustomPaths(prev => prev.filter(p => p.id !== pathId))
      if (selectedCustomPath?.id === pathId) {
        setSelectedCustomPath(null)
        setCustomPathFlight(null)
        setCustomPathDetections(null)
      }
    } catch (error) {
      console.error('Failed to delete custom path:', error)
    }
  }

  const handleSaveResults = async (pathId) => {
    try {
      const response = await axios.post(`${API_BASE}/custom-path/${pathId}/save-results`)
      alert(`Results saved!\n\nTotal detections: ${response.data.stats.total_detections}\nTotal weight: ${response.data.stats.total_weight_kg} kg`)
      return response.data
    } catch (error) {
      console.error('Failed to save results:', error)
      throw error
    }
  }

  const handleRunCustomDemo = (pathId) => {
    // Stop any existing demo first
    if (wsRef.current) {
      wsRef.current.close()
    }

    // Start live demo for custom path
    const path = customPaths.find(p => p.id === pathId)
    if (!path) {
      console.error('Path not found:', pathId)
      return
    }

    // Load path details first
    handleSelectCustomPath(path)

    // Start WebSocket demo with custom_path_id
    const ws = new WebSocket(`${WS_BASE}/ws/live`)
    wsRef.current = ws

    ws.onopen = () => {
      console.log('Starting custom path demo:', pathId)
      setDemoActive(true)
      setDemoDetections([])
      setDemoProgress(0)
      setDronePathHistory([])
      setShowDetectionPanel(true)

      ws.send(JSON.stringify({
        command: 'start',
        custom_path_id: pathId,
        speed: 1.0,  // Default speed
      }))
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.type === 'error') {
        console.error('Demo error:', data.message)
        alert(`Error: ${data.message}`)
        setDemoActive(false)
        return
      }

      if (data.type === 'demo_start') {
        console.log('Custom demo started:', data.location)
        setDroneAltitude(data.altitude || 120)
      } else if (data.type === 'frame') {
        const newPos = {
          lat: data.position.lat,
          lon: data.position.lon,
        }
        setDronePosition(newPos)
        setDemoProgress(data.progress * 100)
        setDroneAltitude(data.altitude || 120)

        // Update path history
        if (data.frame_index % 3 === 0) {
          setDronePathHistory(prev => [...prev, [newPos.lat, newPos.lon]])
        }

        // Handle detections
        if (data.new_detections && data.new_detections.length > 0) {
          setDemoDetections(prev => [...prev, ...data.new_detections])
        }

        // Computer Vision AI panel
        if (data.detection_event && data.new_detection) {
          setScanningDetection(data.new_detection)
          setTimeout(() => setScanningDetection(null), 1200)
        }
      } else if (data.type === 'demo_complete') {
        console.log('Custom demo complete:', data.total_detections, 'detections')
        setDemoActive(false)
        setDronePosition(null)
      }
    }

    ws.onclose = () => {
      setDemoActive(false)
    }

    ws.onerror = (error) => {
      console.error('Custom demo WebSocket error:', error)
      setDemoActive(false)
    }
  }

  // Get map center based on selected location
  const getMapCenter = () => {
    if (demoActive && dronePosition) {
      return [dronePosition.lat, dronePosition.lon]
    }
    // When drawing, don't change center - let user control the map freely
    // The Map component will ignore center updates when isDrawing is true
    if (selectedLocation === 'all') {
      // Center of continental US to show all 3 locations (CA, OH, TX)
      return [38.5, -98.0]
    }
    const loc = locations.find(l => l.id === selectedLocation)
    if (loc && loc.center) {
      return [loc.center.lat, loc.center.lon]
    }
    return [38.5, -98.0]
  }

  const getMapZoom = () => {
    if (demoActive) {
      // Zoomed in close to ground during live flight demo
      const loc = locations.find(l => l.id === (selectedLocation === 'all' ? 'stinson_beach' : selectedLocation))
      if (loc?.id === 'stinson_beach') return 16  // Close ground view
      if (loc?.id === 'lake_erie') return 15       // Highway corridor view
      if (loc?.id === 'nasa_space_center') return 16
      return 16
    }
    // When drawing, don't force zoom - let user control freely
    // The Map component will ignore zoom updates when isDrawing is true
    if (selectedLocation === 'all') {
      return 4  // Wide US view to see all 3 locations (CA, OH, TX)
    }
    // Zoom levels to show full flight path with all waypoints
    if (selectedLocation === 'stinson_beach') return 13  // ~13km path
    if (selectedLocation === 'lake_erie') return 7       // ~430km path - needs wide view
    if (selectedLocation === 'nasa_space_center') return 12  // ~23km path
    return 12
  }

  if (loading) {
    return (
      <div className="app-container">
        <div className="loading">Loading Sylva Dashboard...</div>
      </div>
    )
  }

  // Only show detections during or after a demo has run (demoDetections populated)
  const displayDetections = demoDetections.length > 0 ? demoDetections : (demoActive ? [] : [])

  // Generate progressive heatmap from demo detections (only shows scanned areas)
  const generateProgressiveHeatmap = (demoDetections) => {
    if (!demoDetections || demoDetections.length === 0) return []

    return demoDetections.map(det => {
      const coords = det.geometry.coordinates
      // Calculate intensity based on priority
      let intensity = 0.5
      if (det.properties.priority === 'critical') intensity = 1.0
      else if (det.properties.priority === 'high') intensity = 0.8
      else if (det.properties.priority === 'medium') intensity = 0.6

      return [coords[1], coords[0], intensity]
    })
  }

  const displayFlights = showFlightPath
    ? (selectedLocation === 'all' ? flights : { [selectedLocation]: flights[selectedLocation] })
    : {}

  // Get waypoints for current location
  const currentWaypoints = selectedLocation === 'all'
    ? locations.find(l => l.id === 'stinson_beach')?.waypoints || []
    : locations.find(l => l.id === selectedLocation)?.waypoints || []

  // Calculate live stats from demo detections during simulation
  const calculateLiveStats = (detections) => {
    if (!detections || detections.length === 0) {
      return {
        total_weight_kg: 0,
        by_priority: { critical: 0, high: 0, medium: 0, low: 0 },
        by_category: []
      }
    }

    let totalWeight = 0
    const priorityCounts = { critical: 0, high: 0, medium: 0, low: 0 }
    const categoryCounts = {}

    detections.forEach(det => {
      const props = det.properties
      totalWeight += props.estimated_weight_kg || 0
      priorityCounts[props.priority] = (priorityCounts[props.priority] || 0) + 1
      categoryCounts[props.category] = (categoryCounts[props.category] || 0) + 1
    })

    return {
      total_weight_kg: totalWeight,
      by_priority: priorityCounts,
      by_category: Object.entries(categoryCounts).map(([cat, count]) => ({
        category: cat,
        count
      }))
    }
  }

  // Use live stats during demo, otherwise use static stats from API
  const displayStats = demoActive || demoDetections.length > 0
    ? calculateLiveStats(demoDetections)
    : stats

  return (
    <div className="app-container">
      <Sidebar
        locations={locations}
        selectedLocation={selectedLocation}
        onLocationChange={setSelectedLocation}
        categories={categories}
        activeFilters={activeFilters}
        onToggleCategory={toggleCategoryFilter}
        onTogglePriority={togglePriorityFilter}
        onClearFilters={clearFilters}
        stats={displayStats}
        detectionCount={displayDetections.length}
        showHeatmap={showHeatmap}
        onToggleHeatmap={() => setShowHeatmap(!showHeatmap)}
        showFlightPath={showFlightPath}
        onToggleFlightPath={() => setShowFlightPath(!showFlightPath)}
        satelliteView={satelliteView}
        onToggleSatellite={() => setSatelliteView(!satelliteView)}
        showPopulationDensity={showPopulationDensity}
        onTogglePopulationDensity={() => setShowPopulationDensity(!showPopulationDensity)}
        populationDensity={locations.find(l => l.id === selectedLocation)?.population_density || 0}
      >
        <LiveDemo
          locations={locations}
          selectedLocation={selectedLocation}
          demoActive={demoActive}
          demoProgress={demoProgress}
          demoDetectionCount={demoDetections.length}
          onStart={startDemo}
          onStop={stopDemo}
          waypoints={currentWaypoints}
          currentWaypointName={currentWaypointName}
          droneAltitude={droneAltitude}
          droneSpeed={droneSpeed}
        />
      </Sidebar>

      <div className="main-content">
        <header className="header">
          <div className="header-left">
            <Link to="/" className="logo home-link">
              <span className="back-arrow">←</span>
              <h1 className="sylva-title">SYLVA</h1>
              <span className="logo-subtitle">Environmental Monitoring System</span>
            </Link>
            {/* Watch Showcase Button - in header */}
            {!showcaseMode && !demoActive && (
              <button className="showcase-header-btn" onClick={startShowcase}>
                <span className="showcase-btn-icon">▶</span>
                <span className="showcase-btn-text">Watch Showcase</span>
              </button>
            )}
          </div>
          <div className="header-controls">
            <button
              className="map-toggle-btn"
              onClick={() => setShowAnnualData(true)}
              style={{ background: 'linear-gradient(135deg, #2563eb, #7c3aed)', color: 'white', border: 'none' }}
            >
              Annual Data 2026
            </button>
            <button
              className={`map-toggle-btn ${satelliteView ? 'active' : ''}`}
              onClick={() => setSatelliteView(!satelliteView)}
            >
              {satelliteView ? '🛰️ Satellite' : '🗺️ Map'}
            </button>
            <span className="detection-count">{displayDetections.length} detections</span>
          </div>
        </header>

        <div className="map-container">
          <Map
            center={getMapCenter()}
            zoom={getMapZoom()}
            detections={displayDetections}
            flights={displayFlights}
            heatmapData={showHeatmap ? (demoActive ? generateProgressiveHeatmap(demoDetections) : heatmapData) : []}
            dronePosition={dronePosition}
            categories={categories}
            satelliteView={satelliteView}
            demoActive={demoActive}
            scanningDetection={scanningDetection}
            waypoints={demoActive ? [] : currentWaypoints}
            onWaypointClick={handleWaypointClick}
            droneAltitude={droneAltitude}
            populationDensityData={showPopulationDensity ? populationDensityData : []}
            dronePathHistory={dronePathHistory}
            demoDetections={demoDetections}
            // Custom path drawing props
            isDrawing={isDrawing}
            drawnPoints={drawnPoints}
            onMapClick={handleMapClick}
            customPathFlight={customPathFlight}
            customPathDetections={customPathDetections}
            geographyData={null}
            // Follow drone controls
            followDrone={followDrone}
            onFollowDroneChange={setFollowDrone}
            // Showcase recenter control
            forceRecenter={forceMapRecenter}
            // Initial load callback
            onMapReady={() => setMapReady(true)}
          />

          {/* Computer Vision AI Panel - shows during demo */}
          {demoActive && showDetectionPanel && (
            <DetectionPanel
              detection={scanningDetection}
              isProcessing={!!scanningDetection}
              dronePosition={dronePosition}
              droneAltitude={droneAltitude}
              totalDetections={demoDetections.length}
              onClose={() => setShowDetectionPanel(false)}
            />
          )}

          {/* Custom Path Drawer Panel */}
          <div className="path-drawer-panel">
            <PathDrawer
              isDrawing={isDrawing}
              onStartDrawing={handleStartDrawing}
              onCancelDrawing={handleCancelDrawing}
              drawnPoints={drawnPoints}
              onAddPoint={handleMapClick}
              onRemovePoint={handleRemovePoint}
              onCreatePath={handleCreatePath}
              onSaveResults={handleSaveResults}
              customPaths={customPaths}
              selectedCustomPath={selectedCustomPath}
              onSelectCustomPath={handleSelectCustomPath}
              onDeleteCustomPath={handleDeleteCustomPath}
              onRunCustomDemo={handleRunCustomDemo}
            />
          </div>
        </div>
      </div>

      {/* Annual Data Panel */}
      <AnnualData
        isOpen={showAnnualData}
        onClose={() => setShowAnnualData(false)}
      />

      {/* Instructions Popup */}
      {showInstructions && (
        <InstructionsPopup
          onClose={() => setShowInstructions(false)}
          onDontShowAgain={handleDontShowAgain}
        />
      )}

      {/* Showcase Mode Overlay */}
      {showcaseMode && (
        <ShowcaseOverlay
          step={showcaseStep}
          message={showcaseMessage}
          progress={getShowcaseProgress()}
          onClose={stopShowcase}
        />
      )}

      {/* Initial Map Loading Splash Screen */}
      {!mapReady && !loading && (
        <div className="map-splash-screen">
          <div className="splash-content">
            <div className="splash-logo">SYLVA</div>
            <div className="splash-tagline">Environmental Monitoring System</div>
            <div className="splash-loader">
              <div className="splash-drone">
                <span className="splash-drone-icon">✈</span>
              </div>
              <div className="splash-progress-track">
                <div className="splash-progress-fill"></div>
              </div>
            </div>
            <div className="splash-status">Initializing Map...</div>
          </div>
        </div>
      )}

    </div>
  )
}

export default App
