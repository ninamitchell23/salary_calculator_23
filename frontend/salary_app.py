import streamlit as st
import matplotlib.pyplot as plt

# --- Initialize session state ---
if "net_salary" not in st.session_state:
    st.session_state.net_salary = None
if "salary_calculated" not in st.session_state:
    st.session_state.salary_calculated = False
if "loan_result" not in st.session_state:
    st.session_state.loan_result = None

# --- Function to calculate Net Salary ---
def calculate_net_salary(base_salary, allowances, bonuses, tax_rate, deductions):
    gross_salary = base_salary + allowances + bonuses
    tax = gross_salary * (tax_rate / 100)
    total_deductions = deductions + tax
    net_salary = gross_salary - total_deductions
    return gross_salary, tax, net_salary

# --- Function to calculate Loan Eligibility and EMI ---
def calculate_loan(monthly_salary, loan_amount, loan_tenure, annual_interest_rate):
    monthly_interest_rate = annual_interest_rate / (12 * 100)
    if monthly_interest_rate == 0:
        emi = loan_amount / loan_tenure
    else:
        emi = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_tenure) / \
              (((1 + monthly_interest_rate) ** loan_tenure) - 1)
    total_payment = emi * loan_tenure
    interest_paid = total_payment - loan_amount
    eligible = emi < (monthly_salary * 0.4)  # Rule: EMI must be < 40% of salary
    return round(emi, 2), round(total_payment, 2), round(interest_paid, 2), eligible

# --- Streamlit App UI ---
st.title("💰 Advanced Salary + Loan Calculator")

# Section 1: Salary Calculator
st.header("📌 Salary Calculator")

base_salary = st.number_input("Enter Base Salary:", min_value=0.0)
allowances = st.number_input("Enter Allowances:", min_value=0.0)
bonuses = st.number_input("Enter Bonuses:", min_value=0.0)
tax_rate = st.slider("Tax Rate (%)", 0, 50, 10)
deductions = st.number_input("Other Deductions:", min_value=0.0)

if st.button("Calculate Salary"):
    gross, tax, net = calculate_net_salary(base_salary, allowances, bonuses, tax_rate, deductions)
    st.session_state.net_salary = net
    st.session_state.salary_calculated = True

    st.success(f"Gross Salary: ${gross:,.2f}")
    st.warning(f"Tax Deducted: ${tax:,.2f}")
    st.info(f"Net Salary (Monthly): ${net:,.2f}")



# Section 2: Loan Calculator
if st.session_state.salary_calculated:
    st.header("💸 Loan Calculator")

    loan_amount = st.number_input("Desired Loan Amount ($)", min_value=0.0, step=100.0)
    loan_tenure = st.number_input("Loan Tenure (in months)", min_value=1)
    interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)

    if st.button("Calculate Loan"):
        net = st.session_state.net_salary
        if net <= 0:
            st.error("❌ Net salary must be greater than 0 to calculate loan eligibility.")
        else:
            emi, total_payment, interest_paid, eligible = calculate_loan(net, loan_amount, loan_tenure, interest_rate)
            st.session_state.loan_result = (emi, total_payment, interest_paid, eligible, loan_amount)

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
    ax2.pie(loan_values, labels=loan_labels, autopct='%1.2f%%', startangle=90, colors=['#4CAF50', '#FF9800'])
    ax2.axis('equal')
    st.pyplot(fig2)
