# Knowledge Chunking Guide

## Purpose
- Create consistent, high-signal passages the Custom GPT can retrieve for both present damage assessment and multi-horizon forecasting.
- Preserve traceability back to the source document while emphasizing progression rates, maintenance triggers, and environmental modifiers.

## Workflow Overview
1. **Source Review**
   - Read the full document section to understand scope and quantitative details.
   - Highlight statements that describe damage mechanisms, progression timelines, maintenance thresholds, or environmental accelerants.
2. **Define Chunk Boundaries**
   - Group 2–5 sentences that explain a single actionable concept.
   - Keep chunks under 1,000 characters to stay within embedding limits while retaining context.
   - Split when the topic shifts (e.g., from inspection findings to repair methods) or when multiple environments are discussed.
3. **Summarize & Clarify**
   - Preserve numerical values, units, and time horizons exactly as written.
   - Add clarifying context if the original text is ambiguous, but mark additions with brackets `[clarified text]`.
4. **Assign Metadata**
   - Apply tags defined in `resources/tagging_rubric.md` immediately after drafting the chunk.
   - Ensure `passage_id` ties back to the original source (e.g., `LE-2019:3:2`).
5. **Quality Check**
   - Confirm the passage stands alone without needing the surrounding paragraph.
   - Verify citations in `kb_licenses.md` cover the source document.

## Chunk Types
- **Condition & Detection**: Inspection findings, defect descriptions, sensor triggers.
- **Progression Models**: Probabilities, rates of change, expected timelines (required for forecasting logic).
- **Maintenance Actions**: Repair strategies, intervention timing, resource requirements.
- **Environmental Modifiers**: Climate, operational load, or site conditions that alter progression.

## Formatting Standards
- Use Markdown with full sentences; avoid bullet lists unless the source is a list of procedures.
- Prefix the file with front matter if required by downstream tooling (e.g., YAML metadata blocks).
- Include the source citation immediately below the passage when applicable.

## Example Chunk
```
passage_id: LE-2019:3:2
component_tags: [blade, leading_edge]
damage_tags: [erosion, coating_loss]
progression_model: true
maintenance_action: [schedule_blade_resurfacing, increase_inspection_frequency]
environment: [offshore, high_salt_spray]
---
Laboratory wear tests show that leading edge erosion advances 15–20 mm per 1,000 operating hours under offshore salt-spray conditions. Progression accelerates by 30% when tip speeds exceed 70 m/s, leading to chord-wise delamination within 180 days if untreated. Preventive resurfacing before the second inspection cycle reduces progression risk by half.
```

## Common Pitfalls & Fixes
- **Overly broad chunks** → Split by topic and ensure each chunk answers a single retrieval question.
- **Missing time horizon** → Revisit the source for specific durations or note that the passage lacks progression data.
- **Uncontrolled vocabulary** → Cross-check `schema/taxonomy.csv` and update tags to match accepted terms.
- **Unverifiable claims** → Do not include statements that lack a cited source; flag them for advisor review instead.

## Review Checklist
- [ ] Chunk length ≤ 5 sentences and < 1,000 characters.
- [ ] Includes at least one progression or maintenance detail when available.
- [ ] Metadata matches the tagging rubric and uses controlled vocabulary.
- [ ] Citation recorded in `kb_licenses.md`.
- [ ] Ready for ingestion into retrieval pipelines (clear, self-contained, actionable).
