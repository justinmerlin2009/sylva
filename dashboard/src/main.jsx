import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import DetectionDemo from './pages/DetectionDemo'
import App from './App'
import './styles.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/detection-demo" element={<DetectionDemo />} />
        <Route path="/simulation" element={<App />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)
