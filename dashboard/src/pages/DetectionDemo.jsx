import React, { useState } from 'react'
import { Link } from 'react-router-dom'

function DetectionDemo() {
  const [activeTab, setActiveTab] = useState('demo')

  return (
    <div className="detection-demo-page">
      <header className="demo-header">
        <Link to="/" className="demo-back-link">← Back to Home</Link>
        <div className="demo-title-section">
          <h1>Sylva Detection Pipeline</h1>
          <p className="demo-subtitle">
            TACO + SAM 2 Combined Trash Detection & Segmentation
          </p>
        </div>
        <div className="demo-badge">
          <span className="badge-text">Field Test Results</span>
        </div>
      </header>

      {/* Tab Navigation */}
      <div className="demo-tabs">
        <button
          className={`demo-tab ${activeTab === 'demo' ? 'active' : ''}`}
          onClick={() => setActiveTab('demo')}
        >
          Detection Demo
        </button>
        <button
          className={`demo-tab ${activeTab === 'methodology' ? 'active' : ''}`}
          onClick={() => setActiveTab('methodology')}
        >
          Methodology
        </button>
      </div>

      {/* Demo Tab */}
      {activeTab === 'demo' && (
        <div className="demo-content">
          {/* Video Section */}
          <section className="demo-video-section">
            <h2>Detection Demo Video</h2>
            <p className="section-desc">
              90 frames from 5 DJI drone videos processed through our TACO + SAM 2 pipeline.
              Each colored overlay represents a detected and segmented trash item.
            </p>
            <div className="video-container">
              <video
                controls
                width="100%"
                poster="/detection-demo/tiled_DJI_20251227131705_0159_D.JPG"
              >
                <source src="/detection-demo/videos/Sylva_Detection_Demo_720p.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
            <div className="video-legend">
              <div className="legend-item">
                <span className="legend-color" style={{backgroundColor: '#27ae60'}}></span>
                <span>Low Priority (caps, wrappers)</span>
              </div>
              <div className="legend-item">
                <span className="legend-color" style={{backgroundColor: '#f1c40f'}}></span>
                <span>Medium Priority (bottles, film)</span>
              </div>
              <div className="legend-item">
                <span className="legend-color" style={{backgroundColor: '#e67e22'}}></span>
                <span>High Priority (hazardous)</span>
              </div>
            </div>
          </section>

          {/* Stats Section */}
          <section className="demo-stats-section">
            <h2>Detection Results</h2>
            <div className="stats-grid-large">
              <div className="stat-card-large">
                <div className="stat-icon">🎬</div>
                <div className="stat-value-large">90</div>
                <div className="stat-label-large">Frames Processed</div>
              </div>
              <div className="stat-card-large">
                <div className="stat-icon">🔍</div>
                <div className="stat-value-large">52</div>
                <div className="stat-label-large">Frames with Detections</div>
              </div>
              <div className="stat-card-large">
                <div className="stat-icon">🗑️</div>
                <div className="stat-value-large">103</div>
                <div className="stat-label-large">Total Trash Items</div>
              </div>
              <div className="stat-card-large">
                <div className="stat-icon">📐</div>
                <div className="stat-value-large">601K</div>
                <div className="stat-label-large">Segmented Pixels</div>
              </div>
            </div>

            {/* Category Breakdown */}
            <div className="breakdown-grid">
              <div className="breakdown-card">
                <h3>By Trash Type</h3>
                <div className="breakdown-list">
                  <div className="breakdown-item">
                    <span className="breakdown-icon">🎞️</span>
                    <span className="breakdown-name">Plastic film</span>
                    <span className="breakdown-count">27</span>
                  </div>
                  <div className="breakdown-item">
                    <span className="breakdown-icon">📦</span>
                    <span className="breakdown-name">Styrofoam piece</span>
                    <span className="breakdown-count">23</span>
                  </div>
                  <div className="breakdown-item">
                    <span className="breakdown-icon">🔵</span>
                    <span className="breakdown-name">Plastic bottle cap</span>
                    <span className="breakdown-count">16</span>
                  </div>
                  <div className="breakdown-item">
                    <span className="breakdown-icon">⚪</span>
                    <span className="breakdown-name">Metal bottle cap</span>
                    <span className="breakdown-count">13</span>
                  </div>
                  <div className="breakdown-item">
                    <span className="breakdown-icon">🛍️</span>
                    <span className="breakdown-name">Other plastic wrapper</span>
                    <span className="breakdown-count">13</span>
                  </div>
                  <div className="breakdown-item">
                    <span className="breakdown-icon">🧴</span>
                    <span className="breakdown-name">Clear plastic bottle</span>
                    <span className="breakdown-count">9</span>
                  </div>
                </div>
              </div>
              <div className="breakdown-card">
                <h3>By Priority</h3>
                <div className="breakdown-list">
                  <div className="breakdown-item">
                    <span className="priority-indicator" style={{backgroundColor: '#e67e22'}}></span>
                    <span className="breakdown-name">High</span>
                    <span className="breakdown-count">1</span>
                  </div>
                  <div className="breakdown-item">
                    <span className="priority-indicator" style={{backgroundColor: '#f1c40f'}}></span>
                    <span className="breakdown-name">Medium</span>
                    <span className="breakdown-count">37</span>
                  </div>
                  <div className="breakdown-item">
                    <span className="priority-indicator" style={{backgroundColor: '#27ae60'}}></span>
                    <span className="breakdown-name">Low</span>
                    <span className="breakdown-count">65</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Sample Images */}
          <section className="demo-gallery-section">
            <h2>Sample Detection Results</h2>
            <div className="featured-images">
              <div className="featured-image">
                <h4>TACO Trash Detection (Tiled)</h4>
                <img
                  src="/detection-demo/tiled_DJI_20251227131705_0159_D.JPG"
                  alt="TACO tiled detection"
                />
                <p>YOLOv8 trained on TACO dataset with 2x2 tiled inference for small object detection</p>
              </div>
              <div className="featured-image">
                <h4>SAM 2 Segmentation</h4>
                <img
                  src="/detection-demo/DJI_20251227131758_0163_D_frame_000000_sam.jpg"
                  alt="SAM 2 segmentation"
                />
                <p>Meta's Segment Anything Model 2 generates pixel-precise masks for each detected object</p>
              </div>
            </div>
          </section>
        </div>
      )}

      {/* Methodology Tab */}
      {activeTab === 'methodology' && (
        <div className="demo-content methodology-content">
          <section className="methodology-section">
            <h2>Detection Pipeline Methodology</h2>
            <p className="intro-text">
              The Sylva detection system combines two state-of-the-art AI models to achieve
              accurate trash identification and precise segmentation from aerial drone imagery.
            </p>

            {/* Pipeline Diagram */}
            <div className="pipeline-diagram">
              <div className="pipeline-step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h3>Image Acquisition</h3>
                  <p>DJI drone captures 4K aerial imagery at 1 frame/second during survey flights</p>
                </div>
              </div>
              <div className="pipeline-arrow">→</div>
              <div className="pipeline-step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h3>TACO Detection</h3>
                  <p>TACO-trained YOLOv8 identifies 60 trash classes with tiled inference for small objects</p>
                </div>
              </div>
              <div className="pipeline-arrow">→</div>
              <div className="pipeline-step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h3>SAM 2 Segmentation</h3>
                  <p>Meta's Segment Anything Model 2 generates pixel-precise masks using detection boxes as prompts</p>
                </div>
              </div>
              <div className="pipeline-arrow">→</div>
              <div className="pipeline-step">
                <div className="step-number">4</div>
                <div className="step-content">
                  <h3>Classification & Output</h3>
                  <p>Combined results with class labels, priority scores, and area estimates</p>
                </div>
              </div>
            </div>

            {/* Model Details */}
            <div className="model-details">
              <div className="model-card">
                <h3>TACO Detection Model</h3>
                <table className="model-table">
                  <tbody>
                    <tr><td>Base Model</td><td>YOLOv8m (medium)</td></tr>
                    <tr><td>Training Dataset</td><td>TACO (Trash Annotations in Context)</td></tr>
                    <tr><td>Training</td><td>100 epochs</td></tr>
                    <tr><td>Classes</td><td>60 trash categories</td></tr>
                    <tr><td>Inference</td><td>2x2 tiled with 200px overlap</td></tr>
                    <tr><td>Confidence Threshold</td><td>0.12</td></tr>
                  </tbody>
                </table>
                <div className="model-classes">
                  <h4>Detected Classes Include:</h4>
                  <div className="class-tags">
                    <span>Plastic bottles</span>
                    <span>Bottle caps</span>
                    <span>Plastic film</span>
                    <span>Styrofoam</span>
                    <span>Cigarettes</span>
                    <span>Drink cans</span>
                    <span>Wrappers</span>
                    <span>Glass</span>
                    <span>Paper</span>
                    <span>+51 more</span>
                  </div>
                </div>
              </div>

              <div className="model-card">
                <h3>SAM 2 Segmentation Model</h3>
                <table className="model-table">
                  <tbody>
                    <tr><td>Model</td><td>SAM 2.1 Hiera Small</td></tr>
                    <tr><td>Developer</td><td>Meta AI Research</td></tr>
                    <tr><td>Parameters</td><td>~46M</td></tr>
                    <tr><td>Input</td><td>Bounding box prompts from TACO</td></tr>
                    <tr><td>Output</td><td>Pixel-precise binary masks</td></tr>
                    <tr><td>Acceleration</td><td>Apple Silicon MPS</td></tr>
                  </tbody>
                </table>
                <div className="model-benefits">
                  <h4>Benefits:</h4>
                  <ul>
                    <li>Precise object boundaries (not just boxes)</li>
                    <li>Accurate area estimation for volume calculations</li>
                    <li>Works on any object shape</li>
                    <li>No additional training required</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Why This Approach */}
            <div className="approach-section">
              <h3>Why TACO + SAM?</h3>
              <div className="approach-grid">
                <div className="approach-card">
                  <h4>Problem: Generic Models Don't Detect Trash</h4>
                  <p>
                    Standard YOLO models (trained on COCO) detect common objects like cars, people, and bottles
                    but miss most trash items from aerial perspectives. They have no concept of "litter" as a category.
                  </p>
                </div>
                <div className="approach-card">
                  <h4>Solution: Domain-Specific Training</h4>
                  <p>
                    TACO dataset contains 1,500+ images with 4,784 annotations across 60 trash categories,
                    specifically designed for litter detection. Combined with tiled inference, it handles
                    small objects in high-resolution drone imagery.
                  </p>
                </div>
                <div className="approach-card">
                  <h4>Problem: Bounding Boxes Aren't Precise</h4>
                  <p>
                    Detection models output rectangular boxes that include background pixels.
                    This makes accurate size and volume estimation impossible.
                  </p>
                </div>
                <div className="approach-card">
                  <h4>Solution: SAM Segmentation</h4>
                  <p>
                    SAM 2 generates pixel-perfect masks for each detected object, enabling accurate
                    area calculations. By using detection boxes as prompts, we get classification
                    AND precise boundaries.
                  </p>
                </div>
              </div>
            </div>

            {/* Future Enhancements */}
            <div className="future-section">
              <h3>Production Sylva System Enhancements</h3>
              <div className="future-grid">
                <div className="future-item">
                  <span className="future-icon">🌈</span>
                  <h4>Hyperspectral Confirmation</h4>
                  <p>8-band NIR/SWIR sensor (900-1700nm) confirms material type through spectral signatures</p>
                </div>
                <div className="future-item">
                  <span className="future-icon">📡</span>
                  <h4>LiDAR Integration</h4>
                  <p>3D point cloud for volume estimation and terrain mapping</p>
                </div>
                <div className="future-item">
                  <span className="future-icon">⚡</span>
                  <h4>Edge Processing</h4>
                  <p>NVIDIA Jetson Orin NX for real-time on-board inference (&lt;50ms)</p>
                </div>
                <div className="future-item">
                  <span className="future-icon">🎯</span>
                  <h4>Custom Training</h4>
                  <p>Fine-tuned on aerial trash imagery for higher accuracy</p>
                </div>
              </div>
            </div>
          </section>
        </div>
      )}

      {/* Technology Note */}
      <div className="demo-tech-note">
        <h4>About This Demo</h4>
        <p>
          This demonstration shows real detection results from DJI drone footage captured over a field
          with distributed trash items. The <strong>TACO + SAM pipeline</strong> processes each frame
          through specialized trash detection and pixel-precise segmentation.
        </p>
        <p>
          <strong>Source Code:</strong>{' '}
          <a href="https://github.com/facebookresearch/sam2" target="_blank" rel="noopener noreferrer">SAM 2</a> |{' '}
          <a href="https://github.com/jeremy-rico/litter-detection" target="_blank" rel="noopener noreferrer">TACO YOLOv8</a> |{' '}
          <a href="http://tacodataset.org/" target="_blank" rel="noopener noreferrer">TACO Dataset</a>
        </p>
      </div>
    </div>
  )
}

export default DetectionDemo
