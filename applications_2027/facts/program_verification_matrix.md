# Program Verification Matrix

This matrix is the human-auditable companion to `applications_2027/config/programs.json`. It initializes the current application scope without treating historical notes as verified facts. The current official sources reopened and recorded in Tasks 4-9 control program identity, application requirements, statement requirements, limits, and fit resources.

## Target-list reconciliation

- The two `target_school` notes are historical/discovery sources only. They help explain how the target list developed, but they are not authoritative evidence for any program fact or application requirement.
- The current manifest contains 25 unique program keys: CUHK 5, HKUST 5, PolyU 5, CityUHK 4, NUS 3, and NTU 3. Its direction counts are `robotics_embodied_ai` 6, `computer_science_ai` 14, and `mechanical_smart_manufacturing` 5.
- The agreed expanded scope includes HKUST MSc in Big Data Technology, CUHK MSc in Information Engineering, PolyU MSc in Artificial Intelligence and Big Data Computing, CityUHK MSc in Computer and Information Engineering, and HKUST MEng in Robotics and Embodied AI.
- NTU MSc Artificial Intelligence is outside the current 25-program manifest. The official TOEFL eligibility rationale will be recorded during NTU verification; it is not asserted from `target_school`.

## Source precedence

1. Current official program catalogs and official admissions or application-checklist pages outrank official marketing pages.
2. Within the same current-official tier, the current catalog or program page controls program identity, curriculum, and experiential resources; the current admissions checklist or application portal controls upload requirements and word or character limits.
3. Official university and department pages outrank `target_school` notes and all third-party sources.
4. If current official sources conflict within a field, both sources and the conflict are recorded in the relevant row's Notes field. The row and its output remain provisional until the conflict is resolved; no source is silently chosen.

## Status legend

- `application_ready`: a current Fall 2027 or 2027-28 official source establishes the program identity and the relevant application or statement constraint.
- `provisional`: only a prior-cycle official source or an official announcement is available.
- `official_announcement_only`: a provisional verification subtype for HKUST MEng in Robotics and Embodied AI until a catalog or application page is live.
- `Not yet assessed` in Separate PS requirement or Official limit is an explicit intermediate state, not a claim that a separate statement or limit is absent.
- `—` is an intermediate empty sentinel, never a claim of “not applicable.” The assigned school task must eliminate every standalone em-dash sentinel.
- `No separate statement listed` is a terminal Separate PS requirement value. It may be used only when a current official application checklist or portal affirmatively omits a separate statement and the supporting official URL is recorded.
- `Not publicly specified` is a terminal value meaning that official public sources were searched but do not state the relevant statement requirement or limit. It is distinct from an affirmative checklist or portal omission.
- `Not applicable — single official announcement` is the only permitted terminal value for a missing Supporting official URL in an `official_announcement_only` case. It is allowed only when the primary official announcement URL is recorded and Notes explains that no second official source is yet published; it must not be used for ordinary unsearched rows.

## Operational status gate

Output status values in this skeleton are inherited seed values copied from `programs.json`. A row is not operationally `application_ready` and must not produce an unsuffixed final output until every intermediate sentinel is gone, an ISO verification date is recorded, the required primary official evidence is present, and the matrix and manifest are synchronized. If any part of this evidence gate is unmet, the output must be treated operationally as `provisional` even when the inherited seed value says `application_ready`.

## Verification matrix

| Key | Official program name | Intake or academic year | Separate PS requirement | Official limit | Verified fit resources | Primary official URL | Supporting official URL | Verified on | Output status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cuhk-robotics | MSc in Robotics | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to CUHK Task 4. |
| cuhk-mechanical-automation-engineering | MSc in Mechanical and Automation Engineering | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to CUHK Task 4. |
| cuhk-artificial-intelligence | MSc in Artificial Intelligence | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to CUHK Task 4. |
| cuhk-computer-science | MSc in Computer Science | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to CUHK Task 4. |
| cuhk-information-engineering | MSc in Information Engineering | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to CUHK Task 4. |
| hkust-robotics-embodied-ai | MEng in Robotics and Embodied AI | Fall 2027 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to HKUST Task 5; official_announcement_only until catalog/application page is verified. |
| hkust-artificial-intelligence | MSc in Artificial Intelligence | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to HKUST Task 5. |
| hkust-information-technology | MSc in Information Technology | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to HKUST Task 5. |
| hkust-big-data-technology | MSc in Big Data Technology | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to HKUST Task 5. |
| hkust-mechanical-engineering | MSc in Mechanical Engineering | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to HKUST Task 5. |
| polyu-intelligent-robotics-engineering | MSc in Intelligent Robotics Engineering | 2027/28 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | application_ready | Assigned to PolyU Task 6. |
| polyu-agentic-ai-systems | MSc in Agentic AI Systems | 2027/28 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | application_ready | Assigned to PolyU Task 6. |
| polyu-information-technology | MSc in Information Technology | 2027/28 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | application_ready | Assigned to PolyU Task 6. |
| polyu-artificial-intelligence-big-data-computing | MSc in Artificial Intelligence and Big Data Computing | 2027/28 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | application_ready | Assigned to PolyU Task 6. |
| polyu-smart-manufacturing | MSc in Smart Manufacturing | 2027/28 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | application_ready | Assigned to PolyU Task 6. |
| cityu-artificial-intelligence | MSc in Artificial Intelligence | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to CityUHK Task 7. |
| cityu-computer-science | MSc in Computer Science | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to CityUHK Task 7. |
| cityu-computer-information-engineering | MSc in Computer and Information Engineering | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to CityUHK Task 7. |
| cityu-mechanical-engineering | MSc in Mechanical Engineering | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to CityUHK Task 7. |
| nus-robotics | MSc in Robotics | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to NUS Task 8. |
| nus-data-science-machine-learning | MSc in Data Science and Machine Learning | Fall 2027 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | application_ready | Assigned to NUS Task 8. |
| nus-mechanical-engineering | MSc in Mechanical Engineering | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to NUS Task 8. |
| ntu-robotics-intelligent-systems | MSc in Robotics and Intelligent Systems | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to NTU Task 9. |
| ntu-computer-control-automation | MSc in Computer Control & Automation | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to NTU Task 9. |
| ntu-signal-processing-machine-learning | MSc in Signal Processing and Machine Learning | 2026/27 | Not yet assessed | Not yet assessed | — | — | — | Not yet reopened | provisional | Assigned to NTU Task 9. |

## Completion rule for Tasks 4-9

Each school verification task must replace every intermediate sentinel in its assigned rows, including `Not yet assessed`, every standalone `—`, and `Not yet reopened`. Every em-dash empty sentinel must be removed or replaced; the em dash inside the named terminal value `Not applicable — single official announcement` is not an empty sentinel and is allowed only under the conditions in the Status legend. The task must record an ISO verification date, retain the exact official URLs used, capture official evidence for the separate-statement requirement and any official limit, and select two to four durable official fit resources per program.

The terminal Separate PS requirement value must reflect the evidence: a documented requirement and limit when present, `No separate statement listed` only for an affirmative current checklist or portal omission with its supporting URL, or `Not publicly specified` only after official public sources were searched without finding a stated requirement. A missing Supporting official URL may use `Not applicable — single official announcement` only for the constrained announcement-only case defined above.

After verification, the task must synchronize the corresponding manifest fields `academic_year`, `verification_status`, `output_status`, and `official_limit` with the evidence recorded here. The row may pass the operational `application_ready` gate only after that synchronization and all other gate conditions are met. Any conflict among current official sources must remain visible in Notes, and the row and output must remain provisional until the conflict is resolved.
