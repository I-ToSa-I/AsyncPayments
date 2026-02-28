from pydantic import BaseModel, Field
from typing import Optional, Union


class OrderStatuses:
    PENDING: str = "PENDING"
    CANCELED: str = "CANCELED"
    CONFIRMED: str = "CONFIRMED"
    CHARGEBACKED: str = "CHARGEBACKED"


class Order(BaseModel):
    paymentMethod: Optional[str] = None
    transactionId: Optional[str] = None
    redirect: Optional[str] = None
    return_: Optional[str] = Field(alias="return", default=None)
    paymentDetails: Optional[Union[str, dict]] = None
    status: Optional[str] = None
    expiresIn: Optional[str] = None
    merchantId: Optional[str] = None
    usdtRate: Optional[Union[int, float,]] = None
    
    
class OrderInfo(BaseModel):
    id: Optional[str] = None
    status: Optional[str] = None
    paymentDetails: Optional[dict] = None
    merchantName: Optional[str] = None
    merchantId: Optional[str] = None
    comission: Optional[Union[int, float]] = None
    paymentMethod: Optional[str] = None
    expiresIn: Optional[str] = None
    return_: Optional[str] = Field(alias="return", default=None)
    comissionUsdt: Optional[Union[int, float]] = None
    amountUsdt: Optional[Union[int, float]] = None
    qr: Optional[str] = None
    payformSuccessUrl: Optional[str] = None
    payload: Optional[str] = None
    comissionType: Optional[int] = None
    externalId: Optional[str] = None
    description: Optional[str] = None
    
    
class ExchangeRate(BaseModel):
    paymentMethod: Optional[int] = None
    currencyFrom: Optional[str] = None
    currencyTo: Optional[str] = None
    rate: Optional[float] = None
    updatedAt: Optional[str] = None