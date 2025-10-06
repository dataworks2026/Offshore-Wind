# Wind Turbine Damage Prediction Project Plan (Student Group)

## Overview

- **Duration:** 10 weeks
- **Method:** 1-week iterations (sprints), each delivering a working horizontal slice of functionality
- **Team:** Student group working collaboratively, reviewed weekly
- **Outcome:** A functioning **custom GPT (OpenAI)** that, given a turbine image + situation, (1) **assesses current damage**, and (2) **predicts future maintenance needs and future damage progression** on explicit time horizons, citing expert sources. No code execution—everything is driven by curated text instructions, examples, and knowledge.

### Success Criteria (end-of-project)

- The Custom GPT consistently outputs a **schema-valid JSON** that includes:
  - `current_assessment` (type, severity, action now)
  - **Forecasts**: risk of progression at **30/90/180/365 days** and expected maintenance window(s)
  - **Rationale** with **citations** to expert passages
  - **Calibration note** and uncertainty drivers (image quality, conflicting sources)
- Forecast quality demonstrated on a **held-out set of historical cases with known outcomes**, with metrics reported (e.g., time-to-intervention accuracy, Brier score for 90-day progression).

## Repository & Access Setup (Week 0 / Prep)

- **Private GitHub repo:** Create under organization (visibility: private). Enable branch protections (`main`), require PR review, enable CODEOWNERS.
- **Structure (initial folders):** `/instructions`, `/knowledge`, `/cases`, `/fewshots`, `/schema`, `/eval`, `/reports`, `/resources`.
- **Templates:** `README.md`, `CONTRIBUTING.md`, PR & issue templates, `CODEOWNERS`, `LICENSE` (repo license), `kb_licenses.md` (per‑doc usage), tagging rubric.
- **Access:** Add all students with write access via a team; advisors as admins. Create GitHub Project board (Kanban) with sprint columns.
- **Knowledge management workflow:** Each week, advisors commit new and revised knowledge directly into the `/knowledge` folder, tagged by week and component. The GPT will have access to these through GitHub integration and file references during setup.
- **OpenAI setup:** Create/confirm OpenAI org & project, Custom GPT **Sandbox** with students as editors. Document how to connect GPT’s Knowledge feature directly to `/knowledge` content from the GitHub repo.
- **Resource handoff channel:** One pinned issue “Sprint Resources (Week N)” created by advisors each week with links to new materials and acceptance tests.
- **Repo discipline:** All contributions must be via pull requests with at least one peer review, tracked against weekly sprint issues.

## Iteration Breakdown

### Week 1 — Kickoff & First Instruction Stub

- **Goal:** End-to-end stub that accepts an image + context and produces a placeholder JSON prediction **including a forecast section**.
- **We provide this week:**
  - Private GitHub repo access; repo scaffold from Week 0; PR/issue templates.
  - OpenAI Custom GPT **Sandbox** with editor access linked to repo knowledge.
  - `schema/output_schema.json` (initial) and `taxonomy.csv` (initial) drafts.
  - 3–5 authoritative passages (erosion, cracks, maintenance intervals) added to `/knowledge/week1/`.
  - 1 starter case (`cases/WT-001`) with image(s), `case.yaml`, and stubbed `ground_truth.json`.
- **Definition of Done:** The GPT can take in one case with an image + context and return JSON with both a current assessment and a forecast section (even if stubbed or generic) using materials from the GitHub repo.

### Week 2 — Corpus Ingestion & Knowledge Base Baseline (incl. progression/maintenance)

- **Goal:** Distill expert docs into chunks that cover **damage ID, progression rates, and maintenance decision criteria**.
- **We provide this week:**
  - ≥15 expert sources committed to `/knowledge/week2/` with license notes.
  - Tagging rubric (`resources/tagging_rubric.md`) and chunking guide.
  - Seed cases: add `WT-002..WT-003` with images + truths.
- **Definition of Done:** The GPT can answer a question like “what happens to blade leading edge erosion over time?” by citing from the ingested knowledge in `/knowledge/` and include that reasoning in its JSON outputs.

### Week 3 — Visual Cue & Case Context Templates (forecast-aware)

- **Goal:** Define cue and context templates that surface **forecast-relevant factors** (environment, loading, materials, prior maintenance).
- **We provide this week:**
  - `cue_templates.md` starter with examples of good cue phrasing.
  - Case templates (`case.yaml`, `ground_truth.json`) with time horizons.
  - 3 additional historical cases with known outcomes at 90/180/365 days.
  - New materials committed under `/knowledge/week3/` focusing on environmental accelerants (offshore/cold/sand).
