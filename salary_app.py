import streamlit as st
import matplotlib.pyplot as plt

def calculate_net_salary(base_salary, allowances, bonuses, tax_rate, deductions):
    gross_salary = base_salary + allowances + bonuses
    tax = gross_salary * (tax_rate / 100)
    total_deductions = deductions + tax
    net_salary = gross_salary - total_deductions
    return gross_salary, tax, net_salary

st.title("💰 Advanced Salary Calculator")

base_salary = st.number_input("Enter Base Salary:", min_value=0.0)
allowances = st.number_input("Enter Allowances:", min_value=0.0)
bonuses = st.number_input("Enter Bonuses:", min_value=0.0)
tax_rate = st.slider("Tax Rate (%)", 0, 50, 10)
deductions = st.number_input("Other Deductions:", min_value=0.0)

if st.button("Calculate"):
    gross, tax, net = calculate_net_salary(base_salary, allowances, bonuses, tax_rate, deductions)
    st.success(f"Gross Salary: ${gross:,.2f}")
    st.warning(f"Tax Deducted: ${tax:,.2f}")
    st.info(f"Net Salary: ${net:,.2f}")
    # Data for the pie chart
    labels = ['Base Salary', 'Allowances', 'Bonuses', 'Tax', 'Other Deductions', 'Net Salary']
    sizes = [base_salary, allowances, bonuses, tax, deductions, net]

    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle

    # Display the chart in Streamlit
    st.pyplot(fig)

    
