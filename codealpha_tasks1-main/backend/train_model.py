from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from ucimlrepo import fetch_ucirepo

MODEL_DIR = Path(__file__).resolve().parent / "model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "heart_model.joblib"
META_PATH = MODEL_DIR / "feature_order.json"


def load_uci_heart_dataset() -> tuple[pd.DataFrame, pd.Series]:
    heart_disease = fetch_ucirepo(id=45)
    X = heart_disease.data.features.copy()
    y = heart_disease.data.targets.copy()

    if y.ndim > 1:
        y = y.iloc[:, 0]

    df = X.copy()
    df["target"] = y.astype(int)
    df["target"] = (df["target"] > 0).astype(int)
    return df, df["target"]


def train_heart_model() -> tuple[Pipeline, pd.DataFrame, pd.Series]:
    df, y = load_uci_heart_dataset()

    target_column = "target"
    if target_column not in df.columns:
        raise ValueError("The dataset must contain a 'target' column.")

    X = df.drop(columns=[target_column])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", RandomForestClassifier(
                n_estimators=220,
                max_depth=6,
                min_samples_leaf=2,
                random_state=42,
                class_weight="balanced",
            )),
        ]
    )

    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    feature_order = list(X.columns)
    with META_PATH.open("w", encoding="utf-8") as handle:
        json.dump({"feature_order": feature_order, "accuracy": float(accuracy)}, handle, indent=2)

    joblib.dump(pipeline, MODEL_PATH)
    return pipeline, X, y


if __name__ == "__main__":
    train_heart_model()
    print(f"Model trained and saved to {MODEL_PATH}")
