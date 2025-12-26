import React from 'react'
import { Link } from 'react-router-dom'

function Home() {
  return (
    <div className="home-page">
      <header className="home-header">
        <div className="home-logo">
          <span className="logo-icon">S</span>
          <span className="logo-text">Sylva</span>
        </div>
        <nav className="home-nav">
          <Link to="/simulation" className="nav-link">Simulation</Link>
          <a href="https://sylva-api.onrender.com/docs" target="_blank" rel="noopener noreferrer" className="nav-link">API</a>
        </nav>
      </header>

      <main className="home-main">
        <section className="hero-section">
          <h1 className="hero-title">
            Sylva
          </h1>
          <p className="hero-tagline">
            Turning Aerial Pollution Data Into Action for a Cleaner Earth
          </p>
          <div className="hero-actions">
            <Link to="/simulation" className="btn btn-primary">
              Launch Simulation
            </Link>
            <a href="https://sylva-api.onrender.com/docs" target="_blank" rel="noopener noreferrer" className="btn btn-secondary">
              Explore API
            </a>
          </div>
        </section>

        <section className="features-section">
          <div className="feature-card">
            <div className="feature-icon">drone</div>
            <h3>Drone Surveillance</h3>
            <p>Advanced aerial monitoring with multi-spectral imaging for comprehensive environmental data collection.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">ai</div>
            <h3>AI Detection</h3>
            <p>Machine learning algorithms identify and classify pollution sources with high accuracy in real-time.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">map</div>
            <h3>Mapping & Analytics</h3>
            <p>Interactive visualization of pollution hotspots with actionable insights for cleanup prioritization.</p>
          </div>
        </section>
      </main>

      <footer className="home-footer">
        <p>TamAir - Conrad Challenge 2026</p>
      </footer>
    </div>
  )
}

export default Home
