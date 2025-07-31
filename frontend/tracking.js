const API_BASE = "http://localhost:8000/api"

// --- Tracking Management ---
async function populateTrackingAnimalDropdown() {
  try {
    const res = await fetch(`${API_BASE}/animals/`)
    if (!res.ok) throw new Error("Failed to load animals")
    const data = await res.json()
    const animalOptions = data.results
      .map((animal) => `<option value="${animal.id}">${animal.tag_id} - ${animal.name}</option>`)
      .join("")
    const select = document.getElementById("tracking-animal")
    if (select) select.innerHTML = '<option value="">Assign to Animal</option>' + animalOptions
  } catch (err) {
    showError("tracking-device-error", err.message)
  }
}

async function loadTrackingDevices() {
  try {
    const res = await fetch(`${API_BASE}/tracking/devices/`)
    if (!res.ok) throw new Error("Failed to load tracking devices")
    const data = await res.json()
    const tbody = document.querySelector("#tracking-devices-table tbody")
    tbody.innerHTML = ""
    data.results.forEach((device) => {
      const tr = document.createElement("tr")
      tr.innerHTML = `
                <td>${device.device_id}</td>
                <td>${device.device_type}</td>
                <td>${device.animal_name || "-"}</td>
                <td>${device.is_active ? "Yes" : "No"}</td>
                <td>${device.battery_level}%</td>
                <td>${device.last_seen ? device.last_seen.replace("T", " ").slice(0, 16) : "-"}</td>
                <td><button class="btn-danger" onclick="deleteTrackingDevice(${device.id})">Delete</button></td>
            `
      tbody.appendChild(tr)
    })
  } catch (err) {
    showError("tracking-device-error", err.message)
  }
}

document.getElementById("tracking-device-form").onsubmit = async (e) => {
  e.preventDefault()
  const device_id = document.getElementById("tracking-device-id").value
  const device_type = document.getElementById("tracking-device-type").value
  const animal = document.getElementById("tracking-animal").value
  try {
    const res = await fetch(`${API_BASE}/tracking/devices/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ device_id, device_type, animal }),
    })
    if (!res.ok) {
      const data = await res.json()
      throw new Error(Object.values(data).flat().join(", "))
    }
    showSuccess("tracking-device-success", "Tracking device added!")
    document.getElementById("tracking-device-form").reset()
    await loadTrackingDevices()
    setTimeout(() => clearMessage("tracking-device-success"), 3000)
  } catch (err) {
    showError("tracking-device-error", err.message)
  }
}

async function deleteTrackingDevice(id) {
  if (!confirm("Delete this tracking device?")) return
  try {
    const res = await fetch(`${API_BASE}/tracking/devices/${id}/`, { method: "DELETE" })
    if (!res.ok) throw new Error("Failed to delete tracking device")
    showSuccess("tracking-device-success", "Deleted!")
    await loadTrackingDevices()
    setTimeout(() => clearMessage("tracking-device-success"), 3000)
  } catch (err) {
    showError("tracking-device-error", err.message)
  }
}

// --- Utility Functions ---
function showError(elementId, message) {
  const element = document.getElementById(elementId)
  element.textContent = message
  element.classList.remove("hidden")
}

function showSuccess(elementId, message) {
  const element = document.getElementById(elementId)
  element.textContent = message
  element.classList.remove("hidden")
}

function clearMessage(elementId) {
  const element = document.getElementById(elementId)
  element.classList.add("hidden")
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  populateTrackingAnimalDropdown()
  loadTrackingDevices()
})
