# Knowledge Tagging Rubric

## Purpose
- Provide consistent metadata so retrieval can target present damage assessments and future progression insights.
- Ensure every passage can be traced to turbine subsystems, failure modes, and maintenance decisions.

## Required Metadata Fields
| Field | Description | Allowed Values / Format | Quality Criteria |
|-------|-------------|-------------------------|------------------|
| `passage_id` | Stable identifier linking back to the source | `docID:section:paragraph` (e.g., `LE-2019:3:2`) | Must be unique across the repository and reproducible from the original source structure. |
| `component_tags` | Components or subassemblies affected | List from `schema/taxonomy.csv` (e.g., `blade`, `nacelle`, `gearbox`) | Include the most specific applicable level; multiple tags allowed. |
| `damage_tags` | Failure mode or condition type | Use controlled vocabulary in `schema/taxonomy.csv` | Avoid synonyms; request taxonomy updates if a concept is missing. |
| `progression_model` | Indicates whether the passage contains explicit progression dynamics | Boolean (`true`/`false`) | Mark `true` when timelines, rates, or probabilistic forecasts are stated or derivable. |
| `maintenance_action` | Ranked list of recommended interventions | Controlled verbs (e.g., `perform_blade_repair`, `increase_inspection_frequency`) | Place immediate actions first; use `none` only when the passage explicitly states no action required. |
| `environment` | Contextual factors influencing progression | Controlled descriptors (e.g., `offshore`, `cold_weather`, `high_salt_spray`) | Include all relevant environments; omit `unknown` unless no context is provided. |
| `source_citation` | Link to reference entry in `kb_licenses.md` | `ref_id` defined in license file | Ensures licensing compliance and traceability. |

## Optional Metadata
- `confidence`: Analyst rating (`low`, `medium`, `high`) when synthesizing multiple passages.
- `notes`: Brief clarifications or assumptions not present verbatim in the source (use sparingly and bracket clarifications).

## Tagging Workflow
1. Draft the chunk following `resources/chunking_guide.md`.
2. Populate required fields using the controlled vocabularies.
3. Validate against the checklist below before committing.

## Quality Levels
| Level | Indicators |
|-------|------------|
| **Exceeds** | Metadata complete, progression timelines quantified, maintenance actions prioritized, environmental tags precise. |
| **Meets** | All required fields present, values align with controlled vocabularies, passage supports present and/or future assessments. |
| **Revise** | Missing required fields, vague tags (e.g., `damage`), inconsistent identifiers, or mismatch with passage content. |

## Reviewer Checklist
- [ ] `passage_id` is unique and reproducible from the source outline.
- [ ] Component and damage tags match the taxonomy definitions.
- [ ] `progression_model` accurately reflects whether the chunk supports forecasting.
- [ ] Maintenance actions are actionable verbs with correct priority ordering.
- [ ] Environment tags capture all site or operating conditions discussed.
- [ ] Source citation aligns with an entry in `kb_licenses.md`.

## Examples
### High-Quality Tag Set
```
passage_id: LE-2019:3:2
component_tags: [blade, leading_edge]
damage_tags: [erosion, coating_loss]
progression_model: true
maintenance_action: [schedule_blade_resurfacing, increase_inspection_frequency]
environment: [offshore, high_salt_spray]
source_citation: ref_le_2019
```
- **Why it works:** Specific component/damage pairing, quantifies progression, includes prioritized actions, references license entry.

### Needs Revision
```
passage_id: erosion1
component_tags: [blade]
damage_tags: [damage]
progression_model: false
maintenance_action: []
environment: []
source_citation: ref_unknown
```
- **Issues:** Non-unique ID, vague damage tag, empty maintenance/environment fields despite context, missing valid citation.
