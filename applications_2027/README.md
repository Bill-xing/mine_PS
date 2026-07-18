# Fall 2027 Personal-Statement Portfolio

This directory contains Jianming Xing's English personal statements for 25 Fall 2027 taught-master's targets at CUHK, HKUST, PolyU, CityUHK, NUS, and NTU. The portfolio covers robotics and embodied AI, computer science and AI, and mechanical engineering and smart manufacturing.

## Content architecture

The canonical long-form prose is split into three direction bases under `content/base/` and 25 program-specific modules under `content/programs/`. For 22 programs, the builder combines one base with one module. The three NTU records use compressed derivatives under `content/derivatives/ntu/` as their generated portal responses because the live COAL reason/motivation field has a 2,000-character limit including spaces. Their full base-plus-module versions remain the canonical long-form sources.

`config/programs.json` is the machine-readable manifest. It defines exactly 25 program keys, source selection, output status, official limits, and status-aware filenames. The builder produces exactly 25 LaTeX entry points, 25 Markdown bodies, and 25 PDFs; it does not create an additional main output for any long-form NTU source.

The Markdown file and the corresponding PDF contain the same statement body prose. PDF headers, page numbers, and other layout text are not part of the Markdown body.

## Program inventory

`application_ready` means that a current official Fall 2027, August 2027, or 2027/28 source supports the program identity and relevant application constraint recorded in the verification matrix. `provisional` means that the portfolio still relies on a prior-cycle page, announcement-only evidence, conflicting official sources, an incompatible intake, or another unresolved application constraint. Every provisional Markdown and PDF filename ends in `-provisional`; application-ready filenames do not.

| # | Program key | Program | Status |
| ---: | --- | --- | --- |
| 1 | `cuhk-robotics` | CUHK MSc in Robotics | `provisional` |
| 2 | `cuhk-mechanical-automation-engineering` | CUHK MSc in Mechanical and Automation Engineering | `provisional` |
| 3 | `cuhk-artificial-intelligence` | CUHK MSc in Artificial Intelligence | `provisional` |
| 4 | `cuhk-computer-science` | CUHK MSc in Computer Science | `provisional` |
| 5 | `cuhk-information-engineering` | CUHK MSc in Information Engineering | `provisional` |
| 6 | `hkust-robotics-embodied-ai` | HKUST MEng in Robotics and Embodied AI | `provisional` |
| 7 | `hkust-artificial-intelligence` | HKUST MSc in Artificial Intelligence | `provisional` |
| 8 | `hkust-information-technology` | HKUST MSc in Information Technology | `provisional` |
| 9 | `hkust-big-data-technology` | HKUST MSc in Big Data Technology | `provisional` |
| 10 | `hkust-mechanical-engineering` | HKUST MSc in Mechanical Engineering | `provisional` |
| 11 | `polyu-intelligent-robotics-engineering` | PolyU MSc in Intelligent Robotics Engineering | `application_ready` |
| 12 | `polyu-agentic-ai-systems` | PolyU MSc in Agentic AI Systems | `application_ready` |
| 13 | `polyu-information-technology` | PolyU MSc in Information Technology | `application_ready` |
| 14 | `polyu-artificial-intelligence-big-data-computing` | PolyU MSc in Artificial Intelligence and Big Data Computing | `application_ready` |
| 15 | `polyu-smart-manufacturing` | PolyU MSc in Smart Manufacturing | `application_ready` |
| 16 | `cityu-artificial-intelligence` | CityUHK MSc in Artificial Intelligence | `provisional` |
| 17 | `cityu-computer-science` | CityUHK MSc in Computer Science | `provisional` |
| 18 | `cityu-computer-information-engineering` | CityUHK MSc in Computer and Information Engineering | `provisional` |
| 19 | `cityu-mechanical-engineering` | CityUHK MSc in Mechanical Engineering | `provisional` |
| 20 | `nus-robotics` | NUS MSc in Robotics | `provisional` |
| 21 | `nus-data-science-machine-learning` | NUS MSc in Data Science and Machine Learning | `application_ready` |
| 22 | `nus-mechanical-engineering` | NUS MSc in Mechanical Engineering | `provisional` |
| 23 | `ntu-robotics-intelligent-systems` | NTU MSc in Robotics and Intelligent Systems | `provisional` |
| 24 | `ntu-computer-control-automation` | NTU MSc in Computer Control & Automation | `application_ready` |
| 25 | `ntu-signal-processing-machine-learning` | NTU MSc in Signal Processing and Machine Learning | `application_ready` |

