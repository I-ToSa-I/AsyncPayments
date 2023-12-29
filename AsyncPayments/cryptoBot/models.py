from pydantic import BaseModel
from typing import Union, List


# Balance
class MeInfo(BaseModel):
    app_id: int
    name: str
    payment_processing_bot_username: str

class Invoice(BaseModel):
    invoice_id: int
    hash: str
    currency_type: str
    asset: str = None
    fiat: str = None
    amount: str
    paid_asset: str = None
    paid_amount: str = None
    paid_fiat_rate: str = None
    accepted_assets: List[str] = None
    fee_asset: str = None
    fee_amount: float = None
    fee: str = None
    bot_invoice_url: str
    pay_url: str
    description: str = None
    status: str
    created_at: str
    paid_usd_rate: str = None
    usd_rate: str = None
    allow_comments: bool
    allow_anonymous: bool
    expiration_date: str = None
    paid_at: str = None
    paid_anonymously: bool = None
    comment: str = None
    hidden_message: str = None
    payload: str = None
    paid_btn_name: str = None
    paid_btn_url: str = None

class Check(BaseModel):
    check_id: int
    hash: str
    asset: str
    amount: float
    bot_check_url: str
    status: str
    created_at: str
    activated_at: str

class Transfer(BaseModel):
    transfer_id: int
    user_id: int
    asset: str
    amount: float
    status: str
    completed_at: str
    comment: str = None

class Balance(BaseModel):
    currency_code: str
    available: float
    onhold: float

class ExchangeRate(BaseModel):
    is_valid: bool
    is_crypto: bool
    is_fiat: bool
    source: str
    target: str
    rate: float

class Currency(BaseModel):
    is_blockchain: bool
    is_stablecoin: bool
    is_fiat: bool
    name: str
    code: str
    url: str = None
    decimals: int


