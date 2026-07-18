# 2027 Master's Personal Statement Portfolio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Produce a verified, application-ready-or-clearly-provisional portfolio of 25 English personal statements for Fall 2027 master's applications, using three coherent direction bases, 25 materially distinct program modules, matching Markdown text, and visually verified PDFs.

**Architecture:** Keep the applicant fact bank, official program evidence, reusable narrative, program-specific fit modules, generated LaTeX entry points, and rendered outputs separate. Plain-paragraph LaTeX files are the canonical prose source. A small standard-library Python builder assembles each direction base with one program module, generates the matching Markdown body, and compiles the LaTeX entry file. A second Python tool enforces manifest integrity, fact/status conventions, word limits, cross-school contamination checks, Markdown parity, PDF existence, and extracted-text parity.

**Tech Stack:** Markdown, JSON, Python 3 standard library and unittest, XeLaTeX through latexmk, the existing EasierPS LaTeX class, Poppler tools (pdftotext, pdfinfo, pdftoppm), Git.

---

## Working Rules

- Execute from /Users/xingjianming/profile/mine_PS.
- Treat the accepted design at docs/superpowers/specs/2026-07-18-2027-masters-personal-statements-design.md as the controlling specification.
- Do not edit or delete the user's current uncommitted files under easier_ps, persoal_statement_template, or personal_statement.md.
- Put all new application work under applications_2027, except this plan and the accepted design.
- Use ../target_school as a program-discovery and applicant-notes source, but never as authority over a current official university page.
- Use applicant claims only after they are entered in the fact bank with a local source reference.
- Use program claims only after reopening an official university page and recording the verification date, academic year, exact wording, and URL.
- A program is application_ready only when an official Fall 2027 or 2027/28 source establishes the current program identity and relevant requirements. Otherwise it is provisional, and both PDF and Markdown filenames must end in -provisional.
- Do not infer that a separate statement is required when the official application material does not say so. Record not publicly specified.
- Do not introduce faculty names unless an official taught-program structure supports supervised research and the faculty match is durable and directly relevant.
- Stage and commit only files created by the current task. Never use git add -A or git add ..
- Use ASCII apostrophes and ordinary hyphens in canonical prose unless a Unicode character has been compilation-tested.
- Do not generate bulk DOCX files in this phase; produce one later only if a specific application portal requires it.

## Target Tree

~~~text
applications_2027/
├── .gitignore
├── README.md
├── easier_ps.cls
├── config/
│   └── programs.json
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
├── scripts/
│   ├── __init__.py
│   ├── build_statements.py
│   └── validate_statements.py
├── statements/
│   └── 25 generated LaTeX entry files
├── tests/
│   ├── __init__.py
│   ├── test_manifest.py
│   ├── test_build_statements.py
│   └── test_validate_statements.py
├── build/
│   └── ignored LaTeX intermediates
└── output/
    ├── markdown/
    └── pdf/
~~~

## Manifest Contract

Every program object in applications_2027/config/programs.json must contain:

~~~json
{
  "key": "cuhk-robotics",
  "school": "cuhk",
  "university": "The Chinese University of Hong Kong",
  "university_abbr": "CUHK",
  "program": "MSc in Robotics",
  "direction": "robotics_embodied_ai",
  "program_module": "content/programs/cuhk/robotics.tex",
  "academic_year": "2026/27",
  "verification_status": "latest_official_prior_cycle",
  "output_status": "provisional",
  "official_limit": null
}
~~~

The allowed direction values are robotics_embodied_ai, computer_science_ai, and mechanical_smart_manufacturing. The allowed output_status values are application_ready and provisional. An official_limit is null only when a separate official limit is not publicly specified; otherwise it is an object such as {"unit": "words", "max": 1000} or {"unit": "characters", "max": 4000, "includes_spaces": true}.

The manifest must contain these exact records before any later evidence-driven status changes:

| Key | Exact program name | Direction | Initial status |
| --- | --- | --- | --- |
| cuhk-robotics | MSc in Robotics | robotics_embodied_ai | provisional |
| cuhk-mechanical-automation-engineering | MSc in Mechanical and Automation Engineering | mechanical_smart_manufacturing | provisional |
| cuhk-artificial-intelligence | MSc in Artificial Intelligence | computer_science_ai | provisional |
| cuhk-computer-science | MSc in Computer Science | computer_science_ai | provisional |
| cuhk-information-engineering | MSc in Information Engineering | computer_science_ai | provisional |
| hkust-robotics-embodied-ai | MEng in Robotics and Embodied AI | robotics_embodied_ai | provisional |
| hkust-artificial-intelligence | MSc in Artificial Intelligence | computer_science_ai | provisional |
| hkust-information-technology | MSc in Information Technology | computer_science_ai | provisional |
| hkust-big-data-technology | MSc in Big Data Technology | computer_science_ai | provisional |
| hkust-mechanical-engineering | MSc in Mechanical Engineering | mechanical_smart_manufacturing | provisional |
| polyu-intelligent-robotics-engineering | MSc in Intelligent Robotics Engineering | robotics_embodied_ai | application_ready |
| polyu-agentic-ai-systems | MSc in Agentic AI Systems | computer_science_ai | application_ready |
| polyu-information-technology | MSc in Information Technology | computer_science_ai | application_ready |
| polyu-artificial-intelligence-big-data-computing | MSc in Artificial Intelligence and Big Data Computing | computer_science_ai | application_ready |
| polyu-smart-manufacturing | MSc in Smart Manufacturing | mechanical_smart_manufacturing | application_ready |
| cityu-artificial-intelligence | MSc in Artificial Intelligence | computer_science_ai | provisional |
| cityu-computer-science | MSc in Computer Science | computer_science_ai | provisional |
| cityu-computer-information-engineering | MSc in Computer and Information Engineering | computer_science_ai | provisional |
| cityu-mechanical-engineering | MSc in Mechanical Engineering | mechanical_smart_manufacturing | provisional |
| nus-robotics | MSc in Robotics | robotics_embodied_ai | provisional |
| nus-data-science-machine-learning | MSc in Data Science and Machine Learning | computer_science_ai | application_ready |
| nus-mechanical-engineering | MSc in Mechanical Engineering | mechanical_smart_manufacturing | provisional |
| ntu-robotics-intelligent-systems | MSc in Robotics and Intelligent Systems | robotics_embodied_ai | provisional |
| ntu-computer-control-automation | MSc in Computer Control & Automation | robotics_embodied_ai | provisional |
| ntu-signal-processing-machine-learning | MSc in Signal Processing and Machine Learning | computer_science_ai | provisional |

University metadata is fixed by school:

| School | University | Abbreviation |
| --- | --- | --- |
| cuhk | The Chinese University of Hong Kong | CUHK |
| hkust | The Hong Kong University of Science and Technology | HKUST |
| polyu | The Hong Kong Polytechnic University | PolyU |
| cityu | City University of Hong Kong | CityUHK |
| nus | National University of Singapore | NUS |
| ntu | Nanyang Technological University, Singapore | NTU |

### Task 1: Protect the Existing Worktree and Scaffold the Isolated Portfolio

**Files:**

- Create: applications_2027/.gitignore
- Create: applications_2027/config/programs.json
- Create: applications_2027/scripts/__init__.py
- Create: applications_2027/tests/__init__.py
- Create: applications_2027/tests/test_manifest.py
- Create directories shown in the target tree

- [ ] Record the baseline without modifying it.

Run:

~~~bash
git status --short
git diff -- easier_ps/easier_ps.cls easier_ps/main.tex
~~~

Expected: the known modified and untracked user files remain visible. Save the filenames in the execution log; do not stage them.

- [ ] Create the isolated directory tree and an ignore file containing:

~~~gitignore
build/
__pycache__/
*.aux
*.fdb_latexmk
*.fls
*.log
*.out
*.synctex.gz
~~~

- [ ] Write the manifest test first:

