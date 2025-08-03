from pydantic import BaseModel
from typing import Optional

class ExpenseRequest(BaseModel):
    expense_id: Optional[int] = None  # Auto-generated in DB
    employee_id: int
    expense_date: str
    vendor_name: str
    total_amount: float
    payment_method: str
    payment_status: str
    due_date: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_file_url: Optional[str] = None
    notes: Optional[str] = None
    amount_paid: float
    employee_name: str
    created_by_user_id: int
    user_id: int
    amount_balance: float
