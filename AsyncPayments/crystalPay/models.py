from pydantic import BaseModel
from typing import Optional


class CassaInfo(BaseModel):
    id: int
    name: str
    status_level: int
    created_at: str

class CreatePayment(BaseModel):
    id: str
    url: str
    amount: float
    type: str

class Balance(BaseModel):
    amount: float
    currency: str

class Balances(BaseModel):
    BITCOIN: Balance
    BITCOINCASH: Balance
    BNBCRYPTOBOT: Balance
    BNBSMARTCHAIN: Balance
    BTCBANKER: Balance
    BTCCHATEX: Balance
    BTCCRYPTOBOT: Balance
    CARDRUBP2P: Balance
    CARDTRYP2P: Balance
    DASH: Balance
    DOGECOIN: Balance
    ETHBANKER: Balance
    ETHCRYPTOBOT: Balance
    ETHEREUM: Balance
    LITECOIN: Balance
    LTCBANKER: Balance
    LZTMARKET: Balance
    POLYGON: Balance
    TONCRYPTOBOT: Balance
    TRON: Balance
    USDCTRC: Balance
    USDTBANKER: Balance
    USDTCHATEX: Balance
    USDTCRYPTOBOT: Balance
    USDTTRC: Balance

class PaymentMethod(BaseModel):
    name: str
    enabled: bool
    extra_commission_percent: float
    minimal_status_level: int
    currency: str
    commission_percent: float
    commission: float

class PaymentsMethods(BaseModel):
    CRYSTALPAY: PaymentMethod
    TEST: PaymentMethod
    CARDRUBP2P: PaymentMethod
    CARDTRYP2P: PaymentMethod
    LZTMARKET: PaymentMethod
    BITCOIN: PaymentMethod
    BITCOINCASH: PaymentMethod
    DASH: PaymentMethod
    DOGECOIN: PaymentMethod
    ETHEREUM: PaymentMethod
    LITECOIN: PaymentMethod
    BNBSMARTCHAIN: PaymentMethod
    POLYGON: PaymentMethod
    TRON: PaymentMethod
    USDCTRC: PaymentMethod
    USDTTRC: PaymentMethod
    BNBCRYPTOBOT: PaymentMethod
    BTCCRYPTOBOT: PaymentMethod
    ETHCRYPTOBOT: PaymentMethod
    TONCRYPTOBOT: PaymentMethod
    USDTCRYPTOBOT: PaymentMethod

class PaymentInfo(BaseModel):
    id: str
    url: str
    state: str
    type: str
    method: Optional[str] = None
    required_method: str
    currency: str
    service_commission: float
    extra_commission: float
    amount: float
    pay_amount: float
    remaining_amount: float
    balance_amount: float
    description: str
    redirect_url: str
    callback_url: str
    extra: str
    created_at: str
    expired_at: str

class PayoffCreate(BaseModel):
    id: str
    method: str
    commission: float
    amount: float
    rub_amount: float
    receive_amount: float
    deduction_amount: float
    subtract_from: str
    currency: str

class PayoffRequest(BaseModel):
    id: str
    state: str
    method: str
    currency: str
    commission: float
    amount: float
    rub_amount: float
    receive_amount: float
    deduction_amount: float
    subtract_from: str
    wallet: str
    message: str
    callback_url: str
    extra: str
    created_at: str

class TickersRate(BaseModel):
    base_currency: str
    currencies: dict

class Stats(BaseModel):
    payed_amount: float
    total_count: int
    payed_count: int

class GeneralStats(BaseModel):
    incoming: Stats
    outgoing: Stats
