const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export async function uploadCv(file) {
  const formData = new FormData()
  formData.append("file", file)

  const response = await fetch(`${API_BASE_URL}/cv/upload`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => null)
    throw new Error(error?.detail || "Failed to upload CV")
  }

  return response.json()
}

export async function getMatches({ keywords, location, cvText, num_pages }) {
  const response = await fetch(`${API_BASE_URL}/match/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      keywords,
      location,
      cv_text: cvText,
      num_pages: num_pages,
    }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => null)
    throw new Error(error?.detail || "Failed to get job matches")
  }

  return response.json()
}

export async function getCountries() {
  const response = await fetch(`${API_BASE_URL}/jobs/countries`)

  if (!response.ok) {
    const error = await response.json().catch(() => null)
    throw new Error(error?.detail || "Failed to get countries")
  }

  return response.json()
}

export async function getSuggestions({ cvText, job }) {
  const response = await fetch(`${API_BASE_URL}/suggestions/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      cv_text: cvText,
      job,
    }),
  })

  if (!response.ok) {
    if (response.status === 429) {
      throw new Error("Suggestion limit reached. Please try again later.")
    }

    const error = await response.json().catch(() => null)
    throw new Error(error?.detail || "Failed to get CV suggestions.")
  }

  return response.json()
}