"""
AI Attendance Trend Analyzer - Interactive Streamlit Web App
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.trend_analyzer import AttendanceTrendAnalyzer
from src.excel_reporter import generate_excel_report
from data.generate_attendance_dataset import generate_dataset, DATA_PATH

# Page Config
st.set_page_config(
    page_title="AI Attendance Trend Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 25px;
    }
    .main-title h1 { color: white; margin: 0; font-size: 26px; font-weight: 700; }
    .main-title p { color: #d0e1fd; margin: 5px 0 0 0; font-size: 14px; }
    .stMetric { background-color: #f8f9fa; border-radius: 8px; padding: 15px; }
</style>
""", unsafe_allow_html=True)

# Title Banner
st.markdown("""
<div class="main-title">
    <h1>🎓 AI-Powered Student Attendance Trend Analyzer</h1>
    <p>Predictive Analytical Engine & Automated Reporting for Academic Performance Tracking</p>
</div>
""", unsafe_allow_html=True)

# Ensure sample dataset exists
if not os.path.exists(DATA_PATH):
    generate_dataset()

# Sidebar
st.sidebar.header("📁 Data Source & Options")

uploaded_file = st.sidebar.file_uploader("Upload Student CSV Data", type=["csv"])

if st.sidebar.button("🔄 Regenerate Sample Data"):
    generate_dataset()
    st.sidebar.success("Sample dataset refreshed!")
    st.rerun()

# Load Data
if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)
else:
    analyzer_init = AttendanceTrendAnalyzer()
    df_raw = analyzer_init.load_data()

analyzer = AttendanceTrendAnalyzer()
df_students = analyzer.calculate_student_trends(df_raw)
kpis = analyzer.get_kpi_metrics(df_students)

# KPI Row
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("Total Students", kpis.get("Total_Students", 0))
with c2:
    st.metric("Avg Attendance Rate", f"{kpis.get('Avg_Attendance_Pct', 0)}%")
with c3:
    st.metric("High Risk (<75%)", kpis.get("High_Risk_Count", 0), delta_color="inverse")
with c4:
    st.metric("Declining / Warning", kpis.get("Warning_Count", 0))
with c5:
    st.metric("Attendance-GPA Correlation", f"{kpis.get('Attendance_GPA_Correlation', 0)}")

st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Risk & Trend Dashboard",
    "🔍 Individual Student Inspector",
    "🏫 Department Analytics",
    "📊 Export Formatted Report"
])

with tab1:
    st.subheader("Student Attendance Risk Distribution & GPA Correlation")
    
    col1, col2 = st.columns(2)
    with col1:
        if not df_students.empty:
            risk_counts = df_students["Risk_Level"].value_counts().reset_index()
            risk_counts.columns = ["Risk_Level", "Count"]
            fig_pie = px.pie(
                risk_counts,
                values="Count",
                names="Risk_Level",
                title="Student Risk Classification Ratio",
                color="Risk_Level",
                color_discrete_map={"HIGH": "#e74c3c", "MEDIUM": "#f39c12", "LOW": "#2ecc71"}
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
    with col2:
        if not df_students.empty:
            fig_scatter = px.scatter(
                df_students,
                x="Overall_Attendance_Pct",
                y="Avg_GPA",
                color="Risk_Level",
                hover_data=["Student_Name", "Department"],
                title="Attendance % vs Average GPA Correlation",
                labels={"Overall_Attendance_Pct": "Attendance %", "Avg_GPA": "Average GPA"},
                color_discrete_map={"HIGH": "#e74c3c", "MEDIUM": "#f39c12", "LOW": "#2ecc71"},
                trendline="ols"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    st.subheader("Student Attendance Trajectory Inspection")
    
    student_list = sorted(list(df_raw["Student_Name"].unique()))
    selected_student = st.selectbox("Select Student to Analyze", student_list)
    
    df_single = df_raw[df_raw["Student_Name"] == selected_student].sort_values("Month_Order")
    
    if not df_single.empty:
        c_info1, c_info2, c_info3 = st.columns(3)
        st_summary = df_students[df_students["Student_Name"] == selected_student].iloc[0]
        
        with c_info1:
            st.info(f"**ID:** {st_summary['Student_ID']} | **Dept:** {st_summary['Department']}")
        with c_info2:
            st.metric("Overall Attendance %", f"{st_summary['Overall_Attendance_Pct']}%")
        with c_info3:
            st.metric("Risk Status", st_summary["Risk_Status"])
            
        fig_line = px.line(
            df_single,
            x="Month_Order",
            y="Attendance_Pct",
            color="Semester",
            markers=True,
            title=f"Monthly Attendance Trajectory for {selected_student}",
            labels={"Month_Order": "Timeline (Months across Semesters)", "Attendance_Pct": "Attendance %"}
        )
        fig_line.add_hline(y=75.0, line_dash="dash", line_color="red", annotation_text="75% Minimum Mandatory Threshold")
        st.plotly_chart(fig_line, use_container_width=True)

with tab3:
    st.subheader("Departmental & Semester Comparison")
    dept_grp = df_students.groupby("Department")[["Overall_Attendance_Pct", "Avg_GPA"]].mean().reset_index()
    
    fig_dept = px.bar(
        dept_grp,
        x="Department",
        y="Overall_Attendance_Pct",
        color="Department",
        title="Average Attendance Rate by Department",
        text_auto=".1f"
    )
    st.plotly_chart(fig_dept, use_container_width=True)

with tab4:
    st.subheader("Export Formatted Excel & Audit Summaries")
    st.dataframe(df_students, use_container_width=True)
    
    excel_data = generate_excel_report(df_raw, df_students, kpis)
    st.download_button(
        label="📥 Download Formatted Excel Report (.xlsx)",
        data=excel_data,
        file_name="Student_Attendance_Trend_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("---")
st.caption("Developed by Pratik Sawant | B.Tech Academic Project | Python, Pandas, Streamlit & Excel Automation")
