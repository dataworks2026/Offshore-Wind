# Contributing Guide

Thank you for supporting the Wind Turbine Damage Prediction Custom GPT. This repository is text-only; all contributions should improve the instructions, knowledge, schemas, or evaluation assets that power the model.

## Workflow Overview
1. **Create an issue** referencing the relevant sprint (e.g., "Sprint Resources (Week N)") or open a new discussion outlining your proposal.
2. **Branch naming**: use `feature/<slug>`, `docs/<slug>`, or `fix/<slug>` depending on the change.
3. **Make your changes** following directory-specific instructions and update `kb_licenses.md` or manifests when adding new sources.
4. **Commit style**: use conventional commit prefixes (e.g., `docs:`, `chore:`, `feat:`) and keep messages imperative.
5. **Open a pull request** using the template in `.github/PULL_REQUEST_TEMPLATE.md`. Tag reviewers and link the governing issue.
6. **Reviews**: at least one CODEOWNER must approve. Address feedback promptly and document decisions in the PR conversation.
7. **Merge** once all checklist items are completed and status checks (if any) pass.

## Tagging Conventions
- Apply GitHub labels for sprint week (e.g., `week-03`), change type (`knowledge`, `schema`, `instructions`), and urgency.
- Mention subject-matter advisors via `@` to ensure timely review.

## Knowledge Contributions
- Follow `resources/tagging_rubric.md` for metadata and tagging requirements.
- Update `kb_licenses.md` and `knowledge/kb_manifest.csv` with new entries.
- Ensure passages include unique `passage_id` anchors and cite reputable sources.

## Case Contributions
- Use `cases/CASE_TEMPLATE.md` as the blueprint.
- Provide realistic cues, imagery references (if permitted), and future outcome projections with clear assumptions.

## Schema or Instruction Changes
- Highlight breaking changes in the PR description.
- Coordinate with evaluation owners to update validation scripts and few-shot examples.

## Communication
- Use weekly sprint issues for coordination.
- Document decisions and rationale directly in PRs to maintain traceability for the Custom GPT.
