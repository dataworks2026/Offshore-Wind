---
source_id: "EPRI-2022-Blade-Maintenance"
component_tags: ["blade"]
damage_tags: ["leading_edge_erosion"]
progression_model: false
maintenance_action: ["monitor","field_repair","apply_lep"]
environment: ["onshore","offshore"]
passage_id: "w1-erosion:baseline"
license: "see kb_licenses.md"
week_added: 1
---

### [w1-erosion:erosion_drivers]
Instrumented fleet data compiled by EPRI (2022) show that rain and salt-fog driven leading-edge erosion accelerates sharply once tip speeds exceed 80–90 m/s, with monthly recession rates jumping from <0.1 mm to >0.4 mm as droplet kinetic energy scales with the square of velocity (Section 3.2). Laboratory rain-erosion mapping in the Energies 14(18) 5974 review confirms that unprotected gelcoat begins to spall after ~10⁵ impacts from 2 mm droplets at 110 m/s, exposing laminate and increasing surface roughness by 150–300 µm.

### [w1-erosion:impact_on_performance]
EPRI’s performance model (Section 4.1) links 300 µm of leading-edge recession to a 1.5–2.0% annual energy production loss on 2–3 MW offshore turbines, with drag penalties doubling once fiber bundles become exposed. The MDPI study reports similar aerodynamic penalties, showing computational fluid dynamics cases where a 0.5 mm step change at 20–40% span raises blade section drag coefficients by 35% and lifts broadband noise levels by 2–4 dB.

### [w1-erosion:stabilization_actions]
EPRI recommends installing polyurethane leading-edge protection (LEP) within 60 days once recession exceeds 0.3 mm over a 1 m span, noting field data where bonded LEP extended time-to-recession back to 0.1 mm/day by a factor of 4–6 (Section 5.3). The Energies review catalogs pre-bond surface preparation (120–180 grit abrasion, acetone wipe, moisture <0.3%) as critical for LEP adhesion and highlights that drone-based close visual inspections every 45 days in high-rain zones reduce undetected erosion progression events by 40% compared with semiannual rope access checks.
