from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database.db import fetch_recent, save_prediction

MODEL_DIR = Path(__file__).resolve().parent / 'model'
MODEL_PATH = MODEL_DIR / 'heart_model.joblib'
META_PATH = MODEL_DIR / 'feature_order.json'


class HeartPredictionHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    def do_HEAD(self) -> None:
        if self.path == '/api/history':
            records = fetch_recent(10)
            self._send_json(200, {'records': records})
            return
        self._send_json(404, {'message': 'Not found'})

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

    def do_GET(self) -> None:
        if self.path == '/api/history':
            records = fetch_recent(10)
            self._send_json(200, {'records': records})
            return
        self._send_json(404, {'message': 'Not found'})

    def do_POST(self) -> None:
        if self.path != '/api/predict':
            self._send_json(404, {'message': 'Not found'})
            return

        try:
            content_length = int(self.headers.get('Content-Length', '0'))
            body = self.rfile.read(content_length)
            patient_data = json.loads(body.decode('utf-8'))
        except Exception:
            self._send_json(400, {'message': 'Invalid JSON payload'})
            return

        risk_score, label = predict_heart_risk(patient_data)
        save_prediction(patient_data, risk_score, label)

        self._send_json(
            200,
            {
                'message': 'Prediction completed successfully',
                'risk_score': risk_score,
                'label': label,
            },
        )


def load_model() -> tuple[object, list[str]]:
    if not MODEL_PATH.exists():
        raise FileNotFoundError('Model file is missing. Run train_model.py first.')

    model = joblib.load(MODEL_PATH)
    feature_order = []
    if META_PATH.exists():
        with META_PATH.open('r', encoding='utf-8') as handle:
            feature_order = json.load(handle).get('feature_order', [])
    return model, feature_order


def predict_heart_risk(patient_data: dict) -> tuple[int, str]:
    model, feature_order = load_model()

    incoming = {
        'age': float(patient_data.get('age', 0)),
        'sex': float(patient_data.get('sex', 0)),
        'cp': float(patient_data.get('cp', 0)),
        'trestbps': float(patient_data.get('trestbps', 0)),
        'chol': float(patient_data.get('chol', 0)),
        'fbs': float(patient_data.get('fbs', 0)),
        'restecg': float(patient_data.get('restecg', 0)),
        'thalach': float(patient_data.get('thalach', 0)),
        'exang': float(patient_data.get('exang', 0)),
        'oldpeak': float(patient_data.get('oldpeak', 0)),
        'slope': float(patient_data.get('slope', 0)),
        'ca': float(patient_data.get('ca', 0)),
        'thal': float(patient_data.get('thal', 0)),
    }

    df = pd.DataFrame([incoming])
    if feature_order:
        df = df.reindex(columns=feature_order)

    prediction = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1]) * 100
    risk_score = int(round(probability))

    if prediction == 1:
        label = 'High risk' if risk_score >= 60 else 'Moderate risk'
    else:
        label = 'Low risk'

    return risk_score, label


if __name__ == '__main__':
    try:
        load_model()
    except FileNotFoundError as exc:
        print(exc)
        print('Training the model now...')
        from train_model import train_heart_model
        train_heart_model()

    server = HTTPServer(('127.0.0.1', 5000), HeartPredictionHandler)
    print('Backend server started on http://127.0.0.1:5000')
    server.serve_forever()
