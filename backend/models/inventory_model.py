from pydantic import BaseModel
from typing import Optional

class InventoryRequest(BaseModel):
    item_id: int
    item_name: str
    open_balance: Optional[int] = 0
    supplied_quantity: Optional[int] = 0
    return_quantity: Optional[int] = 0
    stock_out: Optional[int] = 0
    closing_balance: Optional[int] = 0
    log_date: str  # Expecting YYYY-MM-DD format
    last_updated: Optional[str] = None  # Auto-update in backend
    user_id: int
    reorder_level: Optional[int] = 0
    sale_id: Optional[int] = None
    purchase_id: Optional[int] = None
