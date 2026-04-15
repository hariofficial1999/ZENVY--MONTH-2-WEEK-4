import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page aesthetic
st.set_page_config(page_title="Zenvy Payroll Dashboard", page_icon="💰", layout="wide")
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    h2 {
        color: #333333;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("💰 Zenvy Payroll Dashboard")

# Function to load and process data
@st.cache_data
def load_and_process_data():
    try:
        employees = pd.read_csv("zenvy_employees_new.csv")
        attendance = pd.read_csv("zenvy_attendance_new.csv")
        tasks = pd.read_csv("task_assignment_new.csv")
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        return None, None, None

    # Clean role column
    if "role" in employees.columns:
        employees["role"] = employees["role"].str.strip()

    # Create task count
    task_count = tasks.groupby("employee_id").size().reset_index(name="task_count")

    # Merge data
    payroll = employees.merge(attendance, on="employee_id", how="inner")
    payroll = payroll.merge(task_count, on="employee_id", how="left")
    payroll["task_count"] = payroll["task_count"].fillna(0).astype(int)

    # Salary calculations
    salary_map = {
        "Python Intern": 15000,
        "Full Stack": 25000,
        "Data Science": 30000,
        "AI/ML": 32000,
        "Gen AI": 35000
    }
    payroll["basic_salary"] = payroll["role"].map(salary_map)
    payroll["per_day_salary"] = payroll["basic_salary"] / 26
    payroll["salary_paid"] = payroll["per_day_salary"] * payroll["days_present"]
    payroll["loss_of_pay"] = payroll["per_day_salary"] * payroll["leaves"]

    # Add dates
    payroll = payroll.sort_values("employee_id").reset_index(drop=True)
    payroll["date"] = pd.date_range(start="2025-01-01", periods=len(payroll), freq="MS")
    payroll["month"] = payroll["date"].dt.strftime("%b-%Y")

    monthly_payroll = payroll.groupby("month", as_index=False)["salary_paid"].sum()
    cost_per_employee = payroll[["employee_id", "name", "role", "salary_paid"]]

    return payroll, monthly_payroll, cost_per_employee


payroll, monthly_payroll, cost_per_employee = load_and_process_data()

if payroll is not None:
    # Summary Metrics Row
    st.markdown("## Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Employees", value=len(payroll))
    with col2:
        st.metric(label="Total Payroll Paid", value=f"₹{payroll['salary_paid'].sum():,.2f}")
    with col3:
        st.metric(label="Total Loss of Pay", value=f"₹{payroll['loss_of_pay'].sum():,.2f}")
    with col4:
        st.metric(label="Average Basic Salary", value=f"₹{payroll['basic_salary'].mean():,.2f}")
    
    st.markdown("---")
    
    st.markdown("## Analytics")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("<h3 style='text-align: center; color: #444;'>Monthly Payroll Trend</h3>", unsafe_allow_html=True)
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.plot(monthly_payroll["month"], monthly_payroll["salary_paid"], marker="o", color='#1f77b4', linewidth=2)
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Total Payroll")
        ax1.grid(True, linestyle='--', alpha=0.7)
        # remove borders
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        st.pyplot(fig1)

    with col_chart2:
        st.markdown("<h3 style='text-align: center; color: #444;'>Cost per Employee</h3>", unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        # Ensure we're using string names and dealing with potential matching lengths properly
        ax2.bar(cost_per_employee["name"], cost_per_employee["salary_paid"], color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
        ax2.set_xlabel("Employee Name")
        ax2.set_ylabel("Salary Paid")
        plt.xticks(rotation=45)
        # remove borders
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        st.pyplot(fig2)

    st.markdown("---")

    # Data Table
    st.markdown("## Full Data View")
    st.dataframe(payroll.style.format({
        "basic_salary": "₹{:.2f}",
        "per_day_salary": "₹{:.2f}",
        "salary_paid": "₹{:.2f}",
        "loss_of_pay": "₹{:.2f}"
    }), use_container_width=True)

