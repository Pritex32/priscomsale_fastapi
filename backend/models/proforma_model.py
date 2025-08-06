from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date, datetime

class ProformaInvoiceRequest(BaseModel):
    user_id: int
    tenant_name: str
    items: List[Dict]  # Each item: {"name": "Item 1", "qty": 2, "price": 500}
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    date: date
    expiry_date: date
    payment_status: str
    payment_method: str
    customer_name: str
    customer_phone: str
    grand_total: float
    status: str
    invoice_url: Optional[str] = None
    notes: Optional[str] = None

class ProformaInvoiceResponse(ProformaInvoiceRequest):
    proforma_id: int
    created_at: datetime
