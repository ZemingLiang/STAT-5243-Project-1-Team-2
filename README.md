# STAT-5243-Project-1-Team-2
Zeming Liang, Zuer Weng, Duoli Chen, Isaac Beers

## Cleaning and Preprocessing Branch

### Files
- `reddit_wsb.csv`: raw dataset
- `reddit_wsb_cleaned.csv`: cleaned dataset produced in notebook workflow
- `Cleaning-and-Preprocessing.ipynb`: full cleaning and preprocessing notebook
- `code/cleaning_workflow.py`: script-form reproducible pipeline
- `artifacts/figures/*.png`: exported cleaning/preprocessing figures
- `artifacts/json/*.json`: per-figure metadata and section summary

### Reproduce script output
```bash
python3 code/cleaning_workflow.py --input reddit_wsb.csv --output reddit_wsb_cleaned_script.csv
```
