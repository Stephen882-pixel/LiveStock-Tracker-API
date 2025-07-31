const API_BASE = "http://localhost:8000/api"

// Dashboard Statistics
async function loadDashboardStats() {
  try {
    // Load breeds count
    const breedsRes = await fetch(`${API_BASE}/breeds/`)
    if (breedsRes.ok) {
      const breedsData = await breedsRes.json()
      document.getElementById("total-breeds").textContent = breedsData.count || breedsData.results?.length || 0
    }

    // Load animals count and health status
    const animalsRes = await fetch(`${API_BASE}/animals/`)
    if (animalsRes.ok) {
      const animalsData = await animalsRes.json()
      const totalAnimals = animalsData.count || animalsData.results?.length || 0
      document.getElementById("total-animals").textContent = totalAnimals

      // Count healthy animals
      const healthyCount = animalsData.results?.filter((animal) => animal.health_status === "healthy").length || 0
      document.getElementById("healthy-animals").textContent = healthyCount
    }

    // Load tracking devices count
    const devicesRes = await fetch(`${API_BASE}/tracking/devices/`)
    if (devicesRes.ok) {
      const devicesData = await devicesRes.json()
      const activeDevices = devicesData.results?.filter((device) => device.is_active).length || 0
      document.getElementById("active-devices").textContent = activeDevices
    }
  } catch (error) {
    console.error("Error loading dashboard stats:", error)
  }
}

// Initialize dashboard
document.addEventListener("DOMContentLoaded", () => {
  loadDashboardStats()

  // Refresh stats every 30 seconds
  setInterval(loadDashboardStats, 30000)
})
