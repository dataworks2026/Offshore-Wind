# Wind Turbine Damage Prediction (Custom GPT)

## Project Overview
This repository contains the working materials for a custom GPT that helps wind turbine advisors and maintenance planners. The
assistant is expected to reason over inspection cues, weigh competing damage hypotheses, and forecast escalation risk at
30/90/180/365-day horizons while staying inside the JSON contract in `schema/output_schema.json`. Everything the model needs to
reason—cases, source documents, schemas, and reporting templates—lives in this repository so contributors can iterate without
additional tooling.

## Repository Structure
- `PROJECT_PLAN.md` – Ten-week roadmap that explains how instructions, knowledge, and evaluation assets should mature over time.
- `cases/` – Training and evaluation scenarios (WT-001..WT-007). Each folder includes `case.yaml`, cue metadata under `images/`,
  and, where available, `ground_truth.json` and a local `readme.md` explaining why the case matters.
- `docs/` – Source PDFs used to author knowledge passages (erosion studies, maintenance guides, and standards). These feed the
  chunking and tagging workflows described under `resources/`.
- `eval/` – Evaluation guidance, run logs, and placeholder folders (`confusion_matrices/`, `plots/`) for storing scoring
  artefacts when the GPT is benchmarked.
- `instructions/` – The system prompt (`system_instructions.txt`) and prompt assembly skeleton (`prompt_template.txt`) that must
  be copied into the Custom GPT configuration.
- `main/kb_licenses.md` & `kb_licenses.md` – Ledger of licensing terms for every knowledge source so downstream sharing stays
  compliant.
- `reports/` – Markdown templates (`readout_template.md`, `final_report_template.md`) used to turn structured outputs into
  executive summaries.
- `resources/` – Authoring references, including `case_authoring_guide.md`, `chunking_guide.md`, and `tagging_rubric.md` for
  producing consistent knowledge passages.
- `schema/` – The enforced JSON contract (`output_schema.json`), supplemental image description schema, and controlled
  vocabulary (`taxonomy.csv`).
- `LICENSE` – Repository-wide license governing derivative work.

## Configuring the Custom GPT
1. **Load system behaviour** by pasting `instructions/system_instructions.txt` into the Custom GPT’s system prompt slot. This
   enforces the forecasting horizons, probability rules, and citation expectations.
2. **Assemble prompts** using `instructions/prompt_template.txt`. Inline the relevant `cases/WT-*/case.yaml` contents, cue
   descriptors from the case folder, and the knowledge passages you have chunked. (Knowledge passages should ultimately live in
   a dedicated `knowledge/` directory; the `docs/` folder and `resources/` guides show what still needs to be converted.)
3. **Embed the schema** by copying the full contents of `schema/output_schema.json` into the GPT configuration. The model must
   emit responses that validate against this schema before generating a narrative readout using `reports/readout_template.md`.
4. **Track citations and licensing** whenever new passages are added. Update `kb_licenses.md` (and the summary in
   `main/kb_licenses.md`) so every `passage_id` referenced in a case or knowledge chunk ties back to a documented source.

## Authoring New Material
- **Cases:** Follow `resources/case_authoring_guide.md` and the existing WT-series folders. Each case should provide drone/inspection
  context, cue descriptions, `passage_id` references, and, when available, a `ground_truth.json` for evaluation.
- **Knowledge Passages:** Use the PDFs in `docs/` as raw material, the workflow in `resources/chunking_guide.md`, and the
  controlled vocabulary in `resources/tagging_rubric.md`. Store finished passages (with metadata and `passage_id`s) in a future
  `knowledge/` directory so they can be retrieved during prompting.
- **Licenses:** Log every new source in `kb_licenses.md` before committing passages or cases that rely on it.

## Evaluation & Reporting
- Use `eval/evaluation_guide.md` to define metrics (present assessment accuracy, forecast calibration). Record experimental
  results in `eval/evaluation_log.md`, saving artefacts such as confusion matrices or calibration plots in the dedicated
  subfolders.
- After each GPT run, request a narrative readout that mirrors `reports/readout_template.md` so humans receive an actionable
  summary alongside the schema-valid JSON.

## Working Practices
- Consult `PROJECT_PLAN.md` for the staged milestones the student team is expected to hit each week.
- Keep all changes in feature branches and document knowledge-source rights in the license ledgers before sharing outputs.
- When the knowledge base directory is created, ensure the Custom GPT references only repository-hosted passages to keep
  reasoning reproducible.
