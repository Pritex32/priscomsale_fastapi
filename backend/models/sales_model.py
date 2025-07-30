from pydantic import BaseModel
from typing import Optional, List

# ✅ Request model for creating a sale
class SaleRequest(BaseModel):
    user_id: int
    employee_id: int
    customer_name: str
    customer_phone: str
    item_id: int
    item_name: str
    quantity: int
    unit_price: float
    total_amount: float
    amount_paid: float
    amount_balance: float
    payment_method: str
    payment_status: str
    sale_date: str  # YYYY-MM-DD
    due_date: Optional[str] = None
    notes: Optional[str] = None

# ✅ Request model for fetching sales (optional, for filters)
class FetchSalesRequest(BaseModel):
    user_id: int
    limit: Optional[int] = 10  # Default limit

# ✅ Response model for a single sale (optional, improves Swagger docs)
class SaleResponse(BaseModel):
    id: int
    user_id: int
    employee_id: int
    customer_name: str
    customer_phone: str
    item_id: int
    item_name: str
    quantity: int
    unit_price: float
    total_amount: float
    amount_paid: float
    amount_balance: float
    payment_method: str
    payment_status: str
    sale_date: str
    due_date: Optional[str]
    notes: Optional[str]

# ✅ Response model for multiple sales
class SalesListResponse(BaseModel):
    status: str
    data: List[SaleResponse]

