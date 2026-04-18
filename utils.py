import pandas as pd

# Monthly Payroll Trend
def monthly_trend(df):
    df["month"] = pd.to_datetime(df["date"]).dt.month_name()
    return df.groupby("month")["salary"].sum()

# Cost Per Employee
def cost_per_employee(df):
    return df.groupby("name")["salary"].mean()