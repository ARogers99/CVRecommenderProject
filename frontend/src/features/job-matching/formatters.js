export function formatSalary(job) {
  return job.salary || "Salary not listed"
}

export function scoreLabel(score = 0) {
  return `${Math.round(score * 100)}%`
}