~~~python
import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(
            (ROOT / "config" / "programs.json").read_text(encoding="utf-8")
        )
        cls.programs = cls.data["programs"]

    def test_contains_exactly_25_unique_programs(self):
        self.assertEqual(25, len(self.programs))
        self.assertEqual(25, len({p["key"] for p in self.programs}))

    def test_direction_distribution_matches_design(self):
        self.assertEqual(
            {
                "robotics_embodied_ai": 6,
                "computer_science_ai": 14,
                "mechanical_smart_manufacturing": 5,
            },
            dict(Counter(p["direction"] for p in self.programs)),
        )

    def test_school_distribution_matches_design(self):
        self.assertEqual(
            {"cuhk": 5, "hkust": 5, "polyu": 5, "cityu": 4, "nus": 3, "ntu": 3},
            dict(Counter(p["school"] for p in self.programs)),
        )

    def test_required_fields_and_status_values(self):
        required = {
            "key",
            "school",
            "university",
            "university_abbr",
            "program",
            "direction",
            "program_module",
            "academic_year",
            "verification_status",
            "output_status",
            "official_limit",
        }
        for program in self.programs:
            self.assertEqual(required, set(program))
            self.assertIn(program["output_status"], {"application_ready", "provisional"})


if __name__ == "__main__":
    unittest.main()
~~~

- [ ] Run the test and confirm that it fails because programs.json does not yet exist.

Run:

~~~bash
cd applications_2027
python3 -m unittest tests.test_manifest -v
~~~

Expected: ERROR with FileNotFoundError for config/programs.json.

- [ ] Create programs.json from the complete manifest contract above, with a top-level applicant object containing name Jianming Xing and intake Fall 2027.

- [ ] Run the test again.

Expected: four tests pass.

- [ ] Confirm only the new scaffold is staged, then commit.

~~~bash
git status --short
git add applications_2027/.gitignore applications_2027/config/programs.json applications_2027/scripts/__init__.py applications_2027/tests/__init__.py applications_2027/tests/test_manifest.py
git commit -m "feat: scaffold 2027 statement portfolio"
~~~

### Task 2: Build the Applicant Fact Bank

**Files:**

- Create: applications_2027/facts/applicant_fact_bank.md
- Read: ../English_cv/resume_EN.pdf
- Read: ../English_cv/template/main.typ
- Read: ../chinese_cv/resume_CN.pdf
- Read: ../chinese_cv/resume-zh_CN.tex
- Read: ../xing_web project, internship, award, and biography sources
- Read: personal_statement.md only as draft material

- [ ] Render or extract both final resume PDFs and compare them with their source files. Record any discrepancy before using a claim.

- [ ] Create the fact bank with columns Claim ID, Verified wording, Dates, Quantitative detail, Local source, Allowed paraphrase, and Forbidden inflation.

- [ ] Enter education facts, including B.Eng. completion in June 2025 and the ongoing second B.A./bachelor's degree in Computer Science and Technology with expected completion in June 2027. Copy exact degree labels and dates from the final resumes.

- [ ] Enter the Hermite Action Tokenizer facts. Preserve working-paper status, not submitted status, second authorship, responsibility for the discrete autoregressive branch, and the distinct contexts of every recorded metric.

- [ ] Enter the CR5 facts: Dobot CR5, Orbbec Astra2 RGB-D camera, electric gripper, ROS2, HDF5 synchronization, LeRobot v2.0, OpenPI adaptation, WebSocket policy serving, frame-drop improvement from 27.15% to the 2.57%-4.74% range, and the decision to use action chunks with blocking short-horizon ServoP after unstable non-blocking execution.

- [ ] Enter the weld-seam HMI facts: modified-DH kinematics, analytical forward/inverse kinematics, OpenGL digital twin, and segmentation accuracy improvement from 64% to 96.8%. Explicitly forbid relabeling the metric as mIoU.

- [ ] Enter Xbotics, HERO RoboMaster, competition, award, programming, and language facts exactly as supported. Record TOEFL 93 and the decision not to retake it.

- [ ] Add a final section named Narrative Guardrails containing the ten guardrails from the accepted design and a rule that every numeric claim must cite a Claim ID during drafting.

- [ ] Scan for unresolved language.

~~~bash
rg -n -i 'TBD|TODO|FIXME|to verify|need source|maybe|probably' applications_2027/facts/applicant_fact_bank.md
~~~

Expected: no output.

- [ ] Commit only the fact bank.

~~~bash
git add applications_2027/facts/applicant_fact_bank.md
git commit -m "docs: establish applicant fact bank"
~~~

### Task 3: Initialize the 25-Row Program Verification Matrix

**Files:**

- Create: applications_2027/facts/program_verification_matrix.md
- Modify: applications_2027/config/programs.json
- Read: ../target_school

- [ ] Create a table with one row per manifest key and these columns: Key, Official program name, Intake or academic year, Separate PS requirement, Official limit, Verified fit resources, Primary official URL, Supporting official URL, Verified on, Output status, Notes.

- [ ] Cross-check the target_school notes for intended programs and useful leads, then resolve every program name, resource, and requirement against an official source before entering it in the matrix.

- [ ] Set Verified on to 2026-07-18 only for pages actually reopened during implementation; do not carry a date forward merely from this plan.

- [ ] Use not publicly specified for an absent public PS requirement or limit. Use no separate statement listed only when the official application checklist affirmatively omits it.

- [ ] Add a status legend:

  - application_ready: a Fall 2027 or 2027/28 official source establishes the current program identity and the relevant statement/application constraint.
  - provisional: the latest official source is an earlier cycle, or the program has only an official announcement.
  - official_announcement_only: a subtype of provisional for HKUST MEng in Robotics and Embodied AI.

- [ ] Add a source-priority note: current catalog and admissions pages outrank marketing pages; all conflicts are written in Notes.

- [ ] Confirm 25 unique keys against the manifest.

~~~bash
python3 - <<'PY'
import json
from pathlib import Path
programs = json.loads(Path("applications_2027/config/programs.json").read_text())["programs"]
matrix = Path("applications_2027/facts/program_verification_matrix.md").read_text()
missing = [p["key"] for p in programs if p["key"] not in matrix]
assert not missing, missing
print("25 manifest keys represented")
PY
~~~

Expected: 25 manifest keys represented.

- [ ] Commit the matrix skeleton.

~~~bash
git add applications_2027/facts/program_verification_matrix.md
git commit -m "docs: initialize program verification matrix"
~~~

### Task 4: Verify All CUHK Programs from Official Sources

**Files:**

- Modify: applications_2027/facts/program_verification_matrix.md
- Modify: applications_2027/config/programs.json

**Primary official sources:**

- https://www4.mae.cuhk.edu.hk/msc-in-robotics/
- https://www4.mae.cuhk.edu.hk/msc-in-mae/
- https://www.gs.cuhk.edu.hk/programmes/engineering/msc-artificial-intelligence
- https://mscai.erg.cuhk.edu.hk/
- https://www.gs.cuhk.edu.hk/programmes/engineering/msc-computer-science
- http://msc.cse.cuhk.edu.hk/
- https://www.gs.cuhk.edu.hk/programmes/engineering/msc-information-engineering
- https://msc.ie.cuhk.edu.hk/academic/

- [ ] Reopen each source and record the displayed academic year, exact program name, application cycle, public statement requirement, and limit.

- [ ] For CUHK Robotics, verify the exact titles and status of robot learning or embodied AI, robot control, medical robotics, project, and special-topic opportunities. Retain only two to four durable fit resources.

- [ ] For CUHK Mechanical and Automation Engineering, verify a coherent control, robotics, mechatronics, automation, or advanced-manufacturing pathway before selecting resources.

- [ ] For CUHK Artificial Intelligence, verify the curriculum structure and any project or experiential component that supports action representation, learning systems, and embodied AI.

- [ ] For CUHK Computer Science, verify the current machine-learning, vision, systems, project, and internship options. Select resources that connect the second CS degree with real-robot deployment.

- [ ] For CUHK Information Engineering, verify Reinforcement Learning, Research Project I/II, the 12-week internship, and any current multimedia, coding, or emerging-IE offering before citing them.

