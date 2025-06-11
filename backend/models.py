from pydantic import BaseModel

class SalaryInput(BaseModel):
    base_salary: float
    allowances: float
    bonuses: float
    tax_rate: float
    deductions: float

class SalaryOutput(BaseModel):
    gross_salary: float
    tax: float
    net_salary: float

class LoanInput(BaseModel):
    net_salary: float
    loan_amount: float
    loan_tenure: int
    annual_interest_rate: float

class LoanOutput(BaseModel):
    emi: float
    total_payment: float
    interest_paid: float
    eligible: bool
