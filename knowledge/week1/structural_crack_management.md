---
source_id: "DNVGL-ST-0376:2015"
component_tags: ["blade"]
damage_tags: ["structural_crack"]
progression_model: false
maintenance_action: ["derate","field_repair","factory_repair"]
environment: ["onshore","offshore"]
passage_id: "w1-crack:inspection"
license: "see kb_licenses.md"
week_added: 1
---

### [w1-crack:detection_thresholds]
DNVGL-ST-0376 Section 13.5 requires that any visible crack at the spar cap or trailing-edge bondline be evaluated with ultrasonic testing when length exceeds 50 mm or depth appears greater than 2 mm; acceptance criteria limit allowable subsurface cracks to <10% of laminate thickness before immediate corrective action. The BSEE TAP-627AA field survey recorded that cracks propagating through 25–30% of spar cap thickness under cyclic bending grew by ~3 mm per 10⁶ cycles, underscoring the need to capture them before laminate penetration.

### [w1-crack:operational_response]
DNV mandates immediate turbine derating to ≤60% rated power once ultrasonic confirmation shows cracks deeper than 10% thickness in primary load paths, and shutdown when exceeding 20%, to avoid unstable delamination (Section 16.6). The BSEE guidance aligns, recommending rotor lock-out if crack growth rate surpasses 1 mm/week after temporary arrest drilling fails to stabilize the flaw.

### [w1-crack:repair_and_monitoring]
The 2017 “Damage Mitigation Techniques in Wind Turbine Blades” review highlights scarf repairs with ≥20:1 taper ratios and vacuum-assisted curing as the most reliable field solution for structural cracks, restoring ≥95% bending stiffness when coupled with post-repair ultrasonic verification. The same review notes that embedding fiber Bragg grating sensors across repaired joints reduced crack recurrence by 30% compared with visual-only monitoring, while BSEE TAP-627AA recommends follow-up UT at 1, 3, and 6 months to confirm no new delamination growth along adhesive bonds.
