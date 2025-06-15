# import streamlit as st

# st.title("💼 Salary & Loan System")
# st.markdown("### 🌟 Welcome to Your Financial Hub!")
# st.write("This advanced salary and loan calculator enables customers to calculate their net salary, which is then used for loan eligibility calculations. The admin can view visualizations of customer data collected.")
# st.write("Select your role to begin:")

# # Role Selection
# col1, col2, col3 = st.columns([1, 2, 1])
# with col1:
#     st.write("")
# with col2:
#     col_button1, col_button2 = st.columns(2)
#     with col_button1:
#         st.page_link("pages/customer.py", label="🎯 Customer", help="Access loan calculations")
#     with col_button2:
#         st.page_link("pages/admin.py", label="🔒 Admin", help="View data visualizations")
# with col3:
#     st.write("")

# st.markdown("---")

import streamlit as st
#from streamlit_extras.switch_page_button import switch_page
import requests
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Customer Dashboard", layout="wide")
st.header("💰 Customer Dashboard - Loan Calculator")

# Determine active section based on query parameters
section = st.query_params.get("section", [""])[0]
st.write(f"Debug: Current section = {section}, loan_approved = {st.session_state.get('loan_approved', False)}")  # Debug output

# User Guide
with st.expander("📖 User Guide - Understanding Your Finances"):
    st.write("### Welcome to Your Financial Journey!")
    st.write("This dashboard helps you calculate your net salary and check if you can get a loan. Here’s what each term means:")
    st.write("- **Allowances**: Extra money added to your base salary, like housing or transport allowances. For example, if your company pays for your rent, that’s an allowance!")
    st.write("- **Bonuses**: Extra rewards you might receive for good work or performance, like a year-end bonus. It’s like a thank-you gift from your employer.")
    st.write("- **Tax Rate**: This is the percentage of your income the government takes to fund public services. It’s fixed based on your total income: 10% if your total earnings (base salary + allowances + bonuses) are up to $5,000, and 20% if they’re above $5,000.")
    st.write("- **Deductions**: Money taken out of your salary for things like insurance, existing loans, or other commitments. For instance, if you pay for health insurance, that’s a deduction.")
    st.write("To get a loan, we first calculate your net salary. Then, we check eligibility. Eligible users can take a loan, compare EMIs, or see their remaining loan balance over time after approval. Payment tracking is available post-approval.")
    st.write("Start by entering your details below!")

# Use environment variable for flexibility inside Docker
API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Initialize session state
if "net_salary" not in st.session_state:
    st.session_state.net_salary = None
if "salary_calculated" not in st.session_state:
    st.session_state.salary_calculated = False
if "loan_result" not in st.session_state:
    st.session_state.loan_result = None
if "comparison_results" not in st.session_state:
    st.session_state.comparison_results = None
if "loan_approved" not in st.session_state:
    st.session_state.loan_approved = False
if "total_paid" not in st.session_state:
    st.session_state.total_paid = 0.0
if "loan_tenure" not in st.session_state:
    st.session_state.loan_tenure = 0

# Load or create payments file

# Define CSV file path
CSV_FILE = os.path.join(os.path.dirname(__file__), "payments.csv")

# Initialize CSV with header row if it doesn't exist or is empty
if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
    initial_data = pd.DataFrame(columns=[
        "date", "amount"
    ])
    initial_data.to_csv(CSV_FILE, index=False)

# payments_file = "/app/payments.csv"
# if os.path.exists(payments_file):
#     try:
#         payments_df = pd.read_csv(payments_file)
#         if payments_df.empty or payments_df.columns.size == 0:
#             payments_df = pd.DataFrame(columns=["date", "amount"])
#             st.warning("payments.csv was empty or lacked columns, initialized with default columns.")
#             payments_df.to_csv(payments_file, index=False)
#         else:
#             st.session_state.total_paid = payments_df["amount"].sum()
#             st.write(f"Debug: Loaded payments.csv with {len(payments_df)} rows, total paid: ${st.session_state.total_paid:.2f}")
#     except pd.errors.EmptyDataError:
#         payments_df = pd.DataFrame(columns=["date", "amount"])
#         st.warning("payments.csv had no columns, initialized with default columns.")
#         payments_df.to_csv(payments_file, index=False)
#         st.session_state.total_paid = 0.0
# else:
#     payments_df = pd.DataFrame(columns=["date", "amount"])
#     st.warning(f"payments.csv not found at {payments_file}, creating new file with default columns.")
#     payments_df.to_csv(payments_file, index=False)
#     st.session_state.total_paid = 0.0
# st.write(f"Debug: payments_df columns: {payments_df.columns.tolist()}")

