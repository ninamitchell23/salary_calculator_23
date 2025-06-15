import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Loan Repayment", layout="wide")
st.header("💳 Loan Repayment Area")

payments_file = "payments.csv"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of current script
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))  # two levels up from pages folder

csv_path = os.path.join(PROJECT_ROOT, "backend", "salary_loan_data.csv")
loan_df = pd.read_csv(csv_path)

# Initialize or load payments data
if os.path.exists(payments_file):
    payments_df = pd.read_csv(payments_file)
    total_paid = payments_df["amount"].sum()
else:
    payments_df = pd.DataFrame(columns=["date", "amount"])
    total_paid = 0.0

if st.session_state.get("loan_result") and st.session_state.get("loan_approved"):
    emi, _, _, _, initial_loan = st.session_state.loan_result
    loan_tenure = st.session_state.loan_tenure

    st.write(f"Loan Amount: ${initial_loan:.2f}")
    st.write(f"Tenure: {int(loan_tenure)} months")
    st.write(f"Monthly EMI: ${emi:.2f}")
    st.write(f"Total Paid: ${total_paid:.2f}")

    # Payment Input
    with st.expander("📝 Record a Payment"):
        payment_date = st.date_input("Payment Date", value=datetime.now())
        payment_amount = st.number_input("Amount Paid ($)", min_value=0.0, step=100.0)
        if st.button("Record Payment"):
            new_payment = pd.DataFrame({"date": [payment_date], "amount": [payment_amount]})
            payments_df = pd.concat([payments_df, new_payment], ignore_index=True)
            payments_df.to_csv(payments_file, index=False)
            st.session_state.total_paid = payments_df["amount"].sum()
            st.success(f"Payment of ${payment_amount:.2f} recorded on {payment_date}!")
            st.rerun()

    # --- Visualization Section ---
    st.subheader("📊 Loan Data Visualizations")

    if "loan_df" in st.session_state:
        loan_df = st.session_state.loan_df
    else:
        if loan_df is None or loan_df.empty:
            st.warning("Loan data not available for visualization.")
            loan_df = None

    if loan_df is not None and not loan_df.empty:
        # 1) Loan Amount vs Net Salary colored by eligibility
        fig1 = px.scatter(
            loan_df,
            x='net_salary',
            y='loan_amount',
            color='eligible',
            title="💸 Loan Amount vs Net Salary",
            labels={'net_salary': 'Net Salary', 'loan_amount': 'Loan Amount'}
        )
        st.plotly_chart(fig1, use_container_width=True)

        # 2) EMI vs Loan Amount colored by loan tenure
        fig2 = px.scatter(
            loan_df,
            x='loan_amount',
            y='emi',
            color='loan_tenure',
            title="📅 EMI vs Loan Amount (Colored by Tenure)",
            labels={'loan_amount': 'Loan Amount', 'emi': 'Monthly EMI'},
            color_continuous_scale='bluered'
        )
        st.plotly_chart(fig2, use_container_width=True)

        # 3) Total Repayment vs Loan Amount (Eligible vs Not)
        fig3 = px.bar(
            loan_df,
            x='loan_amount',
            y='total_payment',
            color='eligible',
            barmode='group',
            title="🏁 Total Repayment vs Loan Amount (Eligible vs Not)",
            labels={'loan_amount': 'Loan Amount', 'total_payment': 'Total Repayment'}
        )
        st.plotly_chart(fig3, use_container_width=True)

        # 4) Stacked bar: Principal vs Interest
        loan_df['principal_paid'] = loan_df['loan_amount']
        loan_df['interest_paid'] = loan_df['interest_paid'].fillna(0)
        loan_df_sorted = loan_df.sort_values(by='loan_amount', ascending=True).reset_index()

        fig4 = px.bar(
            loan_df_sorted,
            x=loan_df_sorted.index,
            y=['principal_paid', 'interest_paid'],
            title="📊 Principal vs Interest Paid for Each Loan",
            labels={'value': 'Total Repayment', 'index': 'Applicant Index'},
            barmode='stack'
        )
        st.plotly_chart(fig4, use_container_width=True)

        # 5) Interest Rate vs Net Salary colored by loan tenure
        fig5 = px.scatter(
            loan_df,
            x='net_salary',
            y='annual_interest_rate',
            color='loan_tenure',
            title="📈 Interest Rate vs Net Salary (Colored by Tenure)",
            labels={'net_salary': 'Net Salary', 'annual_interest_rate': 'Interest Rate (%)'},
            color_continuous_scale='Spectral'
        )
        st.plotly_chart(fig5, use_container_width=True)

        # Summary Table
        st.subheader("📋 Loan Summary Table")
        st.dataframe(
            loan_df[['net_salary', 'loan_amount', 'emi', 'loan_tenure', 'interest_paid', 'total_payment', 'eligible']]
        )

    else:
        st.info("Loan data is empty or missing. Cannot show visualizations.")

else:
    st.error("Access denied. You must be eligible and have taken a loan to view this page.")
