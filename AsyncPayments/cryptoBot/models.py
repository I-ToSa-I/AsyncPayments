from pydantic import BaseModel
from typing import List, Optional


class MeInfo(BaseModel):
    app_id: Optional[int] = None
    name: Optional[str] = None
    payment_processing_bot_username: Optional[str] = None

class Invoice(BaseModel):
    invoice_id: Optional[int] = None
    hash: Optional[str] = None
    currency_type: Optional[str] = None
    asset: Optional[str] = None
    fiat: Optional[str] = None
    amount: Optional[str] = None
    paid_asset: Optional[str] = None
    paid_amount: Optional[str] = None
    paid_fiat_rate: Optional[str] = None
    accepted_assets: Optional[List[str]] = None
    fee_asset: Optional[str] = None
    fee_amount: Optional[float] = None
    fee: Optional[str] = None
    bot_invoice_url: Optional[str] = None
    pay_url: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    paid_usd_rate: Optional[str] = None
    usd_rate: Optional[str] = None
    allow_comments: Optional[bool] = None
    allow_anonymous: Optional[bool] = None
    expiration_date: Optional[str] = None
    paid_at: Optional[str] = None
    paid_anonymously: Optional[bool] = None
    comment: Optional[str] = None
    hidden_message: Optional[str] = None
    payload: Optional[str] = None
    paid_btn_name: Optional[str] = None
    paid_btn_url: Optional[str] = None

class Check(BaseModel):
    check_id: Optional[int] = None
    hash: Optional[str] = None
    asset: Optional[str] = None
    amount: Optional[float] = None
    bot_check_url: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    activated_at: Optional[str] = None

class Transfer(BaseModel):
    transfer_id: Optional[int] = None
    user_id: Optional[int] = None
    asset: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    completed_at: Optional[str] = None
    comment: Optional[str] = None

class Balance(BaseModel):
    currency_code: Optional[str] = None
    available: Optional[float] = None
    onhold: Optional[float] = None

class ExchangeRate(BaseModel):
    is_valid: Optional[bool] = None
    is_crypto: Optional[bool] = None
    is_fiat: Optional[bool] = None
    source: Optional[str] = None
    target: Optional[str] = None
    rate: Optional[float] = None

class Currency(BaseModel):
    is_blockchain: Optional[bool] = None
    is_stablecoin: Optional[bool] = None
    is_fiat: Optional[bool] = None
    name: Optional[str] = None
    code: Optional[str] = None
    url: Optional[str] = None
    decimals: Optional[int] = None
