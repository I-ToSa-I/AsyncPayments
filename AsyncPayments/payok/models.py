from pydantic import BaseModel
from typing import Optional, Union


class Balance(BaseModel):
    balance: Optional[int] = None
    ref_balance: Optional[Union[str, float, int]] = None
    
    
class Transaction(BaseModel):
    transaction: Optional[Union[str, int]] = None
    email: Optional[str] = None
    amount: Optional[Union[str, int]] = None
    currency: Optional[str] = None
    currency_amount: Optional[Union[str, int]] = None
    comission_percent: Optional[Union[str, int]] = None
    comission_fixed: Optional[str] = None
    amount_profit: Optional[Union[str, int]] = None
    method: Optional[str] = None
    payment_id: Optional[Union[int, str]] = None
    description: Optional[str] = None
    date: Optional[str] = None
    pay_date: Optional[str] = None
    transaction_status: Optional[Union[str, int]] = None
    custom_fields: Optional[Union[str, int, dict]] = None
    webhook_status: Optional[Union[str, int]] = None
    webhook_amount: Optional[Union[str, int]] = None
    
    
class Payout(BaseModel):
    payout: Optional[int] = None
    method: Optional[str] = None
    reciever: Optional[str] = None
    type: Optional[str] = None
    amount: Optional[int] = None
    comission_percent: Optional[int] = None
    comission_fixed: Optional[str] = None
    amount_profit: Optional[int] = None
    date_create: Optional[str] = None
    date_pay: Optional[str] = None
    status: Optional[int] = None
    

class PayoutOnCreate(BaseModel):
    payout_id: Optional[int] = None
    method: Optional[str] = None
    reciever: Optional[str] = None
    amount: Optional[int] = None
    comission_percent: Optional[int] = None
    comission_fixed: Optional[str] = None
    amount_profit: Optional[int] = None
    date: Optional[str] = None
    payout_status_code: Optional[int] = None
    payout_status_text: Optional[str] = None
    
    
class CreatePayout(BaseModel):
    remain_balance: Optional[Union[str, int, float]] = None
    payout: Optional[PayoutOnCreate] = None
    