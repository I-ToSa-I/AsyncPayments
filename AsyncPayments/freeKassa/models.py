from pydantic import BaseModel
from typing import Optional, List, Union


class Balance(BaseModel):
    currency: str
    value: Union[int, str, float]
    

class Order(BaseModel):
    merchant_order_id: str
    fk_order_id: int
    amount: Union[int, float]
    currency: str
    email: str
    account: Optional[str] = None
    date: str
    status: int
    payer_account: Optional[str] = None
    
    
class Orders(BaseModel):
    pages: int
    orders: List[Order]
    
    
class CreateOrder(BaseModel):
    orderId: int
    orderHash: str
    location: str
    
    
class Currency(BaseModel):
    id: int
    name: str
    currency: str
    is_enabled: int
    is_favorite: int
    
    
class WithdrawalCurrency(BaseModel):
    id: int
    name: str
    min: int
    max: int
    currency: str
    can_exchange: int
    
    
class Store(BaseModel):
    id: int
    name: str
    url: Optional[str] = None
    activated: Optional[int] = None
    
    
class Withdrawal(BaseModel):
    id: int
    amount: Union[int, float]
    currency: str
    ext_currency_id: int
    account: str
    date: str
    status: int
    
    
class Withdrawals(BaseModel):
    pages: int
    withdrawals: List[Withdrawal]
    
    
class CreateWithdrawal(BaseModel):
    id: int
    