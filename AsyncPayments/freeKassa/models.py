from pydantic import BaseModel
from typing import Optional, List, Union


class Balance(BaseModel):
    currency: Optional[str] = None
    value: Optional[Union[int, str, float]] = None
    

class Order(BaseModel):
    merchant_order_id: Optional[str] = None
    fk_order_id: Optional[int] = None
    amount: Optional[Union[int, float]] = None
    currency: Optional[str] = None
    email: Optional[str] = None
    account: Optional[str] = None
    date: Optional[str] = None
    status: Optional[int] = None
    payer_account: Optional[str] = None
    
    
class Orders(BaseModel):
    pages: Optional[int] = None
    orders: Optional[List[Order]] = None
    
    
class CreateOrder(BaseModel):
    orderId: Optional[int] = None
    orderHash: Optional[str] = None
    location: Optional[str] = None
    
    
class Currency(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    currency: Optional[str] = None
    is_enabled: Optional[int] = None
    is_favorite: Optional[int] = None
    
    
class WithdrawalCurrency(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    min: Optional[int] = None
    max: Optional[int] = None
    currency: Optional[str] = None
    can_exchange: Optional[int] = None
    
    
class Store(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None
    activated: Optional[int] = None
    
    
class Withdrawal(BaseModel):
    id: Optional[int] = None
    amount: Optional[Union[int, float]] = None
    currency: Optional[str] = None
    ext_currency_id: Optional[int] = None
    account: Optional[str] = None
    date: Optional[str] = None
    status: Optional[int] = None
    
    
class Withdrawals(BaseModel):
    pages: Optional[int] = None
    withdrawals: Optional[List[Withdrawal]] = None
    
    
class CreateWithdrawal(BaseModel):
    id: Optional[int] = None
    