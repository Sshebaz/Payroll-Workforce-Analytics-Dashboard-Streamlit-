import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


# Page Config

st.set_page_config(page_title="Payroll Dashboard", layout="wide")

st.title("Payroll & Workforce Analytics Dashboard")


# Load Data

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(__file__)

    payroll = pd.read_csv(os.path.join(BASE_DIR, "payroll_dataset.csv"))
    attendance = pd.read_csv(os.path.join(BASE_DIR, "zenvy_attendance_new.csv"))
    tasks = pd.read_csv(os.path.join(BASE_DIR, "task_assignment_new.csv"))

    return payroll, attendance, tasks

payroll, attendance, tasks = load_data()


# Clean Column Names

payroll.columns = payroll.columns.str.strip().str.lower()
attendance.columns = attendance.columns.str.strip().str.lower()
tasks.columns = tasks.columns.str.strip().str.lower()


# Sidebar Filter

st.sidebar.header("Filters")

department_filter = st.sidebar.selectbox(
    "Select Department",
    ["All"] + list(payroll["department"].unique())
)

if department_filter != "All":
    payroll = payroll[payroll["department"] == department_filter]


# Data Processing

# Attendance Summary
attendance_summary = attendance.groupby("employee_id").sum().reset_index()

# Add attendance rate
attendance_summary["attendance_rate"] = (
    attendance_summary["days_present"] /
    (attendance_summary["days_present"] + attendance_summary["leaves"])
)

# Task Summary
task_summary = tasks.groupby("employee_id").size().reset_index(name="total_tasks")

# Merge all datasets
df = payroll.merge(attendance_summary, on="employee_id")
df = df.merge(task_summary, on="employee_id")


# KPI Section

st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

total_salary = df["salary"].sum()
avg_salary = df["salary"].mean()
avg_attendance = df["days_present"].mean()

col1.metric("Total Salary", f"{total_salary}")
col2.metric("Avg Salary", f"{round(avg_salary,2)}")
col3.metric("Avg Attendance", f"{round(avg_attendance,1)}")


# Charts Section

st.subheader("Visual Insights")

col1, col2 = st.columns(2)

# Salary Bar Chart
with col1:
    fig, ax = plt.subplots()
    ax.bar(df["name"], df["salary"])
    ax.set_title("Salary by Employee")
    ax.set_xlabel("Employee")
    ax.set_ylabel("Salary")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Attendance Line Chart
with col2:
    fig, ax = plt.subplots()
    ax.plot(df["name"], df["days_present"], marker='o')
    ax.set_title("Attendance Trend")
    ax.set_xlabel("Employee")
    ax.set_ylabel("Days Present")
    plt.xticks(rotation=45)
    st.pyplot(fig)


# Department Insights

st.subheader("Department Insights")

dept_salary = df.groupby("department")["salary"].mean()
dept_attendance = df.groupby("department")["days_present"].mean()

col1, col2 = st.columns(2)

with col1:
    st.write("Average Salary by Department")
    fig, ax = plt.subplots()
    dept_salary.plot(kind="bar", ax=ax)
    st.pyplot(fig)

with col2:
    st.write("Average Attendance by Department")
    fig, ax = plt.subplots()
    dept_attendance.plot(kind="line", marker='o', ax=ax)
    st.pyplot(fig)


# Task Insights

st.subheader("Task Analysis")

fig, ax = plt.subplots()
ax.bar(df["name"], df["total_tasks"])
ax.set_title("Tasks Assigned per Employee")
plt.xticks(rotation=45)
st.pyplot(fig)


# Data Table

st.subheader("Final Merged Dataset")
st.dataframe(df)