- [ ] Keep all five outputs provisional unless an official Fall 2027 or 2027/28 source is live. Synchronize academic_year, verification_status, output_status, and official_limit in programs.json.

- [ ] Commit the CUHK evidence update.

~~~bash
git add applications_2027/facts/program_verification_matrix.md applications_2027/config/programs.json
git commit -m "docs: verify CUHK program evidence"
~~~

### Task 5: Verify All HKUST Programs from Official Sources

**Files:**

- Modify: applications_2027/facts/program_verification_matrix.md
- Modify: applications_2027/config/programs.json

**Primary official sources:**

- https://hkust.edu.hk/boundless/article/robotics-ready-real-world
- https://prog-crs.hkust.edu.hk/pgprog/2026-27/msc-ai
- https://seng.hkust.edu.hk/academics/taught-postgraduate/msc-ai
- https://seng.hkust.edu.hk/academics/taught-postgraduate/msc-it
- https://seng.hkust.edu.hk/academics/taught-postgraduate/msc-it/course-schedule
- https://prog-crs.hkust.edu.hk/pgprog/2026-27/msc-bdt/
- https://seng.hkust.edu.hk/academics/taught-postgraduate/msc-bdt
- https://prog-crs.hkust.edu.hk/pgprog/2026-27/msc-mech

- [ ] Search the HKUST official domain for newly published Fall 2027 catalogs or application pages before relying on the listed 2026/27 pages.

- [ ] For the MEng in Robotics and Embodied AI, use only confirmed announcement facts until a catalog is live: joint ECE/MAE offering, one academic year of coursework, a second year of industry internship, admissions planned for 2026, and first cohort planned for Fall 2027. Do not invent course titles, credit counts, or labs.

- [ ] For MSc Artificial Intelligence, verify current foundation, model, systems, project, and applied-AI components that directly address robust embodied learning.

- [ ] For MSc Information Technology, verify current machine-learning, computer-vision, data, distributed-system, and project options before selecting the strongest two to four.

- [ ] For MSc Big Data Technology, focus the fit on reliable data pipelines, scalable learning infrastructure, and system-level model deployment. Verify every selected course title in the current catalog.

- [ ] For MSc Mechanical Engineering, verify control, robotics, mechatronics, design, manufacturing, and project resources suitable for a mechanical-to-embodied-systems narrative.

- [ ] Synchronize manifest status and official limits with the matrix. Keep the new MEng provisional until both its catalog and application requirement are official.

- [ ] Commit the HKUST evidence update.

~~~bash
git add applications_2027/facts/program_verification_matrix.md applications_2027/config/programs.json
git commit -m "docs: verify HKUST program evidence"
~~~

### Task 6: Verify All PolyU 2027/28 Programs from Official Sources

**Files:**

- Modify: applications_2027/facts/program_verification_matrix.md
- Modify: applications_2027/config/programs.json

**Primary official sources:**

- https://www.polyu.edu.hk/study/pg/tpg/2027/43101-ir-irt
- https://www.polyu.edu.hk/study/pg/tpg/2027/61040-fas-pas
- https://www.polyu.edu.hk/study/pg/tpg/2027/61030-fit-pit
- https://www.polyu.edu.hk/study/pg/tpg/2027/62037-fai-pai
- https://www.polyu.edu.hk/study/pg/tpg/2027/45100-smf-smp

- [ ] Verify that each page still identifies the 2027/28 intake and record any application-statement limit from the official application workflow.

- [ ] For Intelligent Robotics Engineering, verify Embodied Robot Intelligence, Principles of Robotic Mechanisms, Robot Motion Planning, Soft Robotics, Advanced Control, computer vision/AI electives, industrial HRI, and the dissertation route. Select the resources that best bridge CR5 deployment and Hermite research.

- [ ] For Agentic AI Systems, verify end-to-end agents, reasoning, large models, embedded or robotic systems, cloud infrastructure, and the zero-to-physical capstone. Center the fit on embodied agents that survive real deployment constraints.

- [ ] For Information Technology, verify the project/dissertation routes and current advanced-IT offerings. Tie the module to synchronization, serving, modular systems, and model integration.

- [ ] For Artificial Intelligence and Big Data Computing, verify the compulsory/elective structure and dissertation option. Tie the module to action representation, data quality, and scalable learning.

- [ ] For Smart Manufacturing, verify Optimization and Data Analytics for Industry 4.0, Cyber-Physical Industry 4.0 Systems, Advanced Manufacturing Processes, Frontiers in Industry 4.0, industrial human-robot systems or automation, and mixed reality. Select a coherent subset.

- [ ] Keep application_ready only where the 2027/28 page and current requirement remain official; otherwise downgrade conservatively and let filenames reflect the change.

- [ ] Commit the PolyU evidence update.

~~~bash
git add applications_2027/facts/program_verification_matrix.md applications_2027/config/programs.json
git commit -m "docs: verify PolyU 2027 program evidence"
~~~

### Task 7: Verify All CityUHK Programs from Official Sources

**Files:**

- Modify: applications_2027/facts/program_verification_matrix.md
- Modify: applications_2027/config/programs.json

**Primary official sources:**

- https://www.cityu.edu.hk/pg/programme/program-list/2026/college-of-computing/department-of-computer-science/p75
- https://www.cityu.edu.hk/pg/programme/program-list/2026/college-of-computing/department-of-computer-science/p53
- https://www.cityu.edu.hk/zh-cn/pg/programme/program-list/2026/college-of-engineering/department-of-electrical-engineering/p59
- https://www.ee.cityu.edu.hk/prospective_students/graduate_admission/mscie_curriculum#CourseList
- https://www.cityu.edu.hk/en/pg/programme/program-list/2026/college-of-engineering/department-of-mechanical-engineering/p66

- [ ] Search the official CityUHK domain for 2027/28 replacements, then record current program names, streams, application cycle, statement requirement, and limit.

- [ ] For Artificial Intelligence, verify the Autonomous Driving, Generative AI, and Trustworthy AI streams plus project/internship options. Select only the stream/resources that form one credible embodied-AI argument.

- [ ] For Computer Science, verify AI/data/security streams and current internship, project, guided-study, and year-long experiential options. Center the module on learning-system engineering.

- [ ] For Computer and Information Engineering, verify current signal, information, machine-learning, networking, control, or embedded-system offerings from the department curriculum page.

- [ ] For Mechanical Engineering, verify the Robotics stream and the exact control, sensing, robotics, design, and project options that connect CR5 and digital-twin work.

- [ ] Keep programs provisional unless a Fall 2027 or 2027/28 official source is live; synchronize the manifest.

- [ ] Commit the CityUHK evidence update.

~~~bash
git add applications_2027/facts/program_verification_matrix.md applications_2027/config/programs.json
git commit -m "docs: verify CityUHK program evidence"
~~~

### Task 8: Verify All NUS Programs from Official Sources

**Files:**

- Modify: applications_2027/facts/program_verification_matrix.md
- Modify: applications_2027/config/programs.json

**Primary official sources:**

- https://cde.nus.edu.sg/me/graduate/msc-robotics/
- https://www.math.nus.edu.sg/cdsml/ms-dsml/dsml-prospective-students/
- https://cde.nus.edu.sg/me/graduate/msc-me/

- [ ] Reopen each page and record the exact intake, application cycle, program name, statement requirement, and limit. Search the official NUS domain for any linked current curriculum or application checklist.

- [ ] For Robotics, verify current robot-learning, perception, control, autonomous-systems, project, and experiential components. Select a set that directly addresses the gap exposed by CR5 execution instability.

- [ ] For Data Science and Machine Learning, verify the August 2027 application cycles and the exact core/elective structure. Center the fit on representation learning, dataset integrity, evaluation, and scalable inference rather than presenting it as a generic robotics degree.

- [ ] For Mechanical Engineering, verify ME5888M local industrial internship, ME5001/ME5001A project options, and current control, mechatronics, design, or manufacturing pathways.

- [ ] Keep Data Science and Machine Learning application_ready only if the official August 2027 information remains current. Update the other statuses strictly from evidence.

