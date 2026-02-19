# Code Files

This folder contains the full Python workflow scripts for Project 1.

## Files
- `full_workflow.py`: end-to-end workflow (load -> clean -> EDA -> feature diagnostics)
- `cleaning_workflow.py`: cleaning/preprocessing script
- `eda_workflow.py`: EDA/statistical diagnostics script
- `feature_enhancement_workflow.py`: feature engineering/model diagnostics script
- `requirements.txt`: Python dependencies
- `run_full_workflow.sh`: one-command runner for end-to-end workflow

## Run
```bash
python3 -m pip install -r "Project Deliverables/Code Files/requirements.txt"
bash "Project Deliverables/Code Files/run_full_workflow.sh"
```

## Notes
- Script defaults are set to use files under `Project Deliverables/Datasets/` and output under `Project Deliverables/Report/`.
