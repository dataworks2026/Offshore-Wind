# Wind Turbine Damage Prediction (Custom GPT)

## Project Overview
This repository scaffolds a Custom GPT designed to assist wind turbine advisors and maintenance planners. The final objective is to enable the model to: (1) analyze inspection imagery and cues to assess present blade and balance-of-plant damage, and (2) forecast future maintenance needs with risk estimates at 30/90/180/365-day horizons while citing authoritative sources captured in this repo.

## Repo at a Glance
```
.
├── .github/                 # Issue and pull request templates for governance
├── cases/                   # Curated inspection cases with cues and ground truth
├── eval/                    # Evaluation guides, logs, and placeholders for results
├── fewshots/                # JSONL few-shot examples for conditioning the GPT
├── instructions/            # System instructions and prompt scaffolding
├── knowledge/               # Weekly knowledge drops with tagged passages
├── reports/                 # Output templates for narrative readouts and final reports
├── resources/               # Rubrics and guides for authoring knowledge and cases
├── schema/                  # JSON schema and taxonomy for GPT outputs
├── week1..week10/           # Sprint workspaces for each week (notes, TODOs)
├── WT-001/                  # Additional workspace for turbine-specific planning
└── PROJECT_PLAN.md          # Project roadmap (replace placeholder when available)
```

## How to Use This Repo with a Custom GPT
1. **Load instructions**: Provide `instructions/system_instructions.txt` to define the GPT's role and operating rules. Use `instructions/prompt_template.txt` to assemble prompt packets that include case cues and retrieved knowledge.
2. **Attach knowledge**: Populate the GPT's knowledge base with markdown passages under `knowledge/week*/`. Ensure each passage retains its YAML front-matter and `passage_id` anchors so the GPT can cite correctly.
3. **Include schema**: Embed the full JSON schema from `schema/output_schema.json` in the GPT configuration. The GPT must emit responses that validate against this schema.
4. **Case setup**: When running an evaluation, inline the relevant `cases/<CASE_ID>/case.yaml` data, any cue bullets, and associated knowledge passages. Follow the prompt template instructions to construct the final prompt.
5. **Readout**: After the GPT outputs JSON, request a narrative report aligned to `reports/readout_template.md` so humans receive a concise summary.

## Weekly Workflow
- **Advisors** open a `.github/ISSUE_TEMPLATE/sprint_resource_issue.md` titled "Sprint Resources (Week N)" to define weekly knowledge additions, cases, and acceptance criteria.
- **Knowledge updates** are stored under `knowledge/weekN/` with new markdown passages. Update `kb_licenses.md` and `knowledge/kb_manifest.csv` accordingly.
- **Students and contributors** work from feature branches, submit PRs referencing the sprint issue, and request reviews per `CONTRIBUTING.md`.

## Authoring Knowledge
- Review `resources/tagging_rubric.md` for tagging conventions (components, damage types, progression flags, maintenance actions, environments).
- Each knowledge file begins with YAML front-matter capturing metadata (source, tags, week added). Follow `passage_id` conventions (unique repo-wide identifiers) and anchor headings, e.g., `### [doc123:sec4:para2]`.
- Record licensing details for each new source in `kb_licenses.md` so downstream users can respect usage rights.

## Authoring Cases
- Follow the guidance in `resources/case_authoring_guide.md` and `cases/CASE_TEMPLATE.md` to create new case folders.
- Minimum case contents: `case.yaml`, optional imagery references, cue bullets, `ground_truth.json`, and a `readme.md` explaining the instructional value.

## Few-Shot Examples
- Curate high-quality demonstrations in `fewshots/fewshots.jsonl`. Examples should show schema-compliant JSON paired with narrative readouts, balanced probabilities (summing to 1), and clearly cited passages.

## Output Contract
- The GPT must emit responses that validate against `schema/output_schema.json`. After the JSON, it should produce a narrative summary matching `reports/readout_template.md`.

## Evaluation
- Use `eval/evaluation_guide.md` for metrics definitions (present assessment accuracy, forecast calibration) and `eval/evaluation_log.md` to track runs.

## Versioning & Governance
- All changes require a pull request reviewed by CODEOWNERS (see `CODEOWNERS`).
- Follow the workflows in `CONTRIBUTING.md` (branch naming, tagging, commit style).
- Document licenses for knowledge sources in `kb_licenses.md` to maintain compliance.

## Limitations & Ethics
- Outputs are advisory; human experts remain accountable for maintenance decisions.
- Always articulate uncertainty, assumptions, and data gaps in accordance with system instructions.
- Protect the privacy of any inspection imagery and respect all external content licenses.

