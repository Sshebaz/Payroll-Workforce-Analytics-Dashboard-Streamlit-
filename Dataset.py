import pandas as pd


# Load Employee Data

employees = pd.read_csv("zenvy_employees_new.csv")

# Clean column names
employees.columns = employees.columns.str.strip().str.lower()


# Create Salary Mapping (based on role)

salary_map = {
    "Python Intern": 20000,
    "Full Stack": 60000,
    "Data Science": 70000,
    "AI/ML": 80000,
    "Gen AI": 90000
}


# Create Department Mapping

dept_map = {
    "Python Intern": "Engineering",
    "Full Stack": "Engineering",
    "Data Science": "Data",
    "AI/ML": "AI",
    "Gen AI": "AI"
}


# Apply Mappings

employees["salary"] = employees["role"].map(salary_map)
employees["department"] = employees["role"].map(dept_map)


# Handle Missing Values (important)

employees["salary"].fillna(30000, inplace=True)
employees["department"].fillna("Other", inplace=True)


# Final Payroll Dataset

payroll_df = employees.copy()


# Preview

print(payroll_df.head())


# Save to CSV

payroll_df.to_csv("payroll_dataset.csv", index=False)