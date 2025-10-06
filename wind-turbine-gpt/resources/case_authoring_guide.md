# Case Authoring Guide

## Steps
1. Duplicate `cases/CASE_TEMPLATE.md` instructions for a new case folder.
2. Populate `case.yaml` with inspection metadata, cues, and imagery references.
3. Draft `ground_truth.json` including future outcomes at 90/180/365 days with severity and action expectations.
4. Write `readme.md` summarizing instructional goals and notable complexities.

## Cue Bullets
- Capture observable evidence (crack length, erosion span, icing presence).
- Include sensor or SCADA anomalies when relevant.
- Note environmental conditions that influence progression.

## Ground Truth Construction
- Align severity scale with schema (`S0`–`S4`).
- Provide future outcome projections consistent with knowledge passages.
- Reference verification sources (e.g., technician reports).

## Quality Checklist
- Ensure `passage_id`s cited in prompts exist in `knowledge/`.
- Confirm imagery references respect privacy and licensing.
- Update `kb_licenses.md` if new documents were used to create the case.
