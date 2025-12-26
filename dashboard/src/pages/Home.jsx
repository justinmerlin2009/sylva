import React from 'react'
import { Link } from 'react-router-dom'

function Home() {
  return (
    <div className="home-page">
      {/* Navigation */}
      <header className="home-header">
        <div className="home-logo">
          <span className="logo-icon">S</span>
          <span className="logo-text">Sylva</span>
        </div>
        <nav className="home-nav">
          <a href="#why" className="nav-link">Why It Matters</a>
          <a href="#how" className="nav-link">How It Works</a>
          <a href="#team" className="nav-link">Our Team</a>
          <a href="#collab" className="nav-link">Collaborations</a>
          <Link to="/simulation" className="nav-link nav-cta">Simulation</Link>
        </nav>
      </header>

      <main className="home-main">
        {/* Hero Section */}
        <section className="hero-section">
          <h1 className="hero-title">Sylva</h1>
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

        {/* Why It Matters Section */}
        <section id="why" className="content-section">
          <h2 className="section-title">Why It Matters</h2>
          <p className="section-description">
            [Content placeholder: Describe the environmental pollution problem, its impact on ecosystems, communities, and why current detection methods are inadequate. Explain the urgency of addressing this issue.]
          </p>
        </section>

        {/* How It Works Section */}
        <section id="how" className="content-section how-section">
          <h2 className="section-title">How Sylva Works</h2>
          <div className="features-section">
            <div className="feature-card">
              <div className="feature-icon">1</div>
              <h3>Drone Surveillance</h3>
              <p>[Content placeholder: Explain the drone technology, flight patterns, multi-spectral cameras, and data collection capabilities.]</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">2</div>
              <h3>AI Detection</h3>
              <p>[Content placeholder: Describe the machine learning models, object detection algorithms, and classification accuracy.]</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">3</div>
              <h3>Data Analytics</h3>
              <p>[Content placeholder: Explain the heatmapping, hotspot identification, and prioritization algorithms.]</p>
            </div>
          </div>
        </section>

        {/* Technology/Prototype Section */}
        <section className="content-section tech-section">
          <h2 className="section-title">Our Technology</h2>
          <div className="tech-grid">
            <div className="tech-content">
              <h3>The Sylva Platform</h3>
              <p>[Content placeholder: Describe the hardware components - drone specifications, camera systems, sensors. Include technical details about the platform capabilities.]</p>
              <ul className="tech-list">
                <li>[Component 1]</li>
                <li>[Component 2]</li>
                <li>[Component 3]</li>
                <li>[Component 4]</li>
              </ul>
            </div>
            <div className="tech-image">
              <div className="placeholder-image">[Drone/Platform Image]</div>
            </div>
          </div>
        </section>

        {/* API Section */}
        <section className="content-section api-section">
          <h2 className="section-title">Sylva API</h2>
          <p className="section-description">
            [Content placeholder: Describe the data sharing capabilities, API features, integration options, and how organizations can access pollution data.]
          </p>
          <div className="api-features">
            <div className="api-feature">
              <h4>Real-time Data</h4>
              <p>[Placeholder: Live pollution detection feeds]</p>
            </div>
            <div className="api-feature">
              <h4>Historical Analysis</h4>
              <p>[Placeholder: Access to historical data and trends]</p>
            </div>
            <div className="api-feature">
              <h4>Integration Ready</h4>
              <p>[Placeholder: Easy integration with existing systems]</p>
            </div>
          </div>
          <a href="https://sylva-api.onrender.com/docs" target="_blank" rel="noopener noreferrer" className="btn btn-primary">
            View API Documentation
          </a>
        </section>

        {/* Team Section */}
        <section id="team" className="content-section team-section">
          <h2 className="section-title">Our Team</h2>
          <div className="team-grid">
            <div className="team-card">
              <div className="team-avatar">[Photo]</div>
              <h3>[Team Member 1]</h3>
              <p className="team-role">[Role/Title]</p>
              <p className="team-bio">[Short bio placeholder]</p>
            </div>
            <div className="team-card">
              <div className="team-avatar">[Photo]</div>
              <h3>[Team Member 2]</h3>
              <p className="team-role">[Role/Title]</p>
              <p className="team-bio">[Short bio placeholder]</p>
            </div>
            <div className="team-card">
              <div className="team-avatar">[Photo]</div>
              <h3>[Team Member 3]</h3>
              <p className="team-role">[Role/Title]</p>
              <p className="team-bio">[Short bio placeholder]</p>
            </div>
          </div>
        </section>

        {/* Future Plans Section */}
        <section className="content-section future-section">
          <h2 className="section-title">Future Plans</h2>
          <div className="future-grid">
            <div className="future-item">
              <span className="future-number">01</span>
              <h4>[Future Goal 1]</h4>
              <p>[Description placeholder]</p>
            </div>
            <div className="future-item">
              <span className="future-number">02</span>
              <h4>[Future Goal 2]</h4>
              <p>[Description placeholder]</p>
            </div>
            <div className="future-item">
              <span className="future-number">03</span>
              <h4>[Future Goal 3]</h4>
              <p>[Description placeholder]</p>
            </div>
            <div className="future-item">
              <span className="future-number">04</span>
              <h4>[Future Goal 4]</h4>
              <p>[Description placeholder]</p>
            </div>
          </div>
        </section>

        {/* Collaborations Section */}
        <section id="collab" className="content-section collab-section">
          <h2 className="section-title">Collaborations</h2>
          <div className="collab-grid">
            <div className="collab-card">
              <div className="collab-logo">[Logo]</div>
              <h3>[Partner/Collaborator Name]</h3>
              <p className="collab-role">[Organization/Role]</p>
              <p className="collab-desc">[Description of collaboration]</p>
            </div>
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

export default Home
