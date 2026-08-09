# ❤️ Heart Disease Prediction System

A Machine Learning-based web application that predicts the risk of heart disease using patient clinical information. The system combines a trained Random Forest classifier with a Python backend, SQLite database, and an interactive web interface to provide real-time heart disease risk assessment.

---

## 📌 Features

- Predicts heart disease risk using Machine Learning.
- User-friendly web interface for entering patient details.
- Real-time prediction with risk percentage.
- Classifies patients into:
  - 🟢 Low Risk
  - 🟡 Moderate Risk
  - 🔴 High Risk
- Stores prediction history in SQLite database.
- Displays recently saved prediction records.
- Includes sample patient profiles for testing.
- Responsive and modern dashboard design.

---

## 🛠️ Technologies Used

### Programming Languages
- Python 3
- JavaScript
- HTML5
- CSS3

### Machine Learning
- Scikit-learn
- Pandas
- Joblib
- UCI Machine Learning Repository

### Backend
- Python HTTPServer
- BaseHTTPRequestHandler
- JSON API

### Database
- SQLite3

### Frontend
- HTML
- CSS
- JavaScript
- Fetch API

---

## 📂 Project Structure

```
Heart-Disease-Prediction/
│
├── backend/
│   ├── server.py
│   ├── train_model.py
│   ├── model/
│   │   ├── heart_model.joblib
│   │   └── feature_order.json
│
├── database/
│   ├── db.py
│   └── heart_predictions.db
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
│
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

The project uses the **Heart Disease Dataset** from the **UCI Machine Learning Repository**.

Dataset Features:

- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate
- Exercise-Induced Angina
- Oldpeak
- Slope
- Number of Major Vessels
- Thalassemia

Target Variable:

- **0** → No Heart Disease
- **1** → Heart Disease

---

## 🤖 Machine Learning Model

The prediction model uses a **Random Forest Classifier**.

### Model Pipeline

- Median Missing Value Imputation
- Feature Standardization
- Random Forest Classification

### Model Parameters

- n_estimators = 220
- max_depth = 6
- min_samples_leaf = 2
- random_state = 42
- class_weight = balanced

---

## ⚙️ How the System Works

1. The user enters patient medical information.
2. The frontend sends the data to the backend using a POST request.
3. The backend loads the trained Machine Learning model.
4. Patient data is converted into a Pandas DataFrame.
5. The model predicts the probability of heart disease.
6. The probability is converted into a risk score.
7. The system classifies the patient as:
   - Low Risk
   - Moderate Risk
   - High Risk
8. The prediction is stored in the SQLite database.
9. The prediction result and recent history are displayed on the dashboard.

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/Heart-Disease-Prediction.git
cd Heart-Disease-Prediction
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install pandas scikit-learn joblib ucimlrepo
```

---

### Train the Model

```bash
python train_model.py
```

This will:

- Download the UCI Heart Disease dataset.
- Train the Random Forest model.
- Save:
  - `heart_model.joblib`
  - `feature_order.json`

---

### Start the Backend

```bash
python server.py
```

Backend runs at:

```
http://127.0.0.1:5000
```

---

### Open the Frontend

Open `index.html` in your browser.

---

## 📡 API Endpoints

### Predict Heart Disease

**POST**

```
/api/predict
```

Example Request

```json
{
  "age":55,
  "sex":1,
  "cp":2,
  "trestbps":140,
  "chol":220,
  "fbs":0,
  "restecg":1,
  "thalach":150,
  "exang":0,
  "oldpeak":1.5,
  "slope":1,
  "ca":0,
  "thal":2
}
```

Example Response

```json
{
    "message":"Prediction completed successfully",
    "risk_score":78,
    "label":"High risk"
}
```

---

### Prediction History

**GET**

```
/api/history
```

Returns the latest saved prediction records.

---

## 🗄️ Database

SQLite stores:

- Patient Information
- Risk Score
- Prediction Label
- Complete JSON Record
- Timestamp

---

## ✨ Project Highlights

- Full Stack Machine Learning Project
- Healthcare Decision Support System
- REST API Integration
- Machine Learning Pipeline
- SQLite Database Integration
- Interactive Clinical Dashboard
- Responsive User Interface
- Real-Time Prediction

---

## 📸 User Interface

The application includes:

- Dashboard Home Screen
- Patient Information Form
- Risk Prediction Card
- Prediction History
- Random Sample Loader
- Dynamic Risk Indicators

---

## 🔮 Future Enhancements

- Deep Learning Models
- Explainable AI (XAI)
- PDF Medical Reports
- User Authentication
- Cloud Deployment
- Electronic Health Record (EHR) Integration
- Doctor Recommendation System
- Mobile Application

---

## 👨‍💻 Author

**Pratham Bhatt**

B.Tech CSE (AI & ML)

Graphic Era Hill University

---

## 📜 License

This project is developed for educational and research purposes. It may be modified and extended for academic or non-commercial use.

---

## ⚠️ Disclaimer

This application is intended for educational purposes only. The prediction results are generated by a Machine Learning model and should **not** be considered a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for medical decisions.
