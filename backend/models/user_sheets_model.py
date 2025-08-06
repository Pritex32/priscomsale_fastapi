from pydantic import BaseModel
from typing import Dict, List, Optional

class UserSheetRequest(BaseModel):
    user_id: int
    sheet_name: str
    columns: Dict[str, str]  # Example: {"name": "string", "price": "float"}
    employee_access: Optional[List[int]] = []
