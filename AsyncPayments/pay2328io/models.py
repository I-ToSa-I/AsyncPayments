from pydantic import BaseModel, Field
from typing import Optional, List, Union


class Balance(BaseModel):
    uuid: Optional[str] = None
    status: Optional[str] = None
    currency_code: Optional[str] = None
    balance: Optional[str] = None
    balance_usd: Optional[str] = None
    locked_balance: Optional[str] = None


class CryptoPairPrice(BaseModel):
    from_: Optional[str] = Field(alias="from", default=None)
    to: Optional[str] = None
    price: Optional[str] = None
    

class Direction(BaseModel):
    network: Optional[str] = None
    network_code: Optional[str] = None
    currency: Optional[str] = None
    deposit_status: Optional[str] = None
    withdrawal_status: Optional[str] = None
    min_deposit: Optional[str] = None
    max_deposit: Optional[str] = None
    min_withdrawal: Optional[str] = None
    max_withdrawal: Optional[str] = None
    deposit_fee_percent: Optional[str] = None
    withdrawal_fee: Optional[str] = None
    withdrawal_fee_type: Optional[str] = None
    

class ConversionPrice(BaseModel):
    success: Optional[bool] = None
    from_currency: Optional[str] = None
    to_currency: Optional[str] = None
    amount_type: Optional[str] = None
    from_amount: Optional[str] = None
    to_amount: Optional[str] = None
    effective_rate: Optional[str] = None
    from_amount_usd: Optional[str] = None
    to_amount_usd: Optional[str] = None
    

class ConvertInfo(BaseModel):
    id: Optional[int] = None
    type_: Optional[str] = Field(alias="type", default=None)
    status: Optional[str] = None
    from_currency: Optional[str] = None
    to_currency: Optional[str] = None
    from_amount: Optional[str] = None
    requested_from_amount: Optional[str] = None
    refund_amount: Optional[str] = None
    to_amount: Optional[str] = None
    exchange_rate: Optional[str] = None
    fee_amount: Optional[str] = None
    from_amount_usd: Optional[str] = None
    to_amount_usd: Optional[str] = None
    processed_at: Optional[str] = None
    created_at: Optional[str] = None
    

class CreatePayment(BaseModel):
    uuid: Optional[str] = None
    order_id: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    amount_usd: Optional[str] = None
    exchange_rate: Optional[str] = None
    url: Optional[str] = None
    tg_deeplink: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: Optional[str] = None
    payer_currency: Optional[str] = None
    payer_amount: Optional[str] = None
    network: Optional[str] = None
    address: Optional[str] = None
    payment_status: Optional[str] = None
    txid: Optional[str] = None
    payment_amount: Optional[str] = None
    qr: Optional[str] = None
    

class PaymentInfo(BaseModel):
    uuid: Optional[str] = None
    order_id: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    url: Optional[str] = None
    tg_deeplink: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: Optional[str] = None
    payer_currency: Optional[str] = None
    payer_amount: Optional[str] = None
    network: Optional[str] = None
    address: Optional[str] = None
    payment_status: Optional[str] = None
    txid: Optional[str] = None
    payment_amount: Optional[str] = None
    merchant_amount: Optional[str] = None
    qr: Optional[str] = None
    amount_usd: Optional[str] = None
    exchange_rate: Optional[str] = None


class Paginate(BaseModel):
    count: Optional[int] = None
    current_page: Optional[int] = None
    per_page: Optional[int] = None
    total: Optional[int] = None
    total_pages: Optional[int] = None
    has_more: Optional[bool] = None


class PaymentList(BaseModel):
    items: Optional[List[PaymentInfo]] = None
    paginate: Optional[Paginate] = None
    
    
class CreatePayout(BaseModel):
    uuid: Optional[str] = None
    order_id: Optional[str] = None
    status: Optional[str] = None
    currency: Optional[str] = None
    network: Optional[str] = None
    amount: Optional[str] = None
    merchant_amount: Optional[str] = None
    network_amount: Optional[str] = None
    amount_usd: Optional[str] = None
    to_address: Optional[str] = None
    memo: Optional[str] = None
    txid: Optional[str] = None
    block_number: Optional[str] = None
    error_type: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    

