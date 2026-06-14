import { useEffect, useMemo, useState } from "react"

import { getCountries, getMatches, getSuggestions, uploadCv } from "@/lib/api"
import { fallbackCountries, initialSearch } from "../constants"
import { scoreLabel } from "../formatters"

export function useJobMatchingWorkflow() {
  const [file, setFile] = useState(null)
  const [cvData, setCvData] = useState(null)
  const [search, setSearch] = useState(initialSearch)
  const [matches, setMatches] = useState([])
  const [total, setTotal] = useState(0)
  const [status, setStatus] = useState("idle")
  const [error, setError] = useState("")
  const [countries, setCountries] = useState(fallbackCountries)
  const [suggestionsByJob, setSuggestionsByJob] = useState({})
  const [suggestionLoadingJobId, setSuggestionLoadingJobId] = useState(null)

  const canSearch = Boolean(cvData?.raw_text && search.keywords.trim())
  const topScore = useMemo(() => scoreLabel(matches[0]?.score || 0), [matches])

  useEffect(() => {
    let isMounted = true

    async function loadCountries() {
      try {
        const countryList = await getCountries()

        if (isMounted && countryList?.length) {
          setCountries(countryList)
        }
      } catch {
        if (isMounted) {
          setCountries(fallbackCountries)
        }
      }
    }

    loadCountries()

    return () => {
      isMounted = false
    }
  }, [])

  async function selectCv(selectedFile) {
    if (!selectedFile) {
      return
    }

    if (selectedFile.type !== "application/pdf") {
      setError("Please upload a PDF file.")
      setFile(null)
      setCvData(null)
      return
    }

    setFile(selectedFile)
    setCvData(null)
    setMatches([])
    setTotal(0)
    setSuggestionsByJob({})
    setStatus("uploading")
    setError("")

    try {
      const parsedCv = await uploadCv(selectedFile)

      if (!parsedCv?.raw_text) {
        throw new Error("CV uploaded, but no text could be extracted.")
      }

      setCvData(parsedCv)
      setStatus("ready")
    } catch (uploadError) {
      setFile(null)
      setCvData(null)
      setStatus("idle")
      setError(uploadError.message || "Failed to upload CV.")
    }
  }

  async function searchJobs(event) {
    event.preventDefault()

    if (!canSearch) {
      setError("Upload a CV and add a role before searching.")
      return
    }

    setStatus("matching")
    setError("")
    setSuggestionsByJob({})

    try {
      const result = await getMatches({
        keywords: search.keywords.trim(),
        location: search.location.trim() || "gb",
        cvText: cvData.raw_text,
        num_pages: Number(search.num_pages),
      })

      setMatches(result.matches || [])
      setTotal(result.total || 0)
      setStatus("matched")
    } catch (matchError) {
      setStatus("ready")
      setError(matchError.message)
    }
  }

  async function requestSuggestions(job) {
    setError("")
    setSuggestionLoadingJobId(job.job_id)

    try {
      const result = await getSuggestions({
        cvText: cvData.raw_text,
        job,
      })

      setSuggestionsByJob((current) => ({
        ...current,
        [job.job_id]: result,
      }))
    } catch (suggestionError) {
      setError(suggestionError.message || "Failed to get CV suggestions.")
    } finally {
      setSuggestionLoadingJobId(null)
    }
  }

  function updateSearch(field, value) {
    setSearch((current) => ({
      ...current,
      [field]: value,
    }))
  }

  return {
    canSearch,
    countries,
    cvData,
    error,
    file,
    matches,
    search,
    status,
    suggestionLoadingJobId,
    suggestionsByJob,
    summary: {
      topScore,
      total,
    },
    requestSuggestions,
    searchJobs,
    selectCv,
    updateSearch,
  }
}
