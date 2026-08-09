const form = document.getElementById('prediction-form');
const resultMessage = document.getElementById('result-message');
const riskScore = document.getElementById('risk-score');
const riskLabel = document.getElementById('risk-label');
const historyList = document.getElementById('history-list');
const loadSampleButton = document.getElementById('load-sample');
const riskBox = document.querySelector('.risk-box');

const sampleProfiles = [
  {
    label: 'Sample 1 · Very low risk',
    values: { age: 22, sex: 0, cp: 0, trestbps: 110, chol: 160, fbs: 0, restecg: 0, thalach: 180, exang: 0, oldpeak: 0.1, slope: 0, ca: 0, thal: 1 },
  },
  {
    label: 'Sample 2 · Low risk',
    values: { age: 31, sex: 0, cp: 1, trestbps: 118, chol: 200, fbs: 0, restecg: 0, thalach: 175, exang: 0, oldpeak: 0.4, slope: 0, ca: 0, thal: 1 },
  },
  {
    label: 'Sample 3 · Mild risk',
    values: { age: 42, sex: 1, cp: 1, trestbps: 124, chol: 210, fbs: 0, restecg: 0, thalach: 165, exang: 0, oldpeak: 0.8, slope: 1, ca: 0, thal: 2 },
  },
  {
    label: 'Sample 4 · Moderate risk',
    values: { age: 50, sex: 1, cp: 2, trestbps: 132, chol: 220, fbs: 0, restecg: 1, thalach: 150, exang: 0, oldpeak: 1.2, slope: 1, ca: 1, thal: 2 },
  },
  {
    label: 'Sample 5 · Elevated risk',
    values: { age: 56, sex: 1, cp: 2, trestbps: 142, chol: 230, fbs: 1, restecg: 1, thalach: 140, exang: 1, oldpeak: 1.8, slope: 1, ca: 1, thal: 3 },
  },
  {
    label: 'Sample 6 · High risk',
    values: { age: 60, sex: 1, cp: 3, trestbps: 148, chol: 245, fbs: 1, restecg: 1, thalach: 135, exang: 1, oldpeak: 2.4, slope: 2, ca: 2, thal: 3 },
  },
  {
    label: 'Sample 7 · Very high risk',
    values: { age: 64, sex: 1, cp: 3, trestbps: 155, chol: 260, fbs: 1, restecg: 2, thalach: 128, exang: 1, oldpeak: 3.2, slope: 2, ca: 3, thal: 3 },
  },
  {
    label: 'Sample 8 · Critical risk',
    values: { age: 68, sex: 1, cp: 3, trestbps: 160, chol: 280, fbs: 1, restecg: 2, thalach: 120, exang: 1, oldpeak: 4.0, slope: 2, ca: 4, thal: 3 },
  },
  {
    label: 'Sample 9 · Severe ischemia',
    values: { age: 72, sex: 1, cp: 3, trestbps: 170, chol: 288, fbs: 1, restecg: 2, thalach: 110, exang: 1, oldpeak: 4.4, slope: 2, ca: 4, thal: 3 },
  },
  {
    label: 'Sample 10 · Near-critical risk',
    values: { age: 74, sex: 1, cp: 3, trestbps: 175, chol: 300, fbs: 1, restecg: 2, thalach: 105, exang: 1, oldpeak: 4.8, slope: 2, ca: 4, thal: 3 },
  },
  {
    label: 'Sample 11 · Advanced risk',
    values: { age: 76, sex: 1, cp: 3, trestbps: 180, chol: 315, fbs: 1, restecg: 2, thalach: 100, exang: 1, oldpeak: 5.0, slope: 2, ca: 4, thal: 3 },
  },
  {
    label: 'Sample 12 · Extreme risk',
    values: { age: 78, sex: 1, cp: 3, trestbps: 190, chol: 320, fbs: 1, restecg: 2, thalach: 95, exang: 1, oldpeak: 5.4, slope: 2, ca: 4, thal: 3 },
  },
];

let sampleIndex = 0;

function setRiskTheme(label) {
  riskBox.classList.remove('low', 'moderate', 'high');

  if (label === 'Low risk') {
    riskBox.classList.add('low');
  } else if (label === 'Moderate risk') {
    riskBox.classList.add('moderate');
  } else if (label === 'High risk') {
    riskBox.classList.add('high');
  }
}

loadSampleButton.addEventListener('click', () => {
  const activeProfile = sampleProfiles[sampleIndex % sampleProfiles.length];
  sampleIndex += 1;

  Object.entries(activeProfile.values).forEach(([key, value]) => {
    const field = form.elements.namedItem(key);
    if (field) field.value = value;
  });

  resultMessage.textContent = `${activeProfile.label} loaded. Click Predict to run the model.`;
});

async function loadHistory() {
  const response = await fetch('http://127.0.0.1:5000/api/history');
  const data = await response.json();
  historyList.innerHTML = '';

  if (!data.records || data.records.length === 0) {
    historyList.innerHTML = '<li>No records yet.</li>';
    return;
  }

  data.records.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = `${item.label} · age ${item.age} · risk ${item.risk_score}%`;
    historyList.appendChild(li);
  });
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());

  try {
    const response = await fetch('http://127.0.0.1:5000/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const result = await response.json();
    resultMessage.textContent = result.message;
    riskScore.textContent = `${result.risk_score}%`;
    riskLabel.textContent = result.label;
    setRiskTheme(result.label);
    await loadHistory();
  } catch (error) {
    resultMessage.textContent = 'Unable to reach the backend server.';
    riskScore.textContent = '—';
    riskLabel.textContent = 'Check server status';
    riskBox.classList.remove('low', 'moderate', 'high');
  }
});

loadHistory();
