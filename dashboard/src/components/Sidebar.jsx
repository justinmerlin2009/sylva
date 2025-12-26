import React from 'react'

function Sidebar({
  locations,
  selectedLocation,
  onLocationChange,
  categories,
  activeFilters,
  onToggleCategory,
  onTogglePriority,
  onClearFilters,
  stats,
  detectionCount,
  showHeatmap,
  onToggleHeatmap,
  showFlightPath,
  onToggleFlightPath,
  satelliteView,
  onToggleSatellite,
  showPopulationDensity,
  onTogglePopulationDensity,
  populationDensity,
  children,
}) {
  const priorities = ['critical', 'high', 'medium', 'low']

  // Calculate stats for display
  const totalWeight = stats?.total_weight_kg || stats?.total_estimated_weight_kg || 0
  const priorityCounts = stats?.by_priority || {}
  const categoryBreakdown = stats?.by_category || []

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Survey Locations</h2>
        <div className="location-selector">
          <button
            className={`location-btn ${selectedLocation === 'all' ? 'active' : ''}`}
            onClick={() => onLocationChange('all')}
          >
            <div className="location-name">All Locations</div>
            <div className="location-type">Combined View</div>
          </button>
        </div>
        <div className="location-selector">
          {locations.map(loc => (
            <button
              key={loc.id}
              className={`location-btn ${selectedLocation === loc.id ? 'active' : ''}`}
              onClick={() => onLocationChange(loc.id)}
            >
              <div className="location-name">
                {loc.id === 'stinson_beach' ? 'Stinson Beach' :
                 loc.id === 'route_66' ? 'Lake Erie' :
                 loc.id === 'nasa_clear_lake' ? 'NASA Space Center' : loc.name}
              </div>
              <div className="location-type">{loc.type}</div>
            </button>
          ))}
        </div>
      </div>

      <div className="sidebar-content">
        {/* Stats Grid */}
        <div className="stats-grid">
          <div className="stat-card primary">
            <div className="stat-value">{detectionCount}</div>
            <div className="stat-label">Detections</div>
          </div>
          <div className="stat-card warning">
            <div className="stat-value">{totalWeight.toFixed(1)}</div>
            <div className="stat-label">Est. Weight (kg)</div>
          </div>
          <div className="stat-card danger">
            <div className="stat-value">{priorityCounts.critical || 0}</div>
            <div className="stat-label">Critical</div>
          </div>
          <div className="stat-card success">
            <div className="stat-value">{priorityCounts.high || 0}</div>
            <div className="stat-label">High Priority</div>
          </div>
        </div>

        {/* Live Demo Section */}
        {children}

        {/* Map Toggles */}
        <div className="filter-section">
          <h3>Map Layers</h3>
          <div className="toggle-section">
            <span className="toggle-label">Satellite View</span>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={satelliteView}
                onChange={onToggleSatellite}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
          <div className="toggle-section">
            <span className="toggle-label">Heatmap Overlay</span>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={showHeatmap}
                onChange={onToggleHeatmap}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
          <div className="toggle-section">
            <span className="toggle-label">Flight Path</span>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={showFlightPath}
                onChange={onToggleFlightPath}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </div>

        {/* Priority Filter */}
        <div className="filter-section">
          <h3>Filter by Priority</h3>
          <div className="filter-group">
            {priorities.map(priority => (
              <button
                key={priority}
                className={`filter-chip ${activeFilters.priorities.includes(priority) ? 'active' : ''}`}
                onClick={() => onTogglePriority(priority)}
              >
                <span
                  className="color-dot"
                  style={{
                    backgroundColor:
                      priority === 'critical' ? '#ef4444' :
                      priority === 'high' ? '#f59e0b' :
                      priority === 'medium' ? '#22c55e' : '#64748b'
                  }}
                />
                {priority.charAt(0).toUpperCase() + priority.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Category Filter */}
        <div className="filter-section">
          <h3>Filter by Category</h3>
          <div className="filter-group">
            {categories.slice(0, 6).map(cat => (
              <button
                key={cat.id}
                className={`filter-chip ${activeFilters.categories.includes(cat.id) ? 'active' : ''}`}
                onClick={() => onToggleCategory(cat.id)}
              >
                <span
                  className="color-dot"
                  style={{ backgroundColor: cat.color }}
                />
                {cat.name}
              </button>
            ))}
          </div>
          {(activeFilters.categories.length > 0 || activeFilters.priorities.length > 0) && (
            <button
              className="filter-chip"
              onClick={onClearFilters}
              style={{ marginTop: '8px' }}
            >
              Clear Filters
            </button>
          )}
        </div>

        {/* Category Breakdown */}
        <div className="category-list">
          <h3 style={{ marginBottom: '12px', fontSize: '13px', fontWeight: '600' }}>
            Detection Breakdown
          </h3>
          {categoryBreakdown.slice(0, 8).map(cat => (
            <div key={cat.category} className="category-item">
              <div className="category-info">
                <span
                  className="category-color"
                  style={{ backgroundColor: cat.color }}
                />
                <span className="category-name">{cat.name}</span>
              </div>
              <span className="category-count">
                {cat.count} ({cat.percentage}%)
              </span>
            </div>
          ))}
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
