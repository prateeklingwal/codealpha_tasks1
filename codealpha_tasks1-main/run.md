# How to Run

## Prerequisites

- Python 3 installed

## 1. Install dependencies (first time only)

Open a terminal in this folder (`codealpha_tasks1-main`) and run:

```bash
pip install pandas scikit-learn joblib ucimlrepo
```

## 2. Run the app

### Option A — Quick start (Windows)

Double-click `start.bat`, or run:

```bash
start.bat
```

This starts the backend, frontend, and opens the app in your browser.

### Option B — Manual start

Open a terminal in this folder and run **two commands** in separate terminals:

**Terminal 1 — Backend (port 5000):**

```bash
python backend/server.py
```

**Terminal 2 — Frontend (port 8080):**

```bash
python -m http.server 8080 --directory frontend
```

Then open in your browser:

```
http://127.0.0.1:8080/index.html
```

## Notes

- If the ML model is missing, the backend will train it automatically on first run.
- To train the model manually:

```bash
python backend/train_model.py
```

- Backend API: `http://127.0.0.1:5000`
- Frontend UI: `http://127.0.0.1:8080/index.html`
