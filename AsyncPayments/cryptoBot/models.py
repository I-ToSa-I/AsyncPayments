from pydantic import BaseModel
from typing import List, Optional


class MeInfo(BaseModel):
    app_id: int
    name: str
    payment_processing_bot_username: str

class Invoice(BaseModel):
    invoice_id: int
    hash: str
    currency_type: str
    asset: Optional[str] = None
    fiat: Optional[str] = None
    amount: str
    paid_asset: Optional[str] = None
    paid_amount: Optional[str] = None
    paid_fiat_rate: Optional[str] = None
    accepted_assets: Optional[List[str]] = None
    fee_asset: Optional[str] = None
    fee_amount: Optional[float] = None
    fee: Optional[str] = None
    bot_invoice_url: str
    pay_url: str
    description: Optional[str] = None
    status: str
    created_at: str
    paid_usd_rate: Optional[str] = None
    usd_rate: Optional[str] = None
    allow_comments: bool
    allow_anonymous: bool
    expiration_date: Optional[str] = None
    paid_at: Optional[str] = None
    paid_anonymously: Optional[bool] = None
    comment: Optional[str] = None
    hidden_message: Optional[str] = None
    payload: Optional[str] = None
    paid_btn_name: Optional[str] = None
    paid_btn_url: Optional[str] = None

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
    comment: Optional[str] = None

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
    url: Optional[str] = None
    decimals: int
