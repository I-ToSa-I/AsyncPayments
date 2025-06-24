from pydantic import BaseModel
from typing import Union, Optional


class Balance(BaseModel):
    balance_rub: Optional[float] = None
    balance_usd: Optional[float] = None


class CreatePayment(BaseModel):
    id: Optional[int] = None
    hash: Optional[str] = None
    url: Optional[str] = None


class Payment(BaseModel):
    id: Optional[int] = None
    order_id: Optional[Union[int, str]] = None
    in_amount: Optional[float] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    data: Optional[str] = None


class RevokePayment(BaseModel):
    id: Optional[int] = None


class CreateWithdrawRequest(BaseModel):
    id: Optional[int] = None
    status: Optional[str] = None


class CancelWithdrawRequest(BaseModel):
    id: Optional[int] = None
    status: Optional[str] = None


class WithdrawRequest(BaseModel):
    id: Optional[int] = None
    order_id: Optional[Union[int, str]] = None
    amount: Optional[float] = None
    fee: Optional[float] = None
    way: Optional[str] = None
    who_fee: Optional[str] = None
    status: Optional[str] = None
