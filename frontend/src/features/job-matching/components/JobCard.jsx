import { ArrowUpRight, BriefcaseBusiness, FilePenLine, MapPin } from "lucide-react"

import { Button } from "@/components/ui/button"
import { formatSalary, scoreLabel } from "../formatters"
import SuggestionsPanel from "./SuggestionsPanel"

function JobCard({
  jobMatch,
  onRequestSuggestions,
  suggestion,
  suggestionLoadingJobId,
}) {
  const {
    job,
    score,
    matching_skills: matchingSkills = [],
    missing_skills: missingSkills = [],
  } = jobMatch
  const isGenerating = suggestionLoadingJobId === job.job_id

  return (
    <article className="job-card">
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
            {!missingSkills.length ? <span className="muted-text">None detected</span> : null}
          </div>
        </div>
      </div>

      <div className="job-actions">
        <Button asChild className="job-link" variant="outline">
          <a href={job.link} rel="noreferrer" target="_blank">
            View role
            <ArrowUpRight aria-hidden="true" />
          </a>
        </Button>

        <Button
          className="job-link"
          disabled={isGenerating || Boolean(suggestion)}
          variant="outline"
          onClick={() => onRequestSuggestions(job)}
        >
          <FilePenLine aria-hidden="true" />
          {isGenerating ? "Generating" : suggestion ? "Suggestions ready" : "CV suggestions"}
        </Button>
      </div>

      <SuggestionsPanel suggestions={suggestion} />
    </article>
  )
}

export default JobCard
