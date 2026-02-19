# Final Team Handoff (Main-Final-Deliverable)

## What Was Improved in This Finalization Round
- Enforced release branch truth (`Main-Final-Deliverable`) and audited assignment deliverable contract.
- Upgraded root README front matter to prioritize the final PDF first and added submission quick links.
- Stabilized strict notebook-to-PDF build with a reproducible script and compatibility handling for pandoc 3.x.
- Added a canonical one-code notebook deliverable (`Project1_Full_Workflow_Code.ipynb`) that consolidates acquisition, cleaning, EDA, feature engineering, diagnostics, and ablation in one file.
- Expanded report narrative depth in intro/acquisition/summary/challenges sections with quantitative evidence references.
- Kept `full_workflow.py` as backup automation while switching grading contract to notebook-first code review.
- Added a rubric-perfect evidence matrix with explicit advanced-level justification per rubric category.
- Rebuilt final PDF using strict notebook build path and refreshed notebook/PDF consistency checks.
- Generated a hard-gate final release checklist with all critical gates passing.
- Upgraded submission notebook into a dense single-review artifact (57 cells, 5 code cells, 35 embedded figures including appendix evidence) and added a core claim traceability table.
- Enforced one-PDF + one-code-file grading contract in QA (`final_release_checklist.json`).

## Key New/Updated Files
- `README.md`
- `Project Deliverables/Code Files/Project1_Full_Workflow_Code.ipynb`
- `Project Deliverables/Code Files/full_workflow.py`
- `Project Deliverables/Code Files/README.md`
- `Project Deliverables/Report/build_report_pdf.sh`
- `Project Deliverables/Report/REPORT_BUILD_REQUIREMENTS.md`
- `Project Deliverables/Report/CODE_REFERENCE.md`
- `Project Deliverables/Report/Project1_Final_Submission.ipynb`
- `Project Deliverables/Report/STAT5243_Project1_Team2_Final.pdf`
- `Project Workspace/qa/deliverables_contract_audit.json`
- `Project Workspace/qa/strict_pdf_build_log.md`
- `Project Workspace/qa/rubric_perfect_score_matrix.json`
- `Project Workspace/qa/final_release_checklist.json`
- `Project Workspace/qa/final_submission_checklist.json`
- `Project Workspace/qa/notebook_pdf_consistency_report.md`
- `Project Workspace/qa/final_release_summary.md`

## Current Rubric/QA Status
- `Project Workspace/qa/final_release_checklist.json`: all critical gates = `pass`.
- `Project Workspace/qa/rubric_perfect_score_matrix.json`: evidence-validated `47/47` advanced coverage.
- Strict notebook-to-PDF build path: `PASS` via `Project Deliverables/Report/build_report_pdf.sh`.

## What to Submit to Courseworks
- Submit this file as the report PDF:
  - `Project Deliverables/Report/STAT5243_Project1_Team2_Final.pdf`

## Repository Deliverables to Keep Public
- Datasets:
  - `Project Deliverables/Datasets/reddit_wsb.csv`
  - `Project Deliverables/Datasets/reddit_wsb_cleaned.csv`
- Code:
  - `Project Deliverables/Code Files/Project1_Full_Workflow_Code.ipynb` (canonical one-code-file review artifact)
  - `Project Deliverables/Code Files/full_workflow.py`
  - `Project Deliverables/Code Files/README.md`
  - `Project Deliverables/Code Files/requirements.txt`
- Report assets:
  - `Project Deliverables/Report/Project1_Final_Submission.ipynb`
  - `Project Deliverables/Report/STAT5243_Project1_Team2_Final.pdf`
