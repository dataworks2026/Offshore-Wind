---
source_id: "SHM-Guide-2022"
component_tags: ["blade","hub"]
damage_tags: ["structural_crack"]
progression_model: true
maintenance_action: ["monitor","ndt","factory_repair"]
environment: ["offshore","onshore"]
passage_id: "w4-shm:summary"
license: "see kb_licenses.md"
week_added: 4
---

### [w4-shm:sensor_array]
Fiber Bragg grating sensors positioned near the blade root detect strain anomalies associated with crack initiation. Deviations greater than 150 microstrain from baseline trigger follow-up NDT within 14 days.

### [w4-shm:scada_correlation]
Coupling SHM data with SCADA power curves improves detection sensitivity by 30%. When both systems flag anomalies, the posterior probability of a true S2 crack exceeds 0.6.

### [w4-shm:maintenance_triage]
If SHM alerts persist for more than two consecutive rotations, schedule a borescope inspection within the next maintenance window to confirm defect extent before considering factory repair.
