from pydantic import BaseModel
from typing import Optional, Union


class Balance(BaseModel):
    balance: int
    ref_balance: Union[str, float, int]
    
    
class Transaction(BaseModel):
    transaction: Union[str, int]
    email: str
    amount: Union[str, int]
    currency: str
    currency_amount: Union[str, int]
    comission_percent: Union[str, int]
    comission_fixed: str
    amount_profit: Union[str, int]
    method: Optional[str] = None
    payment_id: Union[int, str]
    description: str
    date: str
    pay_date: str
    transaction_status: Union[str, int]
    custom_fields: Optional[Union[str, int, dict]] = None
    webhook_status: Union[str, int]
    webhook_amount: Union[str, int]
    
    
class Payout(BaseModel):
    payout: int
    method: str
    reciever: str
    type: str
    amount: int
    comission_percent: int
    comission_fixed: str
    amount_profit: int
    date_create: str
    date_pay: str
    status: int
    

class PayoutOnCreate(BaseModel):
    payout_id: int
    method: str
    reciever: str
    amount: int
    comission_percent: int
    comission_fixed: str
    amount_profit: int
    date: str
    payout_status_code: int
    payout_status_text: str
    
    
class CreatePayout(BaseModel):
    remain_balance: Union[str, int, float]
    payout: PayoutOnCreate
    