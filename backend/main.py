from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import SalaryInput, SalaryOutput, LoanInput, LoanOutput
from salary_logic import calculate_net_salary, calculate_loan_eligibility

app = FastAPI()

# Enable Cross origin resource sharing for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/calculate-salary", response_model=SalaryOutput)
def get_salary(data: SalaryInput):
    gross, tax, net = calculate_net_salary(**data.dict())
    return SalaryOutput(gross_salary=gross, tax=tax, net_salary=net)

@app.post("/calculate-loan", response_model=LoanOutput)
def get_loan(data: LoanInput):
    emi, total, interest, eligible = calculate_loan_eligibility(**data.dict())
    return LoanOutput(emi=emi, total_payment=total, interest_paid=interest, eligible=eligible)
