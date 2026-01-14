/**
 * SimulationPreloader - Background preloading for the Simulation page
 *
 * This utility preloads API data and map tiles while users browse the Home page,
 * so the Simulation page loads instantly when they navigate to it.
 */

const API_BASE = 'https://sylva-api.onrender.com/api'

// Cache to store preloaded data
const preloadCache = {
  locations: null,
  categories: null,
  detections: null,
  heatmap: null,
  stats: null,
  flights: {},
  tilesLoaded: false,
  isPreloading: false,
  isComplete: false,
}

// Default location for tile preloading (Stinson Beach)
const DEFAULT_LOCATION = {
  lat: 37.8985,
  lon: -122.6352,
  zoom: 14,
}

/**
 * Generate tile URLs for a given location and zoom level
 */
function getTileUrls(lat, lon, zoom, tileProvider) {
  // Convert lat/lon to tile coordinates
  const n = Math.pow(2, zoom)
  const x = Math.floor((lon + 180) / 360 * n)
  const y = Math.floor((1 - Math.log(Math.tan(lat * Math.PI / 180) + 1 / Math.cos(lat * Math.PI / 180)) / Math.PI) / 2 * n)

  const tiles = []

  // Get tiles in a 3x3 grid around the center
  for (let dx = -1; dx <= 1; dx++) {
    for (let dy = -1; dy <= 1; dy++) {
      const tileX = x + dx
      const tileY = y + dy

      if (tileProvider === 'carto') {
        const subdomain = ['a', 'b', 'c', 'd'][Math.abs(tileX + tileY) % 4]
        tiles.push(`https://${subdomain}.basemaps.cartocdn.com/rastertiles/voyager/${zoom}/${tileX}/${tileY}@2x.png`)
      } else if (tileProvider === 'esri') {
        tiles.push(`https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/${zoom}/${tileY}/${tileX}`)
      }
    }
  }

  return tiles
}

/**
 * Preload a single image tile
 */
function preloadTile(url) {
  return new Promise((resolve) => {
    const img = new Image()
    img.crossOrigin = 'anonymous'
    img.onload = () => resolve(true)
    img.onerror = () => resolve(false) // Don't fail on tile errors
    img.src = url
  })
}

/**
 * Preload map tiles for the default location
 */
async function preloadMapTiles() {
  if (preloadCache.tilesLoaded) return

  const { lat, lon, zoom } = DEFAULT_LOCATION
  const zoomLevels = [12, 13, 14, 15] // Preload multiple zoom levels

  const allTileUrls = []

  for (const z of zoomLevels) {
    // Preload both map and satellite tiles
    allTileUrls.push(...getTileUrls(lat, lon, z, 'carto'))
    allTileUrls.push(...getTileUrls(lat, lon, z, 'esri'))
  }

  // Load tiles in batches to avoid overwhelming the browser
  const batchSize = 6
  for (let i = 0; i < allTileUrls.length; i += batchSize) {
    const batch = allTileUrls.slice(i, i + batchSize)
    await Promise.all(batch.map(preloadTile))
    // Small delay between batches to be nice to the network
    await new Promise(resolve => setTimeout(resolve, 50))
  }

  preloadCache.tilesLoaded = true
}

/**
 * Preload API data
 */
async function preloadApiData() {
  try {
    // Fetch all API data in parallel
    const [locationsRes, categoriesRes, detectionsRes, heatmapRes, statsRes] = await Promise.all([
      fetch(`${API_BASE}/locations`),
      fetch(`${API_BASE}/detections/categories`),
      fetch(`${API_BASE}/detections`),
      fetch(`${API_BASE}/heatmap`),
      fetch(`${API_BASE}/stats`),
    ])

    // Parse responses
    const [locations, categories, detections, heatmap, stats] = await Promise.all([
      locationsRes.json(),
      categoriesRes.json(),
      detectionsRes.json(),
      heatmapRes.json(),
      statsRes.json(),
    ])

    // Store in cache
    preloadCache.locations = locations
    preloadCache.categories = categories
    preloadCache.detections = detections
    preloadCache.heatmap = heatmap
    preloadCache.stats = stats

    // Preload flights for each location
    if (locations.locations) {
      const flightPromises = locations.locations.map(async (loc) => {
        try {
          const flightRes = await fetch(`${API_BASE}/flights/${loc.id}`)
          const flightData = await flightRes.json()
          preloadCache.flights[loc.id] = flightData
        } catch (e) {
          // Ignore individual flight errors
        }
      })
      await Promise.all(flightPromises)
    }

    return true
  } catch (error) {
    console.warn('Simulation preload: API data fetch failed', error)
    return false
  }
}

/**
 * Main preload function - call this from Home page
 */
export async function preloadSimulation() {
  // Don't run multiple times
  if (preloadCache.isPreloading || preloadCache.isComplete) {
    return preloadCache
  }

  preloadCache.isPreloading = true

  try {
    // Run API preload and tile preload in parallel
    await Promise.all([
      preloadApiData(),
      preloadMapTiles(),
    ])

    preloadCache.isComplete = true
  } catch (error) {
    console.warn('Simulation preload failed:', error)
  }

  preloadCache.isPreloading = false
  return preloadCache
}

/**
 * Get preloaded data (for use in Simulation page)
 */
export function getPreloadedData() {
  return preloadCache
}

/**
 * Check if preloading is complete
 */
export function isPreloadComplete() {
  return preloadCache.isComplete
}

export default {
  preloadSimulation,
  getPreloadedData,
  isPreloadComplete,
}
