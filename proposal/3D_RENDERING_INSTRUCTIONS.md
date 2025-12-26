# Sylva Drone 3D Rendering Instructions

## Overview

This guide explains how to use the Blender script and Three.js viewer to create 3D renders and interactive visualizations of the Sylva-1 drone.

---

## Part 1: Blender Rendering

### Prerequisites

- **Blender 3.0+** (download from [blender.org](https://www.blender.org/download/))
- Your STL files in: `/Users/olivier/Documents/PERSONAL/Kids/Justin/MOOSE FILES PACK/STL/`

### Steps

1. **Open Blender**

2. **Load the Script**
   - Go to **Scripting** workspace (top menu bar)
   - Click **Open** and select: `proposal/blender_sylva_drone.py`

3. **Run the Script**
   - Press **Alt+P** or click **Run Script** button
   - The script will:
     - Import all STL parts (fuselage, wings, V-tail)
     - Create the sensor payload
     - Set up materials (white body, dark props, green accents)
     - Configure studio lighting
     - Create turntable animation

4. **Adjust Parts (if needed)**
   - Parts may need manual positioning
   - Select parts and use **G** (grab), **R** (rotate), **S** (scale)
   - The STL files may have different origins

5. **Render a Single Image**
   - Press **F12**
   - Save with **Image > Save As**

6. **Render Turntable Animation**
   - Go to **Render > Render Animation**
   - Output: `proposal/renders/` folder
   - 120 frames = 5 second loop at 24fps

### Export for Web Viewer

After assembling in Blender:

1. Select the drone parent object (**Sylva_Drone_Root**)
2. Go to **File > Export > glTF 2.0 (.glb)**
3. Settings:
   - Format: GLB (binary)
   - Include: Selected Objects
   - Transform: +Y Up
4. Save as: `dashboard/public/models/sylva_drone.glb`

---

## Part 2: Three.js Web Viewer

### The Component

Located at: `dashboard/src/components/DroneViewer3D.jsx`

### Using the Placeholder Model

The viewer includes a built-in placeholder drone that works immediately:

```jsx
import DroneViewer3D from './components/DroneViewer3D';

// In your component:
<DroneViewer3D
  width="100%"
  height="500px"
  autoRotate={true}
/>
```

### Using Your Actual Model

1. Export from Blender as GLB (see above)
2. Place in: `dashboard/public/models/sylva_drone.glb`
3. Edit `DroneViewer3D.jsx`:
   ```javascript
   const USE_PLACEHOLDER = false;  // Change to false
   ```

### Features

- **Mouse drag**: Rotate view
- **Scroll wheel**: Zoom in/out
- **Auto-rotation**: Slowly spins the model
- **Responsive**: Adapts to container size

### Adding to the Dashboard

Example integration in a page:

```jsx
import DroneViewer3D from '../components/DroneViewer3D';

const DronePage = () => {
  return (
    <div className="drone-showcase">
      <h2>Sylva-1 UAV System</h2>
      <DroneViewer3D height="600px" autoRotate={true} />
      <p>Interactive 3D model - drag to rotate, scroll to zoom</p>
    </div>
  );
};
```

---

## Part 3: Quick Start

### Fastest Path to Renders

1. Open Blender
2. Load `blender_sylva_drone.py`
3. Run script (Alt+P)
4. Manually adjust part positions if needed
5. Press F12 to render
6. Export as GLB for web viewer

### Fastest Path to Web Viewer

1. The placeholder already works!
2. Start dashboard: `npm run dev`
3. Import component where needed
4. Optionally replace with real model later

---

## Troubleshooting

### Blender Issues

**Parts not aligned?**
- STL files may have different coordinate origins
- Select all parts, **Object > Set Origin > Origin to Geometry**
- Then manually position

**Script errors?**
- Check that STL_BASE_PATH is correct
- Some files may have extra spaces in names

**Slow rendering?**
- Reduce samples: `bpy.context.scene.cycles.samples = 64`
- Use EEVEE instead of Cycles for faster previews

### Three.js Issues

**Model not loading?**
- Check browser console for errors
- Ensure GLB file is in `/public/models/`
- File must be under ~50MB for good performance

**Performance issues?**
- Reduce polygon count in Blender before export
- Use Draco compression in GLTF export

---

## File Locations

```
sylva_conrad_simulation/
├── proposal/
│   ├── blender_sylva_drone.py      # Blender assembly script
│   ├── renders/                     # Output folder for renders
│   └── 3D_RENDERING_INSTRUCTIONS.md # This file
│
└── dashboard/
    ├── public/
    │   └── models/
    │       └── sylva_drone.glb      # Place exported model here
    │
    └── src/
        └── components/
            └── DroneViewer3D.jsx    # Three.js viewer component
```

---

## Tips for Best Results

### Blender Rendering

1. **Increase samples** for final renders (256-512)
2. **Add HDRI lighting** for realistic reflections
3. **Enable denoising** in render settings
4. **Use compositing** for color grading

### Web Optimization

1. **Decimate** high-poly meshes before export
2. **Bake textures** if using complex materials
3. **Use Draco compression** for smaller file sizes
4. **Test on mobile** for performance

---

*TamAir Environmental Technologies - Conrad Challenge 2026*
