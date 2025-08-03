from pydantic import BaseModel
from typing import Optional

class RestockRequest(BaseModel):
    purchase_id: Optional[int] = None  # Auto-generated in DB
    purchase_date: str
    supplier_name: str
    supplier_phone: str
    item_name: str
    item_id: int
    supplied_quantity: int
    unit_price: float
    total_price: float
    total_price_paid: float
    amount_paid: float
    amount_balance: float
    total_cost: float
    payment_status: str
    payment_method: str
    due_date: Optional[str] = None
    notes: Optional[str] = None
    invoice_file_url: Optional[str] = None
    employee_id: int
    employee_name: str
    created_by_user_id: int
    user_id: int

