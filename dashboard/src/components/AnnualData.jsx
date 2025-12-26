import React, { useState, useEffect } from 'react'
import axios from 'axios'
import {
  LineChart, Line, BarChart, Bar, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell
} from 'recharts'

const API_BASE = 'https://sylva-api.onrender.com/api'

function AnnualData({ isOpen, onClose }) {
  const [loading, setLoading] = useState(true)
  const [annualData, setAnnualData] = useState(null)
  const [hotspotsData, setHotspotsData] = useState([])
  const [cleanupsData, setCleanupsData] = useState([])
  const [activeTab, setActiveTab] = useState('overview')
  const [selectedYear] = useState(2026)

  useEffect(() => {
    if (isOpen) {
      loadAnnualData()
    }
  }, [isOpen])

  const loadAnnualData = async () => {
    try {
      setLoading(true)
      const [annualRes, hotspotsRes, cleanupsRes] = await Promise.all([
        axios.get(`${API_BASE}/analytics/annual/${selectedYear}`),
        axios.get(`${API_BASE}/analytics/hotspots/${selectedYear}`),
        axios.get(`${API_BASE}/analytics/cleanups/${selectedYear}`),
      ])
      setAnnualData(annualRes.data)
      setHotspotsData(hotspotsRes.data.hotspots || [])
      setCleanupsData(cleanupsRes.data.cleanups || [])
      setLoading(false)
    } catch (error) {
      console.error('Error loading annual data:', error)
      setLoading(false)
    }
  }

  const handleExportCSV = async () => {
    try {
      const response = await axios.get(`${API_BASE}/reports/export/${selectedYear}`)
      const data = response.data

      // Convert detections to CSV
      const headers = ['ID', 'Date', 'Category', 'Priority', 'Weight (kg)', 'Location', 'Water Risk', 'Lat', 'Lon']
      const rows = data.detections.features.map(f => [
        f.properties.id,
        f.properties.timestamp,
        f.properties.category_name,
        f.properties.priority,
        f.properties.estimated_weight_kg,
        f.properties.location,
        f.properties.water_risk_level,
        f.geometry.coordinates[1],
        f.geometry.coordinates[0]
      ])

      const csv = [headers.join(','), ...rows.map(r => r.join(','))].join('\n')
      const blob = new Blob([csv], { type: 'text/csv' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `sylva_detections_${selectedYear}.csv`
      a.click()
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Export failed:', error)
      alert('Export failed. Please try again.')
    }
  }

  const handleExportJSON = async () => {
    try {
      const response = await axios.get(`${API_BASE}/reports/export/${selectedYear}`)
      const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `sylva_report_${selectedYear}.json`
      a.click()
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Export failed:', error)
      alert('Export failed. Please try again.')
    }
  }

  if (!isOpen) return null

  if (loading) {
    return (
      <div className="annual-data-overlay">
        <div className="annual-data-panel">
          <div className="annual-loading">Loading annual data...</div>
        </div>
      </div>
    )
  }

  if (!annualData) {
    return (
      <div className="annual-data-overlay">
        <div className="annual-data-panel">
          <div className="annual-error">Failed to load data</div>
        </div>
      </div>
    )
  }

  // Prepare monthly chart data
  const monthlyData = Object.entries(annualData.by_month || {}).map(([month, data]) => ({
    month: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][parseInt(month) - 1],
    detections: data.detections,
    weight: Math.round(data.weight_kg),
    flights: data.flights
  }))

  // Category pie data
  const categoryData = (annualData.by_category || []).map(cat => ({
    name: cat.name,
    value: cat.count,
    color: cat.color
  }))

  // Location comparison data
  const locationData = Object.entries(annualData.by_location || {}).map(([id, data]) => ({
    name: id === 'stinson_beach' ? 'Stinson Beach' :
          id === 'route_66' ? 'Lake Erie' : 'NASA Space Center',
    detections: data.total_detections,
    weight: Math.round(data.total_weight_kg),
    critical: data.by_priority?.critical || 0
  }))

  return (
    <div className="annual-data-overlay">
      <div className="annual-data-panel">
        <div className="annual-header">
          <div className="annual-title">
            <h2>Annual Analytics {selectedYear}</h2>
            <span className="annual-subtitle">Multi-Drone Environmental Monitoring</span>
          </div>
          <div className="annual-actions">
            <button className="export-btn" onClick={handleExportCSV}>Export CSV</button>
            <button className="export-btn" onClick={handleExportJSON}>Export JSON</button>
            <button className="close-btn" onClick={onClose}>Close</button>
          </div>
        </div>

        {/* Tabs */}
        <div className="annual-tabs">
          <button
            className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button
            className={`tab-btn ${activeTab === 'trends' ? 'active' : ''}`}
            onClick={() => setActiveTab('trends')}
          >
            Trends
          </button>
          <button
            className={`tab-btn ${activeTab === 'water' ? 'active' : ''}`}
            onClick={() => setActiveTab('water')}
          >
            Water Risk
          </button>
          <button
            className={`tab-btn ${activeTab === 'cleanup' ? 'active' : ''}`}
            onClick={() => setActiveTab('cleanup')}
          >
            Cleanup Impact
          </button>
        </div>

        <div className="annual-content">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="tab-content">
              {/* Key Metrics */}
              <div className="metrics-grid">
                <div className="metric-card large primary">
                  <div className="metric-value">{annualData.total_detections?.toLocaleString()}</div>
                  <div className="metric-label">Total Detections</div>
                </div>
                <div className="metric-card large warning">
                  <div className="metric-value">{annualData.total_weight_kg?.toLocaleString()} kg</div>
                  <div className="metric-label">Debris Identified</div>
                </div>
                <div className="metric-card">
                  <div className="metric-value">{annualData.total_flights}</div>
                  <div className="metric-label">Survey Flights</div>
                </div>
                <div className="metric-card">
                  <div className="metric-value">{annualData.drones_deployed}</div>
                  <div className="metric-label">Drones Deployed</div>
                </div>
                <div className="metric-card">
                  <div className="metric-value">{annualData.total_area_surveyed_km2?.toFixed(1)} km²</div>
                  <div className="metric-label">Area Surveyed</div>
                </div>
                <div className="metric-card">
                  <div className="metric-value">{annualData.locations_monitored}</div>
                  <div className="metric-label">Locations Monitored</div>
                </div>
              </div>

              {/* Priority Breakdown */}
              <div className="section-title">Priority Distribution</div>
              <div className="priority-grid">
                <div className="priority-card critical">
                  <div className="priority-value">{annualData.by_priority?.critical || 0}</div>
                  <div className="priority-label">Critical</div>
                </div>
                <div className="priority-card high">
                  <div className="priority-value">{annualData.by_priority?.high || 0}</div>
                  <div className="priority-label">High</div>
                </div>
                <div className="priority-card medium">
                  <div className="priority-value">{annualData.by_priority?.medium || 0}</div>
                  <div className="priority-label">Medium</div>
                </div>
                <div className="priority-card low">
                  <div className="priority-value">{annualData.by_priority?.low || 0}</div>
                  <div className="priority-label">Low</div>
                </div>
              </div>

              {/* Category Breakdown */}
              <div className="section-title">Detection Categories</div>
              <div className="chart-container small">
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={categoryData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      labelLine={false}
                    >
                      {categoryData.map((entry, index) => (
                        <Cell key={index} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              {/* Location Comparison */}
              <div className="section-title">By Location</div>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={locationData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="detections" fill="#2563eb" name="Detections" />
                    <Bar dataKey="critical" fill="#ef4444" name="Critical" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* Trends Tab */}
          {activeTab === 'trends' && (
            <div className="tab-content">
              <div className="section-title">Monthly Detection Trends</div>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={250}>
                  <AreaChart data={monthlyData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Legend />
                    <Area
                      type="monotone"
                      dataKey="detections"
                      stroke="#2563eb"
                      fill="#2563eb"
                      fillOpacity={0.3}
                      name="Detections"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <div className="section-title">Monthly Weight (kg)</div>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={monthlyData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Bar dataKey="weight" fill="#f59e0b" name="Weight (kg)" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="insight-box">
                <div className="insight-title">Seasonal Pattern</div>
                <div className="insight-text">
                  Peak detection rates occur in summer months (June-August) with +40% higher activity due to increased beach usage.
                  Winter months show reduced detection rates (-20%) due to lower outdoor activity.
                </div>
              </div>
            </div>
          )}

          {/* Water Risk Tab */}
          {activeTab === 'water' && (
            <div className="tab-content">
              <div className="water-risk-header">
                <h3>Water Pollution Risk Assessment</h3>
                <p>Items detected near water bodies that pose environmental risks</p>
              </div>

              <div className="metrics-grid">
                <div className="metric-card danger">
                  <div className="metric-value">{annualData.water_risk_summary?.critical_near_water || 0}</div>
                  <div className="metric-label">Critical Near Water</div>
                </div>
                <div className="metric-card warning">
                  <div className="metric-value">{annualData.water_risk_summary?.high_risk_near_water || 0}</div>
                  <div className="metric-label">High Risk Near Water</div>
                </div>
                <div className="metric-card success">
                  <div className="metric-value">{annualData.water_risk_summary?.estimated_water_pollution_prevented_kg?.toFixed(1) || 0} kg</div>
                  <div className="metric-label">Pollution Prevented</div>
                </div>
                <div className="metric-card primary">
                  <div className="metric-value">{annualData.water_risk_summary?.weight_cleaned_kg?.toFixed(1) || 0} kg</div>
                  <div className="metric-label">Weight Cleaned</div>
                </div>
              </div>

              <div className="section-title">High-Risk Hotspots</div>
              <div className="hotspot-list">
                {hotspotsData.filter(h => h.water_risk === 'critical' || h.water_risk === 'high').slice(0, 6).map((hotspot, idx) => (
                  <div key={idx} className={`hotspot-item ${hotspot.water_risk}`}>
                    <div className="hotspot-name">{hotspot.name}</div>
                    <div className="hotspot-details">
                      <span className="hotspot-location">{hotspot.location_name}</span>
                      <span className={`hotspot-risk ${hotspot.water_risk}`}>{hotspot.water_risk}</span>
                    </div>
                    <div className="hotspot-stats">
                      <span>{hotspot.total_detections} detections</span>
                      <span>{hotspot.total_weight_kg?.toFixed(1)} kg</span>
                    </div>
                    <div className={`hotspot-trend ${hotspot.trend_direction}`}>
                      {hotspot.trend_direction === 'improving' ? 'Improving' :
                       hotspot.trend_direction === 'worsening' ? 'Worsening' : 'Stable'}
                    </div>
                  </div>
                ))}
              </div>

              <div className="water-risk-info">
                <div className="risk-level-legend">
                  <div className="risk-item critical">
                    <span className="risk-dot"></span>
                    <span>Critical (&lt;25m from water)</span>
                  </div>
                  <div className="risk-item high">
                    <span className="risk-dot"></span>
                    <span>High (25-100m)</span>
                  </div>
                  <div className="risk-item medium">
                    <span className="risk-dot"></span>
                    <span>Medium (100-500m)</span>
                  </div>
                  <div className="risk-item low">
                    <span className="risk-dot"></span>
                    <span>Low (&gt;500m)</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Cleanup Impact Tab */}
          {activeTab === 'cleanup' && (
            <div className="tab-content">
              <div className="cleanup-header">
                <h3>Cleanup Operations & Impact</h3>
                <p>Demonstrating measurable environmental improvement</p>
              </div>

              <div className="metrics-grid">
                <div className="metric-card success">
                  <div className="metric-value">{annualData.cleanup_summary?.total_cleanup_events || 0}</div>
                  <div className="metric-label">Cleanup Events</div>
                </div>
                <div className="metric-card primary">
                  <div className="metric-value">{annualData.cleanup_summary?.total_items_removed || 0}</div>
                  <div className="metric-label">Items Removed</div>
                </div>
                <div className="metric-card warning">
                  <div className="metric-value">{annualData.cleanup_summary?.total_weight_removed_kg?.toFixed(1) || 0} kg</div>
                  <div className="metric-label">Weight Removed</div>
                </div>
                <div className="metric-card">
                  <div className="metric-value">{annualData.cleanup_summary?.total_crew_hours || 0}</div>
                  <div className="metric-label">Crew Hours</div>
                </div>
              </div>

              <div className="section-title">Recent Cleanup Events</div>
              <div className="cleanup-list">
                {cleanupsData.slice(0, 8).map((cleanup, idx) => (
                  <div key={idx} className="cleanup-item">
                    <div className="cleanup-date">{new Date(cleanup.date).toLocaleDateString()}</div>
                    <div className="cleanup-location">{cleanup.location_name}</div>
                    <div className="cleanup-stats">
                      <span className="cleanup-items">{cleanup.items_removed} items</span>
                      <span className="cleanup-weight">{cleanup.weight_removed_kg?.toFixed(1)} kg</span>
                    </div>
                    <div className="cleanup-result">
                      <span className="reduction">{cleanup.detection_reduction_pct}% reduction</span>
                    </div>
                  </div>
                ))}
              </div>

              <div className="section-title">Hotspot Improvement</div>
              <div className="improvement-summary">
                {hotspotsData.filter(h => h.trend_direction === 'improving').slice(0, 4).map((hotspot, idx) => (
                  <div key={idx} className="improvement-item">
                    <div className="improvement-name">{hotspot.name}</div>
                    <div className="improvement-stats">
                      <span className="before">Before: {hotspot.monthly_detections?.[0] || 0}</span>
                      <span className="arrow">to</span>
                      <span className="after">Now: {hotspot.monthly_detections?.[11] || 0}</span>
                    </div>
                  </div>
                ))}
              </div>

              <div className="roi-box">
                <div className="roi-title">Operational Efficiency</div>
                <div className="roi-metrics">
                  <div className="roi-item">
                    <span className="roi-value">${annualData.operational_metrics?.cost_per_detection_usd?.toFixed(2)}</span>
                    <span className="roi-label">Cost per Detection</span>
                  </div>
                  <div className="roi-item">
                    <span className="roi-value">${annualData.operational_metrics?.manual_equivalent_cost_usd?.toFixed(2)}</span>
                    <span className="roi-label">Manual Equivalent</span>
                  </div>
                  <div className="roi-item highlight">
                    <span className="roi-value">
                      {((1 - annualData.operational_metrics?.cost_per_detection_usd / annualData.operational_metrics?.manual_equivalent_cost_usd) * 100).toFixed(0)}%
                    </span>
                    <span className="roi-label">Cost Savings</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AnnualData
