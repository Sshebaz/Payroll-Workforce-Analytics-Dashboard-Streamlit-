import pandas as pd

# -----------------------------
# Load Data
# -----------------------------
employees = pd.read_csv("zenvy_employees_new.csv")
attendance = pd.read_csv("zenvy_attendance_new.csv")
tasks = pd.read_csv("task_assignment_new.csv")

# -----------------------------
# Clean Columns
# -----------------------------
employees.columns = employees.columns.str.strip().str.lower()
attendance.columns = attendance.columns.str.strip().str.lower()
tasks.columns = tasks.columns.str.strip().str.lower()

# -----------------------------
# Base Salary Mapping
# -----------------------------
salary_map = {
    "Python Intern": 20000,
    "Full Stack": 60000,
    "Data Science": 70000,
    "AI/ML": 80000,
    "Gen AI": 90000
}

# -----------------------------
# Department Mapping
# -----------------------------
dept_map = {
    "Python Intern": "Engineering",
    "Full Stack": "Engineering",
    "Data Science": "Data",
    "AI/ML": "AI",
    "Gen AI": "AI"
}

# -----------------------------
# Apply Base Salary
# -----------------------------
employees["base_salary"] = employees["role"].map(salary_map)

# Handle missing salary
employees["base_salary"].fillna(30000, inplace=True)

# -----------------------------
# Merge Attendance
# -----------------------------
attendance_summary = attendance.groupby("employee_id").sum().reset_index()

df = employees.merge(attendance_summary, on="employee_id", how="left")

# Fill missing attendance values
df["days_present"].fillna(0, inplace=True)
df["leaves"].fillna(0, inplace=True)

# -----------------------------
# Attendance Bonus & Penalty
# -----------------------------
df["attendance_bonus"] = df["days_present"] * 500
df["leave_penalty"] = df["leaves"] * 300

# -----------------------------
# Task Summary
# -----------------------------
task_summary = tasks.groupby("employee_id").size().reset_index(name="total_tasks")

df = df.merge(task_summary, on="employee_id", how="left")

# Fill missing task values
df["total_tasks"].fillna(0, inplace=True)

# -----------------------------
# Task Bonus
# -----------------------------
df["task_bonus"] = df["total_tasks"] * 1000

# -----------------------------
# Final Salary Calculation
# -----------------------------
df["salary"] = (
    df["base_salary"]
    + df["attendance_bonus"]
    - df["leave_penalty"]
    + df["task_bonus"]
)

# -----------------------------
# Department
# -----------------------------
df["department"] = df["role"].map(dept_map)
df["department"].fillna("Other", inplace=True)

# -----------------------------
# 🔥 ADD DATE COLUMN (Week-4 Requirement)
# -----------------------------
dates = pd.date_range(start="2024-01-01", periods=len(df), freq="M")
df["date"] = dates

# -----------------------------
# Final Dataset
# -----------------------------
payroll_df = df.copy()

# -----------------------------
# Save
# -----------------------------
payroll_df.to_csv("payroll_dataset.csv", index=False)

print(payroll_df.head())