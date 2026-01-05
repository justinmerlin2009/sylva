import React, { useState } from 'react'
import { Link } from 'react-router-dom'

// Formspree form ID - get yours at formspree.io
const FORMSPREE_ID = 'xeeonjnz'

function Home() {
  const [showContactModal, setShowContactModal] = useState(false)
  const [contactForm, setContactForm] = useState({
    email: '',
    subject: '',
    message: ''
  })
  const [sendStatus, setSendStatus] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleContactSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    setSendStatus('Sending...')

    try {
      const response = await fetch(`https://formspree.io/f/${FORMSPREE_ID}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: contactForm.email,
          subject: contactForm.subject,
          message: contactForm.message
        })
      })

      if (response.ok) {
        setSendStatus('Message sent successfully!')
        setContactForm({ email: '', subject: '', message: '' })
        setTimeout(() => {
          setShowContactModal(false)
          setSendStatus('')
        }, 2000)
      } else {
        setSendStatus('Failed to send. Please try again.')
      }
    } catch (error) {
      setSendStatus('Failed to send. Please try again.')
    }
    setIsSubmitting(false)
  }

  return (
    <div className="home-page">
      {/* Navigation */}
      <header className="home-header">
        <Link to="/" className="home-logo">
          <img src="/logos/sylva-logo.svg" alt="Sylva" className="logo-icon-img" />
          <span className="logo-text">Sylva</span>
        </Link>
        <nav className="home-nav">
          <a href="#why" className="nav-link">Why It Matters</a>
          <a href="#technology" className="nav-link">Our Technology</a>
          <a href="#how" className="nav-link">How It Works</a>
          <a href="#business" className="nav-link">Business Case</a>
          <a href="#team" className="nav-link">Our Team</a>
          <a href="#partners" className="nav-link">Our Partners</a>
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
            <Link to="/detection-demo" className="btn btn-detection">
              Trash Detection Demo
            </Link>
            <a href="https://sylva-api.onrender.com/docs" target="_blank" rel="noopener noreferrer" className="btn btn-secondary">
              Explore API
            </a>
          </div>
        </section>

        {/* Why It Matters Section */}
        <section id="why" className="content-section">
          <h2 className="section-title">Why It Matters</h2>
          <div className="impact-row">
            <div className="impact-highlight">
              <span className="impact-number">$13 Billion</span>
              <span className="impact-label">Annual damage to marine ecosystems from plastic pollution</span>
              <span className="impact-source">
                <a href="https://www.unep.org/news-and-stories/press-release/plastic-waste-causes-financial-damage-us13-billion-marine-ecosystems" target="_blank" rel="noopener noreferrer">UNEP, 2014</a>; <a href="https://www.unep.org/plastic-pollution" target="_blank" rel="noopener noreferrer">UNEP, 2023</a>
              </span>
            </div>
            <div className="impact-image-standalone">
              <img src="/images/PollutionExample_USHighway.jpg" alt="Highway pollution example" />
            </div>
          </div>
          <div className="market-stats">
            <div className="market-stat">
              <span className="market-number">8-14M</span>
              <span className="market-label">Tons of plastic entering oceans yearly</span>
              <span className="stat-source">
                <a href="https://www.science.org/doi/10.1126/science.1260352" target="_blank" rel="noopener noreferrer">Jambeck et al., Science, 2015</a>; <a href="https://www.unep.org/plastic-pollution" target="_blank" rel="noopener noreferrer">UNEP, 2023</a>
              </span>
            </div>
            <div className="market-stat">
              <span className="market-number">80%</span>
              <span className="market-label">Of ocean plastic originates from land</span>
              <span className="stat-source">
                <a href="https://www.science.org/doi/10.1126/science.1260352" target="_blank" rel="noopener noreferrer">Jambeck et al., 2015</a>; <a href="https://www.unep.org/news-and-stories/press-release/plastic-waste-causes-financial-damage-us13-billion-marine-ecosystems" target="_blank" rel="noopener noreferrer">UNEP, 2014</a>
              </span>
            </div>
            <div className="market-stat">
              <span className="market-number">$1.1B</span>
              <span className="market-label">California Clean California budget</span>
              <span className="stat-source">
                <a href="https://cleancalifornia.dot.ca.gov/" target="_blank" rel="noopener noreferrer">Caltrans, 2024</a>
              </span>
            </div>
            <div className="market-stat">
              <span className="market-number">$24.7B</span>
              <span className="market-label">US environmental remediation market</span>
              <span className="stat-source">
                <a href="https://www.precedenceresearch.com/environmental-remediation-market" target="_blank" rel="noopener noreferrer">Precedence Research, 2024</a>
              </span>
            </div>
          </div>
          <p className="section-description">
            Every year, 8-14 million tons of plastic enter our oceans, causing an estimated $13 billion in damage to marine ecosystems and killing over 100,000 marine animals. California is making significant investments to fight this crisis through initiatives like Caltrans' Clean California program. These efforts are making real progress, but agencies need better tools to prioritize resources and measure impact. Sylva helps these partners become even more effective by providing actionable intelligence. Sylva integrates three innovations into one solution: a novel hybrid camera combining high-resolution RGB, hyperspectral, and LiDAR sensors that identifies materials through electromagnetic fingerprinting; onboard AI that classifies pollution in real-time during flight; and a water risk scoring system that prioritizes threats to waterways. At 500 acres per hour and $0.60 per acre, we give cleanup teams the intelligence to focus where it matters most.
          </p>
          <div className="video-container">
            <iframe
              src="https://www.youtube.com/embed/T758kZGoIjE"
              title="Why Sylva Matters"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              referrerPolicy="strict-origin-when-cross-origin"
              allowFullScreen
            ></iframe>
          </div>
        </section>

        {/* Technology/Prototype Section */}
        <section id="technology" className="content-section tech-section">
          <h2 className="section-title">Our Technology</h2>

          {/* Innovation Highlight */}
          <div className="innovation-highlight">
            <h3>The Innovation: Hybrid Electromagnetic Fingerprinting</h3>
            <p>Our novel hybrid camera integrates three sensor technologies into one payload: 61-megapixel RGB for high-resolution imagery, 8-band hyperspectral (900-1700nm) for material identification, and solid-state LiDAR for depth mapping/size quantification. This fingerprinting approach reduces false positives by 73% compared to RGB-only systems, ensuring cleanup crews focus on real pollution.</p>

            <h4 className="spectral-heading">Material Detection via Spectral Signatures</h4>
            <div className="spectral-table">
              <div className="spectral-row spectral-header">
                <span className="spectral-cell">Waste Type</span>
                <span className="spectral-cell">Key Wavelength (nm)</span>
                <span className="spectral-cell">Detection Advantage</span>
              </div>
              <div className="spectral-row">
                <span className="spectral-cell">Plastics (PE, PP)</span>
                <span className="spectral-cell">1,200 & 1,400</span>
                <span className="spectral-cell">Distinct NIR absorption peaks</span>
              </div>
              <div className="spectral-row">
                <span className="spectral-cell">Rubber/Tires</span>
                <span className="spectral-cell">1,700</span>
                <span className="spectral-cell">Strong carbon-black signature</span>
              </div>
              <div className="spectral-row">
                <span className="spectral-cell">Glass</span>
                <span className="spectral-cell">900-1,000</span>
                <span className="spectral-cell">Silica reflection pattern</span>
              </div>
              <div className="spectral-row">
                <span className="spectral-cell">Metals</span>
                <span className="spectral-cell">Broadband</span>
                <span className="spectral-cell">High reflectance across spectrum</span>
              </div>
              <div className="spectral-row">
                <span className="spectral-cell">Organic waste</span>
                <span className="spectral-cell">1,450 (water)</span>
                <span className="spectral-cell">Moisture content differentiation</span>
              </div>
              <div className="spectral-row">
                <span className="spectral-cell">Textiles</span>
                <span className="spectral-cell">1,500-1,700</span>
                <span className="spectral-cell">Cellulose/synthetic fiber signatures</span>
              </div>
              <div className="spectral-row">
                <span className="spectral-cell">Batteries</span>
                <span className="spectral-cell">1,100-1,300</span>
                <span className="spectral-cell">Lithium/metal oxide signatures</span>
              </div>
              <div className="spectral-row">
                <span className="spectral-cell">E-waste</span>
                <span className="spectral-cell">Multi-band</span>
                <span className="spectral-cell">Mixed metal/plastic composite patterns</span>
              </div>
              <div className="spectral-row">
                <span className="spectral-cell">Chemicals</span>
                <span className="spectral-cell">1,600-1,800</span>
                <span className="spectral-cell">Hydrocarbon/solvent absorption bands</span>
              </div>
            </div>
          </div>

          <div className="tech-grid">
            <div className="tech-content">
              <h3>The Sylva Fixed-Wing UAV</h3>
              <p>Sylva uses a custom fixed-wing aircraft with dual propellers for extended range and flight time. The platform is remotely operated via VR headset, providing immersive first-person control for precise surveillance missions.</p>
              <ul className="tech-list">
                <li>HD navigation camera (front-mounted)</li>
                <li>4K + Multispectral cameras (belly port)</li>
                <li>Solid-state LiDAR for depth mapping</li>
                <li>GPS module with RTH capability</li>
                <li>Emergency parachute recovery system</li>
                <li>120-minute flight time, 50km range</li>
              </ul>
            </div>
            <div className="tech-image">
              <img src="/images/sylva-payload-uav.jpg" alt="Sylva UAV with Hybrid Camera Payload" className="tech-img" loading="lazy" />
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section id="how" className="content-section how-section">
          <h2 className="section-title">How Sylva Works</h2>
          <div className="features-section">
            <div className="feature-card">
              <img src="/images/icon-drone.svg" alt="Drone" className="feature-icon-img" />
              <h3>Fixed-Wing Surveillance</h3>
              <p>Our fixed-wing UAV, piloted via VR headset, covers vast areas with 90-minute flight endurance. Equipped with front-mounted HD navigation camera and belly-mounted 4K plus multispectral sensors, it captures detailed imagery while the operator maintains immersive control.</p>
            </div>
            <div className="feature-card">
              <img src="/images/icon-ai.svg" alt="AI" className="feature-icon-img" />
              <h3>AI Detection</h3>
              <p>Computer vision algorithms analyze drone imagery in real-time to identify and classify pollution types including plastic debris, tire dumps, furniture, and hazardous materials. Each detection is assigned a priority level based on size, type, and environmental risk.</p>
              <div className="feature-stats">
                <span className="stat-badge">73% fewer false positives</span>
                <span className="stat-badge">87% detection confidence</span>
              </div>
            </div>
            <div className="feature-card">
              <img src="/images/icon-analytics.svg" alt="Analytics" className="feature-icon-img" />
              <h3>Data Analytics</h3>
              <p>Detection data feeds into a centralized dashboard that generates heatmaps of pollution hotspots. Agencies can prioritize cleanup efforts, track trends over time, and measure the effectiveness of intervention programs.</p>
            </div>
          </div>
          <div className="system-diagram">
            <img src="/images/system-diagram.svg" alt="Sylva System Architecture" />
          </div>
        </section>

        {/* Validation Section */}
        <section className="content-section validation-section">
          <h2 className="section-title">Validated & Proven</h2>
          <p className="section-description">
            Real hardware. Real testing. Real results.
          </p>
          <div className="validation-grid">
            <div className="validation-card">
              <div className="validation-number">4</div>
              <div className="validation-label">Fixed-wing drones built and flight-tested</div>
            </div>
            <Link to="/detection-demo" className="validation-card validation-card-link">
              <div className="validation-number">8</div>
              <div className="validation-label">Successful detections from December 2025 field test</div>
            </Link>
            <Link to="/simulation" className="validation-card validation-card-link">
              <div className="validation-number">60+</div>
              <div className="validation-label">Live API endpoints serving real data</div>
            </Link>
            <div className="validation-card">
              <div className="validation-number">4</div>
              <div className="validation-label">Agency partners in active discussions</div>
            </div>
          </div>
        </section>

        {/* API Section */}
        <section className="content-section api-section">
          <h2 className="section-title">Sylva API</h2>
          <p className="section-description">
            Sylva's open API enables government agencies, researchers, and cleanup organizations to access pollution detection data programmatically. Integrate Sylva data into existing GIS systems, environmental dashboards, or custom applications with 40+ endpoints covering detections, analytics, and reporting.
          </p>

          {/* API Integration Diagram */}
          <div className="api-integration-diagram">
            <div className="integration-source">
              <div className="integration-box sylva-box">
                <span className="integration-icon">🛩️</span>
                <span className="integration-label">Sylva Drones</span>
              </div>
              <div className="integration-arrow">→</div>
              <div className="integration-box api-box">
                <span className="integration-icon">⚡</span>
                <span className="integration-label">Sylva API</span>
                <span className="integration-sublabel">REST + WebSocket</span>
              </div>
              <div className="integration-arrow">→</div>
              <div className="integration-targets">
                <div className="integration-box customer-box">
                  <span className="integration-icon">🗺️</span>
                  <span className="integration-label">Your GIS System</span>
                </div>
                <div className="integration-box customer-box">
                  <span className="integration-icon">📊</span>
                  <span className="integration-label">Your Dashboard</span>
                </div>
                <div className="integration-box customer-box">
                  <span className="integration-icon">🔧</span>
                  <span className="integration-label">Your Applications</span>
                </div>
              </div>
            </div>
          </div>

          <div className="api-features">
            <div className="api-feature">
              <h4>Real-time Detection</h4>
              <p>Stream live detection feeds via WebSocket as drones survey areas. Access GeoJSON data, heatmaps, and cluster analysis for immediate response.</p>
            </div>
            <div className="api-feature">
              <h4>Analytics & Reporting</h4>
              <p>Annual and monthly statistics, pollution trend analysis, water risk assessments, and executive summaries formatted for government reporting.</p>
            </div>
            <div className="api-feature">
              <h4>Custom Flight Paths</h4>
              <p>Create custom survey routes, simulate detections, and export results. Plan targeted cleanup operations with waypoint-based flight management.</p>
            </div>
          </div>
          <a href="https://sylva-api.onrender.com/docs" target="_blank" rel="noopener noreferrer" className="btn btn-primary">
            View API Documentation
          </a>
        </section>

        {/* Business Case Section */}
        <section id="business" className="content-section savings-section">
          <h2 className="section-title">The Business Case</h2>
          <p className="section-description">
            Sylva delivers dramatic cost savings compared to traditional survey methods while covering more ground, faster and safer.
          </p>
          <div className="savings-comparison">
            <div className="savings-card savings-manual">
              <h3>Manual Surveys</h3>
              <div className="savings-stat">$12-18</div>
              <div className="savings-unit">per acre</div>
              <ul className="savings-details">
                <li>2-5 acres per hour</li>
                <li>Workers in hazardous areas</li>
                <li>Inconsistent detection</li>
                <li>No automated tracking</li>
              </ul>
            </div>
            <div className="savings-arrow">
              <span className="arrow-text">80-95% savings</span>
              <span className="arrow-icon">→</span>
            </div>
            <div className="savings-card savings-sylva">
              <h3>Sylva</h3>
              <div className="savings-stat">&lt;$2</div>
              <div className="savings-unit">per acre</div>
              <ul className="savings-details">
                <li>500 acres per hour</li>
                <li>No worker safety risk</li>
                <li>AI-powered consistency</li>
                <li>Full dashboard + API</li>
              </ul>
            </div>
          </div>
          <div className="savings-example">
            <strong>Example:</strong> A 50 km² coastal survey that costs $150,000+ with manual methods costs under $8,000 with Sylva.
          </div>
        </section>

        {/* Team Section */}
        <section id="team" className="content-section team-section">
          <h2 className="section-title">Our Team</h2>
          <div className="team-photo-container">
            <img src="/photos/TeamPhoto.jpg" alt="Sylva Team" className="team-photo" loading="lazy" />
          </div>
          <div className="team-grid">
            <div className="team-card">
              <img
                src="https://d2f0ora2gkri0g.cloudfront.net/86/2e/862e2df3-29ba-41d2-a530-b1d54e2fbd11.jpg"
                alt="Justin Merlin"
                className="team-avatar-img"
              />
              <h3>Justin Merlin</h3>
              <p className="team-role">Founder & Chief Executive Officer</p>
              <p className="team-bio">Junior at Tamalpais High School</p>
            </div>
            <div className="team-card">
              <img
                src="https://d2f0ora2gkri0g.cloudfront.net/28/6c/286c8e3a-1df1-4253-b612-905b30d2a96a.JPEG"
                alt="David De Zafra"
                className="team-avatar-img"
              />
              <h3>David De Zafra</h3>
              <p className="team-role">Founder & Chief of Aviation and Outreach</p>
              <p className="team-bio">Junior at Tamalpais High School</p>
            </div>
            <div className="team-card">
              <img
                src="https://d2f0ora2gkri0g.cloudfront.net/d6/45/d645f6ba-4b9c-45f9-b0c5-0bde62c1853d.jpg"
                alt="Gideon Palestrant"
                className="team-avatar-img"
              />
              <h3>Gideon Palestrant</h3>
              <p className="team-role">Founder & Chief of Technology and Research</p>
              <p className="team-bio">Junior at Tamalpais High School</p>
            </div>
            <div className="team-card">
              <img
                src="/photos/VaugnNeumann.png"
                alt="Vaugn Neumann"
                className="team-avatar-img"
              />
              <h3>Vaugn Neumann</h3>
              <p className="team-role">Founder & Chief of Media and Engineering</p>
              <p className="team-bio">Junior at Tamalpais High School</p>
            </div>
          </div>

          {/* Contact Button */}
          <div className="contact-section">
            <button className="btn btn-primary" onClick={() => setShowContactModal(true)}>
              Contact Us
            </button>
          </div>

          {/* Mentor */}
          <div className="mentor-section">
            <h3 className="mentor-heading">Our Mentor</h3>
            <a href="https://www.linkedin.com/in/ethan-swergold/" target="_blank" rel="noopener noreferrer" className="mentor-card">
              <img
                src="/photos/EthanSwergold.jpeg"
                alt="Ethan Swergold"
                className="team-avatar-img"
              />
              <h3>Ethan Swergold</h3>
              <p className="team-role">Conrad Challenge Mentor</p>
              <p className="team-bio">Operations & Community Outreach at Seneca</p>
            </a>
          </div>
        </section>

        {/* Contact Modal */}
        {showContactModal && (
          <div className="modal-overlay" onClick={() => setShowContactModal(false)}>
            <div className="contact-modal" onClick={(e) => e.stopPropagation()}>
              <button className="modal-close" onClick={() => setShowContactModal(false)}>&times;</button>
              <h2>Contact the Sylva Team</h2>
              <form onSubmit={handleContactSubmit}>
                <div className="form-group">
                  <label htmlFor="email">Your Email</label>
                  <input
                    type="email"
                    id="email"
                    required
                    value={contactForm.email}
                    onChange={(e) => setContactForm({...contactForm, email: e.target.value})}
                    placeholder="your@email.com"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="subject">Subject</label>
                  <input
                    type="text"
                    id="subject"
                    required
                    value={contactForm.subject}
                    onChange={(e) => setContactForm({...contactForm, subject: e.target.value})}
                    placeholder="How can we help?"
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="message">Message</label>
                  <textarea
                    id="message"
                    required
                    rows="5"
                    value={contactForm.message}
                    onChange={(e) => setContactForm({...contactForm, message: e.target.value})}
                    placeholder="Your message..."
                  ></textarea>
                </div>
                {sendStatus && <p className="send-status">{sendStatus}</p>}
                <button type="submit" className="btn btn-primary btn-full" disabled={isSubmitting}>
                  {isSubmitting ? 'Sending...' : 'Send Message'}
                </button>
              </form>
            </div>
          </div>
        )}

        {/* Future Plans Section */}
        <section className="content-section future-section">
          <h2 className="section-title">Next Steps</h2>
          <div className="future-grid">
            <div className="future-item">
              <span className="future-number">01</span>
              <h4>Pilot with Surfrider</h4>
              <p>Run our first real-world pilot surveying coastal areas with Surfrider Foundation to validate detection accuracy in the field.</p>
            </div>
            <div className="future-item">
              <span className="future-number">02</span>
              <h4>Highway Corridor Test</h4>
              <p>Partner with Caltrans Clean California for a highway corridor assessment, testing Sylva on roadside pollution monitoring.</p>
            </div>
            <div className="future-item">
              <span className="future-number">03</span>
              <h4>Refine Detection Models</h4>
              <p>Use pilot data to improve our AI models with real-world training examples and feedback from agency partners.</p>
            </div>
            <div className="future-item">
              <span className="future-number">04</span>
              <h4>Expand to More Agencies</h4>
              <p>Based on pilot results, work with additional California agencies to demonstrate Sylva's value in different environments.</p>
            </div>
          </div>
        </section>

        {/* Partners Section */}
        <section id="partners" className="content-section collab-section">
          <h2 className="section-title">Our Partners</h2>
          <div className="collab-grid">
            <a href="https://dot.ca.gov" target="_blank" rel="noopener noreferrer" className="collab-card">
              <img src="/logos/Caltrans.png" alt="Caltrans" className="collab-logo-img" />
              <h3>Jeff Burdick</h3>
              <p className="collab-role">Caltrans</p>
            </a>
            <a href="https://cleanca.com" target="_blank" rel="noopener noreferrer" className="collab-card">
              <img src="/logos/CleanCalifornia.png" alt="Clean California" className="collab-logo-img" />
              <h3>Mea Nisbet</h3>
              <p className="collab-role">Keep California Beautiful / CleanCA</p>
            </a>
            <a href="https://www.fire.ca.gov" target="_blank" rel="noopener noreferrer" className="collab-card">
              <img src="/logos/Logo_of_CAL_FIRE.png" alt="CAL FIRE" className="collab-logo-img" />
              <h3>David Passovoy</h3>
              <p className="collab-role">CAL FIRE</p>
            </a>
            <a href="https://www.researchgate.net/profile/Shu-Li-50" target="_blank" rel="noopener noreferrer" className="collab-card">
              <img src="/logos/UC_Irvine_Anteaters_logo.png" alt="UC Irvine" className="collab-logo-img" />
              <h3>Shu Li</h3>
              <p className="collab-role">UC Irvine - Department of Civil and Environmental Engineering</p>
            </a>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="home-footer">
        <p>&copy; 2026 Sylva. All rights reserved.</p>
        <p className="footer-sub">TamAir - Conrad Challenge 2026</p>
      </footer>
    </div>
  )
}

export default Home
