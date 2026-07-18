# 2027 Master's Personal Statements Design

**Date:** 2026-07-18  
**Applicant:** Jianming Xing  
**Intake:** Fall 2027  
**Target regions:** Hong Kong and Singapore  
**Output language:** English

## 1. Objective

Create an application-ready personal-statement system for 25 taught master's programs at CUHK, HKUST, PolyU, CityUHK, NUS, and NTU. The system will use three direction-specific base statements and one verified customization module per program. It must preserve a coherent personal identity while giving each program a materially different and factually grounded fit argument.

The central applicant narrative is:

> A mechanical-engineering graduate who deliberately added computer-science training, then developed from robot perception and digital twins into real-robot VLA systems and embodied-intelligence research. The immediate career goal is robotics or embodied-AI R&D engineering, with future doctoral study remaining an option after gaining stronger real-system experience.

## 2. Approved Scope

The deliverable will contain:

1. Three direction-specific English base statements.
2. Twenty-five program-specific customization modules.
3. Twenty-five assembled PDFs: application-ready versions where official 2027/28 requirements are available, and clearly labeled provisional versions where they are not.
4. Twenty-five Markdown text versions for application portals.
5. Reusable LaTeX sources based on the existing EasierPS layout.
6. A program verification matrix recording official program names, relevant curriculum or experiential resources, source URLs, word limits, word counts, and verification dates.

DOCX generation is outside the initial scope. A DOCX will be produced later only when a particular application system requires Word format.

Existing files in `mine_PS` will not be overwritten. New work will live under an independent `applications_2027` directory.

## 3. Source-of-Truth Hierarchy

Applicant facts will be derived in this order:

1. Final English resume: `../English_cv/resume_EN.pdf` and `../English_cv/template/main.typ`.
2. Final Chinese resume: `../chinese_cv/resume_CN.pdf` and `../chinese_cv/resume-zh_CN.tex`.
3. Personal website source: `../xing_web`, especially the project summaries, project reports, and internship data.
4. Project repositories and technical documentation when a resume claim needs implementation context.
5. Existing `mine_PS/personal_statement.md` and `easier_ps/content/*.tex` as draft material, not as unquestioned factual authority.

Program facts will come from official university, department, program-catalog, or admissions pages. Third-party admissions blogs, rankings, forum posts, and unverified course lists will not be used in the statements.

## 4. Factual Guardrails

The following facts must remain consistent across all versions:

- The applicant earned a B.Eng. in Mechanical Design, Manufacturing and Automation from HIT Weihai in June 2025.
- The applicant is currently pursuing a second bachelor's degree in Computer Science and Technology at HIT Shenzhen and expects to complete it in June 2027. It must not be described as already completed.
- The Hermite Action Tokenizer work is a working paper, is not submitted, and lists the applicant as second author responsible for the discrete autoregressive tokenization branch.
- Hermite performance numbers may be used only with their correct comparison context. Reconstruction error, endpoint error, LIBERO full-50 performance, and LIBERO-Plus performance must not be conflated.
- The CR5 project uses a Dobot CR5, Orbbec Astra2 RGB-D camera, electric gripper, ROS2, HDF5 synchronization, LeRobot v2.0, OpenPI adaptation, and WebSocket policy serving.
- Camera frame drops improved from 27.15% to the 2.57%-4.74% range. The range must not be rewritten as a single best-case result without context.
- The stable CR5 deployment path used action chunks and blocking short-horizon ServoP execution after non-blocking execution produced unstable corrections from intermediate states.
- For the weld-seam HMI, technical figures control metric definitions when a summary or resume shorthand conflicts. The original U-Net recorded 81.19% mIoU and 0.64 seam-class IoU; the final 939-image configuration recorded 96.80% mIoU and 0.94 seam-class IoU. The shorthand 64% -> 96.8% is prohibited because it crosses metric types. Architecture, pretraining, and dataset size all changed across stages, so the results do not support a single-factor causal claim or controlled-ablation claim.
- The Xbotics work was a community internship involving MotrixLab, Isaac Lab, MuJoCo heightfields, quadruped navigation, and reinforcement-learning environment migration.
- TOEFL is currently 93. NTU MSc Artificial Intelligence, whose current requirement is 100, is excluded because the applicant does not plan to retake TOEFL.
- Awards may be stated exactly as recorded in the final resumes. Additional claims about personal contribution or competition methodology require supporting material.

## 5. Narrative Strategy

All three statements will express one shared principle: intelligent robot behavior is meaningful only when algorithms, data, control, sensing, timing, safety, and hardware work together on a physical system.

Each direction will enter that principle through a different authentic technical scene.

