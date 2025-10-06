# WT-001 Cold-Weather Blade Damage Walkthrough

## Summary
- **Case ID:** WT-001
- **Primary Focus:** Leading-edge erosion with a trailing-edge crack interaction on a V126 blade.
- **Learning Objective:** Practice balancing erosion progression models against structural crack uncertainty when imagery coverage is limited.

## Why This Case Is Instructional
1. **Multi-cue synthesis:** Analysts must reconcile erosion streaking with a discrete crack cue, prioritising field repair while reserving NDT time.
2. **Progression modelling:** Freeze–thaw acceleration requires explicit use of the interval model priors to justify a 90-day maintenance window.
3. **Risk communication:** Forecasters translate probability curves into staged work orders that coordinate drone follow-up and repair crew mobilisation.

## Inspection Context
- **Inspection Date:** 2025-01-15  
- **Method:** Drone survey at ~12 m standoff with three passes.  
- **Site Conditions:** Onshore, cold-weather regime with freeze–thaw cycles but no active icing during the sortie.  
- **Key Visual Cues:**
  1. Longitudinal crack (~0.8 m) near the trailing edge with exposed fibres.
  2. Leading-edge erosion concentrated between 30–40% span with matte streaking and minor fibre exposure.
  3. Clean surfaces elsewhere; no icing overlay at the time of inspection.

## Knowledge References
| Passage ID | Knowledge File | Why It Matters |
|------------|----------------|----------------|
| `w1-erosion:baseline` | `knowledge/week1/blade_erosion_basics.md` | Defines expected span bands and surface appearance for S1–S2 erosion, anchoring the primary hypothesis. |
| `w2-progression:interval_model` | `knowledge/week2/progression_and_intervals.md` | Supplies the 90–180 day escalation probabilities used in the forecast curve. |
| `w3-environment:freeze_thaw` | `knowledge/week3/environmental_modifiers.md` | Quantifies freeze–thaw multipliers that justify tightening the maintenance window. |

## Key Decision Points
1. **Primary Hypothesis Selection:** Leading-edge erosion is favoured (0.70) because the cue aligns with baseline patterns and exposes fibres in the expected span band. The crack is tracked as a secondary hypothesis (0.20) pending NDT confirmation.
2. **Maintenance Timing:** With a 0.48 risk of escalation by 90 days, planners commit to a field repair crew within the quarter while booking NDT resources as a contingency.
3. **Monitoring Plan:** Even though icing is not present, SCADA monitoring continues to capture any overlay risk (0.10) that would amplify laminate exposure in future freeze events.

## Forecast Snapshot
| Horizon | Escalation Risk | Expected Severity | Recommended Posture |
|---------|-----------------|-------------------|---------------------|
| 30 days | 0.32 | S2 | Execute field repair work order. |
| 90 days | 0.48 | S2–S3 | Hold contingency slot for deeper repair if slippage occurs. |
| 180 days | 0.63 | S3 | Escalate to factory repair if repair is missed. |
| 365 days | 0.80 | S3–S4 | Budget for replacement if deferred across winter. |

- **Maintenance Window Guidance:** Complete field repairs within 90 days to prevent freeze–thaw amplified laminate exposure.
- **Forecast Assumptions:** Access windows remain typical for the site, and drone follow-up confirms the crack has not propagated beyond the photographed zone.

## Caveats and Follow-up Actions
- Imagery angles are limited; trailing-edge delamination depth remains uncertain until NDT is performed.
- No SCADA anomaly data accompanied the inspection, so power curve impacts are inferred rather than measured.
- Schedule a follow-up drone run after field repairs to validate coating restoration and confirm crack arrest.

## Imagery Handling
Placeholder imagery paths (`./images/wt001_1.jpg`, `./images/wt001_2.jpg`) represent redacted inspection stills. Replace with approved media once privacy and licensing reviews are complete.
