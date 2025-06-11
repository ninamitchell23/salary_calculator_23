def calculate_net_salary(base_salary, allowances, bonuses, tax_rate, deductions):
    gross_salary = base_salary + allowances + bonuses
    tax = gross_salary * (tax_rate / 100)
    total_deductions = deductions + tax
    net_salary = gross_salary - total_deductions
    return round(gross_salary, 2), round(tax, 2), round(net_salary, 2)


def calculate_loan_eligibility(net_salary, loan_amount, loan_tenure, annual_interest_rate):
    monthly_interest_rate = annual_interest_rate / (12 * 100)
    if monthly_interest_rate == 0:
        emi = loan_amount / loan_tenure
    else:
        emi = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_tenure) / \
              (((1 + monthly_interest_rate) ** loan_tenure) - 1)
    total_payment = emi * loan_tenure
    interest_paid = total_payment - loan_amount
    eligible = emi < (net_salary * 0.4)
    return round(emi, 2), round(total_payment, 2), round(interest_paid, 2), eligible