### 5.1 Robotics and Embodied Intelligence

Open with the CR5 deployment observation that non-blocking execution increased apparent command frequency but caused the policy to infer from intermediate robot states, producing unstable corrective motion. Use this to establish an interest in the interaction among robot learning, control, sensing, latency, and safety.

Primary evidence:

- CR5 real-robot VLA/OpenPI loop.
- Hermite Action Tokenizer research.

Supporting evidence:

- Xbotics reinforcement-learning environment work.
- Weld-seam HMI and digital twin.
- HERO RoboMaster ROS2 migration.

### 5.2 Computer Science and Artificial Intelligence

Open with the realization that a learning policy depends on the quality and semantics of the system around the model: timestamp alignment, state/action representation, dataset validation, model serving, and inference behavior.

Primary evidence:

- Hermite action representation and tokenization.
- CR5 synchronization, data pipeline, OpenPI adaptation, and deployment infrastructure.

Supporting evidence:

- Vision segmentation and C++/Qt integration.
- ROS2 modularization and communication.
- Reinforcement-learning environment design and regression tests.

### 5.3 Mechanical Engineering and Smart Manufacturing

Open with the applicant's progression from reasoning about mechanism geometry and kinematics to building machines that integrate perception, software, and learning.

Primary evidence:

- Weld-seam recognition HMI, modified-DH kinematics, analytical forward/inverse kinematics, and OpenGL digital twin.
- CR5 calibration, servo control, work-space validation, and real-robot integration.

Supporting evidence:

- Mechanical undergraduate preparation.
- Intelligent-vehicle competition experience.
- Automation, control, data-driven manufacturing, and embodied-intelligence interests.

## 6. Statement Architecture and Word Budget

When a program publishes no stricter limit, each complete statement will target 850-950 words and approximately two pages in the EasierPS layout.

| Section | Purpose | Target length |
| --- | --- | ---: |
| Technical opening | Establish motivation through a concrete engineering observation | 70-100 words |
| Academic transition | Explain Mechanical Engineering to Computer Science as expansion, not abandonment | 100-130 words |
| Primary experiences | Present two connected experiences with actions, results, and reflection | 350-420 words |
| Supporting evidence | Add one or two experiences without repeating the resume | 100-140 words |
| Goals and open questions | Define near-term R&D goal and longer-term research option | 80-110 words |
| Program fit | Explain specific curricular or experiential fit and contribution | 160-220 words |

If an official portal or program imposes a lower limit, the statement will be compressed in this order:

1. Remove secondary team experience.
2. Shorten implementation detail while preserving the engineering decision and result.
3. Keep one primary experience rather than listing several.
4. Preserve the program-fit argument and career goal.

The statements will not repeat every resume item. They will prioritize reflection, technical judgment, and progression.

## 7. Program-to-Base Mapping

### 7.1 Robotics and Embodied Intelligence Base (6)

1. CUHK MSc in Robotics.
2. HKUST MEng in Robotics and Embodied AI.
3. PolyU MSc in Intelligent Robotics Engineering.
4. NUS MSc in Robotics.
5. NTU MSc in Robotics and Intelligent Systems.
6. NTU MSc in Computer Control & Automation.

### 7.2 Computer Science and Artificial Intelligence Base (14)

1. CUHK MSc in Artificial Intelligence.
2. CUHK MSc in Computer Science.
3. CUHK MSc in Information Engineering.
4. HKUST MSc in Artificial Intelligence.
5. HKUST MSc in Information Technology.
6. HKUST MSc in Big Data Technology.
7. PolyU MSc in Agentic AI Systems.
8. PolyU MSc in Information Technology.
9. PolyU MSc in Artificial Intelligence and Big Data Computing.
10. CityUHK MSc in Artificial Intelligence.
11. CityUHK MSc in Computer Science.
12. CityUHK MSc in Computer and Information Engineering.
13. NUS MSc in Data Science and Machine Learning.
14. NTU MSc in Signal Processing and Machine Learning.

### 7.3 Mechanical Engineering and Smart Manufacturing Base (5)

1. CUHK MSc in Mechanical and Automation Engineering.
2. HKUST MSc in Mechanical Engineering.
3. PolyU MSc in Smart Manufacturing.
4. CityUHK MSc in Mechanical Engineering.
5. NUS MSc in Mechanical Engineering.

## 8. Program Customization Rules

Each program module will contribute 160-220 words and answer four questions:

1. What specific knowledge or capability gap does the program address?
2. Which two to four official courses, projects, capstones, internships, laboratories, or cross-disciplinary structures address that gap?
3. Which applicant experience provides a credible foundation for using those resources?
4. How does the program connect to the applicant's robotics or embodied-AI R&D goal?

