---
source_id: "EPRI-2019-BLADE-CRACKS"
component_tags: ["blade"]
damage_tags: ["structural_crack"]
progression_model: true
maintenance_action: ["field_repair","factory_repair"]
environment: ["onshore","offshore"]
passage_id: "w1-crack:inspection"
license: "see kb_licenses.md"
week_added: 1
---

### [w1-crack:inspection]
Utility inspections flag structural cracks when ultrasonic phased-array scans detect delamination exceeding 25 mm in depth or 150 mm in length along the spar cap interface. Certified inspectors correlate scan anomalies with visible chordwise fissures near the root 5–15% span, often accompanied by resin-rich whitening.

### [w1-crack:progression]
If untreated, spar cap cracks migrate toward load-bearing webs at a rate of roughly 10 mm per 1000 operating hours under Class II wind regimes. Supervisory control data typically records concurrent vibration increases of 0.2–0.4 ips in the 1P band as stiffness diminishes.

### [w1-crack:actions]
EPRI guidance requires immediate load derating once ultrasonic confirmation is obtained and mandates composite scarf repairs or factory segment replacement when crack depth exceeds 30% of laminate thickness. Post-repair proof load testing ensures flexural stiffness recovery within 5% of baseline.
