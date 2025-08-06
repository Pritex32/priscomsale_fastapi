from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class SheetDataRequest(BaseModel):
    user_id: int
    sheet_name: str
    data: Dict  # Store dynamic rows or any structured data

class SheetDataResponse(SheetDataRequest):
    id: int
    created_at: datetime