# Debug: List files in pages directory
# import glob
# pages_dir = "/app/pages/"
# st.write(f"Debug: Files in pages directory: {glob.glob(pages_dir + '*.py')}")

# Salary Calculator
base_salary = st.number_input("Enter Base Salary:", min_value=0.0)
allowances = st.number_input("Enter Allowances:", min_value=0.0)
bonuses = st.number_input("Enter Bonuses:", min_value=0.0)
deductions = st.number_input("Other Deductions:", min_value=0.0)

# Calculate total income for fixed tax rate
total_income = base_salary + allowances + bonuses
tax_rate = 0.10 if total_income <= 5000 else 0.20  # Fixed tax rate: 10% up to $5,000, 20% above

if st.button("Calculate Salary"):
    payload = {
        "base_salary": base_salary,
        "allowances": allowances,
        "bonuses": bonuses,
        "tax_rate": tax_rate,
        "deductions": deductions
    }
    try:
        response = requests.post(f"{API_BASE_URL}/calculate-salary", json=payload)
        response.raise_for_status()
        data = response.json()
        st.session_state.net_salary = data["net_salary"]
        st.session_state.salary_calculated = True
        st.success(f"Gross Salary: ${data['gross_salary']:.2f}")
        st.warning(f"Tax Deducted: ${data['tax']:.2f} (at {int(tax_rate * 100)}%)")
        st.info(f"Net Salary: ${data['net_salary']:.2f}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

# Loan Calculator
if st.session_state.salary_calculated:
    st.header("💸 Loan Calculator")
    loan_amount = st.number_input("Desired Loan Amount ($):", min_value=0.0, step=100.0)
    loan_tenure = st.number_input("Loan Tenure (months):", min_value=1)
    interest_rate = st.number_input("Annual Interest Rate (%):", min_value=0.0)

    if st.button("Calculate Loan"):
        payload = {
            "net_salary": st.session_state.net_salary,
            "loan_amount": loan_amount,
            "loan_tenure": loan_tenure,
            "annual_interest_rate": interest_rate
        }
        try:
            response = requests.post(f"{API_BASE_URL}/calculate-loan", json=payload)
            response.raise_for_status()
            data = response.json()
            st.session_state.loan_result = (
                data["emi"], data["total_payment"], data["interest_paid"], data["eligible"], loan_amount
            )
            st.session_state.loan_tenure = loan_tenure  # Store tenure in session state
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")

    # Loan Results
    if st.session_state.loan_result:
        emi, total_payment, interest_paid, eligible, loan_amount = st.session_state.loan_result
        st.subheader("📊 Loan Summary")
        st.write(f"**Monthly EMI:** ${emi:.2f}")
        st.write(f"**Total Payment:** ${total_payment:.2f}")
        st.write(f"**Interest Paid:** ${interest_paid:.2f}")
        if eligible:
            st.success("✅ Eligible for loan")
            st.session_state.loan_approved = True
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("")
            with col2:
                col_button1, col_button2 = st.columns(2)
                with col_button1:
                    st.page_link("pages/repayment.py", label="📥 Take Loan", help="Go to loan repayment page")
                with col_button2:
                    def compare_emi_callback():
                        st.query_params.update({"section": "comparison"})
                        st.rerun()
                    st.button("Custom EMI Comparison", on_click=compare_emi_callback, help="Compare loan scenarios")
            with col3:
                def remaining_loan_callback():
                    st.query_params.update({"section": "remaining"})
                    st.rerun()
                st.button("Remaining Loan Over Time", on_click=remaining_loan_callback, help="View loan balance over time")
        else:
            st.error("🚫 Not eligible")
            st.write("Adjust your loan amount or tenure and recalculate to improve eligibility.")

        

    


