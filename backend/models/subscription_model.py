from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubscriptionRequest(BaseModel):
    id: Optional[int] = None  # Auto-increment in DB
    user_id: int
    plan: str
    price_ngn: float
    features: Optional[str] = None
    plan_id: Optional[str] = None
    is_active: bool = False
    started_at: Optional[str] = None  # Will be set in API
    expires_at: Optional[str] = None
    paid_at: Optional[str] = None
    status: Optional[str] = "pending"  # e.g., pending, paid, expired
    amount: Optional[float] = None
    reference: Optional[str] = None
