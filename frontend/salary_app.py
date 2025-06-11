import streamlit as st
import requests
import matplotlib.pyplot as plt
import os

# Use environment variable for flexibility inside Docker
API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("💰 Advanced Salary + Loan Calculator")

# --- Initialize session state ---
if "net_salary" not in st.session_state:
    st.session_state.net_salary = None
if "salary_calculated" not in st.session_state:
    st.session_state.salary_calculated = False
if "loan_result" not in st.session_state:
    st.session_state.loan_result = None

# --- Section 1: Salary Calculator ---
st.header("📌 Salary Calculator")

base_salary = st.number_input("Enter Base Salary:", min_value=0.0)
allowances = st.number_input("Enter Allowances:", min_value=0.0)
bonuses = st.number_input("Enter Bonuses:", min_value=0.0)
tax_rate = st.slider("Tax Rate (%)", 0, 50, 10)
deductions = st.number_input("Other Deductions:", min_value=0.0)

if st.button("Calculate Salary"):
    salary_payload = {
        "base_salary": base_salary,
        "allowances": allowances,
        "bonuses": bonuses,
        "tax_rate": tax_rate,
        "deductions": deductions
    }

    try:
        response = requests.post(f"{API_BASE_URL}/calculate-salary", json=salary_payload)
        response.raise_for_status()

        data = response.json()
        st.session_state.net_salary = data["net_salary"]
        st.session_state.salary_calculated = True

        st.success(f"Gross Salary: ${data['gross_salary']:,.2f}")
        st.warning(f"Tax Deducted: ${data['tax']:,.2f}")
        st.info(f"Net Salary (Monthly): ${data['net_salary']:,.2f}")

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to calculate salary: {e}")

# --- Section 2: Loan Calculator ---
if st.session_state.salary_calculated:
    st.header("💸 Loan Calculator")

    loan_amount = st.number_input("Desired Loan Amount ($)", min_value=0.0, step=100.0)
    loan_tenure = st.number_input("Loan Tenure (in months)", min_value=1)
    interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)

    if st.button("Calculate Loan"):
        loan_payload = {
            "net_salary": st.session_state.net_salary,
            "loan_amount": loan_amount,
            "loan_tenure": loan_tenure,
            "annual_interest_rate": interest_rate
        }

        try:
            response = requests.post(f"{API_BASE_URL}/calculate-loan", json=loan_payload)
            response.raise_for_status()

            data = response.json()
            st.session_state.loan_result = (
                data["emi"], data["total_payment"], data["interest_paid"], data["eligible"], loan_amount
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to calculate loan eligibility: {e}")

# --- Loan Results ---
if st.session_state.loan_result:
    emi, total_payment, interest_paid, eligible, loan_amount = st.session_state.loan_result

    st.subheader("📊 Loan Summary")
    st.write(f"**Monthly EMI (Equated Monthly Installment):** ${emi}")
    st.write(f"**Total Payment (Principal + Interest):** ${total_payment}")
    st.write(f"**Total Interest Payable:** ${interest_paid}")

    if eligible:
        st.success("✅ You are eligible for this loan.")
    else:
        st.error("🚫 EMI exceeds 40% of your net salary. Please lower the loan amount or increase the tenure.")

    # Loan breakdown chart
    loan_labels = ['Principal', 'Interest']
    loan_values = [loan_amount, interest_paid]
    fig2, ax2 = plt.subplots()
    ax2.pie(loan_values, labels=loan_labels, autopct='%1.2f%%', startangle=90,
            colors=['#4CAF50', '#FF9800'])
    ax2.axis('equal')
    st.pyplot(fig2)
