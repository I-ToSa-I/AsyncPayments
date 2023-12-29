from pydantic import BaseModel
from typing import Union


# Balance
class Balance(BaseModel):
    balance: float
    referral: float
    hold: float


# Orders
class Order(BaseModel):
    id: str
    order_id: Union[int, str]
    desc: str
    merchant_id: str
    merchant_domain: str
    method: str = None
    amount: float
    currency: str
    profit: float = None
    commission: float = None
    commission_client: float = None
    commission_type: str = None
    email: str = None
    status: str
    date: str
    expired_date: str
    complete_date: str = None
    us_vars: dict

class OrderMethodCurrencies(BaseModel):
    RUB: float
    UAH: float
    USD: float
    EUR: float

class OrderMethod(BaseModel):
    min: OrderMethodCurrencies
    max: OrderMethodCurrencies
    commission_percent: float


# Withdrawals
class Withdrawal(BaseModel):
    id: str
    my_id: Union[int, str]
    method: str
    wallet: str
    amount: float
    amount_down: float
    commission: float
    commission_type: int
    status: str
    cancel_message: str = None
    date: str
    complete_date: str = None


class WithdrawalMethod(BaseModel):
    min: float
    max: float
    commission_percent: float
    commission_sum: float

class CreateWithdrawalInfo(BaseModel):
    id: str
    my_id: Union[str, int]
    method: str
    wallet: str
    amount: float
    amount_in_currency: float
    amount_currency: str
    amount_rate: float
    amount_down: float
    commission: float
    commission_type: int
    status: str