#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DELIVERABLES_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

python3 "$SCRIPT_DIR/full_workflow.py" \
  --raw "$DELIVERABLES_DIR/Datasets/reddit_wsb.csv" \
  --cleaned-out reddit_wsb_cleaned_full_workflow.csv \
  --out-dir "$DELIVERABLES_DIR/Report"
