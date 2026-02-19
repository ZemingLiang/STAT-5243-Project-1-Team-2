# STAT-5243-Project-1-Team-2

Final integrated deliverables for Project 1 are stored in this branch.

## Included Deliverables
- `reddit_wsb.csv` (raw dataset)
- `reddit_wsb_cleaned.csv` (cleaned/processed dataset)
- `code/full_workflow.py` (full end-to-end code workflow)
- `code/requirements.txt` (dependencies)
- `report/main_report.tex` (combined LaTeX report source)
- `report/Project1_Final_Submission.ipynb` (submission notebook source)
- `artifacts/figures/*.png` (individual figure exports)
- `artifacts/json/*.json` (per-figure and section-level metadata)
- `submission/STAT5243_Project1_Team2_Final.pdf` (final submission PDF)

## Run Instructions
```bash
python3 -m pip install -r code/requirements.txt
bash code/run_full_workflow.sh
```

## Build PDF from notebook
```bash
jupyter nbconvert --to pdf report/Project1_Final_Submission.ipynb --output ../submission/STAT5243_Project1_Team2_Final.pdf
```
