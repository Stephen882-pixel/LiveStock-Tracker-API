const API_BASE = "http://localhost:8000/api"

// --- Breeds Management ---
async function loadBreeds() {
  try {
    const res = await fetch(`${API_BASE}/breeds/`)
    if (!res.ok) throw new Error("Failed to load breeds")
    const data = await res.json()
    const tbody = document.querySelector("#breeds-table tbody")
    tbody.innerHTML = ""
    data.results.forEach((breed) => {
      const tr = document.createElement("tr")
      tr.innerHTML = `
                <td>${breed.name}</td>
                <td>${breed.description || "-"}</td>
                <td>${breed.origin_country || "-"}</td>
                <td>${breed.animals_count}</td>
                <td><button class="btn-danger" onclick="deleteBreed(${breed.id})">Delete</button></td>
            `
      tbody.appendChild(tr)
    })
  } catch (err) {
    showError("breed-error", err.message)
  }
}

document.getElementById("breed-form").onsubmit = async (e) => {
  e.preventDefault()
  const name = document.getElementById("breed-name").value
  const description = document.getElementById("breed-description").value
  const origin_country = document.getElementById("breed-origin").value

  try {
    const res = await fetch(`${API_BASE}/breeds/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, description, origin_country }),
    })

    if (!res.ok) {
      const data = await res.json()
      throw new Error(Object.values(data).flat().join(", "))
    }

    showSuccess("breed-success", "Breed added successfully!")
    document.getElementById("breed-form").reset()
    await loadBreeds()
    setTimeout(() => clearMessage("breed-success"), 3000)
  } catch (err) {
    showError("breed-error", err.message)
  }
}

async function deleteBreed(id) {
  if (!confirm("Are you sure you want to delete this breed?")) return

  try {
    const res = await fetch(`${API_BASE}/breeds/${id}/`, {
      method: "DELETE",
    })

    if (!res.ok) throw new Error("Failed to delete breed")

    showSuccess("breed-success", "Breed deleted successfully!")
    await loadBreeds()
    setTimeout(() => clearMessage("breed-success"), 3000)
  } catch (err) {
    showError("breed-error", err.message)
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
})
