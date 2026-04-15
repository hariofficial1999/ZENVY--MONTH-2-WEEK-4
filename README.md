# Zenvy Payroll Dashboard

This repository contains the data analysis and visualization components for the Zenvy Payroll system. The project ingests raw employee data, calculates total compensations and loss of pay based on role and attendance, and visualizes workforce metrics in an interactive Streamlit dashboard.

## Project Structure

The project consists of the following key files:

*   **`app.py`**: The main Streamlit dashboard application. It reads the CSV data, processes the salary metrics on-the-fly, and renders the UI components including data tables and visualizations.
*   **`Data.ipynb`**: The original Jupyter notebook used for exploratory data analysis (EDA), data cleaning, data merging, and prototyping the matplotlib charts.
*   **CSV Data Files**:
    *   `zenvy_employees_new.csv`: Contains employee ID, name, and role.
    *   `zenvy_attendance_new.csv`: Contains employee ID, days present, and leaves taken.
    *   `task_assignment_new.csv`: Contains employee task statuses mapping back to the employee ID.
*   **`final_payroll_with_dates.csv`**: The combined and processed final output dataset containing full salary metrics and chronological identifiers.

## Salary Structure Mapping

Basic salaries are standardized based on the employee's role within the organization:
*   **Python Intern:** ₹15,000
*   **Full Stack:** ₹25,000
*   **Data Science:** ₹30,000
*   **AI/ML:** ₹32,000
*   **Gen AI:** ₹35,000

*Note: Per-day salary is calculated assuming a flat 26-day working month.*

## Installation & Setup

To run this dashboard locally on your machine, ensure you have Python installed along with the requisite dependencies:

1. Open your terminal or command prompt.
2. Install the required libraries using pip:
   ```bash
   pip install pandas matplotlib streamlit
   ```

## Running the Dashboard

Once the dependencies are installed, you can start the Streamlit web server.

1. In your terminal, navigate to the folder containing `app.py` (e.g., `D:\project intership\ZENVY -MONTH 2 WEEK 4\`).
2. Run the following command:
   ```bash
   streamlit run app.py
   ```
3. A browser window will automatically pop up directing you to `http://localhost:8501`.

## Features
- **Key Metrics View:** Quick insights detailing total employees, gross payroll issued, gross lost pay, and median base salaries.
- **Monthly Payroll Trend:** Time-series line chart tracking aggregate payroll scale across months.
- **Cost per Employee Breakdown:** Stylized bar chart providing a comparative view of distinct employee payouts.
- **Processed Data View:** Complete, sortable tabular presentation of every individual's processed payroll figures. 