- [ ] Commit the NUS evidence update.

~~~bash
git add applications_2027/facts/program_verification_matrix.md applications_2027/config/programs.json
git commit -m "docs: verify NUS program evidence"
~~~

### Task 9: Verify All NTU Programs and Preserve the TOEFL Exclusion

**Files:**

- Modify: applications_2027/facts/program_verification_matrix.md
- Modify: applications_2027/config/programs.json

**Primary official sources:**

- https://www.ntu.edu.sg/education/graduate-programme/master-of-science-%28robotics-and-intelligent-systems%29
- https://www.ntu.edu.sg/education/graduate-programme/master-of-science-in-computer-control-automation
- https://www.ntu.edu.sg/education/graduate-programme/master-of-science-in-signal-processing
- https://www.ntu.edu.sg/eee/admissions/programmes/graduate-programmes/msc
- https://www.ntu.edu.sg/computing/admissions/graduate-programmes/detail/master-of-science-in-artificial-intelligence

- [ ] Verify the August 2027 application timeline, currently expected to run from 1 October 2026 through 31 March 2027, against the live EEE page.

- [ ] For Robotics and Intelligent Systems, verify current robotics, perception, learning, control, autonomy, and project resources. Tie the module to the real-robot learning/control interface.

- [ ] For Computer Control & Automation, verify advanced control, automation, robotics, intelligent systems, and project options. Center the module on the blocking/non-blocking ServoP lesson and safe closed-loop behavior.

- [ ] For Signal Processing and Machine Learning, verify signal representation, estimation, learning, vision, and project options. Connect action tokenization and synchronized multimodal robot data without calling the program a robotics degree.

- [ ] Reconfirm that NTU MSc Artificial Intelligence requires TOEFL 100 or its current equivalent. Keep it excluded while TOEFL remains 93 and no retake is planned; mention the exclusion only in the matrix notes, not in statements.

- [ ] Synchronize all NTU statuses and official limits with the manifest.

- [ ] Commit the NTU evidence update.

~~~bash
git add applications_2027/facts/program_verification_matrix.md applications_2027/config/programs.json
git commit -m "docs: verify NTU program evidence"
~~~

### Task 10: Implement the Statement Builder Test-First

**Files:**

- Create: applications_2027/tests/test_build_statements.py
- Create: applications_2027/scripts/build_statements.py

- [ ] Write tests for provisional suffixes, application-ready filenames, LaTeX-to-plain conversion, entry rendering, and exact body composition:

~~~python
import tempfile
import unittest
from pathlib import Path

from scripts.build_statements import (
    compose_plain,
    output_stem,
    render_entry,
    tex_to_plain,
)


