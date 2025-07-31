const API_BASE = "http://localhost:8000/api"

// --- Animals Management ---
async function loadAnimals() {
  try {
    const res = await fetch(`${API_BASE}/animals/`)
    if (!res.ok) throw new Error("Failed to load animals")
    const data = await res.json()
    const tbody = document.querySelector("#animals-table tbody")
    tbody.innerHTML = ""
    data.results.forEach((animal) => {
      const tr = document.createElement("tr")
      tr.innerHTML = `
                <td>${animal.tag_id}</td>
                <td>${animal.name}</td>
                <td>${animal.breed_name}</td>
                <td>${animal.gender}</td>
                <td>${animal.age_in_years || 0}</td>
                <td>${animal.weight} kg</td>
                <td>${animal.status}</td>
                <td>${animal.health_status}</td>
                <td><button class="btn-danger" onclick="deleteAnimal(${animal.id})">Delete</button></td>
            `
      tbody.appendChild(tr)
    })
  } catch (err) {
    showError("animal-error", err.message)
  }
}

async function loadBreeds() {
  try {
    const res = await fetch(`${API_BASE}/breeds/`)
    if (!res.ok) throw new Error("Failed to load breeds")
    const data = await res.json()

    // Update breed dropdown for animals
    const breedSelect = document.getElementById("animal-breed")
    breedSelect.innerHTML = '<option value="">Select Breed</option>'
    data.results.forEach((breed) => {
      const option = document.createElement("option")
      option.value = breed.name
      option.textContent = breed.name
      breedSelect.appendChild(option)
    })
  } catch (err) {
    showError("animal-error", err.message)
  }
}

document.getElementById("animal-form").onsubmit = async (e) => {
  e.preventDefault()
  const tag_id = document.getElementById("animal-tag").value
  const name = document.getElementById("animal-name").value
  const breed = document.getElementById("animal-breed").value
  const gender = document.getElementById("animal-gender").value
  const date_of_birth = document.getElementById("animal-dob").value
  const weight = document.getElementById("animal-weight").value
  const color = document.getElementById("animal-color").value
  const status = document.getElementById("animal-status").value
  const health_status = document.getElementById("animal-health").value
  const location = document.getElementById("animal-location").value
  const notes = document.getElementById("animal-notes").value

  try {
    const res = await fetch(`${API_BASE}/animals/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tag_id,
        name,
        breed,
        gender,
        date_of_birth,
        weight,
        color,
        status,
        health_status,
        location,
        notes,
      }),
    })

    if (!res.ok) {
      const data = await res.json()
      throw new Error(Object.values(data).flat().join(", "))
    }

    showSuccess("animal-success", "Animal added successfully!")
    document.getElementById("animal-form").reset()
    await loadAnimals()
    setTimeout(() => clearMessage("animal-success"), 3000)
  } catch (err) {
    showError("animal-error", err.message)
  }
}

async function deleteAnimal(id) {
  if (!confirm("Are you sure you want to delete this animal?")) return

  try {
    const res = await fetch(`${API_BASE}/animals/${id}/`, {
      method: "DELETE",
    })

    if (!res.ok) throw new Error("Failed to delete animal")

    showSuccess("animal-success", "Animal deleted successfully!")
    await loadAnimals()
    setTimeout(() => clearMessage("animal-success"), 3000)
  } catch (err) {
    showError("animal-error", err.message)
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
  loadBreeds()
  loadAnimals()
})
