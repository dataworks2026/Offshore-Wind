# Task: Curate Week 1 Authoritative Passages

## Objective
Create 3–5 authoritative knowledge passages that align with the Week 1 deliverables in `PROJECT_PLAN.md`. These passages must enable the Custom GPT to cite expert-backed guidance when producing initial damage assessments and maintenance forecasts.

## What Counts as an Authoritative Passage?
An authoritative passage is a short, self-contained markdown document grounded in a named expert source (standards body, utility consortium, peer-reviewed study, or OEM manual). Each passage must:
- Summarize prescriptive practices or empirical findings relevant to blade erosion, structural cracking, or maintenance intervals.
- Include YAML front-matter capturing `source_id`, tagging metadata, licensing note, and a unique `passage_id` anchor.
- Provide 2–3 clearly headed sections that the GPT can quote verbatim for rationale and forecasting logic.
- Reference procedures or thresholds that practitioners would rely on for compliance or safety decisions.

## Deliverables
- 3–5 new markdown files stored under `/knowledge/week1/` following the knowledge authoring conventions in the repo README.
- Updated `knowledge/kb_manifest.csv` entries for each passage so retrieval tools can locate them.
- Updated `kb_licenses.md` table documenting the source and allowable usage for every newly added document.

## Definition of Done
- [ ] All passages include correct metadata, unique `passage_id` anchors, and at least two substantive sections.
- [ ] Content aligns with reputable sources and covers erosion signatures, crack diagnostics, and maintenance planning expectations.
- [ ] Repository manifests (`kb_manifest.csv`, `kb_licenses.md`) reflect the new knowledge and pass linting/CI checks.
- [ ] Team reviewers can trace each passage back to a cited standard or consortium guidance.

## Additional Notes
- Prioritize sources that advisors or reliability engineers would trust (e.g., DNV, ISO, EPRI). Avoid speculative or marketing content.
- Use concise, factual sentences; avoid hypothetical language so the GPT can cite concrete recommendations.
- Link the task to the Week 1 sprint board once created and reference this document in the PR description when delivering the knowledge set.
