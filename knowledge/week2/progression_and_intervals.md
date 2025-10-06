---
source_id: "IEC-TS-61400-progress"
component_tags: ["blade"]
damage_tags: ["leading_edge_erosion","structural_crack"]
progression_model: true
maintenance_action: ["monitor","field_repair","factory_repair"]
environment: ["onshore","offshore"]
passage_id: "w2-progression:summary"
license: "see kb_licenses.md"
week_added: 2
---

### [w2-progression:interval_model]
Progression models calibrated on North Sea fleets show a median 0.35 probability that S2 erosion escalates to S3 within 90 days when left untreated, assuming average precipitation and no icing. The risk increases to 0.55 by 180 days absent mitigation.

### [w2-progression:maintenance_window]
Scheduling field repairs within 120 days of detection minimizes downtime because blade removal is usually avoidable. Beyond 180 days, factory repair or full replacement becomes more likely due to structural laminate exposure.

### [w2-progression:assumption_notes]
Probability curves assume weekly SCADA monitoring to flag power deviations ≥2%. Lack of monitoring increases uncertainty and should be reflected in wider maintenance windows.
