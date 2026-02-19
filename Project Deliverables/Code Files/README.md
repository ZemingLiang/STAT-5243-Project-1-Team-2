# Code Files

This folder keeps only the final integrated workflow code.

## Files
- `full_workflow.py`: end-to-end workflow (load -> clean -> EDA -> feature diagnostics)
- `requirements.txt`: Python dependencies

## Run
```bash
python3 -m pip install -r "Project Deliverables/Code Files/requirements.txt"
python3 "Project Deliverables/Code Files/full_workflow.py"
```

## CLI Options
```bash
python3 "Project Deliverables/Code Files/full_workflow.py" \
  --raw "Project Deliverables/Datasets/reddit_wsb.csv" \
  --out-dir "Project Workspace/Supporting Materials/Generated Outputs" \
  --cleaned-out "reddit_wsb_cleaned_full_workflow.csv" \
  --sample-size 20000
```

## Input/Output Defaults
- Input dataset defaults to `Project Deliverables/Datasets/reddit_wsb.csv`
- Output defaults to `Project Workspace/Supporting Materials/Generated Outputs/`
- Output artifacts include:
  - cleaned CSV (`--cleaned-out` filename under `--out-dir`)
  - figure exports under `artifacts/figures/`
  - JSON summaries under `artifacts/json/`

## Data Contract
The raw input must include these columns:
- `title`
- `body`
- `url`
- `score`
- `comms_num`
- `timestamp`
