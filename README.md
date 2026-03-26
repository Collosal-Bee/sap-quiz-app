# 🎓 Enterprise SAP Certification Testing Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sap-quiz.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](#)
[![SAP](https://img.shields.io/badge/SAP-0FAAFF?style=for-the-badge&logo=sap&logoColor=white)](#)

A stateful, cloud-deployed testing engine designed to help professionals prepare for complex enterprise certifications, specifically **SAP HANA Database (C_DBADM)** and **SAP Integration Suite (C_CPI)**. 

This application simulates the strict, multi-select logic of actual SAP exams while utilizing a decoupled data architecture to ensure the question banks remain continuously updated without requiring code redeployments.

## 🧠 Architecture & Engineering Highlights

### 1. Decoupled "Headless CMS" Data Architecture
Rather than hardcoding questions or provisioning a heavy relational database, the application utilizes a live Google Spreadsheet as a headless backend. Using `pandas.read_excel` mapped to a published cloud URL, Subject Matter Experts (SMEs) can dynamically add, edit, or remove exam questions in a familiar spreadsheet interface. The app caches this data (TTL) and updates the frontend automatically.

### 2. Complex Session State Management
Streamlit operates on a continuous rerun paradigm, which usually destroys user progress on every click. This application implements deep `st.session_state` management to track the user's current question index, running score, randomized option arrays, and lock-out feedback states, ensuring a seamless, uninterrupted exam flow.

### 3. Dynamic Multi-Select Parsing
Enterprise exams frequently utilize "Select all that apply" questions. The backend dynamically intercepts the delimiter (`str.split(';')`) from the dataset, calculates the required `set()` array, and evaluates the user's boolean checkbox inputs against the strictly defined correct subset.

## 🚀 How It Works
1. **Select Domain:** The user selects their target SAP certification from the sidebar.
2. **Dynamic Ingestion:** The app fetches the live dataset, shuffles the question deck, and randomizes the order of the multiple-choice options to prevent pattern memorization.
3. **Evaluation:** Upon submission, the UI locks the inputs and provides immediate, context-aware feedback (Correct vs. Incorrect) alongside the required answers.

## 💻 Local Development Setup

**1. Clone the repository**
```bash
git clone [https://github.com/Collosal-Bee/sap-quiz-app.git](https://github.com/Collosal-Bee/sap-quiz-app.git)
cd sap-quiz-app
```

**2. Install Dependencies**
```bash
pip install streamlit pandas openpyxl
```

**3. Run the Application**
```bash
streamlit run app.py
```
