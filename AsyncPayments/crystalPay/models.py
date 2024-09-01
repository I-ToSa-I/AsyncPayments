from pydantic import BaseModel, Field
from typing import Optional


class CassaInfo(BaseModel):
    id: int
    name: str
    status_level: int
    created_at: str


class BalanceListField(BaseModel):
    name: str
    amount: str
    currency: str
    amount_accuracy: int
    
    
class Method(BaseModel):
    name: str
    currency: str
    amount_accuracy: int
    minimal_status_level: int
    settings: dict
    in_: Optional[dict] = Field(alias="in", default=None)
    out: Optional[dict] = None
    

class Methods(BaseModel):
    BITCOIN: Method
    BITCOINCASH: Method
    BNBCRYPTOBOT: Method
    BNBSMARTCHAIN: Method
    BTCCRYPTOBOT: Method
    CARDRUBP2P: Method
    DASH: Method
    DOGECOIN: Method
    ETHCRYPTOBOT: Method
    ETHEREUM: Method
    LITECOIN: Method
    LTCCRYPTOBOT: Method
    LZTMARKET: Method
    POLYGON: Method
    SBERPAYP2P: Method
    SBPP2P: Method
    TONCOIN: Method
    TONCRYPTOBOT: Method
    TRON: Method
    USDCTRC: Method
    USDTCRYPTOBOT: Method
    USDTTRC: Method


class BalancesList(BaseModel):
    BITCOIN: BalanceListField
    BITCOINCASH: BalanceListField
    BNBCRYPTOBOT: BalanceListField
    BNBSMARTCHAIN: BalanceListField
    BTCCRYPTOBOT: BalanceListField
    CARDRUBP2P: BalanceListField
    DASH: BalanceListField
    DOGECOIN: BalanceListField
    ETHCRYPTOBOT: BalanceListField
    ETHEREUM: BalanceListField
    LITECOIN: BalanceListField
    LTCCRYPTOBOT: BalanceListField
    LZTMARKET: BalanceListField
    POLYGON: BalanceListField
    SBERPAYP2P: BalanceListField
    SBPP2P: BalanceListField
    TONCOIN: BalanceListField
    TONCRYPTOBOT: BalanceListField
    TRON: BalanceListField
    USDCTRC: BalanceListField
    USDTCRYPTOBOT: BalanceListField
    USDTTRC: BalanceListField


class CreatePayment(BaseModel):
    id: str
    url: str
    type_: str = Field(alias="type")
    rub_amount: str


class Balance(BaseModel):
    method: str
    name: str
    amount: str
    currency: str
    amount_accuracy: int


class PaymentInfo(BaseModel):
    id: str
    url: str
    state: str
    type_: str = Field(alias="type")
    method: Optional[str] = None
    required_method: Optional[str] = None
    amount_currency: str
    rub_amount: str
    initial_amount: str
    remaining_amount: str
    balance_amount: str
    commission_amount: str
    description: Optional[str] = None
    redirect_url: Optional[str] = None
    callback_url: Optional[str] = None
    extra: Optional[str] = None
    created_at: str
    expired_at: str
    final_at: Optional[str] = None


class PayoffCreate(BaseModel):
    id: str
    method: str
    commission_amount: str
    amount: str
    rub_amount: str
    receive_amount: str
    deduction_amount: str
    subtract_from: str
    amount_currency: str
    wallet: str


class PayoffRequest(BaseModel):
    id: str
    state: str
    method: str
    amount: str
    amount_currency: str
    commission_amount: str
    rub_amount: str
    receive_amount: str
    deduction_amount: str
    subtract_from: str
    wallet: str
    message: Optional[str] = None
    callback_url: Optional[str] = None
    extra: Optional[str] = None
    created_at: str
    final_at: Optional[str] = None
    

class SwapPair(BaseModel):
    pair_id: Optional[int] = None
    source: dict
    target: dict
    price: str


class CreateSwap(BaseModel):
    id: str
    pair_id: int
    amount_type: str
    amount: str
    source: dict
    target: dict
    price: str
    

class SwapInfo(BaseModel):
    id: str
    state: str
    pair_id: int
    amount_type: str
    amount: str
    source: dict
    target: dict
    price: str
    created_at: str
    expired_at: str
    final_at: Optional[str] = None


class TickersRate(BaseModel):
    base_currency: str
    currencies: dict
    
    
class CreateTransfer(BaseModel):
    id: int
    method: str
    amount_currency: str
    amount: str
    sender: str
    receiver: str
    
    
class TransferInfo(BaseModel):
    id: int
    state: str
    type_: str = Field(alias="type")
    method: str
    amount_currency: str
    amount: str
    sender: str
    receiver: str
    description: Optional[str] = None
    created_at: str
    final_at: str
    
    
class Stats(BaseModel):
    payed_rub_amount: str
    payed_count: int
    total_count: int
    conversion_percent: int
    