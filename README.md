# STAT-5243-Project-1-Team-2

This branch is reorganized into two top-level folders for clarity.

## 1) Project Deliverables
- `Project Deliverables/Datasets/`
  - `reddit_wsb.csv` (raw dataset)
  - `reddit_wsb_cleaned.csv` (cleaned dataset)
- `Project Deliverables/Code Files/`
  - Full workflow scripts and dependencies
  - See `Project Deliverables/Code Files/README.md` for run steps
- `Project Deliverables/Report/`
  - `main_report.tex`
  - `Project1_Final_Submission.ipynb`
  - `artifacts/` (PNG + JSON outputs)
  - `sections/` and report sources
  - `submission/STAT5243_Project1_Team2_Final.pdf`

## 2) Project Workspace
- `Project Workspace/Source Files/` (working notebooks and narrative source text files)
- `Project Workspace/qa/` (QA matrices/checklists/diff audits)
- `Project Workspace/session_logs/` (session-by-session execution logs)

## Quick Run
```bash
python3 -m pip install -r "Project Deliverables/Code Files/requirements.txt"
bash "Project Deliverables/Code Files/run_full_workflow.sh"
```

## Build Report PDF (LaTeX, recommended)
```bash
cd "Project Deliverables/Report"
pdflatex -interaction=nonstopmode main_report.tex
pdflatex -interaction=nonstopmode main_report.tex
mv main_report.pdf submission/STAT5243_Project1_Team2_Final.pdf
```

## Build Report PDF (Notebook, optional)
```bash
cd "Project Deliverables/Report"
jupyter nbconvert --to pdf Project1_Final_Submission.ipynb --output submission/STAT5243_Project1_Team2_Final.pdf
```
