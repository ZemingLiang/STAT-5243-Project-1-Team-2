"""Cleaning and preprocessing workflow for reddit_wsb.csv.

This script mirrors the core branch workflow in script form for reproducibility.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r"http[s]?://\\S+", "", text)
    text = re.sub(r"\\[([^\\]]+)\\]\\([^\\)]+\\)", r"\\1", text)
    text = re.sub(r"[*_]{1,3}", "", text)
    text = re.sub(r"#{1,6}\\s*", "", text)
    text = (
        text.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&nbsp;", " ")
        .replace("&#x200B;", "")
    )
    text = re.sub(r"\\s+", " ", text).strip()
    return text


def infer_post_type(url: str) -> str:
    if not isinstance(url, str):
        return "other"
    u = url.lower()
    if "v.redd.it" in u or "youtube" in u or "youtu.be" in u:
        return "video"
    if "i.redd.it" in u or u.endswith((".png", ".jpg", ".jpeg", ".gif")):
        return "image"
    if "reddit.com/r/wallstreetbets/comments" in u:
        return "text"
    return "link"


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["timestamp"] = pd.to_datetime(out["timestamp"], errors="coerce")
    out = out.dropna(subset=["timestamp"]).copy()
    out["date"] = out["timestamp"].dt.date.astype(str)
    out["hour"] = out["timestamp"].dt.hour
    out["day_of_week"] = out["timestamp"].dt.day_name()

    out["title_clean"] = out["title"].fillna("").map(clean_text)
    out["body_clean"] = out["body"].fillna("").map(clean_text)
    out["title_nlp"] = out["title_clean"].str.lower()

    out["has_body"] = out["body"].fillna("").str.strip().ne("")
    out["title_length"] = out["title_clean"].str.len()

    out["post_type"] = out["url"].map(infer_post_type)
    freq = out["post_type"].value_counts(normalize=True)
    keep = set(freq[freq >= 0.05].index)
    out["post_type_lumped"] = out["post_type"].where(out["post_type"].isin(keep), "Other")

    out["score_log"] = np.log1p(out["score"].clip(lower=0))
    out["comms_num_log"] = np.log1p(out["comms_num"].clip(lower=0))

    numeric_for_scaling = ["score_log", "comms_num_log", "title_length", "hour"]
    z = StandardScaler().fit_transform(out[numeric_for_scaling])
    m = MinMaxScaler().fit_transform(out[numeric_for_scaling])
    for i, col in enumerate(numeric_for_scaling):
        out[f"{col}_zscore"] = z[:, i]
        out[f"{col}_minmax"] = m[:, i]

    out["day_of_week_encoded"] = out["day_of_week"].astype("category").cat.codes
    out["type_image"] = out["post_type_lumped"].eq("image")
    out["type_text"] = out["post_type_lumped"].eq("text")

    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="reddit_wsb.csv")
    parser.add_argument("--output", default="reddit_wsb_cleaned_script.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw = pd.read_csv(args.input)
    cleaned = build_features(raw)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(args.output, index=False)
    print(f"Saved cleaned dataset to {args.output} with shape {cleaned.shape}")


if __name__ == "__main__":
    main()
