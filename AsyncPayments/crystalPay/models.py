from pydantic import BaseModel, Field
from typing import Optional


class CassaInfo(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    status_level: Optional[int] = None
    created_at: Optional[str] = None


class BalanceListField(BaseModel):
    name: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    amount_accuracy: Optional[int] = None


class CreatePayment(BaseModel):
    id: Optional[str] = None
    url: Optional[str] = None
    type_: Optional[str] = Field(alias="type", default=None)
    rub_amount: Optional[str] = None


class Balance(BaseModel):
    method: Optional[str] = None
    name: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    amount_accuracy: Optional[int] = None


class PaymentInfo(BaseModel):
    id: Optional[str] = None
    url: Optional[str] = None
    state: Optional[str] = None
    type_: Optional[str] = Field(alias="type", default=None)
    method: Optional[str] = None
    required_method: Optional[str] = None
    amount_currency: Optional[str] = None
    rub_amount: Optional[str] = None
    initial_amount: Optional[str] = None
    remaining_amount: Optional[str] = None
    balance_amount: Optional[str] = None
    commission_amount: Optional[str] = None
    description: Optional[str] = None
    redirect_url: Optional[str] = None
    callback_url: Optional[str] = None
    extra: Optional[str] = None
    created_at: Optional[str] = None
    expired_at: Optional[str] = None
    final_at: Optional[str] = None


class PayoffCreate(BaseModel):
    id: Optional[str] = None
    method: Optional[str] = None
    commission_amount: Optional[str] = None
    amount: Optional[str] = None
    rub_amount: Optional[str] = None
    receive_amount: Optional[str] = None
    deduction_amount: Optional[str] = None
    subtract_from: Optional[str] = None
    amount_currency: Optional[str] = None
    wallet: Optional[str] = None


class PayoffRequest(BaseModel):
    id: Optional[str] = None
    state: Optional[str] = None
    method: Optional[str] = None
    amount: Optional[str] = None
    amount_currency: Optional[str] = None
    commission_amount: Optional[str] = None
    rub_amount: Optional[str] = None
    receive_amount: Optional[str] = None
    deduction_amount: Optional[str] = None
    subtract_from: Optional[str] = None
    wallet: Optional[str] = None
    message: Optional[str] = None
    callback_url: Optional[str] = None
    extra: Optional[str] = None
    created_at: Optional[str] = None
    final_at: Optional[str] = None
    

class SwapPair(BaseModel):
    pair_id: Optional[int] = None
    source: Optional[dict] = None
    target: Optional[dict] = None
    price: Optional[str] = None


class CreateSwap(BaseModel):
    id: Optional[str] = None
    pair_id: Optional[int] = None
    amount_type: Optional[str] = None
    amount: Optional[str] = None
    source: Optional[dict] = None
    target: Optional[dict] = None
    price: Optional[str] = None
    

class SwapInfo(BaseModel):
    id: Optional[str] = None
    state: Optional[str] = None
    pair_id: Optional[int] = None
    amount_type: Optional[str] = None
    amount: Optional[str] = None
    source: Optional[dict] = None
    target: Optional[dict] = None
    price: Optional[str] = None
    created_at: Optional[str] = None
    expired_at: Optional[str] = None
    final_at: Optional[str] = None


class TickersRate(BaseModel):
    base_currency: Optional[str] = None
    currencies: Optional[dict] = None
    
    
class CreateTransfer(BaseModel):
    id: Optional[int] = None
    method: Optional[str] = None
    amount_currency: Optional[str] = None
    amount: Optional[str] = None
    sender: Optional[str] = None
    receiver: Optional[str] = None
    
    
class TransferInfo(BaseModel):
    id: Optional[int] = None
    state: Optional[str] = None
    type_: Optional[str] = Field(alias="type", default=None)
    method: Optional[str] = None
    amount_currency: Optional[str] = None
    amount: Optional[str] = None
    sender: Optional[str] = None
    receiver: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    final_at: Optional[str] = None
    
    
class Stats(BaseModel):
    payed_rub_amount: Optional[str] = None
    payed_count: Optional[int] = None
    total_count: Optional[int] = None
    conversion_percent: Optional[int] = None
    