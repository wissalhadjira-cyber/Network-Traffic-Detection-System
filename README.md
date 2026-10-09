# 🛡️ Network Traffic Detection System

A Machine Learning based system for detecting malicious network traffic.

---

## 📌 About the Project

This project uses a Random Forest Classifier to analyze network traffic and classify it as either **BENIGN** or a specific type of cyber attack.

It provides:
- CSV file analysis
- Real-time packet capture
- Interactive web dashboard

---

## 🛠️ Built With

- Python
- Scikit-learn
- Pandas & NumPy
- Streamlit
- Scapy
- Plotly

---

## 📁 Project Files

| File | Description |
|------|-------------|
| `Stream.py` | Web interface (Streamlit) |
| `predict.py` | CSV batch analysis |
| `main.py` | Model training script |
| `requirements.txt` | Required libraries |
| `random_forest_model.pkl` | Trained model |
| `label_encoder.pkl` | Label encoder |
| `scaler.pkl` | Feature scaler |

---

## 🚀 How to Run

### Step 1 — Download the project

Click the green **Code** button on GitHub and choose **Download ZIP**, then extract it.

Or clone it with Git:

```bash
git clone https://github.com/wissalhadjira-cyber/Network-Traffic-Detection-System.git
```

### Step 2 — Open the project folder

Open a terminal inside the project folder.

### Step 3 — Install the required libraries

```bash
pip install -r requirements.txt
```

### Step 4 — Run the application

```bash
streamlit run Stream.py
```

The browser will open automatically at `http://localhost:8501`.

---

## 📊 How to Use

Once the app is running:

1. Choose a mode from the sidebar:
   - **📂 CSV File** — upload a CSV file with network traffic data
   - **⚡ Realtime Capture** — capture live packets (needs Administrator rights)

2. Press the **Start** button.

3. View the results: safe or attack detected.

---

## 📈 Model Performance

| Metric | Value |
|--------|-------|
| Algorithm | Random Forest |
| Accuracy | 97.37% |
| Dataset | CIC-IDS-2017 |
| Attack Classes | 15 |

---

## 📚 Dataset

The training data comes from **CIC-IDS-2017** and is not included in this repository due to its size.

Download it from: [UNB CIC](https://www.unb.ca/cic/datasets/ids-2017.html)

---

## 👩‍💻 Author

**Hadjira Wissal**
University of Batna 2 — Cyber Security
