"""End-to-end STAT 5243 Project 1 workflow.

Stages:
1) Data loading and acquisition checks
2) Cleaning and preprocessing
3) EDA summaries and core figures
4) Feature engineering and diagnostics
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

POS_WORDS = {
    "gain", "moon", "bull", "buy", "rocket", "win", "green", "profit", "up", "long", "calls", "squeeze"
}
NEG_WORDS = {
    "loss", "bear", "sell", "drop", "down", "red", "bagholder", "panic", "short", "puts", "crash"
}
SCRIPT_DIR = Path(__file__).resolve().parent
DELIVERABLES_DIR = SCRIPT_DIR.parent
DEFAULT_RAW = DELIVERABLES_DIR / "Datasets" / "reddit_wsb.csv"
DEFAULT_OUT_DIR = DELIVERABLES_DIR / "Report"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", default=str(DEFAULT_RAW))
    parser.add_argument("--cleaned-out", default="reddit_wsb_cleaned_full_workflow.csv")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--sample-size", type=int, default=20000)
    return parser.parse_args()


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
    return re.sub(r"\\s+", " ", text).strip()


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


def simple_sentiment(text: str) -> float:
    tokens = re.findall(r"[A-Za-z]{2,}", text.lower() if isinstance(text, str) else "")
    if not tokens:
        return 0.0
    pos = sum(t in POS_WORDS for t in tokens)
    neg = sum(t in NEG_WORDS for t in tokens)
    return (pos - neg) / len(tokens)


def preprocess(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"]).copy()

    if "created" in df.columns:
        df = df.drop(columns=["created"])

    df["date"] = df["timestamp"].dt.date.astype(str)
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.day_name()

    df["title_clean"] = df["title"].fillna("").map(clean_text)
    df["body_clean"] = df["body"].fillna("").map(clean_text)
    df["title_nlp"] = df["title_clean"].str.lower()

    df["has_body"] = df["body"].fillna("").str.strip().ne("")
    df["title_length"] = df["title_clean"].str.len()

    df["post_type"] = df["url"].map(infer_post_type)
    freq = df["post_type"].value_counts(normalize=True)
    keep = set(freq[freq >= 0.05].index)
    df["post_type_lumped"] = df["post_type"].where(df["post_type"].isin(keep), "Other")

    df["score_log"] = np.log1p(df["score"].clip(lower=0))
    df["comms_num_log"] = np.log1p(df["comms_num"].clip(lower=0))

    for col in ["score_log", "comms_num_log", "title_length", "hour"]:
        mu = df[col].mean()
        sd = df[col].std(ddof=0)
        mn = df[col].min()
        mx = df[col].max()
        df[f"{col}_zscore"] = (df[col] - mu) / (sd if sd else 1.0)
        df[f"{col}_minmax"] = (df[col] - mn) / ((mx - mn) if (mx - mn) else 1.0)

    df["day_of_week_encoded"] = df["day_of_week"].astype("category").cat.codes
    df["type_image"] = df["post_type_lumped"].eq("image")
    df["type_text"] = df["post_type_lumped"].eq("text")

    return df


def run_eda(df: pd.DataFrame, out_dir: Path) -> dict:
    fig_dir = out_dir / "artifacts" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    # Core reproducible figures
    plt.figure(figsize=(8, 4))
    plt.hist(df["score_log"].dropna(), bins=50)
    plt.title("Distribution of score_log")
    plt.tight_layout()
    plt.savefig(fig_dir / "workflow_eda_score_log_distribution.png", dpi=200)
    plt.close()

    plt.figure(figsize=(8, 4))
    plt.scatter(df["score_log"], df["comms_num_log"], s=5, alpha=0.3)
    plt.title("score_log vs comms_num_log")
    plt.xlabel("score_log")
    plt.ylabel("comms_num_log")
    plt.tight_layout()
    plt.savefig(fig_dir / "workflow_eda_score_vs_comments_scatter.png", dpi=200)
    plt.close()

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_body_pct": float(df["body"].isna().mean() * 100 if "body" in df.columns else 0.0),
        "score_log_mean": float(df["score_log"].mean()),
        "comms_num_log_mean": float(df["comms_num_log"].mean()),
    }


def run_feature_stage(df: pd.DataFrame, out_dir: Path, sample_size: int) -> dict:
    fig_dir = out_dir / "artifacts" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    # Sentiment + topics
    df = df.copy()
    df["sentiment_score"] = df["title_nlp"].fillna("").map(simple_sentiment)

    tokenized = df["title_nlp"].fillna("").map(lambda t: re.findall(r"[A-Za-z]{2,}", t.lower()))
    dictionary = corpora.Dictionary(tokenized)
    dictionary.filter_extremes(no_below=30, no_above=0.5, keep_n=2000)
    corpus = [dictionary.doc2bow(t) for t in tokenized]
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=3, random_state=42)

    topic_probs = []
    for bow in corpus:
        dist = lda.get_document_topics(bow, minimum_probability=0.0)
        dist = [p for _, p in sorted(dist, key=lambda x: x[0])]
        topic_probs.append(dist)
    topic_df = pd.DataFrame(topic_probs, columns=[f"topic_{i}" for i in range(5)])
    df = pd.concat([df.reset_index(drop=True), topic_df.reset_index(drop=True)], axis=1)

    threshold = float(df["score"].quantile(0.95))
    df["viral_flag"] = (df["score"] >= threshold).astype(int)

    sample = df.sample(min(sample_size, len(df)), random_state=42)
    feat_cols = [
        "score_log", "comms_num_log", "title_length", "hour", "score_log_zscore", "comms_num_log_zscore", "sentiment_score"
    ] + [c for c in df.columns if c.startswith("topic_")]
    X = sample[feat_cols].fillna(0.0)
    y = sample["viral_flag"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = LogisticRegression(max_iter=1200, class_weight="balanced", solver="liblinear")
    model.fit(X_train, y_train)
    pred_prob = model.predict_proba(X_test)[:, 1]
    pred = (pred_prob >= 0.5).astype(int)

    roc_auc = float(roc_auc_score(y_test, pred_prob))
    ap = float(average_precision_score(y_test, pred_prob))
    f1 = float(f1_score(y_test, pred))

    plt.figure(figsize=(8, 4))
    plt.hist(df["sentiment_score"], bins=50)
    plt.title("Sentiment score distribution")
    plt.tight_layout()
    plt.savefig(fig_dir / "workflow_feature_sentiment_distribution.png", dpi=200)
    plt.close()

    return {
        "roc_auc": roc_auc,
        "average_precision": ap,
        "f1": f1,
        "virality_threshold": threshold,
        "topic_top_terms": {f"topic_{i}": [w for w, _ in lda.show_topic(i, topn=8)] for i in range(5)},
    }


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "artifacts" / "json").mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(args.raw)
    cleaned = preprocess(raw)

    cleaned_out = out_dir / args.cleaned_out
    cleaned.to_csv(cleaned_out, index=False)

    eda_stats = run_eda(cleaned, out_dir)
    feature_stats = run_feature_stage(cleaned, out_dir, args.sample_size)

    summary = {
        "generated_at": datetime.now().isoformat(),
        "inputs": {"raw": args.raw},
        "outputs": {"cleaned": str(cleaned_out)},
        "eda": eda_stats,
        "feature_engineering": feature_stats,
    }
    (out_dir / "artifacts" / "json" / "full_workflow_summary.json").write_text(json.dumps(summary, indent=2))

    print("Full workflow complete")
    print(f"Saved cleaned output: {cleaned_out}")


if __name__ == "__main__":
    main()
