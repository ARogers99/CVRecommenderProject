function SummaryMetrics({ total, topScore }) {
  return (
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
  )
}

export default SummaryMetrics
