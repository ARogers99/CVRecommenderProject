import { useMemo, useState } from "react"
import {
  ArrowUpRight,
  BriefcaseBusiness,
  CheckCircle2,
  FileText,
  Loader2,
  MapPin,
  Search,
  Sparkles,
  Upload,
  XCircle,
} from "lucide-react"

import "./App.css"
import { Button } from "@/components/ui/button"
import { getMatches, uploadCv } from "@/lib/api"

const initialSearch = {
  keywords: "",
  location: "gb",
  num_pages: 1,
}

function formatSalary(job) {
  return job.salary || "Salary not listed"
}

function scoreLabel(score) {
  return `${Math.round(score * 100)}%`
}

function App() {
  const [file, setFile] = useState(null)
  const [cvData, setCvData] = useState(null)
  const [search, setSearch] = useState(initialSearch)
  const [matches, setMatches] = useState([])
  const [total, setTotal] = useState(0)
  const [status, setStatus] = useState("idle")
  const [error, setError] = useState("")

  const canSearch = Boolean(cvData?.raw_text && search.keywords.trim())
  const topScore = useMemo(() => {
    if (!matches.length) {
      return "0%"
    }

    return scoreLabel(matches[0].score)
  }, [matches])

  async function handleUpload(event) {
    event.preventDefault()
    if (!file) {
      setError("Choose a PDF CV first.")
      return
    }

    setStatus("uploading")
    setError("")
    setMatches([])
    setTotal(0)

    try {
      const parsedCv = await uploadCv(file)
      setCvData(parsedCv)
      setStatus("ready")
    } catch (uploadError) {
      setStatus("idle")
      setError(uploadError.message)
    }
  }

  async function handleSearch(event) {
    event.preventDefault()
    if (!canSearch) {
      setError("Upload a CV and add a role before searching.")
      return
    }

    setStatus("matching")
    setError("")

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

  function updateSearch(field, value) {
    setSearch(current => ({
      ...current,
      [field]: value,
    }))
  }

    return (
    <main className="app-shell">
      <section className="workspace-header">
        <div>
          <p className="eyebrow">CV Recommender</p>
          <h1>Find roles that fit your CV</h1>
        </div>

        <div className="summary-strip" aria-label="Match summary">
          <div>
            <span>{total}</span>
            <p>Matches</p>
          </div>
          <div>
            <span>{topScore}</span>
            <p>Top score</p>
          </div>
        </div>
      </section>

      <section className="workflow-grid">
        <aside className="control-panel" aria-label="Search controls">
          <form className="panel-section" onSubmit={handleUpload}>
            <div className="section-title">
              <FileText aria-hidden="true" />
              <h2>CV</h2>
            </div>

            <label className="file-drop">
              <input
                accept="application/pdf"
                type="file"
                onChange={(event) => {
                  const selected = event.target.files?.[0] || null
                  setFile(selected)
                  setCvData(null)
                  setMatches([])
                  setTotal(0)
                  setStatus("idle")
                  setError("")
                }}
              />
              <Upload aria-hidden="true" />
              <strong>{file?.name || "Select PDF"}</strong>
              <span>
                {file ? `${Math.max(1, Math.round(file.size / 1024))} KB` : "PDF only"}
              </span>
            </label>

            <Button className="wide-button" disabled={status === "uploading"} type="submit">
              {status === "uploading" ? (
                <Loader2 className="spin" aria-hidden="true" />
              ) : (
                <Upload aria-hidden="true" />
              )}
              {status === "uploading" ? "Uploading" : "Upload CV"}
            </Button>

            {cvData?.raw_text ? (
              <div className="cv-ready" role="status">
                <CheckCircle2 aria-hidden="true" />
                <span>{cvData.raw_text.length.toLocaleString()} characters parsed</span>
              </div>
            ) : null}
          </form>

          <form className="panel-section" onSubmit={handleSearch}>
            <div className="section-title">
              <Search aria-hidden="true" />
              <h2>Search</h2>
            </div>

            <label className="field">
              <span>Role</span>
              <input
                value={search.keywords}
                onChange={(event) => updateSearch("keywords", event.target.value)}
                placeholder="Data analyst"
              />
            </label>

            <label className="field">
              <span>Location</span>
              <input
                value={search.location}
                onChange={(event) => updateSearch("location", event.target.value)}
                placeholder="ie"
              />
            </label>

            <label className="field">
              <span>Number of Pages</span>
              <input
                type="number"
                min="1"
                max="20"
                value={search.num_pages}
                onChange={(event) => updateSearch("num_pages", event.target.value)}
              />
            </label>

            <Button
              className="wide-button search-button"
              disabled={!canSearch || status === "matching"}
              type="submit"
            >
              {status === "matching" ? (
                <Loader2 className="spin" aria-hidden="true" />
              ) : (
                <Sparkles aria-hidden="true" />
              )}
              {status === "matching" ? "Matching" : "Find Matches"}
            </Button>
          </form>

          {error ? (
            <div className="error-banner" role="alert">
              <XCircle aria-hidden="true" />
              <span>{error}</span>
            </div>
          ) : null}
        </aside>

        <section className="results-panel" aria-label="Matched jobs">
          <div className="results-heading">
            <div>
              <p className="eyebrow">Matched Jobs</p>
              <h2>{matches.length ? `${matches.length} roles ranked` : "Ready when you are"}</h2>
            </div>

            {status === "matching" ? (
              <Loader2 className="spin subtle-loader" aria-hidden="true" />
            ) : null}
          </div>

          {matches.length ? (
            <div className="job-list">
              {matches.map(({ job, score, matching_skills: matchingSkills, missing_skills: missingSkills }) => (
                <article className="job-card" key={job.job_id}>
                  <div className="job-main">
                    <div>
                      <div className="company-line">
                        <BriefcaseBusiness aria-hidden="true" />
                        <span>{job.company}</span>
                      </div>
                      <h3>{job.title}</h3>
                    </div>

                    <div className="score-pill" aria-label={`Match score ${scoreLabel(score)}`}>
                      {scoreLabel(score)}
                    </div>
                  </div>

                  <div className="job-meta">
                    <span>
                      <MapPin aria-hidden="true" />
                      {job.location}
                    </span>
                    <span>{formatSalary(job)}</span>
                  </div>

                  <p className="job-description">{job.description}</p>

                  <div className="skill-grid">
                    <div>
                      <span className="skill-label">Matched</span>
                      <div className="chips">
                        {matchingSkills.length ? (
                          matchingSkills.map((skill) => (
                            <span className="chip match" key={skill}>
                              {skill}
                            </span>
                          ))
                        ) : (
                          <span className="muted-text">None listed</span>
                        )}
                      </div>
                    </div>

                    <div>
                      <span className="skill-label">Gaps</span>
                      <div className="chips">
                        {missingSkills.slice(0, 5).map((skill) => (
                          <span className="chip gap" key={skill}>
                            {skill}
                          </span>
                        ))}
                        {!missingSkills.length ? (
                          <span className="muted-text">None detected</span>
                        ) : null}
                      </div>
                    </div>
                  </div>

                  <Button asChild className="job-link" variant="outline">
                    <a href={job.link} rel="noreferrer" target="_blank">
                      View role
                      <ArrowUpRight aria-hidden="true" />
                    </a>
                  </Button>
                </article>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <Search aria-hidden="true" />
              <h3>No matches yet</h3>
            </div>
          )}
        </section>
      </section>
    </main>
  )
}

export default App