Current total: 8 `application_ready` and 17 `provisional` programs.

## Evidence and editing rules

- `facts/applicant_fact_bank.md` is the auditable authority for applicant history, project roles, quantitative claims, claim boundaries, and approved career framing. Do not add or strengthen an applicant claim without support there.
- `facts/program_verification_matrix.md` records official program URLs, intake evidence, statement requirements and limits, selected fit resources, verification dates, status decisions, and unresolved conflicts. Admissions information is mutable; update this matrix before changing a program's status or claims.
- `config/programs.json` selects the exact canonical sources and output filename for each program. Edit canonical prose rather than generated files, then rebuild.

## Build and verification

Run these commands after the worktree is integrated at its normal repository path. The explicit PATH selects the user-space TeX Live installation required for XeLaTeX builds.

```bash
cd /Users/xingjianming/profile/mine_PS/applications_2027
export PATH="/Users/xingjianming/.local/texlive/2026/bin/universal-darwin:$PATH"
python3 -m unittest discover -s tests -v
python3 scripts/build_statements.py
python3 scripts/validate_statements.py --require-pdfs
test "$(find statements -maxdepth 1 -name '*.tex' | wc -l | tr -d ' ')" = 25
test "$(find output/markdown -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')" = 25
test "$(find output/pdf -maxdepth 1 -name '*.pdf' | wc -l | tr -d ' ')" = 25
```

Render every PDF to PNG at 150 DPI for visual inspection:

```bash
cd /Users/xingjianming/profile/mine_PS/applications_2027
preview_dir=$(mktemp -d /private/tmp/mine_ps_2027_preview.XXXXXX)
printf 'Preview directory: %s\n' "$preview_dir"
for pdf in output/pdf/*.pdf; do
  stem=$(basename "$pdf" .pdf)
  mkdir -p "$preview_dir/$stem"
  pdftoppm -png -r 150 "$pdf" "$preview_dir/$stem/page"
done
find "$preview_dir" -name '*.png' | wc -l
```

## Submission cautions

- Recheck every `provisional` program's live portal, compatible intake, program title, required document route, and word/character limit before submission. Remove the suffix only after synchronizing verified evidence, manifest status, and regenerated outputs.
- Treat `application_ready` as evidence status, not permission to submit without review. Confirm the live fields, upload route, and limits again on the actual submission date.
- NTU's current COAL component exposes a profile-scoped, program-neutral “Reason for pursuing programme” field with a 2,000-character limit including spaces. Because the public component does not expose a program parameter, multiple NTU applications may share one profile value. Confirm in the live portal whether the response can vary by program before using the three distinct derivatives.
- The currently published NTU MSc in Robotics and Intelligent Systems intake is January 2027, before the applicant's expected June 2027 completion of the second bachelor's degree. No compatible August 2027 RIS intake was found at the latest verification, so the output remains provisional. Its main Markdown/PDF is the compressed portal response; `content/base/robotics_embodied_ai.tex` plus `content/programs/ntu/robotics_intelligent_systems.tex` remains the clear-SOP source if a later portal provides a separate upload or a compatible intake opens.
- NTU MSc in Artificial Intelligence is excluded from this 25-program scope because the current TOEFL score is 93, no retake is planned, and no official English-medium certification has yet been verified. This is a scope decision, not a categorical ineligibility finding; reassess it if an acceptable official medium-of-instruction certificate becomes available or the admissions rules change.
