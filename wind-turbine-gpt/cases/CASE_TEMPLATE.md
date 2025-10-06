# Case Authoring Template

1. Create a folder under `cases/` named after the case ID (e.g., `WT-002`).
2. Add the following files:
   - `case.yaml`: Structured case metadata matching the schema used in `cases/WT-001/case.yaml`.
   - `ground_truth.json`: Expected outcomes including progression forecasts.
   - `readme.md`: Explain why the case is instructional, key decision points, and any caveats.
   - `images/`: Optional folder with placeholder paths or redacted imagery (respect privacy and licenses).
3. Update `knowledge/kb_manifest.csv` if new passages are referenced.
4. Document any source licenses or proprietary notes in `kb_licenses.md`.
5. If the case is used in few-shots, ensure the `fewshots/fewshots.jsonl` file references the correct `passage_id`s.
