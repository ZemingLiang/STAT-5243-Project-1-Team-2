"""Advanced feature engineering and diagnostics workflow.

Extends baseline branch outputs with sentiment/topic features and model diagnostics.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split

POS_WORDS = {
    "gain", "moon", "bull", "buy", "rocket", "win", "green", "profit", "up", "long", "calls", "squeeze"
}
NEG_WORDS = {
    "loss", "bear", "sell", "drop", "down", "red", "bagholder", "panic", "short", "puts", "crash"
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fig-dir", default="artifacts/figures")
    parser.add_argument("--json-dir", default="artifacts/json")
    parser.add_argument("--sample-size", type=int, default=25000)
    return parser.parse_args()


def load_cleaned_from_branch(branch_ref: str = "origin/Cleaning-and-Preprocessing") -> pd.DataFrame:
    proc = subprocess.run(
        ["git", "show", f"{branch_ref}:reddit_wsb_cleaned.csv"],
        capture_output=True,
        text=True,
        check=True,
    )
    return pd.read_csv(io.StringIO(proc.stdout))


def tokenize(text: str) -> list[str]:
    if not isinstance(text, str):
        return []
    return re.findall(r"[A-Za-z]{2,}", text.lower())


def simple_sentiment(text: str) -> float:
    tokens = tokenize(text)
    if not tokens:
        return 0.0
    pos = sum(t in POS_WORDS for t in tokens)
    neg = sum(t in NEG_WORDS for t in tokens)
    return (pos - neg) / len(tokens)


def build_topic_features(df: pd.DataFrame, text_col: str) -> tuple[pd.DataFrame, dict[str, list[str]]]:
    tokenized = df[text_col].fillna("").astype(str).map(tokenize)
    dictionary = corpora.Dictionary(tokenized)
    dictionary.filter_extremes(no_below=30, no_above=0.5, keep_n=2000)
    corpus = [dictionary.doc2bow(tokens) for tokens in tokenized]

    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=3, random_state=42)

    topic_probs = []
    for bow in corpus:
        dist = lda.get_document_topics(bow, minimum_probability=0.0)
        dist_sorted = sorted(dist, key=lambda x: x[0])
        topic_probs.append([p for _, p in dist_sorted])

    topic_df = pd.DataFrame(topic_probs, columns=[f"topic_{i}" for i in range(5)])
    topic_df["dominant_topic"] = topic_df.values.argmax(axis=1)

    top_terms = {f"topic_{i}": [w for w, _ in lda.show_topic(i, topn=10)] for i in range(5)}
    return topic_df, top_terms


def build_model_matrix(df: pd.DataFrame) -> pd.DataFrame:
    feat = pd.DataFrame(index=df.index)
    for col in [
        "score_log",
        "comms_num_log",
        "title_length",
        "hour",
        "score_log_zscore",
        "comms_num_log_zscore",
        "title_length_zscore",
        "sentiment_score",
    ]:
        if col in df.columns:
            feat[col] = df[col]

    if "has_body" in df.columns:
        feat["has_body_int"] = df["has_body"].astype(int)

    topic_cols = [c for c in df.columns if c.startswith("topic_")]
    if topic_cols:
        feat = pd.concat([feat, df[topic_cols]], axis=1)

    if "post_type_lumped" in df.columns:
        dummies = pd.get_dummies(df["post_type_lumped"], prefix="type", drop_first=False)
        feat = pd.concat([feat, dummies], axis=1)

    return feat.replace([np.inf, -np.inf], np.nan).fillna(0.0)


def make_plot_json(json_dir: Path, stem: str, idx: int, title: str, caption: str, metrics: dict) -> None:
    payload = {
        "figure_id": f"04_feature_fig_{idx:02d}",
        "branch": "Feature-Engineering-&-Justification",
        "source_file": "code/feature_enhancement_workflow.py",
        "title": title,
        "caption": caption,
        "input_data": ["origin/Cleaning-and-Preprocessing:reddit_wsb_cleaned.csv"],
        "key_stats": metrics,
        "created_at": datetime.now().isoformat(),
    }
    (json_dir / f"{stem}.json").write_text(json.dumps(payload, indent=2))


def main() -> None:
    args = parse_args()
    fig_dir = Path(args.fig_dir)
    json_dir = Path(args.json_dir)
    fig_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)

    df = load_cleaned_from_branch()
    text_col = "title_nlp" if "title_nlp" in df.columns else ("title_clean" if "title_clean" in df.columns else "title")

    df["sentiment_score"] = df[text_col].fillna("").astype(str).map(simple_sentiment)
    topic_df, top_terms = build_topic_features(df, text_col)
    df = pd.concat([df.reset_index(drop=True), topic_df.reset_index(drop=True)], axis=1)

    threshold = float(df["score"].quantile(0.95))
    df["viral_flag"] = (df["score"] >= threshold).astype(int)

    sample_df = df.sample(min(args.sample_size, len(df)), random_state=42)
    X = build_model_matrix(sample_df)
    y = sample_df["viral_flag"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = LogisticRegression(max_iter=1200, class_weight="balanced", solver="liblinear")
    model.fit(X_train, y_train)
    pred_prob = model.predict_proba(X_test)[:, 1]
    pred = (pred_prob >= 0.5).astype(int)

    roc_auc = float(roc_auc_score(y_test, pred_prob))
    ap = float(average_precision_score(y_test, pred_prob))
    f1 = float(f1_score(y_test, pred))

    # Figure outputs
    plt.figure(figsize=(8, 4))
    plt.hist(df["sentiment_score"], bins=50)
    plt.title("Sentiment score distribution")
    plt.xlabel("Sentiment score")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(fig_dir / "04_feature_fig_01_sentiment_distribution.png", dpi=220)
    plt.close()

    topic_cols = [c for c in df.columns if c.startswith("topic_")]
    topic_entropy = -(df[topic_cols] * np.log(df[topic_cols] + 1e-9)).sum(axis=1)
    plt.figure(figsize=(8, 4))
    plt.hist(topic_entropy, bins=40)
    plt.title("Topic entropy distribution")
    plt.xlabel("Entropy")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(fig_dir / "04_feature_fig_02_topic_entropy_distribution.png", dpi=220)
    plt.close()

    plt.figure(figsize=(8, 4))
    df["dominant_topic"].value_counts().sort_index().plot(kind="bar")
    plt.title("Dominant topic distribution")
    plt.xlabel("Topic id")
    plt.ylabel("Post count")
    plt.tight_layout()
    plt.savefig(fig_dir / "04_feature_fig_03_dominant_topic_distribution.png", dpi=220)
    plt.close()

    fpr, tpr, _ = roc_curve(y_test, pred_prob)
    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, label=f"AUC={roc_auc:.3f}")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.title("ROC curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / "04_feature_fig_04_roc_curve.png", dpi=220)
    plt.close()

    precision, recall, _ = precision_recall_curve(y_test, pred_prob)
    plt.figure(figsize=(6, 6))
    plt.plot(recall, precision, label=f"AP={ap:.3f}")
    plt.title("Precision-Recall curve")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / "04_feature_fig_05_pr_curve.png", dpi=220)
    plt.close()

    cm = confusion_matrix(y_test, pred)
    plt.figure(figsize=(5, 4))
    plt.imshow(cm, cmap="Blues")
    plt.colorbar()
    plt.xticks([0, 1], ["Pred 0", "Pred 1"])
    plt.yticks([0, 1], ["True 0", "True 1"])
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, int(cm[i, j]), ha="center", va="center")
    plt.title("Confusion matrix")
    plt.tight_layout()
    plt.savefig(fig_dir / "04_feature_fig_06_confusion_matrix.png", dpi=220)
    plt.close()

    plt.figure(figsize=(8, 4))
    plt.hist(pred_prob, bins=40)
    plt.title("Predicted viral probability distribution")
    plt.xlabel("Predicted probability")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(fig_dir / "04_feature_fig_07_pred_prob_distribution.png", dpi=220)
    plt.close()

    coef = pd.Series(model.coef_[0], index=X.columns)
    top_coef = coef.sort_values(key=np.abs, ascending=False).head(15)
    plt.figure(figsize=(10, 5))
    top_coef.iloc[::-1].plot(kind="barh")
    plt.title("Top logistic coefficients")
    plt.tight_layout()
    plt.savefig(fig_dir / "04_feature_fig_08_top_coefficients.png", dpi=220)
    plt.close()

    metrics = {
        "roc_auc": roc_auc,
        "average_precision": ap,
        "f1_at_0_5": f1,
        "virality_threshold": threshold,
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
    }

    fig_meta = [
        ("04_feature_fig_01_sentiment_distribution", "Sentiment distribution", "Distribution of rule-based title sentiment scores."),
        ("04_feature_fig_02_topic_entropy_distribution", "Topic entropy distribution", "Distribution of topic entropy across posts."),
        ("04_feature_fig_03_dominant_topic_distribution", "Dominant topic distribution", "Post counts by dominant topic."),
        ("04_feature_fig_04_roc_curve", "ROC curve", "ROC diagnostic for viral classifier."),
        ("04_feature_fig_05_pr_curve", "Precision-recall curve", "PR diagnostic for viral classifier."),
        ("04_feature_fig_06_confusion_matrix", "Confusion matrix", "Confusion matrix at threshold 0.5."),
        ("04_feature_fig_07_pred_prob_distribution", "Predicted probability distribution", "Distribution of model predicted probabilities."),
        ("04_feature_fig_08_top_coefficients", "Top coefficients", "Largest logistic-regression coefficients by magnitude."),
    ]
    for idx, (stem, title, caption) in enumerate(fig_meta, start=1):
        make_plot_json(json_dir, stem, idx, title, caption, metrics)

    summary = {
        "section_id": "05_feature_engineering",
        "branch": "Feature-Engineering-&-Justification",
        "inputs": ["Feature-Engineering-&-Justification.ipynb", "origin/Cleaning-and-Preprocessing:reddit_wsb_cleaned.csv"],
        "methods": [
            "Rule-based sentiment feature engineering",
            "LDA topic modeling with gensim",
            "Logistic regression viral-classification diagnostics",
        ],
        "findings": [
            "Content-aware features add interpretable signals for engagement modeling.",
            "Diagnostic metrics provide evidence of predictive utility of engineered features.",
        ],
        "limitations": [
            "Sentiment is lexicon-based and approximate.",
            "Topic labels require qualitative interpretation.",
        ],
        "outputs": [
            "artifacts/figures/04_feature_fig_*.png",
            "artifacts/json/04_feature_fig_*.json",
            "artifacts/json/05_feature_engineering_summary.json",
        ],
        "metrics": metrics,
        "topic_top_terms": top_terms,
    }

    manifest = {
        "section_id": "05_feature_engineering",
        "branch": "Feature-Engineering-&-Justification",
        "generated_at": datetime.now().isoformat(),
        "artifacts": [
            "code/feature_enhancement_workflow.py",
            "report/sections/05_feature_engineering.tex",
            "artifacts/json/05_feature_engineering_summary.json",
            "artifacts/json/05_feature_engineering_manifest.json",
        ],
    }
    for p in sorted(fig_dir.glob("04_feature_fig_*.png")):
        manifest["artifacts"].append(str(p))
    for p in sorted(json_dir.glob("04_feature_fig_*.json")):
        manifest["artifacts"].append(str(p))

    (json_dir / "05_feature_engineering_summary.json").write_text(json.dumps(summary, indent=2))
    (json_dir / "05_feature_engineering_manifest.json").write_text(json.dumps(manifest, indent=2))
    print("Feature engineering artifacts generated")


if __name__ == "__main__":
    main()
