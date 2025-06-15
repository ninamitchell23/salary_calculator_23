import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.header("📊 Admin Dashboard - Data Visualizations")

# Use environment variable for flexibility inside Docker
csv_path = "/app/salary_loan_data.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    if not df.empty:
        st.write("### Summary of User Data")
        st.write(f"Total Entries: {len(df)}")

        # Net Salary Trend (Line Chart)
        if 'net_salary' in df.columns:
            fig1, ax1 = plt.subplots()
            ax1.plot(df.index, df['net_salary'], marker='o', label='Net Salary')
            ax1.set_xlabel('Entry Number')
            ax1.set_ylabel('Net Salary ($)')
            ax1.set_title('Net Salary Trend')
            ax1.legend()
            ax1.grid(True)
            st.pyplot(fig1)

        # Loan Breakdown (Pie Chart) - Average per Entry
        if 'loan_amount' in df.columns and 'interest_paid' in df.columns:
            avg_loan_amount = df['loan_amount'].mean() if not df['loan_amount'].empty else 0
            avg_interest_paid = df['interest_paid'].mean() if not df['interest_paid'].empty else 0
            fig2, ax2 = plt.subplots()
            ax2.pie([avg_loan_amount, avg_interest_paid], labels=['Principal', 'Interest'], autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF9800'])
            ax2.axis('equal')
            ax2.set_title('Average Loan Breakdown')
            st.pyplot(fig2)
    else:
        st.write("No data available yet. Encourage customers to use the system.")
else:
    st.write("No data stored yet. Encourage customers to use the system.")

# Back Button
if st.page_link("salary_app.py", label="⬅ Back"):
    pass