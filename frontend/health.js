const API_BASE = "http://localhost:8000/api"

// --- Health Management Tabs ---
function showHealthTab(tab) {
  document.querySelectorAll(".tab-btn").forEach((btn) => btn.classList.remove("active"))
  document.querySelectorAll(".health-tab").forEach((tabDiv) => tabDiv.classList.remove("active"))
  document.querySelector(`.tab-btn[onclick*="${tab}"]`).classList.add("active")
  document.getElementById(`health-${tab}-tab`).classList.add("active")
}

// --- Populate Animal Dropdowns for Health ---
async function populateHealthAnimalDropdowns() {
  try {
    const res = await fetch(`${API_BASE}/animals/`)
    if (!res.ok) throw new Error("Failed to load animals")
    const data = await res.json()
    const animalOptions = data.results
      .map((animal) => `<option value="${animal.id}">${animal.tag_id} - ${animal.name}</option>`)
      .join("")
    ;["health-animal-event", "vacc-animal", "treat-animal"].forEach((id) => {
      const select = document.getElementById(id)
      if (select) select.innerHTML = '<option value="">Select Animal</option>' + animalOptions
    })
  } catch (err) {
    showError("health-event-error", err.message)
  }
}

// --- Health Events ---
async function loadHealthEvents() {
  try {
    const res = await fetch(`${API_BASE}/health/events/`)
    if (!res.ok) throw new Error("Failed to load health events")
    const data = await res.json()
    const tbody = document.querySelector("#health-events-table tbody")
    tbody.innerHTML = ""
    data.results.forEach((event) => {
      const tr = document.createElement("tr")
      tr.innerHTML = `
                <td>${event.animal_id}</td>
                <td>${event.event_type}</td>
                <td>${event.title}</td>
                <td>${event.severity}</td>
                <td>${event.event_date.replace("T", " ").slice(0, 16)}</td>
                <td>${event.veterinarian || "-"}</td>
                <td>${event.cost || "-"}</td>
                <td><button class="btn-danger" onclick="deleteHealthEvent(${event.id})">Delete</button></td>
            `
      tbody.appendChild(tr)
    })
  } catch (err) {
    showError("health-event-error", err.message)
  }
}

document.getElementById("health-event-form").onsubmit = async (e) => {
  e.preventDefault()
  const animal_id = document.getElementById("health-animal-event").value
  const event_type = document.getElementById("health-event-type").value
  const title = document.getElementById("health-title").value
  const description = document.getElementById("health-description").value
  const severity = document.getElementById("health-severity").value
  const event_date = document.getElementById("health-event-date").value
  const veterinarian = document.getElementById("health-vet").value
  const cost = document.getElementById("health-cost").value
  const notes = document.getElementById("health-notes").value
  try {
    const res = await fetch(`${API_BASE}/health/events/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        animal_id,
        event_type,
        title,
        description,
        severity,
        event_date,
        veterinarian,
        cost,
        notes,
      }),
    })
    if (!res.ok) {
      const data = await res.json()
      throw new Error(Object.values(data).flat().join(", "))
    }
    showSuccess("health-event-success", "Health event added!")
    document.getElementById("health-event-form").reset()
    await loadHealthEvents()
    setTimeout(() => clearMessage("health-event-success"), 3000)
  } catch (err) {
    showError("health-event-error", err.message)
  }
}

async function deleteHealthEvent(id) {
  if (!confirm("Delete this health event?")) return
  try {
    const res = await fetch(`${API_BASE}/health/events/${id}/`, { method: "DELETE" })
    if (!res.ok) throw new Error("Failed to delete health event")
    showSuccess("health-event-success", "Deleted!")
    await loadHealthEvents()
    setTimeout(() => clearMessage("health-event-success"), 3000)
  } catch (err) {
    showError("health-event-error", err.message)
  }
}

// --- Vaccinations ---
async function loadVaccinations() {
  try {
    const res = await fetch(`${API_BASE}/health/vaccinations/`)
    if (!res.ok) throw new Error("Failed to load vaccinations")
    const data = await res.json()
    const tbody = document.querySelector("#vaccinations-table tbody")
    tbody.innerHTML = ""
    data.results.forEach((vacc) => {
      const tr = document.createElement("tr")
      tr.innerHTML = `
                <td>${vacc.animal_id}</td>
                <td>${vacc.vaccine_name}</td>
                <td>${vacc.vaccine_type}</td>
                <td>${vacc.administered_date}</td>
                <td>${vacc.next_due_date || "-"}</td>
                <td>${vacc.veterinarian || "-"}</td>
                <td>${vacc.cost || "-"}</td>
                <td><button class="btn-danger" onclick="deleteVaccination(${vacc.id})">Delete</button></td>
            `
      tbody.appendChild(tr)
    })
  } catch (err) {
    showError("vaccination-error", err.message)
  }
}

document.getElementById("vaccination-form").onsubmit = async (e) => {
  e.preventDefault()
  const animal_id = document.getElementById("vacc-animal").value
  const vaccine_name = document.getElementById("vaccine-name").value
  const vaccine_type = document.getElementById("vaccine-type").value
  const administered_date = document.getElementById("vaccine-admin-date").value
  const next_due_date = document.getElementById("vaccine-next-due").value
  const batch_number = document.getElementById("vaccine-batch").value
  const veterinarian = document.getElementById("vaccine-vet").value
  const cost = document.getElementById("vaccine-cost").value
  const notes = document.getElementById("vaccine-notes").value
  try {
    const res = await fetch(`${API_BASE}/health/vaccinations/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        animal_id,
        vaccine_name,
        vaccine_type,
        administered_date,
        next_due_date,
        batch_number,
        veterinarian,
        cost,
        notes,
      }),
    })
    if (!res.ok) {
      const data = await res.json()
      throw new Error(Object.values(data).flat().join(", "))
    }
    showSuccess("vaccination-success", "Vaccination added!")
    document.getElementById("vaccination-form").reset()
    await loadVaccinations()
    setTimeout(() => clearMessage("vaccination-success"), 3000)
  } catch (err) {
    showError("vaccination-error", err.message)
  }
}