Customization must be material, not cosmetic. It must not rely on university rankings, location, prestige, generic faculty excellence, or phrases such as "world-class resources."

Faculty names will be included only when the taught program formally supports supervised research or projects and an official faculty research profile provides a direct, durable match. A faculty name will not be inserted merely to imitate a research-degree statement.

The HKUST MEng in Robotics and Embodied AI is provisional. Until its catalog and application page are published, its module may use only facts confirmed by HKUST's official announcement: joint ECE/MAE offering, one academic year followed by one industry-internship year, admissions planned for 2026, and first intake planned for Fall 2027. Unpublished course names will not be invented.

## 9. Content and Build Architecture

The new directory will separate facts, reusable narrative, customization, assembled sources, and final artifacts:

```text
applications_2027/
├── README.md
├── facts/
│   ├── applicant_fact_bank.md
│   └── program_verification_matrix.md
├── content/
│   ├── base/
│   │   ├── robotics_embodied_ai.tex
│   │   ├── computer_science_ai.tex
│   │   └── mechanical_smart_manufacturing.tex
│   └── programs/
│       ├── cuhk/
│       ├── hkust/
│       ├── polyu/
│       ├── cityu/
│       ├── nus/
│       └── ntu/
├── statements/
│   └── one LaTeX entry file per program
└── output/
    ├── pdf/
    └── markdown/
```

The existing EasierPS class will be reused. A program entry file will set the applicant name, university name, and exact program name, then include one approved base and one program module. The Markdown version will contain the same prose without LaTeX commands.

Content data flow:

```text
resumes + website + technical docs
              ↓
      applicant fact bank
              ↓
   three direction base drafts
              +
official program page → verification record → program module
              ↓
       assembled statement
              ↓
    compile + render + text QA
              ↓
        PDF and Markdown
```

## 10. Program Research and Change Handling

- Program and curriculum research will prioritize 2027/28 pages. If they are unavailable, the latest official page may inform a provisional draft and will be labeled with its academic year in the verification matrix.
- Before final delivery, every provisional record will be checked again for a 2027/28 update.
- If two official pages conflict, the program catalog and current admissions page take priority over marketing copy. The conflict will be recorded rather than silently resolved.
- If a program changes name, curriculum, eligibility, or statement limit, the program module and output filenames will be updated together.
- If an official word or character limit conflicts with the default design, the stricter official limit controls.
- If a program does not request a separate statement, its prose will remain available as an application-answer source but will not be falsely labeled as a mandatory upload.

## 11. Quality Assurance

Every assembled statement must pass all checks below.

### 11.1 Factual QA

- Exact degree and program names match current official pages.
- Courses and experiential components exist in the cited academic year.
- Applicant dates, roles, authorship, metrics, hardware, and software match the fact bank.
- The second bachelor's degree and unpublished paper are described with their current status.
- No statement contains another university's name, acronym, course, or program.

### 11.2 Writing QA

- The opening contains a concrete scene or engineering observation.
- Each technical paragraph includes reflection or a decision, not only task description.
- The academic transition is presented as a coherent expansion of capability.
- The career goal is R&D engineering first, with doctoral study as an option rather than a promise.
- Generic prestige language, resume-listing, fabricated emotion, and unsupported faculty fit are absent.
- Reused base text does not make program modules sound interchangeable.

### 11.3 Mechanical QA

- Each LaTeX file compiles without errors or missing references.
- Placeholder scans find no bracketed school names, `Target University`, `TBD`, or template sample text.
- Word counts comply with verified limits.
- Each PDF is rendered to images and visually inspected for clipping, bad page breaks, crowded headers, broken glyphs, and inconsistent whitespace.
- PDF text extraction is compared with the Markdown version to detect missing or duplicated paragraphs.

## 12. Acceptance Criteria

The work is complete when:

1. All three base statements are coherent independent narratives.
2. All 25 program modules use verified, program-specific evidence.
3. All 25 statements compile into readable PDFs; any statement awaiting unpublished 2027/28 requirements is visibly marked provisional in its filename and verification record.
4. All 25 Markdown versions match their corresponding PDFs.
5. The verification matrix contains no unresolved placeholders and clearly labels any official 2027/28 information that remains unpublished.
6. Final scans find no program-name contamination, unsupported applicant claims, or formatting defects.

## 13. Out of Scope

This project does not include recommendation letters, CV rewriting, transcript explanations, scholarship essays, video statements, professor-contact emails, or general admissions-strategy ranking. Those can be handled as separate tasks using the same fact bank.