- **Definition of Done:** The GPT can incorporate visual cues and environmental context into its reasoning, producing different forecasts depending on factors such as offshore vs. onshore conditions.

### Week 4 — Retrieval + Reasoning Prototype (now + future)

- **Goal:** Connect knowledge and GPT reasoning to produce **current assessment + time-bucket forecasts**.
- **We provide this week:**
  - `fewshots.jsonl` starter examples (present + 30/90/180/365 forecasts) with proper citations.
  - Knowledge additions in `/knowledge/week4/` (progression tables, maintenance intervals, repair durability excerpts).
  - 2 new cases (WT-007..WT-008) with outcomes.
- **Definition of Done:** The GPT can take a case with cues + context, retrieve relevant knowledge from the GitHub repo, and produce JSON outputs with present assessment and 30/90/180/365-day forecasts that cite knowledge passages.

### Week 5 — Validation & Guardrails (forecast consistency)

- **Goal:** Strengthen instructions so outputs are internally consistent across time horizons.
- **We provide this week:**
  - Validation checklist (`validation_guide.md`) and examples of contradictions to avoid.
  - Threshold rules (e.g., severity bands, action mapping) added to `/knowledge/week5/`.
  - 2 edge-case scenarios (ambiguous images, conflicting sources).
- **Definition of Done:** The GPT can generate outputs where probabilities are valid (0–1), consistent across horizons (risk at 180 days ≥ risk at 90 days unless justified), and where uncertainty is flagged with clear assumptions.

### Week 6 — Expanded Corpus & Forecast Ground Truth

- **Goal:** Scale knowledge and build a forecastable test set.
- **We provide this week:**
  - Expanded corpus in `/knowledge/week6/` with additional expert material on repair durability and inspection intervals.
  - Additional images for 8–10 cases in `/cases/`.
  - Evaluation rubric for severity/action agreement.
- **Definition of Done:** The GPT can process multiple cases from the GitHub repo, consistently returning schema-valid outputs with both present and forecast sections that align with known historical outcomes.

### Week 7 — Evaluation (forecast metrics)

- **Goal:** Establish evaluation focused on forecasting quality.
- **We provide this week:**
  - `evaluation_guide.md` with metric formulas and scoring sheets.
  - Examples in `/knowledge/week7/` for evaluation context.
- **Definition of Done:** The GPT can generate predictions that can be scored using accuracy for present assessments and calibration/forecast metrics (e.g., Brier score) for forecasts, drawing all reasoning from the GitHub-stored knowledge.

### Week 8 — Iteration & Robustness (forecast stress tests)

- **Goal:** Improve forecast robustness via instruction tuning and example curation.
- **We provide this week:**
  - `robustness_tests.md` scenarios (poor QC, deferred maintenance, extreme environments) and additional expert commentary in `/knowledge/week8/`.
- **Definition of Done:** The GPT can handle stress-test inputs and still produce plausible, schema-valid forecasts with citations, or clearly state limitations, using only materials available in the repo.

### Week 9 — Polish & Presentation Prep (future-focused readouts)

- **Goal:** Produce clear outputs that decision-makers can act on.
- **We provide this week:**
  - `readout.md` template and reviewer bundle structure.
  - Final reference passages committed to `/knowledge/week9/`.
- **Definition of Done:** The GPT can output both JSON and natural-language summaries highlighting current state, forecast risks, and recommended maintenance windows, based entirely on the repo’s content.

### Week 10 — Final Demo & Handoff

- **Goal:** Deliver final custom GPT configuration and evidence of **forecasting** capability.
- **We provide this week:**
  - Final acceptance criteria; demo script; 5 unseen cases.
  - `final_report_template.md` with required sections: Methods, Results (present + forecast), Lessons Learned, Recommendations.
- **Definition of Done:** The GPT can successfully process unseen cases end-to-end using only the GitHub repo’s materials, returning schema-valid JSON with present assessment, forecast risks, and recommended maintenance windows, all supported by citations. The GPT’s outputs are consistent with historical truths and usable for decision-making.

## Weekly Review Structure

- **Who:** Student team + project advisor(s).
- **What:** Demo of the week’s slice, with explicit attention to the **forecast section**: Are risks and maintenance windows well-cited and plausible?
- **When:** End of each week.
- **Output:** Updated project log + acceptance of iteration goal + list of knowledge gaps to close for better forecasting.

---

This plan now assumes the entire team has access to the private GitHub repo, removing the need for zipped weekly knowledge packs. All knowledge, resources, and references live directly in the shared repository for use by the GPT and the team.

