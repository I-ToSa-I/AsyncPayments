from pydantic import BaseModel
from typing import Optional, List, Union


class User(BaseModel):
    user_id: int
    username: str
    balance: float
    hold: float

class Payments(BaseModel):
    payments: dict
    page: int
    hasNextPage: bool


class Invoice(BaseModel):
    amount: Union[float, int]
    currency: str
    payment_id: str
    merchant_id: int
    comment: str
    additional_data: str
    url_success: str
    url_callback: str
    expires_at: int
    user_id: int
    invoice_date: int
    status: str
    paid_date: int
    invoice_id: int
    url: str
    
    
class Invoices(BaseModel):
    invoices: Optional[List[Invoice]] = []
    count: int
    page: int
    perPage: int