async function deleteVaccination(id) {
  if (!confirm("Delete this vaccination?")) return
  try {
    const res = await fetch(`${API_BASE}/health/vaccinations/${id}/`, { method: "DELETE" })
    if (!res.ok) throw new Error("Failed to delete vaccination")
    showSuccess("vaccination-success", "Deleted!")
    await loadVaccinations()
    setTimeout(() => clearMessage("vaccination-success"), 3000)
  } catch (err) {
    showError("vaccination-error", err.message)
  }
}

// --- Treatments ---
async function loadTreatments() {
  try {
    const res = await fetch(`${API_BASE}/health/treatments/`)
    if (!res.ok) throw new Error("Failed to load treatments")
    const data = await res.json()
    const tbody = document.querySelector("#treatments-table tbody")
    tbody.innerHTML = ""
    data.results.forEach((treat) => {
      const tr = document.createElement("tr")
      tr.innerHTML = `
                <td>${treat.animal_id}</td>
                <td>${treat.condition}</td>
                <td>${treat.medication}</td>
                <td>${treat.start_date}</td>
                <td>${treat.end_date || "-"}</td>
                <td>${treat.status}</td>
                <td>${treat.veterinarian || "-"}</td>
                <td>${treat.cost || "-"}</td>
                <td><button class="btn-danger" onclick="deleteTreatment(${treat.id})">Delete</button></td>
            `
      tbody.appendChild(tr)
    })
  } catch (err) {
    showError("treatment-error", err.message)
  }
}

document.getElementById("treatment-form").onsubmit = async (e) => {
  e.preventDefault()
  const animal_id = document.getElementById("treat-animal").value
  const condition = document.getElementById("treat-condition").value
  const medication = document.getElementById("treat-medication").value
  const dosage = document.getElementById("treat-dosage").value
  const frequency = document.getElementById("treat-frequency").value
  const start_date = document.getElementById("treat-start-date").value
  const end_date = document.getElementById("treat-end-date").value
  const status = document.getElementById("treat-status").value
  const veterinarian = document.getElementById("treat-vet").value
  const cost = document.getElementById("treat-cost").value
  const notes = document.getElementById("treat-notes").value
  try {
    const res = await fetch(`${API_BASE}/health/treatments/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        animal_id,
        condition,
        medication,
        dosage,
        frequency,
        start_date,
        end_date,
        status,
        veterinarian,
        cost,
        notes,
      }),
    })
    if (!res.ok) {
      const data = await res.json()
      throw new Error(Object.values(data).flat().join(", "))
    }
    showSuccess("treatment-success", "Treatment added!")
    document.getElementById("treatment-form").reset()
    await loadTreatments()
    setTimeout(() => clearMessage("treatment-success"), 3000)
  } catch (err) {
    showError("treatment-error", err.message)
  }
}

async function deleteTreatment(id) {
  if (!confirm("Delete this treatment?")) return
  try {
    const res = await fetch(`${API_BASE}/health/treatments/${id}/`, { method: "DELETE" })
    if (!res.ok) throw new Error("Failed to delete treatment")
    showSuccess("treatment-success", "Deleted!")
    await loadTreatments()
    setTimeout(() => clearMessage("treatment-success"), 3000)
  } catch (err) {
    showError("treatment-error", err.message)
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
  populateHealthAnimalDropdowns()
  loadHealthEvents()
  loadVaccinations()
  loadTreatments()
})
