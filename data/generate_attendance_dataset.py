"""
AI Attendance Trend Analyzer - Synthetic Dataset Generator
Generates realistic multi-year student attendance and academic tracking data.
"""

import os
import random
import pandas as pd
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(__file__), "sample_attendance_data.csv")

STUDENT_NAMES = [
    "Aarav Sharma", "Priya Kulkarni", "Rahul Deshmukh", "Neha Patil", "Amit Joshi",
    "Siddharth Verma", "Ananya Rao", "Vikram Mane", "Pooja Shinde", "Rohan Pawar",
    "Sneha Kadam", "Tanmay Gaikwad", "Aditya Joshi", "Isha Nair", "Karan Mehta",
    "Meera Iyer", "Nikhil Gupta", "Riya Sen", "Sahil Kapoor", "Tanya Bhatia",
    "Varun Malhotra", "Yash Singhania", "Zoya Khan", "Bhavya Reddy", "Chirag Shetty"
]

DEPARTMENTS = ["Computer Science", "Information Technology", "AI & Data Science"]
SUBJECTS = ["DBMS", "Machine Learning", "Software Engineering", "Data Structures", "Python Programming"]

def generate_dataset(num_students=25):
    records = []
    
    for i in range(1, num_students + 1):
        student_id = f"DYP2024CS{100 + i}"
        student_name = STUDENT_NAMES[(i - 1) % len(STUDENT_NAMES)]
        dept = random.choice(DEPARTMENTS)
        
        # Base attendance trajectory (Good student vs At-Risk student vs Fluctuating)
        profile = random.choices(["CONSISTENT_HIGH", "AT_RISK", "DECLINING", "IMPROVING"], weights=[0.4, 0.2, 0.2, 0.2])[0]
        
        for sem in [1, 2, 3, 4]:
            for month_idx, month_name in enumerate(["Aug", "Sep", "Oct", "Nov"], start=1):
                if profile == "CONSISTENT_HIGH":
                    att_rate = round(random.uniform(82.0, 98.0), 1)
                elif profile == "AT_RISK":
                    att_rate = round(random.uniform(55.0, 74.0), 1)
                elif profile == "DECLINING":
                    att_rate = round(max(50.0, 90.0 - (sem * 6.0) - (month_idx * 3.0) + random.uniform(-4, 4)), 1)
                else: # IMPROVING
                    att_rate = round(min(96.0, 60.0 + (sem * 5.0) + (month_idx * 2.5) + random.uniform(-3, 3)), 1)
                    
                total_classes = random.randint(22, 28)
                attended_classes = int(round(total_classes * (att_rate / 100.0)))
                actual_pct = round((attended_classes / total_classes) * 100.0, 1)
                
                # GPA correlates with attendance
                gpa = round(min(10.0, max(4.0, (actual_pct / 10.0) + random.uniform(-1.0, 0.8))), 2)
                
                records.append({
                    "Student_ID": student_id,
                    "Student_Name": student_name,
                    "Department": dept,
                    "Semester": f"Sem {sem}",
                    "Month": month_name,
                    "Month_Order": month_idx + ((sem - 1) * 4),
                    "Total_Classes": total_classes,
                    "Attended_Classes": attended_classes,
                    "Attendance_Pct": actual_pct,
                    "Semester_GPA": gpa
                })
                
    df = pd.DataFrame(records)
    df.to_csv(DATA_PATH, index=False)
    print(f"[SUCCESS] Generated synthetic dataset with {len(df)} records at {DATA_PATH}")

if __name__ == "__main__":
    generate_dataset()
