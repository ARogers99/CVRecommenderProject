# Job Matching Feature

This feature keeps the CV upload, job search, job cards, and CV suggestions isolated from the app shell.

- `hooks/useJobMatchingWorkflow.js` owns data fetching and local workflow state.
- `components/` contains presentational pieces with narrow props.
- `constants.js` and `formatters.js` keep shared feature utilities out of render code.

The structure follows the project direction of feature-owned code, low colocated state, reusable components, and API logic outside the presentation layer.
