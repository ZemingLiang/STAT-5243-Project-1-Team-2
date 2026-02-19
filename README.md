# STAT-5243-Project-1-Team-2

This branch is reorganized into two top-level folders for clarity.

## 1) Project Deliverables
- `Project Deliverables/Datasets/`
  - `reddit_wsb.csv` (raw dataset)
  - `reddit_wsb_cleaned.csv` (cleaned dataset)
- `Project Deliverables/Code Files/`
  - `full_workflow.py` (single integrated workflow code)
  - `requirements.txt`
  - `README.md` (run instructions)
- `Project Deliverables/Report/`
  - `Project1_Final_Submission.ipynb`
  - `STAT5243_Project1_Team2_Final.pdf`

This folder intentionally contains only final deliverable-facing artifacts.

## 2) Project Workspace
- `Project Workspace/Source Files/` (working notebooks and narrative source text files)
- `Project Workspace/Supporting Materials/`
  - `Code Files/` (helper/branch-specific scripts)
  - `Report Sources/` (LaTeX sections, figures, JSON metadata, manifests)
- `Project Workspace/qa/` (QA matrices/checklists/diff audits)
- `Project Workspace/session_logs/` (session-by-session execution logs)

## Quick Run (Integrated Workflow)
```bash
python3 -m pip install -r "Project Deliverables/Code Files/requirements.txt"
python3 "Project Deliverables/Code Files/full_workflow.py"
```

## Reproducibility Verification
Expected key outputs after setup/integration:
- `Project Deliverables/Datasets/reddit_wsb.csv`
- `Project Deliverables/Datasets/reddit_wsb_cleaned.csv`
- `Project Deliverables/Code Files/full_workflow.py`
- `Project Deliverables/Report/Project1_Final_Submission.ipynb`
- `Project Deliverables/Report/STAT5243_Project1_Team2_Final.pdf`
- `Project Workspace/Supporting Materials/Report Sources/artifacts/figures/05_feature_ablation_comparison.png`
- `Project Workspace/Supporting Materials/Report Sources/artifacts/json/05_feature_ablation_table.json`
- `Project Workspace/qa/evidence_registry_report_depth.json`

Single validation command:
```bash
required=(
  "Project Deliverables/Datasets/reddit_wsb.csv"
  "Project Deliverables/Datasets/reddit_wsb_cleaned.csv"
  "Project Deliverables/Code Files/full_workflow.py"
  "Project Deliverables/Report/Project1_Final_Submission.ipynb"
  "Project Deliverables/Report/STAT5243_Project1_Team2_Final.pdf"
  "Project Workspace/Supporting Materials/Report Sources/artifacts/figures/05_feature_ablation_comparison.png"
  "Project Workspace/Supporting Materials/Report Sources/artifacts/json/05_feature_ablation_table.json"
  "Project Workspace/qa/evidence_registry_report_depth.json"
); missing=0; for f in "${required[@]}"; do [[ -f "$f" ]] || { echo "MISSING: $f"; missing=1; }; done; [[ $missing -eq 0 ]] && echo "PASS: all required outputs exist." || echo "FAIL: missing required outputs."
```

Pass condition:
- Command prints `PASS: all required outputs exist.` and no `MISSING:` lines.

## Build Report PDF (Notebook, optional)
```bash
cd "Project Deliverables/Report"
jupyter nbconvert --to pdf Project1_Final_Submission.ipynb --output STAT5243_Project1_Team2_Final.pdf
```

Note:
- Notebook-to-PDF conversion may fail on machines missing compatible `pandoc`/TeX toolchain.
- If conversion fails, use the checked-in final PDF (`Project Deliverables/Report/STAT5243_Project1_Team2_Final.pdf`) and the LaTeX source under `Project Workspace/Supporting Materials/Report Sources/`.
