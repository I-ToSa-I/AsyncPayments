from pydantic import BaseModel
from typing import Optional, List, Union


class User(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    balance: Optional[float] = None
    hold: Optional[float] = None

class Payments(BaseModel):
    payments: Optional[dict] = None
    page: Optional[int] = None
    hasNextPage: Optional[bool] = None


class Invoice(BaseModel):
    amount: Optional[Union[float, int]] = None
    payment_id: Optional[str] = None
    merchant_id: Optional[int] = None
    comment: Optional[str] = None
    additional_data: Optional[str] = None
    url_success: Optional[str] = None
    url_callback: Optional[str] = None
    is_test: Optional[bool] = None
    expires_at: Optional[int] = None
    user_id: Optional[int] = None
    invoice_date: Optional[int] = None
    status: Optional[str] = None
    paid_date: Optional[int] = None
    payer_user_id: Optional[int] = None
    resend_attempts: Optional[int] = None
    invoice_id: Optional[int] = None
    url: Optional[str] = None
    
    
class Invoices(BaseModel):
    invoices: Optional[List[Invoice]] = []
    count: Optional[int] = None
    page: Optional[int] = None
    perPage: Optional[int] = None