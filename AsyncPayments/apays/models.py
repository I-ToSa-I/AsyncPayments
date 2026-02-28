from pydantic import BaseModel
from typing import Optional


class OrderStatuses:
    PENDING: str = "pending"
    APPROVE: str = "approve"
    DECLINE: str = "decline"
    EXPIRED: str = "expired"


class Order(BaseModel):
    status: Optional[bool] = None
    url: Optional[str] = None
    
    
class OrderInfo(BaseModel):
    status: Optional[bool] = None
    order_status: Optional[str] = None