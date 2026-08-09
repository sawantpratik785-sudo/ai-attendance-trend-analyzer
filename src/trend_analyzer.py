"""
AI Attendance Trend Analyzer - Predictive Core Engine
Calculates rolling metrics, linear trend slopes, risk flag classifier, and academic correlation.
"""

import os
import pandas as pd
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_attendance_data.csv")

class AttendanceTrendAnalyzer:
    def __init__(self, data_filepath=DATA_PATH):
        self.data_filepath = data_filepath

    def load_data(self):
        if not os.path.exists(self.data_filepath):
            from data.generate_attendance_dataset import generate_dataset
            generate_dataset()
        return pd.read_csv(self.data_filepath)

    def calculate_student_trends(self, df):
        if df.empty:
            return pd.DataFrame()

        # Group by student and analyze trajectory
        student_summaries = []

        for student_id, group in df.groupby("Student_ID"):
            group = group.sort_values("Month_Order")
            student_name = group["Student_Name"].iloc[0]
            dept = group["Department"].iloc[0]
            
            total_classes = group["Total_Classes"].sum()
            total_attended = group["Attended_Classes"].sum()
            overall_pct = round((total_attended / total_classes) * 100.0, 2)
            avg_gpa = round(group["Semester_GPA"].mean(), 2)

            # Recent 3-month trend vs historical
            recent_pct = group.tail(3)["Attendance_Pct"].mean()
            prior_pct = group.iloc[:-3]["Attendance_Pct"].mean() if len(group) > 3 else recent_pct
            trend_delta = round(recent_pct - prior_pct, 2)

            # Slope calculation
            x = group["Month_Order"].values
            y = group["Attendance_Pct"].values
            if len(x) > 1:
                slope = np.polyfit(x, y, 1)[0]
            else:
                slope = 0.0

            # Classification Logic
            if overall_pct < 75.0:
                risk_status = "CRITICAL_SHORTAGE (<75%)"
                risk_level = "HIGH"
            elif overall_pct < 80.0 or slope < -1.5:
                risk_status = "WARNING_DECLINING"
                risk_level = "MEDIUM"
            else:
                risk_status = "SAFE_COMPLIANT"
                risk_level = "LOW"

            student_summaries.append({
                "Student_ID": student_id,
                "Student_Name": student_name,
                "Department": dept,
                "Total_Classes": total_classes,
                "Attended_Classes": total_attended,
                "Overall_Attendance_Pct": overall_pct,
                "Recent_3M_Avg": round(recent_pct, 2),
                "Trend_Delta": trend_delta,
                "Trajectory_Slope": round(slope, 2),
                "Avg_GPA": avg_gpa,
                "Risk_Status": risk_status,
                "Risk_Level": risk_level
            })

        return pd.DataFrame(student_summaries).sort_values("Overall_Attendance_Pct")

    def get_kpi_metrics(self, df_students):
        if df_students.empty:
            return {}

        total_students = len(df_students)
        high_risk_count = len(df_students[df_students["Risk_Level"] == "HIGH"])
        warning_count = len(df_students[df_students["Risk_Level"] == "MEDIUM"])
        safe_count = len(df_students[df_students["Risk_Level"] == "LOW"])
        avg_att = round(df_students["Overall_Attendance_Pct"].mean(), 2)
        
        # Correlation
        corr = df_students["Overall_Attendance_Pct"].corr(df_students["Avg_GPA"])

        return {
            "Total_Students": total_students,
            "Avg_Attendance_Pct": avg_att,
            "High_Risk_Count": high_risk_count,
            "Warning_Count": warning_count,
            "Safe_Count": safe_count,
            "Attendance_GPA_Correlation": round(corr, 2) if not np.isnan(corr) else 0.0
        }
