import { Search, Sparkles, Loader2 } from "lucide-react"

import { Button } from "@/components/ui/button"

function SearchForm({ canSearch, countries, onSearch, onUpdateSearch, search, status }) {
  return (
    <form className="panel-section" onSubmit={onSearch}>
      <div className="section-title">
        <Search aria-hidden="true" />
        <h2>Search</h2>
      </div>

      <label className="field">
        <span>Role and query</span>
        <input
          value={search.keywords}
          onChange={(event) => onUpdateSearch("keywords", event.target.value)}
          placeholder="Data analyst in London"
        />
      </label>

      <label className="field">
        <span>Country</span>
        <select value={search.location} onChange={(event) => onUpdateSearch("location", event.target.value)}>
          {countries.map((country) => (
            <option key={country.code} value={country.code}>
              {country.name}
            </option>
          ))}
        </select>
      </label>

      <label className="field">
        <span>Result pages</span>
        <input
          max="20"
          min="1"
          type="number"
          value={search.num_pages}
          onChange={(event) => onUpdateSearch("num_pages", event.target.value)}
        />
      </label>

      <Button className="wide-button search-button" disabled={!canSearch || status === "matching"} type="submit">
        {status === "matching" ? (
          <Loader2 className="spin" aria-hidden="true" />
        ) : (
          <Sparkles aria-hidden="true" />
        )}
        {status === "matching" ? "Matching" : "Find matches"}
      </Button>
    </form>
  )
}

export default SearchForm
