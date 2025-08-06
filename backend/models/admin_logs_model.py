from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AdminLogRequest(BaseModel):
    action: str
    vendor_id: Optional[int] = None
    vendor_name: Optional[str] = None
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    user_id: int  # Who performed the action

class AdminLogResponse(AdminLogRequest):
    id: int
    timestamp: datetime
