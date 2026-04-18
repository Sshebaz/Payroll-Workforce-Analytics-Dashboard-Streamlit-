import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from utils import monthly_trend, cost_per_employee

# Page config
st.set_page_config(page_title="Payroll Dashboard", layout="wide")
st.title("📊 Payroll & Workforce Analytics Dashboard")

# Load Data
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(BASE_DIR, "payroll_dataset.csv"))
    return df

df = load_data()

# Clean columns
df.columns = df.columns.str.strip().str.lower()

# Sidebar Filter
st.sidebar.header("🔍 Filters")

dept_filter = st.sidebar.selectbox(
    "Select Department",
    ["All"] + list(df["department"].unique())
)

if dept_filter != "All":
    df = df[df["department"] == dept_filter]

# KPI Section
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Salary", int(df["salary"].sum()))
col2.metric("📊 Avg Salary", round(df["salary"].mean(), 2))
col3.metric("📅 Avg Attendance", round(df["days_present"].mean(), 1))

# -----------------------------
# Week 3 Charts
# -----------------------------
st.subheader("📊 Employee Insights")

col1, col2 = st.columns(2)

# Salary Chart
with col1:
    fig, ax = plt.subplots()
    ax.bar(df["name"], df["salary"])
    ax.set_title("Salary by Employee")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Attendance Chart
with col2:
    fig, ax = plt.subplots()
    ax.plot(df["name"], df["days_present"], marker='o')
    ax.set_title("Attendance Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Department Insights
st.subheader("🏢 Department Insights")

dept_salary = df.groupby("department")["salary"].mean()
dept_attendance = df.groupby("department")["days_present"].mean()

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    dept_salary.plot(kind="bar", ax=ax)
    ax.set_title("Avg Salary by Department")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    dept_attendance.plot(kind="line", marker='o', ax=ax)
    ax.set_title("Avg Attendance by Department")
    st.pyplot(fig)

# Task Analysis
st.subheader("📋 Task Analysis")

task_counts = df.groupby("name")["total_tasks"].sum()

fig, ax = plt.subplots()
task_counts.plot(kind="bar", ax=ax)
ax.set_title("Tasks per Employee")
plt.xticks(rotation=45)

st.pyplot(fig)

# Week 4 Features

st.header("📈 Advanced Analytics (Week-4)")

# Monthly Trend
st.subheader(" Monthly Payroll Trend")

trend = monthly_trend(df)

fig, ax = plt.subplots()
trend.plot(kind="line", marker='o', ax=ax)
ax.set_title("Payroll Trend")

st.pyplot(fig)

# Cost Per Employee
st.subheader("💰 Cost Per Employee")

cost = cost_per_employee(df)

fig, ax = plt.subplots()
cost.plot(kind="bar", ax=ax)
plt.xticks(rotation=45)

st.pyplot(fig)

# Final Data Table
st.subheader(" Final Dataset")
st.dataframe(df)
