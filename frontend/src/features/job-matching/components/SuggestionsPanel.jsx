function SuggestionsPanel({ suggestions }) {
  if (!suggestions) {
    return null
  }

  return (
    <div className="suggestions-box">
      <div>
        <span className="skill-label">CV suggestions</span>
        <p>{suggestions.overall_match}</p>
      </div>

      <ul className="suggestion-list">
        {suggestions.suggestions.map((suggestion, index) => (
          <li key={`${suggestion.section}-${index}`}>
            <strong>{suggestion.section}</strong>
            <p>
              <span>Current:</span> {suggestion.current}
            </p>
            <p>
              <span>Suggested:</span> {suggestion.suggested}
            </p>
            <p>
              <span>Reason:</span> {suggestion.reason}
            </p>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default SuggestionsPanel
