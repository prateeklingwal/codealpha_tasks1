from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent / "heart_predictions.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER,
                sex INTEGER,
                cp INTEGER,
                trestbps INTEGER,
                chol INTEGER,
                fbs INTEGER,
                restecg INTEGER,
                thalach INTEGER,
                exang INTEGER,
                oldpeak REAL,
                slope INTEGER,
                ca INTEGER,
                thal INTEGER,
                risk_score INTEGER,
                label TEXT,
                dataset_json TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_prediction(patient_data: dict[str, Any], risk_score: int, label: str) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO predictions (
                age, sex, cp, trestbps, chol, fbs, restecg, thalach,
                exang, oldpeak, slope, ca, thal, risk_score, label, dataset_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(patient_data.get("age", 0)),
                int(patient_data.get("sex", 0)),
                int(patient_data.get("cp", 0)),
                int(patient_data.get("trestbps", 0)),
                int(patient_data.get("chol", 0)),
                int(patient_data.get("fbs", 0)),
                int(patient_data.get("restecg", 0)),
                int(patient_data.get("thalach", 0)),
                int(patient_data.get("exang", 0)),
                float(patient_data.get("oldpeak", 0)),
                int(patient_data.get("slope", 0)),
                int(patient_data.get("ca", 0)),
                int(patient_data.get("thal", 0)),
                risk_score,
                label,
                json.dumps(patient_data),
            ),
        )


def fetch_recent(limit: int = 10) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT age, risk_score, label FROM predictions ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


init_db()
