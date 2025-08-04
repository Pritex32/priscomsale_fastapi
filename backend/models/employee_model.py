from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EmployeeRequest(BaseModel):
    employee_id: Optional[int] = None  # Auto-increment in DB
    name: str
    email: EmailStr
    password: str
    role: str
    job_title: Optional[str] = None
    created_by_user_id: int
    created_at: Optional[str] = None  # Will be set automatically
    user_id: int
