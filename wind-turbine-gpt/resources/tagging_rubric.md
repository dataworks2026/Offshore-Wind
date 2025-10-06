# Knowledge Tagging Rubric

## Required Metadata
- **component_tags**: Identify affected turbine components (e.g., blade, tower, nacelle).
- **damage_tags**: Use controlled vocabulary (see `schema/taxonomy.csv`).
- **progression_model**: `true` if the passage contains predictive relationships; otherwise `false`.
- **maintenance_action**: List recommended actions in priority order.
- **environment**: Capture contextual factors such as onshore/offshore, cold_weather, arid.
- **passage_id**: Unique identifier formatted as `docID:section:paragraph`. Must be unique across the repository.

## Best Practices
- Keep passages concise (2–4 sentences) focused on a single concept.
- Include quantitative details when available to support risk forecasting.
- Reference original source IDs and maintain links in `kb_licenses.md`.

## Examples
- **Good**: Provides clear condition thresholds, includes numeric probabilities, cites environment context.
- **Weak**: Vague descriptions without actionable thresholds or missing metadata fields.
