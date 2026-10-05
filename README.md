# Network Traffic Detection System

## 📌 Project Overview

This project is a machine learning-based system designed to detect malicious network traffic.

The system analyzes network traffic data and classifies network flows as either **BENIGN** or **malicious traffic**. It uses a Random Forest machine learning model and provides both CSV-based analysis and real-time traffic analysis.

## 🎯 Objectives

The main objectives of this project are:

- Detect malicious network traffic using Machine Learning.
- Classify network flows into different traffic categories.
- Analyze network traffic from CSV datasets.
- Provide real-time network traffic monitoring.
- Display detection results through an interactive dashboard.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Streamlit
- Scapy
- Plotly

## 🤖 Machine Learning Model

The project uses a **Random Forest Classifier** for traffic classification.

The trained model is saved in:

```text
random_forest_model.pkl
