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

    fig, ax = plt.subplots(figsize=(8, 8))

    # Create pie chart WITHOUT labels or autopct
    wedges, texts = ax.pie(
        sizes, 
        startangle=90,
        wedgeprops=dict(width=0.4)  # Optional: donut style
    )

    # Format percentages for legend
    percentages = [f"{(s / sum(sizes)) * 100:.2f}%" for s in sizes]
    custom_labels = [f"{label}: {pct}" for label, pct in zip(labels, percentages)]

    # Add a clean legend instead of overlapping labels
    ax.legend(wedges, custom_labels, title="Salary Breakdown", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    ax.axis('equal')  # Make pie chart round
    st.pyplot(fig)
    
