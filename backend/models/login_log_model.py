from pydantic import BaseModel
from typing import Optional

class LoginLogRequest(BaseModel):
    user_id: int
    login_time: str  # ISO format: "YYYY-MM-DDTHH:MM:SS"
    ip_address: str
    device: str
    role: str
    username: str
    user_agent: str

class LoginLogResponse(LoginLogRequest):
    log_id: int
