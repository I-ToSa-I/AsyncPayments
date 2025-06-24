from pydantic import BaseModel
from typing import Union, Optional


class Balance(BaseModel):
    balance: Optional[float] = None
    referral: Optional[float] = None
    hold: Optional[float] = None

class Order(BaseModel):
    id: Optional[str] = None
    order_id: Optional[Union[int, str]] = None
    desc: Optional[str] = None
    merchant_id: Optional[str] = None
    merchant_domain: Optional[str] = None
    method: Optional[str] = None
    amount: Optional[Union[int, float]] = None
    currency: Optional[str] = None
    profit: Optional[float] = None
    commission: Optional[float] = None
    commission_client: Optional[float] = None
    commission_type: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None
    date: Optional[str] = None
    expired_date: Optional[str] = None
    complete_date: Optional[str] = None
    us_vars: Optional[Union[dict, str, list]] = None

class OrderMethodCurrencies(BaseModel):
    RUB: Optional[float] = None
    UAH: Optional[float] = None
    USD: Optional[float] = None
    EUR: Optional[float] = None

class OrderMethod(BaseModel):
    name: Optional[str] = None
    min: Optional[OrderMethodCurrencies] = None
    max: Optional[OrderMethodCurrencies] = None
    commission_percent: Optional[float] = None

class Withdrawal(BaseModel):
    id: Optional[str] = None
    my_id: Optional[Union[int, str]] = None
    method: Optional[str] = None
    wallet: Optional[str] = None
    amount: Optional[float] = None
    amount_down: Optional[float] = None
    commission: Optional[float] = None
    commission_type: Optional[int] = None
    status: Optional[str] = None
    cancel_message: Optional[str] = None
    date: Optional[str] = None
    complete_date: Optional[str] = None

class WithdrawalMethod(BaseModel):
    name: Optional[str] = None
    min: Optional[float] = None
    max: Optional[float] = None
    commission_percent:Optional[float] = None
    commission_sum: Optional[float] = None

class CreateWithdrawalInfo(BaseModel):
    id: Optional[str] = None
    my_id: Optional[Union[str, int]] = None
    method: Optional[str] = None
    wallet: Optional[str] = None
    amount: Optional[float] = None
    amount_in_currency: Optional[float] = None
    amount_currency: Optional[str] = None
    amount_rate: Optional[float] = None
    amount_down: Optional[float] = None
    commission: Optional[float] = None
    commission_type: Optional[int] = None
    status: Optional[str] = None