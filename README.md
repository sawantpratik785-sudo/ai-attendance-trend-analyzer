# AI-Powered Attendance Trend Analyzer 🎓

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Logic-150458.svg)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)](https://streamlit.io/)
[![Excel Automation](https://img.shields.io/badge/Excel-openpyxl-green.svg)]()

An end-to-end analytical framework and interactive web portal for evaluating multi-year student attendance datasets, identifying at-risk academic trajectories, and generating automated Excel reports.

---

## 🌟 Key Features & Analytical Architecture

```mermaid
flowchart TD
    RAW[Multi-Semester Attendance CSV\nStudent ID, Month, Attendance %, GPA] --> ENGINE[Python Analytics Core\ntrend_analyzer.py]
    
    ENGINE --> TRAJ[Rolling Trend & Linear Slope Engine\nPolyfit Trajectory Slope]
    ENGINE --> RISK[Predictive Risk Classifier\nCRITICAL (<75%), WARNING, SAFE]
    ENGINE --> CORR[Attendance ⟷ GPA Correlation Engine]
    
    RISK --> APP[Interactive Web Portal\nStreamlit + Plotly]
    CORR --> APP
    ENGINE --> EXCEL[Automated Formatted Excel Reporter\nopenpyxl conditional styling]
```

### 1. Rolling Trend & Trajectory Engine
- Computes 3-month rolling attendance averages, semester-over-semester progression, and linear polynomial slope ($\text{polyfit}$) to detect upward or downward attendance momentum before exams.

### 2. Predictive Risk Classification Model
- **`CRITICAL_SHORTAGE (<75%)`**: Flags students below the mandatory university attendance threshold ($75\%$).
- **`WARNING_DECLINING`**: Flags students between $75\% - 80\%$ or exhibiting steep downward trajectory ($slope < -1.5$).
- **`SAFE_COMPLIANT`**: Identifies consistent students ($> 80\%$).

### 3. Attendance ⟷ Academic GPA Correlation Engine
- Evaluates the Pearson correlation coefficient between student class participation and semester GPA score.

### 4. Automated Excel Audit Exporter
- Uses `openpyxl` to build multi-sheet formatted reports with executive KPI blocks, conditional color-coded rows (Red/Yellow/Green), and auto-calculated column widths.

---

## 📁 Repository Structure

```
ai-attendance-trend-analyzer/
├── data/
│   ├── generate_attendance_dataset.py  # Synthetic multi-semester student dataset generator
│   └── sample_attendance_data.csv       # Multi-year student attendance history
├── src/
│   ├── trend_analyzer.py               # Core analytical & predictive engine
│   ├── excel_reporter.py               # Formatted Excel report builder with conditional styles
│   └── app.py                          # Streamlit web dashboard
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚡ Quickstart Guide

### 1. Installation
```bash
git clone https://github.com/PratikS3005/ai-attendance-trend-analyzer.git
cd ai-attendance-trend-analyzer
pip install -r requirements.txt
```

### 2. Generate Synthetic Dataset
```bash
python data/generate_attendance_dataset.py
```

### 3. Launch Web Dashboard
```bash
streamlit run src/app.py
```
Open `http://localhost:8501` to view the interactive dashboard, inspect individual student trajectories, and export Excel reports.

---

## 📄 License & Attribution
Developed by **Pratik Sawant** as an academic data analytics project demonstrating Python data manipulation, predictive risk modeling, and automated report generation.
