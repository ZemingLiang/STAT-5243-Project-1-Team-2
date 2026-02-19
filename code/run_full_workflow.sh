#!/usr/bin/env bash
set -euo pipefail

python3 code/full_workflow.py \
  --raw reddit_wsb.csv \
  --cleaned-out reddit_wsb_cleaned_full_workflow.csv \
  --out-dir .
