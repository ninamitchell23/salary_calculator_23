import pandas as pd
import os

# Define CSV file path
CSV_FILE = os.path.join(os.path.dirname(__file__), "salary_loan_data.csv")

# Initialize CSV with header row if it doesn't exist or is empty
if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
    initial_data = pd.DataFrame(columns=[
        'base_salary', 'allowances', 'bonuses', 'tax_rate', 'deductions',
        'gross_salary', 'tax', 'net_salary', 'loan_amount', 'loan_tenure',
        'annual_interest_rate', 'emi', 'total_payment', 'interest_paid', 'eligible'
    ])
    initial_data.to_csv(CSV_FILE, index=False)

def calculate_net_salary(base_salary, allowances, bonuses, tax_rate, deductions):
    data = pd.DataFrame({
        'base_salary': [base_salary],
        'allowances': [allowances],
        'bonuses': [bonuses],
        'tax_rate': [tax_rate],
        'deductions': [deductions]
    })
    
    data['gross_salary'] = data['base_salary'] + data['allowances'] + data['bonuses']
    data['tax'] = data['gross_salary'] * (data['tax_rate'] / 100)
    data['total_deductions'] = data['deductions'] + data['tax']
    data['net_salary'] = data['gross_salary'] - data['total_deductions']
    
    # Append to existing data
    if os.path.exists(CSV_FILE):
        existing_data = pd.read_csv(CSV_FILE)
        updated_data = pd.concat([existing_data, data], ignore_index=True)
    else:
        updated_data = data
    updated_data.to_csv(CSV_FILE, index=False)
    
    return (
        round(float(data['gross_salary'].iloc[0]), 2),
        round(float(data['tax'].iloc[0]), 2),
        round(float(data['net_salary'].iloc[0]), 2)
    )

def calculate_loan_eligibility(net_salary, loan_amount, loan_tenure, annual_interest_rate):
    data = pd.DataFrame({
        'net_salary': [net_salary],
        'loan_amount': [loan_amount],
        'loan_tenure': [loan_tenure],
        'annual_interest_rate': [annual_interest_rate]
    })
    
    data['monthly_interest_rate'] = data['annual_interest_rate'] / (12 * 100)
    data['emi'] = data.apply(
        lambda row: row['loan_amount'] / row['loan_tenure'] if row['monthly_interest_rate'] == 0
        else row['loan_amount'] * row['monthly_interest_rate'] * ((1 + row['monthly_interest_rate']) ** row['loan_tenure']) /
             (((1 + row['monthly_interest_rate']) ** row['loan_tenure'] - 1)),
        axis=1
    )
    data['total_payment'] = data['emi'] * data['loan_tenure']
    data['interest_paid'] = data['total_payment'] - data['loan_amount']
    data['eligible'] = data['emi'] < (data['net_salary'] * 0.4)
    
    # Append to existing data
    if os.path.exists(CSV_FILE):
        existing_data = pd.read_csv(CSV_FILE)
        loan_data = data[['net_salary', 'loan_amount', 'loan_tenure', 'annual_interest_rate', 'emi', 'total_payment', 'interest_paid', 'eligible']]
        updated_data = pd.concat([existing_data, loan_data], ignore_index=True)
    else:
        updated_data = data
    updated_data.to_csv(CSV_FILE, index=False)
    
    return (
        round(float(data['emi'].iloc[0]), 2),
        round(float(data['total_payment'].iloc[0]), 2),
        round(float(data['interest_paid'].iloc[0]), 2),
        bool(data['eligible'].iloc[0])
    )