class CalculatePayout(BaseModel):
    currency: Optional[str] = None
    network: Optional[str] = None
    amount: Optional[str] = None
    fee_option: Optional[str] = None
    merchant_amount: Optional[str] = None
    network_amount: Optional[str] = None
    total_fee: Optional[str] = None
    total_fee_usd: Optional[str] = None
    

class PayoutInfo(BaseModel):
    uuid: Optional[str] = None
    order_id: Optional[str] = None
    status: Optional[str] = None
    currency: Optional[str] = None
    network: Optional[str] = None
    amount: Optional[str] = None
    merchant_amount: Optional[str] = None
    network_amount: Optional[str] = None
    amount_usd: Optional[str] = None
    to_address: Optional[str] = None
    memo: Optional[str] = None
    txid: Optional[str] = None
    block_number: Optional[Union[int, str]] = None
    error_type: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    from_currency: Optional[str] = None
    debited_amount: Optional[str] = None
    debited_currency: Optional[str] = None
    

class CreateStaticWallet(BaseModel):
    uuid: Optional[str] = None
    address: Optional[str] = None
    currency: Optional[str] = None
    network: Optional[str] = None
    label: Optional[str] = None
    order_id: Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[str] = None
    qr: Optional[str] = None
    

class StaticWalletInfo(BaseModel):
    uuid: Optional[str] = None
    address: Optional[str] = None
    currency: Optional[str] = None
    network: Optional[str] = None
    status: Optional[str] = None
    total_received: Optional[str] = None
    transactions_count: Optional[int] = None
    created_at: Optional[str] = None
    qr: Optional[str] = None
    
    
class StaticWalletList(BaseModel):
    items: Optional[List[StaticWalletInfo]] = None
    paginate: Optional[Paginate] = None
    

class StatusStaticWallet(BaseModel):
    uuid: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None


class StaticWalletTransaction(BaseModel):
    uuid: Optional[str] = None
    order_id: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    payment_status: Optional[str] = None
    txid: Optional[str] = None
    fee_amount: Optional[str] = None
    net_amount: Optional[str] = None
    created_at: Optional[str] = None


class StaticWalletTransactionsPaginate(BaseModel):
    count: Optional[int] = None
    hasPages: Optional[bool] = None
    perPage: Optional[int] = None
    page: Optional[int] = None


class StaticWalletTransactions(BaseModel):
    items: Optional[List[StaticWalletTransaction]] = None
    paginate: Optional[StaticWalletTransactionsPaginate] = None
    

class PaymentStatuses:
    pending: str = "pending"
    check: str = "check"
    paid: str = "paid"
    underpaid_check: str = "underpaid_check"
    underpaid: str = "underpaid"
    overpaid: str = "overpaid"
    cancel: str = "cancel"
    aml_lock: str = "aml_lock"
    
    
class PayoutStatuses:
    pending: str = "pending"
    completed: str = "completed"
    failed: str = "failed"
    cancelled: str = "cancelled"
    

class NetworkCodes:
    TRX_TRC20: str = "TRX-TRC20"
    BSC_BEP20: str = "BSC-BEP20"
    ETH_ERC20: str = "ETH-ERC20"
    AVAX_C: str = "AVAX-C"
    POL_MATIC: str = "POL-MATIC"
    TON: str = "TON"
    BTC: str = "BTC"
    LTC: str = "LTC"
    DASH: str = "DASH"
    SOL: str = "SOL"
    DOGE: str = "DOGE"
    ZEC: str = "ZEC"
    XRP: str = "XRP"
    XMR: str = "XMR"
    

class Currencies:
    USDT: str = "USDT"
    USDC: str = "USDC"
    BTC: str = "BTC"
    ETH: str = "ETH"
    BNB: str = "BNB"
    TRX: str = "TRX"
    LTC: str = "LTC"
    DASH: str = "DASH"
    GRAM: str = "GRAM"
    AVAX: str = "AVAX"
    POL: str = "POL"
    SOL: str = "SOL"
    DOGE: str = "DOGE"
    ZEC: str = "ZEC"
    XRP: str = "XRP"
    XMR: str = "XMR"