import { Loader2, Search } from "lucide-react"

import JobCard from "./JobCard"

function JobResults({
  matches,
  onRequestSuggestions,
  status,
  suggestionLoadingJobId,
  suggestionsByJob,
}) {
  return (
    <section className="results-panel" aria-label="Matched jobs">
      <div className="results-heading">
        <div>
          <p className="eyebrow">Matched Jobs</p>
          <h2>{matches.length ? `${matches.length} roles ranked` : "Ready to rank roles"}</h2>
        </div>

        {status === "matching" ? <Loader2 className="spin subtle-loader" aria-hidden="true" /> : null}
      </div>

      {matches.length ? (
        <div className="job-list">
          {matches.map((jobMatch) => (
            <JobCard
              jobMatch={jobMatch}
              key={jobMatch.job.job_id}
              suggestion={suggestionsByJob[jobMatch.job.job_id]}
              suggestionLoadingJobId={suggestionLoadingJobId}
              onRequestSuggestions={onRequestSuggestions}
            />
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <Search aria-hidden="true" />
          <h3>No matches yet</h3>
        </div>
      )}
    </section>
  )
}

export default JobResults
