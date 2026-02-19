"""EDA workflow script for reddit_wsb_cleaned.csv.

Generates summary statistics, advanced diagnostics, and figure outputs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kruskal, spearmanr

SCRIPT_DIR = Path(__file__).resolve().parent
DELIVERABLES_DIR = SCRIPT_DIR.parent
DEFAULT_INPUT = DELIVERABLES_DIR / "Datasets" / "reddit_wsb_cleaned.csv"
DEFAULT_FIG_DIR = DELIVERABLES_DIR / "Report" / "artifacts" / "figures"
DEFAULT_JSON_DIR = DELIVERABLES_DIR / "Report" / "artifacts" / "json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--fig-dir", default=str(DEFAULT_FIG_DIR))
    parser.add_argument("--json-dir", default=str(DEFAULT_JSON_DIR))
    return parser.parse_args()


def save_basic_figures(df: pd.DataFrame, fig_dir: Path) -> None:
    fig_dir.mkdir(parents=True, exist_ok=True)
    numeric_cols = ["score", "comms_num", "score_log", "comms_num_log", "title_length", "hour"]
    for col in numeric_cols:
        if col not in df.columns:
            continue
        plt.figure(figsize=(8, 5))
        plt.hist(df[col].dropna(), bins=50)
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(fig_dir / f"03_eda_{col}_distribution.png", dpi=200)
        plt.close()


def save_advanced_stats(df: pd.DataFrame, json_dir: Path, fig_dir: Path) -> None:
    json_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    advanced = {}
    if {"score_log", "comms_num_log"}.issubset(df.columns):
        rho, pval = spearmanr(df["score_log"], df["comms_num_log"], nan_policy="omit")
        advanced["spearman_score_vs_comments"] = {"rho": float(rho), "p_value": float(pval)}

    if {"post_type_lumped", "score_log"}.issubset(df.columns):
        groups = [grp["score_log"].dropna().values for _, grp in df.groupby("post_type_lumped") if len(grp) > 0]
        if len(groups) > 1:
            stat, pval = kruskal(*groups)
            advanced["kruskal_score_by_post_type"] = {"statistic": float(stat), "p_value": float(pval)}

    if "score_log_zscore" in df.columns:
        outlier_rate = (df["score_log_zscore"].abs() >= 3).mean()
        advanced["score_log_outlier_rate_abs_ge_3"] = float(outlier_rate)

    (json_dir / "03_eda_advanced_stats.json").write_text(json.dumps(advanced, indent=2))


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input)
    fig_dir = Path(args.fig_dir)
    json_dir = Path(args.json_dir)
    save_basic_figures(df, fig_dir)
    save_advanced_stats(df, json_dir, fig_dir)
    print("EDA workflow artifacts generated")


if __name__ == "__main__":
    main()