class BuilderTests(unittest.TestCase):
    def setUp(self):
        self.program = {
            "key": "cuhk-robotics",
            "school": "cuhk",
            "university": "The Chinese University of Hong Kong",
            "university_abbr": "CUHK",
            "program": "MSc in Robotics",
            "direction": "robotics_embodied_ai",
            "program_module": "content/programs/cuhk/robotics.tex",
            "academic_year": "2026/27",
            "verification_status": "latest_official_prior_cycle",
            "output_status": "provisional",
            "official_limit": None,
        }

    def test_output_stem_marks_only_provisional_outputs(self):
        self.assertEqual("cuhk-robotics-provisional", output_stem(self.program))
        ready = dict(self.program, output_status="application_ready")
        self.assertEqual("cuhk-robotics", output_stem(ready))

    def test_tex_to_plain_accepts_only_plain_paragraph_escapes(self):
        self.assertEqual(
            "Accuracy rose from 64% to 96.8% in R&D work.",
            tex_to_plain(r"Accuracy rose from 64\% to 96.8\% in R\&D work."),
        )
        with self.assertRaises(ValueError):
            tex_to_plain(r"\textbf{Unsupported markup}")

    def test_render_entry_selects_exact_base_and_module(self):
        entry = render_entry(self.program)
        self.assertIn(r"\SetBaseContentPath{content/base/robotics_embodied_ai}", entry)
        self.assertIn(r"\SetUniContentPath{content/programs/cuhk/robotics}", entry)
        self.assertIn(r"\SetProgramName{MSc in Robotics}", entry)

    def test_compose_plain_preserves_paragraph_order(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = root / "base.tex"
            module = root / "module.tex"
            base.write_text("Base one.\n\nBase two.\n", encoding="utf-8")
            module.write_text("Fit one.\n\nFit two.\n", encoding="utf-8")
            self.assertEqual(
                "Base one.\n\nBase two.\n\nFit one.\n\nFit two.\n",
                compose_plain(base, module),
            )


if __name__ == "__main__":
    unittest.main()
~~~

- [ ] Run the tests and confirm they fail because build_statements.py does not exist.

~~~bash
cd applications_2027
python3 -m unittest tests.test_build_statements -v
~~~

Expected: import error for scripts.build_statements.

- [ ] Implement build_statements.py with these exact public behaviors:

  - ROOT is applications_2027.
  - load_manifest returns the programs list from config/programs.json.
  - output_stem appends -provisional only for provisional records.
  - latex_escape protects ampersands, percent signs, hash signs, underscores, dollar signs, braces, and carets in metadata.
  - tex_to_plain permits only escaped ampersands and percent signs in canonical prose; any other LaTeX command raises ValueError.
  - compose_plain concatenates base then program module with one blank line and a terminal newline.
  - render_entry sets the exact applicant, program, university, base, and module paths and applies firstpageheader.
  - generate_program writes statements/KEY.tex and output/markdown/OUTPUT_STEM.md.
  - compile_program invokes latexmk with XeLaTeX, halt-on-error, an isolated build/KEY directory, and OUTPUT_STEM as the job name, then copies only the final PDF into output/pdf.
  - CLI options are --only KEY and --no-pdf.
  - The default command generates and compiles all 25 programs.

Use this entry template:

~~~python
def render_entry(program):
    base = f"content/base/{program['direction']}"
    module = str(Path(program["program_module"]).with_suffix(""))
    return (
        "\\documentclass{easier_ps}\n"
        f"\\SetStudentName{{{latex_escape('Jianming Xing')}}}\n"
        f"\\SetProgramName{{{latex_escape(program['program'])}}}\n"
        f"\\SetUniversityName{{{latex_escape(program['university'])}}}\n"
        f"\\SetUniversityAbbr{{{latex_escape(program['university_abbr'])}}}\n"
        f"\\SetBaseContentPath{{{base}}}\n"
        f"\\SetUniContentPath{{{module}}}\n"
        "\\begin{document}\n"
        "\\thispagestyle{firstpageheader}\n"
        "\\input{\\GetBaseContentPath}\n"
        "\\input{\\GetUniContentPath}\n"
        "\\end{document}\n"
    )
~~~

Use this compilation contract:

~~~python
command = [
    "latexmk",
    "-xelatex",
    "-interaction=nonstopmode",
    "-halt-on-error",
    f"-outdir={build_dir}",
    f"-jobname={output_stem(program)}",
    str(entry_path),
]
subprocess.run(command, cwd=ROOT, check=True)
shutil.copy2(
    build_dir / f"{output_stem(program)}.pdf",
    ROOT / "output" / "pdf" / f"{output_stem(program)}.pdf",
)
~~~

- [ ] Run the builder tests.

Expected: four tests pass.

- [ ] Run all existing tests.

~~~bash
cd applications_2027
python3 -m unittest discover -s tests -v
~~~

Expected: eight tests pass at this stage.

- [ ] Commit the builder and tests.

~~~bash
git add applications_2027/scripts/build_statements.py applications_2027/tests/test_build_statements.py
git commit -m "feat: add statement build pipeline"
~~~

### Task 11: Implement the Portfolio Validator Test-First

**Files:**

- Create: applications_2027/tests/test_validate_statements.py
- Create: applications_2027/scripts/validate_statements.py

- [ ] Write tests for word counting, placeholder detection, cross-school contamination, status-aware output paths, and Markdown parity:

~~~python
import unittest

from scripts.validate_statements import (
    contamination_errors,
    placeholder_errors,
    word_count,
)


class ValidatorTests(unittest.TestCase):
    def test_word_count_handles_hyphenated_terms_and_percentages(self):
        self.assertEqual(7, word_count("A real-robot policy reduced drops by 27.15%."))

    def test_placeholder_scan_rejects_template_language(self):
        errors = placeholder_errors("I am applying to Target University.")
        self.assertTrue(errors)
        self.assertFalse(placeholder_errors("I am applying to CUHK."))

    def test_contamination_scan_rejects_another_school(self):
        errors = contamination_errors(
            "CUHK's program fits me, and HKUST is also excellent.",
            own_school="cuhk",
        )
        self.assertTrue(errors)

    def test_contamination_scan_accepts_only_own_school(self):
        self.assertFalse(
            contamination_errors(
                "CUHK's robotics curriculum connects learning and control.",
                own_school="cuhk",
            )
        )


if __name__ == "__main__":
    unittest.main()
~~~

- [ ] Run the tests and confirm the import failure.

~~~bash
cd applications_2027
python3 -m unittest tests.test_validate_statements -v
~~~

Expected: import error for scripts.validate_statements.

- [ ] Implement validate_statements.py with these checks:

  1. Exactly 25 unique manifest keys.
  2. Direction distribution 6/14/5 and school distribution 5/5/5/4/3/3.
  3. Every base and module file exists.
  4. Canonical prose contains no LaTeX command beyond escaped percent and ampersand.
  5. No placeholder term: Target University, Student Name Here, Program Name Here, TBD, TODO, FIXME, lorem ipsum, or an unfilled square/angle-bracket token.
  6. Every program module mentions its own university abbreviation or full name.
  7. No assembled body mentions another target university or abbreviation.
  8. No base mentions a target university.
  9. Default assembled word count is 850-950. A verified official limit overrides this and is enforced in its declared unit.
  10. The generated Markdown file exactly equals compose_plain output.
  11. With --require-pdfs, every status-aware PDF exists.
  12. With --require-pdfs, pdftotext extraction contains the normalized canonical body.

Use these school markers:

~~~python
SCHOOL_MARKERS = {
    "cuhk": ("CUHK", "Chinese University of Hong Kong"),
    "hkust": ("HKUST", "Hong Kong University of Science and Technology"),
    "polyu": ("PolyU", "Hong Kong Polytechnic University"),
    "cityu": ("CityUHK", "City University of Hong Kong"),
    "nus": ("NUS", "National University of Singapore"),
    "ntu": ("NTU", "Nanyang Technological University"),
}
~~~

Normalize PDF comparison text by lowercasing and removing every non-alphanumeric character. This absorbs line-wrap hyphenation without weakening the comparison to a keyword check.

Implement word_count with the expression [A-Za-z0-9]+(?:[.'-][A-Za-z0-9]+)* so decimal metrics and hyphenated technical terms count as one token.

The CLI must accept --require-pdfs and a repeatable --only KEY. With no --only argument it validates all 25 programs; with --only it performs all global manifest checks but content/output checks only for the selected keys. It prints one PASS line per selected program, then a final summary. Any error prints the program key and check name to stderr and exits 1.

- [ ] Run validator tests and the full unit suite.

~~~bash
cd applications_2027
python3 -m unittest discover -s tests -v
~~~

Expected: twelve tests pass.

- [ ] Commit the validator and tests.

~~~bash
git add applications_2027/scripts/validate_statements.py applications_2027/tests/test_validate_statements.py
git commit -m "feat: validate statement content and outputs"
~~~

### Task 12: Snapshot and Smoke-Test the Approved EasierPS Layout

**Files:**

- Create: applications_2027/easier_ps.cls
- Read: easier_ps/easier_ps.cls
- Read: easier_ps/main.tex
- Read: persoal_statement_template

- [ ] Use apply_patch to add an exact snapshot of the current EasierPS class at applications_2027/easier_ps.cls without altering the user's source file.

- [ ] Inspect the Word-template examples only for page hierarchy, header density, margins, and typographic cues. Do not reuse sample-applicant prose or unsupported facts.

- [ ] Review the copied class for sample prose. The class may keep default metadata internally because every generated entry overrides it, but no generated entry or final output may expose those defaults.

- [ ] Confirm the expected public commands exist:

~~~bash
rg -n 'SetStudentName|SetProgramName|SetUniversityName|SetUniversityAbbr|SetBaseContentPath|SetUniContentPath|firstpageheader' applications_2027/easier_ps.cls
~~~

Expected: all seven interfaces are present.

- [ ] Add a manifest test asserting applications_2027/easier_ps.cls exists and each interface is present.

- [ ] Run the full unit suite.

Expected: all tests pass.

- [ ] Commit the class snapshot and updated test.

~~~bash
git add applications_2027/easier_ps.cls applications_2027/tests/test_manifest.py
git commit -m "style: snapshot personal statement layout"
~~~

### Task 13: Draft the Robotics and Embodied-Intelligence Base

**Files:**

- Create: applications_2027/content/base/robotics_embodied_ai.tex
- Read: applications_2027/facts/applicant_fact_bank.md

- [ ] Draft 690-730 words in five or six plain paragraphs. Use only escaped percent and ampersand LaTeX syntax.

- [ ] Paragraph 1, 80-100 words: open on the CR5 non-blocking execution observation. Explain that higher command frequency caused the policy to observe intermediate states and issue unstable corrections. End with the question of how learning, control, timing, sensing, and safety can form one reliable robot system.

- [ ] Paragraph 2, 105-125 words: present Mechanical Engineering at HIT Weihai and the ongoing Computer Science degree at HIT Shenzhen as one deliberate expansion from physical-system understanding into computation, not a change caused by dissatisfaction.

- [ ] Paragraphs 3 and 4, 350-390 words total: connect CR5 implementation decisions with Hermite Action Tokenizer research. Include only fact-bank-approved metrics and make the intellectual progression explicit: synchronized data and action representation affect what a policy can learn; execution semantics affect what the policy actually controls.

- [ ] Paragraph 5, 90-120 words: use Xbotics plus either the weld-seam HMI or HERO ROS2 migration as supporting evidence. Emphasize one engineering judgment rather than listing tasks.

- [ ] Final base paragraph, 70-90 words: state the immediate goal of robotics/embodied-AI R&D engineering and the option of later doctoral study after stronger real-system experience. End by creating a natural handoff to a program-specific fit module.

- [ ] Check word count and forbidden claims.

~~~bash
python3 - <<'PY'
from pathlib import Path
from applications_2027.scripts.build_statements import tex_to_plain
from applications_2027.scripts.validate_statements import word_count, placeholder_errors
path = Path("applications_2027/content/base/robotics_embodied_ai.tex")
text = tex_to_plain(path.read_text())
count = word_count(text)
assert 690 <= count <= 730, count
assert not placeholder_errors(text)
print(count)
PY
~~~

Expected: an integer from 690 through 730.

- [ ] Perform a claim-by-claim read against the fact bank. Remove any unsupported emotional claim, causal claim, or metric.

- [ ] Commit the robotics base.

~~~bash
git add applications_2027/content/base/robotics_embodied_ai.tex
git commit -m "docs: draft robotics statement base"
~~~

### Task 14: Draft the Computer-Science and AI Base

**Files:**

- Create: applications_2027/content/base/computer_science_ai.tex
- Read: applications_2027/facts/applicant_fact_bank.md

- [ ] Draft 690-730 words in five or six plain paragraphs.

- [ ] Paragraph 1, 80-100 words: open with the realization that a learned robot policy depends on the semantics and integrity of the surrounding system: timestamps, state/action representation, dataset validation, serving, and inference behavior.

- [ ] Paragraph 2, 105-125 words: explain the Mechanical Engineering to Computer Science bridge as a search for end-to-end competence across machines and computation. State the current expected June 2027 completion accurately.

- [ ] Paragraphs 3 and 4, 350-390 words total: lead with the Hermite discrete autoregressive branch and connect it to CR5 synchronization, LeRobot conversion, OpenPI adaptation, WebSocket serving, and deployment testing. Distinguish algorithmic evaluation from systems reliability.

- [ ] Paragraph 5, 90-120 words: use weld-seam segmentation/C++-Qt integration, HERO ROS2 modularization, or Xbotics environment regression testing to show software-engineering maturity. Use no more than two supporting projects.

- [ ] Final base paragraph, 70-90 words: target AI/ML or learning-systems R&D serving embodied agents, with later doctoral work as an option. Transition to program-specific resources without naming a school.

- [ ] Run the same 690-730 word and placeholder checks used in Task 13, then verify no target-school marker appears.

- [ ] Commit the CS/AI base.

~~~bash
git add applications_2027/content/base/computer_science_ai.tex
git commit -m "docs: draft computer science statement base"
~~~

### Task 15: Draft the Mechanical Engineering and Smart-Manufacturing Base

**Files:**

- Create: applications_2027/content/base/mechanical_smart_manufacturing.tex
- Read: applications_2027/facts/applicant_fact_bank.md

- [ ] Draft 690-730 words in five or six plain paragraphs.

- [ ] Paragraph 1, 80-100 words: open on the progression from mechanism geometry and kinematics to machines that integrate perception, software, control, and learning.

- [ ] Paragraph 2, 105-125 words: establish the mechanical undergraduate foundation and explain the ongoing CS degree as a way to build more capable physical systems.

- [ ] Paragraphs 3 and 4, 350-390 words total: lead with the weld-seam HMI, modified-DH model, analytical kinematics, OpenGL twin, and fact-bank-approved segmentation accuracy. Connect this to CR5 calibration, workspace validation, servo execution, and real-robot integration.

- [ ] Paragraph 5, 90-120 words: use the intelligent-vehicle competition, HERO, or Xbotics as evidence of multidisciplinary engineering and verification under real constraints.

- [ ] Final base paragraph, 70-90 words: target robotics, automation, or intelligent-manufacturing R&D, preserve later doctoral study as an option, and transition to program-specific fit.

- [ ] Run the same 690-730 word, placeholder, school-marker, and fact-bank checks.

- [ ] Commit the mechanical base.

~~~bash
git add applications_2027/content/base/mechanical_smart_manufacturing.tex
git commit -m "docs: draft mechanical statement base"
~~~

### Task 16: Draft and Validate the Five CUHK Modules

**Files:**

- Create: applications_2027/content/programs/cuhk/robotics.tex
- Create: applications_2027/content/programs/cuhk/mechanical_automation_engineering.tex
- Create: applications_2027/content/programs/cuhk/artificial_intelligence.tex
- Create: applications_2027/content/programs/cuhk/computer_science.tex
- Create: applications_2027/content/programs/cuhk/information_engineering.tex

Each module must be 160-220 words, contain two compact paragraphs, name CUHK or the full university, identify a capability gap, use two to four matrix-verified resources, connect them to one or two applicant experiences, and end in a concrete contribution or career link.

- [ ] Robotics: connect CR5 execution instability and Hermite action representation to verified robot-learning/embodied-AI and robot-control resources. Use a project, special topic, or medical-robotics component only when it strengthens one coherent argument.

- [ ] Mechanical and Automation Engineering: connect kinematics/digital twin and CR5 control to verified automation, control, mechatronics, or advanced-manufacturing resources.

- [ ] Artificial Intelligence: connect action representation and robust deployment to verified AI foundations, advanced learning, and project/experiential resources.

- [ ] Computer Science: connect the second CS degree, OpenPI pipeline, ROS2 modularity, and system validation to verified ML/vision/systems/project resources.

- [ ] Information Engineering: connect synchronized multimodal data and policy serving to verified Reinforcement Learning, Research Project I/II, and the 12-week internship or another current experiential resource.

- [ ] Run the no-PDF build and validator for the five keys.

~~~bash
cd applications_2027
for key in cuhk-robotics cuhk-mechanical-automation-engineering cuhk-artificial-intelligence cuhk-computer-science cuhk-information-engineering; do
  python3 scripts/build_statements.py --only "$key" --no-pdf
  python3 scripts/validate_statements.py --only "$key"
done
~~~

Expected: each of the five CUHK programs reports PASS; undrafted schools are outside the selected content check while global manifest checks still run.

- [ ] Read the five modules consecutively and remove interchangeable phrases. Each must remain identifiable after the program name is hidden.

- [ ] Commit the CUHK modules.

~~~bash
git add applications_2027/content/programs/cuhk
git commit -m "docs: tailor statements for CUHK programs"
~~~

### Task 17: Draft and Validate the Five HKUST Modules

**Files:**

- Create: applications_2027/content/programs/hkust/robotics_embodied_ai.tex
- Create: applications_2027/content/programs/hkust/artificial_intelligence.tex
- Create: applications_2027/content/programs/hkust/information_technology.tex
- Create: applications_2027/content/programs/hkust/big_data_technology.tex
- Create: applications_2027/content/programs/hkust/mechanical_engineering.tex

- [ ] Robotics and Embodied AI: base the fit only on the verified joint ECE/MAE structure, coursework year, industry-internship year, and first-cohort timing unless a live catalog now adds official details. Present the two-year structure as a bridge from laboratory reasoning to production deployment.

- [ ] Artificial Intelligence: connect Hermite and CR5 to verified learning foundations, robust AI, and applied/project components.

- [ ] Information Technology: connect ROS2, HDF5/LeRobot data conversion, WebSocket serving, and model integration to verified software, systems, ML, vision, or project resources.

- [ ] Big Data Technology: connect synchronization failures, dataset integrity, action-token data, and serving scale to verified big-data systems, analytics, and ML resources.

- [ ] Mechanical Engineering: connect kinematics, calibration, workspace validation, and servo behavior to verified control, robotics, mechatronics, design, or project resources.

- [ ] Build and validate the five HKUST keys with --no-pdf and --only, then remove generic prestige language and any unpublished MEng claim.

- [ ] Commit the HKUST modules.

~~~bash
git add applications_2027/content/programs/hkust
git commit -m "docs: tailor statements for HKUST programs"
~~~

### Task 18: Draft and Validate the Five PolyU Modules

**Files:**

- Create: applications_2027/content/programs/polyu/intelligent_robotics_engineering.tex
- Create: applications_2027/content/programs/polyu/agentic_ai_systems.tex
- Create: applications_2027/content/programs/polyu/information_technology.tex
- Create: applications_2027/content/programs/polyu/artificial_intelligence_big_data_computing.tex
- Create: applications_2027/content/programs/polyu/smart_manufacturing.tex

- [ ] Intelligent Robotics Engineering: combine Embodied Robot Intelligence with Robot Motion Planning or Advanced Control and one mechanism/HRI/dissertation resource. Tie them to the action-representation/execution interface.

- [ ] Agentic AI Systems: connect Hermite, OpenPI, and real-robot policy serving to end-to-end agents, reasoning/large models, embedded or robotic systems, and the zero-to-physical capstone.

- [ ] Information Technology: connect synchronization, modular ROS2 software, model serving, and integration testing to verified advanced-IT and project/dissertation routes.

- [ ] Artificial Intelligence and Big Data Computing: connect action tokenization, evaluation, data quality, and scalable learning to the verified compulsory/elective structure and dissertation option.

- [ ] Smart Manufacturing: connect the weld-seam HMI/digital twin and CR5 integration to cyber-physical Industry 4.0 systems, data analytics, advanced manufacturing, and industrial HRI/automation.

- [ ] Build and validate the five PolyU keys. Verify that all application_ready filenames omit -provisional and that every cited title matches the 2027/28 matrix.

- [ ] Commit the PolyU modules.

~~~bash
git add applications_2027/content/programs/polyu
git commit -m "docs: tailor statements for PolyU programs"
~~~

### Task 19: Draft and Validate the Four CityUHK Modules

**Files:**

- Create: applications_2027/content/programs/cityu/artificial_intelligence.tex
- Create: applications_2027/content/programs/cityu/computer_science.tex
- Create: applications_2027/content/programs/cityu/computer_information_engineering.tex
- Create: applications_2027/content/programs/cityu/mechanical_engineering.tex

- [ ] Artificial Intelligence: choose one verified stream rather than listing all three. Use Autonomous Driving only if the argument is about embodied perception/control transfer; use Trustworthy or Generative AI only if its official resources directly address reliable policy learning.

- [ ] Computer Science: connect the ongoing CS degree and robot-learning stack to the verified AI/data pathway plus a project, internship, or guided-study option.

- [ ] Computer and Information Engineering: connect synchronized sensing, communications, signal/data representation, and system integration to verified CIE resources.

- [ ] Mechanical Engineering: use the verified Robotics stream to connect kinematics, control, and real-robot deployment, with one project or experiential resource.

- [ ] Build and validate the four CityUHK keys. Check that neither CityU nor another legacy abbreviation appears unless the current official program uses it; use CityUHK consistently in prose.

- [ ] Commit the CityUHK modules.

~~~bash
git add applications_2027/content/programs/cityu
git commit -m "docs: tailor statements for CityUHK programs"
~~~

### Task 20: Draft and Validate the Three NUS Modules

**Files:**

- Create: applications_2027/content/programs/nus/robotics.tex
- Create: applications_2027/content/programs/nus/data_science_machine_learning.tex
- Create: applications_2027/content/programs/nus/mechanical_engineering.tex

- [ ] Robotics: connect action representation, control semantics, perception, and real-robot validation to the verified robotics core and project/experiential structure.

- [ ] Data Science and Machine Learning: focus on representation, dataset validation, rigorous evaluation, and scalable learning. Use Hermite and the CR5 data pipeline as evidence without overstating robotics-specific curriculum.

- [ ] Mechanical Engineering: connect digital twins, kinematics, CR5 integration, and automation goals to verified project options, ME5888M if current, and a coherent control/mechatronics/manufacturing pathway.

- [ ] Build and validate the three NUS keys. Recheck that the DSML filename status agrees with the live August 2027 source.

- [ ] Commit the NUS modules.

~~~bash
git add applications_2027/content/programs/nus
git commit -m "docs: tailor statements for NUS programs"
~~~

### Task 21: Draft and Validate the Three NTU Modules

**Files:**

- Create: applications_2027/content/programs/ntu/robotics_intelligent_systems.tex
- Create: applications_2027/content/programs/ntu/computer_control_automation.tex
- Create: applications_2027/content/programs/ntu/signal_processing_machine_learning.tex

- [ ] Robotics and Intelligent Systems: connect CR5 and Hermite to verified robotics, perception, control, learning, autonomy, and project resources. Keep the emphasis on their interaction.

- [ ] Computer Control & Automation: center the module on why apparently faster non-blocking execution destabilized the learned controller, then connect that gap to verified advanced control, automation, robotics, and project resources.

- [ ] Signal Processing and Machine Learning: connect synchronized RGB-D/state/action data and Hermite action representation to verified signal modeling, estimation, vision, ML, or project resources. Do not describe it as a robotics curriculum.

- [ ] Build and validate the three NTU keys. Confirm NTU MSc Artificial Intelligence appears nowhere in generated statements or output paths.

- [ ] Commit the NTU modules.

~~~bash
git add applications_2027/content/programs/ntu
git commit -m "docs: tailor statements for NTU programs"
~~~

### Task 22: Generate All 25 Entry Files and Markdown Outputs

**Files:**

- Generate: applications_2027/statements/*.tex
- Generate: applications_2027/output/markdown/*.md
- Modify if required by evidence: applications_2027/config/programs.json
- Modify if required by an official strict limit: a program-specific compressed derivative documented in the verification matrix

- [ ] Run the complete unit suite before generation.

~~~bash
cd applications_2027
python3 -m unittest discover -s tests -v
~~~

Expected: all tests pass.

- [ ] Generate all entry and Markdown files without PDFs.

~~~bash
python3 scripts/build_statements.py --no-pdf
find statements -maxdepth 1 -name '*.tex' | wc -l
find output/markdown -maxdepth 1 -name '*.md' | wc -l
~~~

Expected: 25 and 25.

- [ ] Run content validation.

~~~bash
python3 scripts/validate_statements.py
~~~

Expected: 25 PASS lines and final summary PASS: 25 programs.

- [ ] If a verified official limit is below the default 850-950-word body, create a compressed derivative that follows the accepted compression order: remove secondary experience, reduce implementation detail, keep one primary experience, preserve program fit and career goal. Record the derivative path in the manifest and teach the builder to use it for only that key. Add a regression test proving other programs still use the canonical base.

- [ ] Inspect all filenames and status suffixes against the matrix.

~~~bash
python3 - <<'PY'
import json
from pathlib import Path
root = Path(".")
programs = json.loads((root / "config" / "programs.json").read_text())["programs"]
for p in programs:
    stem = p["key"] + ("-provisional" if p["output_status"] == "provisional" else "")
    assert (root / "output" / "markdown" / f"{stem}.md").exists(), stem
print("25 status-aware Markdown files present")
PY
~~~

- [ ] Commit generated entry files and Markdown outputs. Do not commit build intermediates.

~~~bash
git add applications_2027/statements applications_2027/output/markdown applications_2027/config/programs.json applications_2027/scripts applications_2027/tests
git commit -m "build: assemble 25 personal statements"
~~~

### Task 23: Compile and Mechanically Validate All 25 PDFs

**Files:**

- Generate: applications_2027/output/pdf/*.pdf
- Generate but do not commit: applications_2027/build/

- [ ] Confirm tools before compiling.

~~~bash
command -v latexmk
command -v xelatex
command -v pdftotext
command -v pdfinfo
command -v pdftoppm
~~~

Expected: five executable paths.

- [ ] Compile all statements.

~~~bash
cd applications_2027
python3 scripts/build_statements.py
find output/pdf -maxdepth 1 -name '*.pdf' | wc -l
~~~

Expected: 25 PDFs and no latexmk failure.

- [ ] Run full validation with PDF parity.

~~~bash
python3 scripts/validate_statements.py --require-pdfs
~~~

Expected: 25 PASS lines and final summary PASS: 25 programs.

- [ ] Verify page counts and metadata.

~~~bash
for pdf in output/pdf/*.pdf; do
  pages=$(pdfinfo "$pdf" | awk '/^Pages:/ {print $2}')
  test "$pages" -ge 1 -a "$pages" -le 2 || {
    echo "Unexpected page count: $pdf ($pages)"
    exit 1
  }
done
echo "All PDFs are one or two pages"
~~~

Expected: All PDFs are one or two pages.

- [ ] Scan compile logs for layout or font defects.

~~~bash
rg -n 'Overfull|Underfull|Missing character|LaTeX Error|Emergency stop' build
~~~

Expected: no output. Treat meaningful Underfull warnings as defects rather than ignoring them automatically.

- [ ] Commit only final PDFs.

~~~bash
git add applications_2027/output/pdf
git commit -m "build: render 25 personal statement PDFs"
~~~

### Task 24: Perform Content-Level Cross-Statement QA

**Files:**

- Modify as needed: applications_2027/content/base/*.tex
- Modify as needed: applications_2027/content/programs/**/*.tex
- Regenerate: applications_2027/statements/*.tex
- Regenerate: applications_2027/output/markdown/*.md
- Regenerate: applications_2027/output/pdf/*.pdf

- [ ] Create a private review grid from the 25 outputs with columns Opening, Primary experience 1, Primary experience 2, Program resources, Career link, Distinctive sentence, Fact-bank claim IDs, and concern. Do not add this temporary grid to Git unless it contains durable evidence worth preserving.

- [ ] Read the six robotics statements together. Verify they share identity but differ in the learning/control/system gap each program addresses.

- [ ] Read the fourteen CS/AI statements together. Ensure Big Data, IT, CIE, DSML, signal processing, agentic AI, and general CS are not all described as interchangeable AI programs.

- [ ] Read the five mechanical/smart-manufacturing statements together. Ensure each preserves physical-system depth and does not merely reuse the CS/AI fit paragraph.

- [ ] Search every canonical and generated source for forbidden inflation and template residue.

~~~bash
rg -n -i \
  'submitted paper|published paper|first author|completed.*computer science|mIoU|Target University|Student Name Here|Program Name Here|TBD|TODO|FIXME|lorem ipsum|world-class|prestigious|top-ranked' \
  content statements output/markdown
~~~

Expected: no unsupported or generic matches. A legitimate phrase must be manually justified against the fact bank.

- [ ] Search for school contamination, including common abbreviations and full names. Use the validator result as the gate, not visual intuition.

- [ ] Confirm the weld metric is always segmentation accuracy, the CR5 range remains 2.57%-4.74%, Hermite remains a not-submitted working paper, and the second CS degree remains ongoing with expected June 2027 completion.

- [ ] Rebuild and rerun unit, content, and PDF validation after every correction.

~~~bash
python3 -m unittest discover -s tests -v
python3 scripts/build_statements.py
python3 scripts/validate_statements.py --require-pdfs
~~~

Expected: all commands pass.

- [ ] Commit the reviewed prose and regenerated outputs as one traceable QA change.

~~~bash
git add applications_2027/content applications_2027/statements applications_2027/output/markdown applications_2027/output/pdf
git commit -m "docs: complete cross-statement content review"
~~~

### Task 25: Render and Visually Inspect Every PDF Page

**Files:**

- Generate outside Git: /private/tmp/mine_ps_2027_preview/
- Modify as needed: source and regenerated outputs under applications_2027

- [ ] Create a fresh explicit preview directory and render every PDF at 150 DPI.

~~~bash
preview_dir=/private/tmp/mine_ps_2027_preview
test "$preview_dir" = /private/tmp/mine_ps_2027_preview
rm -rf "$preview_dir"
mkdir -p "$preview_dir"
for pdf in output/pdf/*.pdf; do
  stem=$(basename "$pdf" .pdf)
  mkdir -p "$preview_dir/$stem"
  pdftoppm -png -r 150 "$pdf" "$preview_dir/$stem/page"
done
find "$preview_dir" -name '*.png' | wc -l
~~~

Expected: between 25 and 50 rendered page images.

- [ ] Inspect every rendered page with the image-viewing tool. For each PDF verify:

  - correct applicant, university, and program in the header;
  - no clipping, overlap, broken glyph, or missing paragraph;
  - no orphaned one-line final page;
  - balanced whitespace and readable density;
  - consistent margins, page number, and header behavior;
  - provisional status is visible in the filename and verification matrix, not inserted into the application prose.

- [ ] Fix source prose or layout only at the smallest responsible layer. A content overflow is fixed in the relevant prose; a global spacing defect is fixed in the copied applications_2027/easier_ps.cls, never in the user's original class.

- [ ] Rebuild, rerender, and reinspect every PDF affected by a global layout change; reinspect only the affected program for a local prose correction.

- [ ] Rerun the complete verification gate:

~~~bash
python3 -m unittest discover -s tests -v
python3 scripts/build_statements.py
python3 scripts/validate_statements.py --require-pdfs
~~~

Expected: all tests pass and all 25 programs pass.

- [ ] Commit any verified visual corrections and regenerated artifacts.

~~~bash
git add applications_2027/easier_ps.cls applications_2027/content applications_2027/statements applications_2027/output/markdown applications_2027/output/pdf
git commit -m "style: finish visual QA for statement portfolio"
~~~

### Task 26: Perform the Official-Source Freshness Gate

**Files:**

- Modify: applications_2027/facts/program_verification_matrix.md
- Modify: applications_2027/config/programs.json
- Modify as needed: applications_2027/content/programs/**/*.tex
- Regenerate as needed: statements and outputs

- [ ] Reopen all 25 primary official pages on the final QA date. Search each official university domain for a newer 2027/28 catalog, admissions page, renamed program, revised curriculum, or portal-specific PS limit.

- [ ] Update Verified on for every row that was actually reopened. Preserve the earlier page year in Notes when no 2027/28 replacement exists.

- [ ] Change provisional to application_ready only when the accepted status rule is satisfied. A program announcement without a catalog/application requirement remains provisional.

- [ ] If a program name or cited resource changed, update the matrix, manifest, module, generated entry, Markdown filename, and PDF filename together. Remove superseded generated files only after resolving their exact paths and confirming the new outputs exist.

- [ ] Run the full verification gate again.

~~~bash
cd applications_2027
python3 -m unittest discover -s tests -v
python3 scripts/build_statements.py
python3 scripts/validate_statements.py --require-pdfs
~~~

Expected: all tests pass and all 25 programs pass.

- [ ] Confirm there are exactly 25 current Markdown files and 25 current PDFs, with no duplicate old-status filenames.

~~~bash
test "$(find output/markdown -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')" = 25
test "$(find output/pdf -maxdepth 1 -name '*.pdf' | wc -l | tr -d ' ')" = 25
echo "25 Markdown files and 25 PDFs confirmed"
~~~

- [ ] Commit freshness changes.

~~~bash
git add applications_2027/facts/program_verification_matrix.md applications_2027/config/programs.json applications_2027/content/programs applications_2027/statements applications_2027/output/markdown applications_2027/output/pdf
git commit -m "docs: refresh 2027 program verification"
~~~

### Task 27: Write the Delivery README and Run the Final Acceptance Check

**Files:**

- Create: applications_2027/README.md

- [ ] Write a concise README containing:

  - applicant and Fall 2027 scope;
  - three-base architecture;
  - list of all 25 program keys and current application_ready/provisional status;
  - exact build, test, validate, and render commands;
  - explanation of the -provisional suffix;
  - location and meaning of the fact bank and verification matrix;
  - warning that provisional programs require a final portal-limit check before submission;
  - statement that Markdown contains the same body prose as PDF.

- [ ] Run the final acceptance commands from a clean process:

~~~bash
cd /Users/xingjianming/profile/mine_PS/applications_2027
python3 -m unittest discover -s tests -v
python3 scripts/build_statements.py
python3 scripts/validate_statements.py --require-pdfs
test "$(find statements -maxdepth 1 -name '*.tex' | wc -l | tr -d ' ')" = 25
test "$(find output/markdown -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')" = 25
test "$(find output/pdf -maxdepth 1 -name '*.pdf' | wc -l | tr -d ' ')" = 25
~~~

Expected: unit tests pass, validator reports PASS: 25 programs, and all three count checks succeed.

- [ ] Review Git scope before the final commit.

~~~bash
cd /Users/xingjianming/profile/mine_PS
git status --short
git diff --check
git diff --stat HEAD
~~~

Expected: the user's pre-existing easier_ps and template/draft changes remain unstaged; no whitespace errors exist in the new work.

- [ ] Commit the README only after acceptance succeeds.

~~~bash
git add applications_2027/README.md
git commit -m "docs: document 2027 statement portfolio"
~~~

- [ ] Record final evidence for handoff: latest commit hash, test count, 25/25 validator result, 25 Markdown count, 25 PDF count, number of application_ready programs, number of provisional programs, and the exact paths to README, verification matrix, Markdown directory, and PDF directory.

## Final Acceptance Criteria

- [ ] Three direction bases each read as a coherent independent narrative.
- [ ] Twenty-five modules are factually verified and materially program-specific.
- [ ] All applicant claims trace to the fact bank.
- [ ] All program claims trace to a current official URL and verification date.
- [ ] Exactly 25 generated LaTeX entries, 25 Markdown bodies, and 25 PDFs exist.
- [ ] Every provisional file has the -provisional suffix; no application-ready file does.
- [ ] Unit tests, content validation, PDF text parity, and page-count checks all pass.
- [ ] Every rendered page has been visually inspected.
- [ ] No target-school contamination, unsupported metric, completed-degree misstatement, publication-status inflation, template residue, or generic prestige language remains.
- [ ] Existing user changes outside applications_2027 are untouched and unstaged.
