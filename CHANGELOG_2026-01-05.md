# Sylva Website Changes - January 5, 2026

## Summary
Major updates to the Sylva website (sylva-us.com) for the Conrad Challenge 2026 submission. Focus on improving the technology section with sensor fusion accuracy visualization and enhancing the overall user experience.

---

## Sensor Fusion Accuracy Chart (Our Technology Section)

### New Feature: Vertical Bar Chart
Added a visual bar chart showing how detection accuracy improves as sensors are combined:

| Sensor Configuration | Accuracy | Bar Color |
|---------------------|----------|-----------|
| RGB Only | ~70% | Orange |
| Hyperspectral Only | ~70% | Orange |
| RGB + Hyperspectral | ~78% | Yellow |
| RGB + LiDAR | ~80% | Lime |
| Sylva Full Fusion | >90% | Green |

### Chart Features:
- **Y-axis**: Vertical label "Trash Detection Accuracy" (removed percentage numbers for cleaner look)
- **X-axis**: Sensor configuration labels with accuracy values
- **Customer Threshold Line**: Red dashed line at 85% with label "Customer Desired Performance (85%)"
- **Reference Citation**: Linked to Zhang et al. (2024) multi-sensor fusion paper from Int. J. Remote Sensing
- **Animated bars**: Bars grow on page load with CSS animation

### Related Commits:
- `918feb0` - Replace sensor fusion line chart with vertical bar chart
- `2c23558` - Fix bar chart: add bars, correct threshold alignment, Y-axis 50-100%
- `be42a81` - Correct bar heights to match accuracy values
- `b892097` - Wrap threshold label text across multiple lines
- `d157826` - Replace Y-axis numbers with vertical label
- `cd1dbc1` - Increase threshold label font size
- `bb2f042` - Add reference citation below sensor fusion chart
- `5b3d8a1` - Add clickable link to chart reference

---

## Map Loading Experience

### Splash Screen
Added an impressive loading screen while the map initializes:
- Animated drone icon with rotation effect
- Progress bar animation
- "Initializing Map..." text
- **Maximum timeout: 6 seconds** (prevents indefinite loading)

### Related Commits:
- `1ef622f` - Move Watch Showcase to header and add impressive loading screen
- `87f0b35` - Add 10-second max timeout to splash screen
- `93a5d09` - Reduce splash screen timeout to 6 seconds

---

## Watch Showcase Feature

### Improvements:
- Moved "Watch Showcase" button to header (next to "SYLVA Environmental Monitoring System")
- Fully automated hands-off demo experience
- Reduced to 2 locations for better pacing
- Fixed sidebar button styling

### Related Commits:
- `1ef622f` - Move Watch Showcase to header
- `53af4a8` - Fix Watch Showcase for fully hands-off automated experience
- `a8c21a1` - Overhaul Watch Showcase feature for better demo experience
- `6a53e49` - Fix sidebar button styling and reduce showcase to 2 locations

---

## Text Content Updates

### Technology Section:
- Changed hybrid sensor description from "— capturing" to "thus capturing"
- Updated Sylva accuracy from 87% to 90% in "How We Compare" section

### Related Commits:
- `b7da8eb` - Update hybrid sensor description text
- `3cb05a4` - Update Sylva accuracy from 87% to 90%

---

## Visual Enhancements

### Spectral Visualization:
- Redesigned to show full hybrid camera coverage
- Separate visible/IR sections
- Highlighted infrared detection capabilities
- Full-spectrum scan line with detection ping animations

### Related Commits:
- `35d775f` - Update spectral visualization to show full hybrid camera coverage
- `4e8f47c` - Redesign spectral visualization with separate visible/IR sections
- `3b0e3ca` - Enhance spectral visualization to highlight infrared detection
- `3f7baed` - Add full-spectrum scan line with detection ping animations
- `99c0a00` - Fine-tune detection ping timings to match scan line

---

## Other Updates

### Timeline:
- Updated dates in "Our Journey" and "Next Steps" sections

### Footer:
- Added subtle Claude Code credit

### Conrad Challenge Badge:
- Fixed link to correct URL

### Related Commits:
- `de4cb07` - Update timeline dates in Our Journey and Next Steps
- `cf8f418` - Add subtle Claude Code credit in footer
- `ade0ec5` - Fix Conrad Challenge badge link to correct URL

---

## Files Modified

### Primary Files:
- `dashboard/src/pages/Home.jsx` - Main website with all sections
- `dashboard/src/styles.css` - All styling
- `dashboard/src/App.jsx` - Simulation app with showcase features
- `dashboard/src/components/Map.jsx` - Map component with loading callback

### Key CSS Classes Added:
- `.accuracy-bar-chart` - Bar chart container
- `.bar-chart-y-axis` - Y-axis with vertical label
- `.y-axis-label` - Vertical "Trash Detection Accuracy" text
- `.bar-wrapper` - Container for each bar
- `.bar` - Individual bar styling (`.orange`, `.yellow`, `.lime`, `.green`)
- `.threshold-line-container` - Customer threshold line
- `.threshold-label` - "Customer Desired Performance (85%)" label
- `.chart-reference` - Reference citation styling

---

## Technical Notes

### Bar Height Calculations (Y-axis 50-100% range):
The bar heights needed manual adjustment to compensate for container padding:
- 70% accuracy → 32% height
- 78% accuracy → 50% height
- 80% accuracy → 56% height
- 90% accuracy → 80% height

### Threshold Line Position:
- 85% accuracy = 70% up from 50% baseline
- Position: `bottom: 212px`

---

## Deployment
All changes automatically deployed to sylva-us.com via Render.
