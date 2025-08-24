#!/usr/bin/env python3
# train_microsleep_az_only.py
# Train an AZ-only microsleep detector with threshold-based labeling + smoothing

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib


def label_by_threshold_and_smoothing(az: pd.Series, lower: float, upper: float, window: int) -> pd.Series:
    """
    Label microsleep when az is outside [lower, upper].
    Then require `window` consecutive threshold hits to confirm (smoothing).
    Uses trailing rolling window (no center) so it's aligned with live streaming behavior.
    """
    raw = ((az < lower) | (az > upper)).astype(int)
    if window <= 1:
        return raw

    # Trailing rolling sum: mark 1 only when last `window` samples are all 1
    smooth = (raw.rolling(window=window, min_periods=window).sum() == window).astype(int)
    smooth = smooth.fillna(0).astype(int)
    return smooth


def train_model(X_train, y_train, model_type: str):
    if model_type == "logreg":
        model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    elif model_type == "rf":
        model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")
    else:
        raise ValueError(f"Unsupported model_type: {model_type}")
    model.fit(X_train, y_train)
    return model


def main():
    parser = argparse.ArgumentParser(description="Train AZ-only microsleep model with threshold labeling + smoothing.")
    parser.add_argument("--data", type=str, default="dataset.csv",
                        help="Path to CSV with 6 columns (ax, ay, az, gx, gy, gz) and no header.")
    parser.add_argument("--lower", type=float, default=8.0, help="Lower az threshold for microsleep.")
    parser.add_argument("--upper", type=float, default=11.0, help="Upper az threshold for microsleep.")
    parser.add_argument("--window", type=int, default=3, help="Consecutive hits required to confirm microsleep.")
    parser.add_argument("--model", type=str, default="logreg", choices=["logreg", "rf"], help="Model type.")
    parser.add_argument("--test_size", type=float, default=0.2, help="Test split ratio.")
    parser.add_argument("--out_prefix", type=str, default="", help="Optional prefix for output files.")
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"❌ Dataset not found: {data_path.resolve()}", file=sys.stderr)
        sys.exit(1)

    # --- Load dataset ---
    df = pd.read_csv(data_path, header=None)
    if df.shape[1] < 3:
        print("❌ Expected at least 3 columns (ax, ay, az) in dataset.", file=sys.stderr)
        sys.exit(1)

    df.columns = ["ax", "ay", "az", "gx", "gy", "gz"][:df.shape[1]]

    # Only keep az
    az = df["az"].astype(float)

    # --- Labeling ---
    labels = label_by_threshold_and_smoothing(az, args.lower, args.upper, args.window)
    labeled_df = pd.DataFrame({"az": az, "label": labels})

    # Basic sanity + counts
    counts = labeled_df["label"].value_counts().sort_index()
    n0 = int(counts.get(0, 0))
    n1 = int(counts.get(1, 0))
    total = len(labeled_df)
    print("Label counts after smoothing:")
    print(counts.to_string())
    if n1 == 0:
        print("⚠️ Warning: No microsleep (label=1) samples found. Model will not learn to detect microsleep.")
    if n0 == 0:
        print("⚠️ Warning: No normal (label=0) samples found. Model will not learn to detect the normal state.")
    if total < 50:
        print("⚠️ Warning: Very few samples; consider collecting more data.")

    # --- Train/test split ---
    X = labeled_df[["az"]].values
    y = labeled_df["label"].values

    # If one class absent, stratify fails; handle gracefully
    stratify = y if (n0 > 0 and n1 > 0) else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42, stratify=stratify
    )

    # --- Scale ---
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # --- Train ---
    model = train_model(X_train_scaled, y_train, args.model)

    # --- Evaluate ---
    y_pred = model.predict(X_test_scaled)
    try:
        y_prob = model.predict_proba(X_test_scaled)[:, 1]
    except Exception:
        y_prob = None

    report = classification_report(y_test, y_pred, digits=4)
    cm = confusion_matrix(y_test, y_pred)

    print("\n=== Classification Report ===")
    print(report)
    print("=== Confusion Matrix ===")
    print(cm)

    # --- Save artifacts ---
    prefix = (args.out_prefix + "_") if args.out_prefix else ""
    model_path = f"{prefix}microsleep_model.pkl"
    scaler_path = f"{prefix}scaler.pkl"
    labeled_csv = f"{prefix}labeled_dataset_az.csv"
    report_path = f"{prefix}training_report.txt"
    meta_path = f"{prefix}training_meta.json"

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    labeled_df.to_csv(labeled_csv, index=False)

    # Save textual report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Data: {data_path}\n")
        f.write(f"Thresholds: lower={args.lower}, upper={args.upper}, window={args.window}\n")
        f.write(f"Model: {args.model}\n")
        f.write("\nLabel counts:\n")
        f.write(counts.to_string())
        f.write("\n\n=== Classification Report ===\n")
        f.write(report)
        f.write("\n=== Confusion Matrix ===\n")
        f.write(str(cm))

    # Save metadata JSON
    meta = {
        "data": str(data_path),
        "lower": args.lower,
        "upper": args.upper,
        "window": args.window,
        "model": args.model,
        "test_size": args.test_size,
        "samples_total": int(total),
        "samples_label0": n0,
        "samples_label1": n1,
        "artifacts": {
            "model": model_path,
            "scaler": scaler_path,
            "labeled_csv": labeled_csv,
            "report": report_path
        }
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print("\n✅ Saved:")
    print(f"  Model:        {model_path}")
    print(f"  Scaler:       {scaler_path}")
    print(f"  Labeled CSV:  {labeled_csv}")
    print(f"  Report:       {report_path}")
    print(f"  Meta:         {meta_path}")

    print("\nNext:")
    print("  1) Start your server that loads these exact files:")
    print("       model = joblib.load('microsleep_model.pkl')")
    print("       scaler = joblib.load('scaler.pkl')")
    print("  2) Use only az in the server: np.array([[az]])")
    print("  3) Keep your threshold logic in ws_server_az_only.py consistent (lower/upper/window).")


if __name__ == "__main__":
    main()
