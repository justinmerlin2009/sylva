import React from 'react'
import { Link } from 'react-router-dom'
import DroneViewer3D from '../components/DroneViewer3D'

function Technology() {
  return (
    <div className="technology-page">
      {/* Navigation */}
      <header className="home-header">
        <Link to="/" className="home-logo">
          <img src="/logos/sylva-logo.svg" alt="Sylva" className="logo-icon-img" />
          <span className="logo-text">Sylva</span>
        </Link>
        <nav className="home-nav">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/technology" className="nav-link active">Technology</Link>
          <Link to="/simulation" className="nav-link nav-cta">Simulation</Link>
        </nav>
      </header>

      <main className="technology-main">
        {/* Hero Section with 3D Viewer */}
        <section className="tech-hero-section">
          <div className="tech-hero-content">
            <h1 className="tech-hero-title">Sylva-1 UAV Platform</h1>
            <p className="tech-hero-subtitle">
              Advanced fixed-wing surveillance system for environmental monitoring
            </p>
          </div>
          <div className="drone-viewer-container">
            <DroneViewer3D height="500px" autoRotate={true} />
            <p className="viewer-hint">Drag to rotate | Scroll to zoom</p>
          </div>
        </section>

        {/* Drone Specifications */}
        <section className="specs-section">
          <h2 className="section-title">Aircraft Specifications</h2>
          <div className="specs-grid">
            <div className="spec-card">
              <div className="spec-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/>
                </svg>
              </div>
              <h3>Airframe</h3>
              <ul className="spec-list">
                <li><span>Type:</span> Fixed-wing pusher configuration</li>
                <li><span>Wingspan:</span> 1.8m (71 inches)</li>
                <li><span>Length:</span> 1.2m (47 inches)</li>
                <li><span>Weight:</span> 3.2kg (7 lbs) with payload</li>
                <li><span>Material:</span> LW-PLA / ASA 3D printed</li>
              </ul>
            </div>

            <div className="spec-card">
              <div className="spec-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </div>
              <h3>Performance</h3>
              <ul className="spec-list">
                <li><span>Flight Time:</span> 90 minutes</li>
                <li><span>Range:</span> 50km operational radius</li>
                <li><span>Cruise Speed:</span> 15-20 m/s (33-44 mph)</li>
                <li><span>Max Altitude:</span> 400ft AGL (FAA limit)</li>
                <li><span>Survey Rate:</span> 100+ acres/hour</li>
              </ul>
            </div>

            <div className="spec-card">
              <div className="spec-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                </svg>
              </div>
              <h3>Propulsion</h3>
              <ul className="spec-list">
                <li><span>Motors:</span> Dual brushless (tractor config)</li>
                <li><span>Props:</span> 10x6 folding propellers</li>
                <li><span>Battery:</span> 6S 10,000mAh LiPo</li>
                <li><span>ESC:</span> 40A with BEC</li>
                <li><span>Tail:</span> V-tail configuration</li>
              </ul>
            </div>

            <div className="spec-card">
              <div className="spec-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm-5 14H4v-4h11v4zm0-5H4V9h11v4zm5 5h-4V9h4v9z"/>
                </svg>
              </div>
              <h3>Control Systems</h3>
              <ul className="spec-list">
                <li><span>FC:</span> Pixhawk 6X flight controller</li>
                <li><span>Radio:</span> ExpressLRS 915MHz (50km+)</li>
                <li><span>Video:</span> DJI O3 Air Unit</li>
                <li><span>GPS:</span> u-blox M10 with RTK option</li>
                <li><span>Telemetry:</span> MAVLink protocol</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Sensor Payload Section */}
        <section className="payload-section">
          <h2 className="section-title">Sensor Payload</h2>
          <p className="section-description">
            The Sylva-1 carries a gimbal-stabilized multi-sensor payload for comprehensive environmental monitoring.
            All sensors are synchronized for precise data correlation and real-time AI processing.
          </p>

          <div className="payload-grid">
            <div className="payload-card primary">
              <div className="payload-header">
                <h3>RGB Camera</h3>
                <span className="payload-badge">Primary</span>
              </div>
              <div className="payload-specs">
                <div className="payload-stat">
                  <span className="stat-value">61MP</span>
                  <span className="stat-label">Resolution</span>
                </div>
                <div className="payload-stat">
                  <span className="stat-value">1"</span>
                  <span className="stat-label">Sensor Size</span>
                </div>
                <div className="payload-stat">
                  <span className="stat-value">4K60</span>
                  <span className="stat-label">Video</span>
                </div>
              </div>
              <ul className="payload-features">
                <li>Sony IMX455 CMOS sensor</li>
                <li>24mm f/2.8 autofocus lens</li>
                <li>HDR and low-light capability</li>
                <li>Mechanical global shutter</li>
              </ul>
            </div>

            <div className="payload-card">
              <div className="payload-header">
                <h3>Hyperspectral Imager</h3>
                <span className="payload-badge">Multispectral</span>
              </div>
              <div className="payload-specs">
                <div className="payload-stat">
                  <span className="stat-value">8</span>
                  <span className="stat-label">Bands</span>
                </div>
                <div className="payload-stat">
                  <span className="stat-value">450-850</span>
                  <span className="stat-label">nm Range</span>
                </div>
                <div className="payload-stat">
                  <span className="stat-value">12MP</span>
                  <span className="stat-label">Per Band</span>
                </div>
              </div>
              <ul className="payload-features">
                <li>Material identification (plastic, metal, organic)</li>
                <li>Vegetation health analysis (NDVI)</li>
                <li>Water quality assessment</li>
                <li>Chemical contamination detection</li>
              </ul>
            </div>

            <div className="payload-card">
              <div className="payload-header">
                <h3>LiDAR Scanner</h3>
                <span className="payload-badge">3D Mapping</span>
              </div>
              <div className="payload-specs">
                <div className="payload-stat">
                  <span className="stat-value">200m</span>
                  <span className="stat-label">Range</span>
                </div>
                <div className="payload-stat">
                  <span className="stat-value">300k</span>
                  <span className="stat-label">Points/sec</span>
                </div>
                <div className="payload-stat">
                  <span className="stat-value">2cm</span>
                  <span className="stat-label">Accuracy</span>
                </div>
              </div>
              <ul className="payload-features">
                <li>Solid-state MEMS scanner</li>
                <li>Real-time point cloud generation</li>
                <li>Volume estimation for debris piles</li>
                <li>Terrain mapping in vegetation</li>
              </ul>
            </div>

            <div className="payload-card accent">
              <div className="payload-header">
                <h3>Edge AI Processor</h3>
                <span className="payload-badge nvidia">NVIDIA</span>
              </div>
              <div className="payload-specs">
                <div className="payload-stat">
                  <span className="stat-value">100</span>
                  <span className="stat-label">TOPS</span>
                </div>
                <div className="payload-stat">
                  <span className="stat-value">8GB</span>
                  <span className="stat-label">Memory</span>
                </div>
                <div className="payload-stat">
                  <span className="stat-value">25W</span>
                  <span className="stat-label">Power</span>
                </div>
              </div>
              <ul className="payload-features">
                <li>NVIDIA Jetson Orin NX module</li>
                <li>Real-time object detection (YOLOv8)</li>
                <li>Multi-sensor fusion algorithms</li>
                <li>On-device model inference</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Sensor Fusion Accuracy Section */}
        <section className="accuracy-section">
          <h2 className="section-title">Sensor Fusion Accuracy</h2>
          <p className="section-description">
            Combining sensors creates synergy. Sylva's hybrid camera achieves higher accuracy than any single sensor alone.
          </p>

          <div className="accuracy-chart-container">
            {/* Line Chart Visual */}
            <div className="accuracy-line-chart">
              <div className="chart-y-axis">
                <span>90%</span>
                <span>80%</span>
                <span>70%</span>
                <span>60%</span>
              </div>
              <div className="chart-area">
                {/* Grid lines */}
                <div className="chart-grid">
                  <div className="grid-line"></div>
                  <div className="grid-line"></div>
                  <div className="grid-line"></div>
                  <div className="grid-line"></div>
                </div>
                {/* Data points and connecting line */}
                <svg className="chart-svg" viewBox="0 0 400 200" preserveAspectRatio="none">
                  {/* Gradient fill under line */}
                  <defs>
                    <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stopColor="#22c55e" stopOpacity="0.3"/>
                      <stop offset="100%" stopColor="#22c55e" stopOpacity="0.05"/>
                    </linearGradient>
                  </defs>
                  {/* Area fill */}
                  <path
                    className="chart-area-fill"
                    d="M 50,140 L 150,120 L 250,60 L 350,20 L 350,200 L 50,200 Z"
                    fill="url(#chartGradient)"
                  />
                  {/* Line */}
                  <path
                    className="chart-line"
                    d="M 50,140 L 150,120 L 250,60 L 350,20"
                    fill="none"
                    stroke="#22c55e"
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  {/* Data points */}
                  <circle className="chart-point" cx="50" cy="140" r="8" fill="#f59e0b"/>
                  <circle className="chart-point" cx="150" cy="120" r="8" fill="#eab308"/>
                  <circle className="chart-point" cx="250" cy="60" r="8" fill="#84cc16"/>
                  <circle className="chart-point" cx="350" cy="20" r="8" fill="#22c55e"/>
                </svg>
                {/* Data labels */}
                <div className="chart-labels">
                  <div className="chart-label" style={{ left: '12.5%' }}>
                    <span className="label-value orange">74%</span>
                    <span className="label-sensor">RGB</span>
                  </div>
                  <div className="chart-label" style={{ left: '37.5%' }}>
                    <span className="label-value yellow">78%</span>
                    <span className="label-sensor">+ Hyperspectral</span>
                  </div>
                  <div className="chart-label" style={{ left: '62.5%' }}>
                    <span className="label-value lime">85%</span>
                    <span className="label-sensor">+ LiDAR</span>
                  </div>
                  <div className="chart-label highlight" style={{ left: '87.5%' }}>
                    <span className="label-value green">91%</span>
                    <span className="label-sensor">Full Fusion</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Legend */}
            <div className="accuracy-legend">
              <div className="legend-item">
                <span className="legend-dot orange"></span>
                <span>RGB Only (mAP@0.5)</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot yellow"></span>
                <span>+ Hyperspectral bands</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot lime"></span>
                <span>+ LiDAR depth</span>
              </div>
              <div className="legend-item highlight">
                <span className="legend-dot green"></span>
                <span>Sylva Hybrid Camera</span>
              </div>
            </div>

            {/* Source citation */}
            <div className="accuracy-sources">
              <p>
                Based on YOLOv8 waste detection benchmarks. RGB baseline from
                <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC11244501/" target="_blank" rel="noopener noreferrer"> MRS-YOLO (2024)</a>;
                sensor fusion improvements from
                <a href="https://www.tandfonline.com/doi/full/10.1080/01431161.2024.2429784" target="_blank" rel="noopener noreferrer"> multi-sensor fusion review (2024)</a>.
              </p>
            </div>
          </div>
        </section>

        {/* Gimbal System */}
        <section className="gimbal-section">
          <h2 className="section-title">3-Axis Gimbal Stabilization</h2>
          <div className="gimbal-content">
            <div className="gimbal-info">
              <p>
                The sensor payload is mounted on a precision 3-axis brushless gimbal for vibration-free imaging
                during flight. The gimbal provides 360° yaw rotation, ±45° pitch, and ±25° roll compensation.
              </p>
              <div className="gimbal-specs-grid">
                <div className="gimbal-spec">
                  <span className="gimbal-axis">Yaw</span>
                  <span className="gimbal-range">360° unlimited</span>
                </div>
                <div className="gimbal-spec">
                  <span className="gimbal-axis">Pitch</span>
                  <span className="gimbal-range">-90° to +45°</span>
                </div>
                <div className="gimbal-spec">
                  <span className="gimbal-axis">Roll</span>
                  <span className="gimbal-range">±25° stabilization</span>
                </div>
              </div>
              <ul className="gimbal-features">
                <li>Brushless direct-drive motors</li>
                <li>6-axis IMU for stabilization</li>
                <li>Quick-release dovetail mount</li>
                <li>Vibration dampening system</li>
              </ul>
            </div>
            <div className="gimbal-diagram">
              <img
                src="/images/sylva_payload_prototype.png"
                alt="Sylva Sensor Payload"
                className="payload-image"
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'block';
                }}
              />
              <div className="payload-fallback" style={{ display: 'none' }}>
                <div className="fallback-box">
                  <span>Sensor Payload</span>
                  <span className="fallback-sub">3-Axis Gimbal Mount</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* AI Detection Section */}
        <section className="ai-section">
          <h2 className="section-title">AI Detection Pipeline</h2>
          <div className="ai-pipeline">
            <div className="pipeline-step">
              <div className="step-number">1</div>
              <h4>Capture</h4>
              <p>61MP images + multispectral data captured at 2 frames/second during survey flight</p>
            </div>
            <div className="pipeline-arrow"></div>
            <div className="pipeline-step">
              <div className="step-number">2</div>
              <h4>Process</h4>
              <p>NVIDIA Jetson runs YOLOv8 detection model trained on 50,000+ pollution samples</p>
            </div>
            <div className="pipeline-arrow"></div>
            <div className="pipeline-step">
              <div className="step-number">3</div>
              <h4>Classify</h4>
              <p>14 categories identified: plastics, metals, tires, furniture, hazmat, and more</p>
            </div>
            <div className="pipeline-arrow"></div>
            <div className="pipeline-step">
              <div className="step-number">4</div>
              <h4>Prioritize</h4>
              <p>Risk scoring based on size, material type, and proximity to waterways</p>
            </div>
            <div className="pipeline-arrow"></div>
            <div className="pipeline-step">
              <div className="step-number">5</div>
              <h4>Transmit</h4>
              <p>Geo-tagged detections streamed to dashboard via cellular or satellite link</p>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="tech-cta-section">
          <h2>See Sylva in Action</h2>
          <p>Launch the interactive simulation to see real-time pollution detection across our survey sites.</p>
          <div className="cta-buttons">
            <Link to="/simulation" className="btn btn-primary">
              Launch Simulation
            </Link>
            <a href="https://sylva-api.onrender.com/docs" target="_blank" rel="noopener noreferrer" className="btn btn-secondary">
              API Documentation
            </a>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="home-footer">
        <p>&copy; 2025 Sylva. All rights reserved.</p>
        <p className="footer-sub">TamAir - Conrad Challenge 2026</p>
      </footer>
    </div>
  )
}

export default Technology
