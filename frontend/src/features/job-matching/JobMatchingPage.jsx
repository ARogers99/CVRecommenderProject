import { XCircle } from "lucide-react"

import CvUploader from "./components/CvUploader"
import JobResults from "./components/JobResults"
import SearchForm from "./components/SearchForm"
import SummaryMetrics from "./components/SummaryMetrics"
import { useJobMatchingWorkflow } from "./hooks/useJobMatchingWorkflow"

function JobMatchingPage() {
  const workflow = useJobMatchingWorkflow()

  return (
    <main className="app-shell">
      <section className="workspace-header">
        <div className="header-copy">
          <p className="eyebrow">CV Recommender</p>
          <h1>Job Matches and CV Tips</h1>
        </div>

        <SummaryMetrics total={workflow.summary.total} topScore={workflow.summary.topScore} />
      </section>

      <section className="workflow-grid">
        <aside className="control-panel" aria-label="Search controls">
          <CvUploader
            cvData={workflow.cvData}
            file={workflow.file}
            status={workflow.status}
            onSelectCv={workflow.selectCv}
          />

          <SearchForm
            canSearch={workflow.canSearch}
            countries={workflow.countries}
            search={workflow.search}
            status={workflow.status}
            onSearch={workflow.searchJobs}
            onUpdateSearch={workflow.updateSearch}
          />

          {workflow.error ? (
            <div className="error-banner" role="alert">
              <XCircle aria-hidden="true" />
              <span>{workflow.error}</span>
            </div>
          ) : null}
        </aside>

        <JobResults
          matches={workflow.matches}
          status={workflow.status}
          suggestionLoadingJobId={workflow.suggestionLoadingJobId}
          suggestionsByJob={workflow.suggestionsByJob}
          onRequestSuggestions={workflow.requestSuggestions}
        />
      </section>
    </main>
  )
}

export default JobMatchingPage
