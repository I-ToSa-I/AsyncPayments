from pydantic import BaseModel, Field
from typing import Optional, Union, List


class Balances(BaseModel):
    merchant: list
    user: list


class Balance(BaseModel):
    uuid: str
    balance: str
    currency_code: str
    balance_usd: str


class CreatePayment(BaseModel):
    uuid: str
    order_id: str
    amount: str
    payment_amount: Optional[Union[str, int]] = None
    payment_amount_usd: Optional[Union[str, int]] = None
    payer_amount: Optional[Union[str, int]] = None
    payer_amount_exchange_rate: Optional[Union[str, int]] = None
    discount_percent: Optional[Union[str, int]] = None
    discount: str
    payer_currency: Optional[Union[str, int]] = None
    currency: str
    comments: Optional[Union[str, dict, list]] = None
    merchant_amount: Optional[Union[str, int]] = None
    network: Optional[str] = None
    address: Optional[str] = None
    from_: Optional[str] = Field(alias="from", default=None)
    txid: Optional[str] = None
    payment_status: str
    url: str
    expired_at: int
    status: str
    is_final: bool
    aditional_data: Optional[str] = None
    created_at: str
    updated_at: str
    commission: Optional[Union[str, int]] = None
    address_qr_code: Optional[str] = None
    mercuryo_payment_link: Optional[str] = None


class GenerateStaticWallet(BaseModel):
    wallet_uuid: str
    uuid: str
    address: str
    network: str
    currency: str
    url: str
    

class GenerateQrCode(BaseModel):
    image: str


class BlockStaticWallet(BaseModel):
    uuid: str
    status: str


class RefundPaymentsOnBlockedAddress(BaseModel):
    commission: str
    amount: str


class PaymentInfo(BaseModel):
    uuid: str
    order_id: str
    amount: str
    payment_amount: Optional[str] = None
    payer_amount: Optional[str] = None
    discount_percent: Optional[Union[int, float, str]] = None
    discount: str
    payer_currency: Optional[str] = None
    currency: str
    merchant_amount: Optional[str] = None
    network: Optional[str] = None
    address: Optional[str] = None
    from_: Optional[str] = Field(alias="from", default=None)
    txid: Optional[str] = None
    payment_status: str
    url: str
    expired_at: int
    status: str
    is_final: bool
    additional_data: Optional[str] = None
    created_at: str
    updated_at: str


class ServiceInfo:
    class ServiceLimit(BaseModel):
        min_amount: str
        max_amount: str


    class ServiceCommission(BaseModel):
        fee_amount: str
        percent: str


class ListOfServices(BaseModel):
    network: str
    currency: str
    is_available: bool
    limit: ServiceInfo.ServiceLimit
    commission: ServiceInfo.ServiceCommission


class HistoryPaginate(BaseModel):
    count: int
    hasPages: bool
    nextCursor: Optional[str] = None
    previousCursor: Optional[str] = None
    perPage: int


class PaymentHistory(BaseModel):
    items: List[PaymentInfo]
    paginate: HistoryPaginate


class PayoutHistoryItem(BaseModel):
    uuid: str
    amount: str
    currency: str
    network: str
    address: str
    txid: Optional[str] = None
    status: str
    is_final: bool
    balance: Union[str, int]
    created_at: str
    updated_at: str


class PayoutHistory(BaseModel):
    merchant_uuid: Optional[str] = None
    items: List[PayoutHistoryItem]
    paginate: HistoryPaginate


class Payout(BaseModel):
    uuid: str
    amount: str
    currency: str
    network: str
    address: str
    txid: Optional[str] = None
    status: str
    is_final: bool
    balance: Union[str, int]
    payer_currency: str
    payer_amount: Union[str, int]


class ListOfServicesPayout(BaseModel):
    network: str
    currency: str
    is_available: bool
    limit: ServiceInfo.ServiceLimit
    commission: ServiceInfo.ServiceCommission


class TransferWallet(BaseModel):
    user_wallet_transaction_uuid: str
    user_wallet_balance: str
    merchant_transaction_uuid: str
    merchant_balance: str


class RecurringPayment(BaseModel):
    uuid: str
    name: str
    order_id: Optional[str] = None
    amount: str
    currency: str
    payer_currency: str
    payer_amount_usd: str
    payer_amount: str
    url_callback: Optional[str] = None
    period: str
    status: str
    url: str
    last_pay_off: Optional[str] = None
    additional_data: Optional[str] = None


class ListOfRecurringPayments(BaseModel):
    merchant_uuid: Optional[str] = None
    items: List[RecurringPayment]
    paginate: HistoryPaginate


class ExchangeRatesList(BaseModel):
    from_: Optional[str] = Field(alias="from", default=None)
    to: str
    course: str


class Discount(BaseModel):
    currency: str
    network: str
    discount: Union[str, int, float]


class CurrenciesNames:
    USDC: str = "USDC"
    ETH: str = "ETH"
    USDT: str = "USDT"
    AVAX: str = "AVAX"
    BCH: str = "BCH"
    BNB: str = "BNB"
    CGPT: str = "CGPT"
    DAI: str = "DAI"
    BTC: str = "BTC"
    DASH: str = "DASH"
    DOGE: str = "DOGE"
    SHIB: str = "SHIB"
    MATIC: str = "MATIC"
    VERSE: str = "VERSE"
    LTC: str = "LTC"
    CRMS: str = "CRMS"
    SOL: str = "SOL"
    TON: str = "TON"
    HMSTR: str = "HMSTR"
    TRX: str = "TRX"
    XMR: str = "XMR"


class NetworkNames:
    ARBITRUM: str = "ARBITRUM"
    AVALANCHE: str = "AVALANCHE"
    BCH: str = "BCH"
    BSC: str = "BSC"
    BTC: str = "BTC"
    DASH: str = "DASH"
    DOGE: str = "DOGE"
    ETH: str = "ETH"
    LTC: str = "LTC"
    POLYGON: str = "POLYGON"
    SOL: str = "SOL"
    TON: str = "TON"
    TRON: str = "TRON"
    XMR: str = "XMR"


class InvoiceStatuses:
    PROCESS: str = "process"
    CHECK: str = "check"
    CONFIRM_CHECK: str = "confirm_check"
    PAID: str = "paid"
    PAID_OVER: str = "paid_over"
    FAIL: str = "fail"
    WRONG_AMOUNT: str = "wrong_amount"
    WRONG_AMOUNT_WAITING = "wrong_amount_waiting"
    CANCEL: str = "cancel"
    SYSTEM_FAIL: str = "system_fail"
    REFUND_PROCESS: str = "refund_process"
    REFUND_FAIL: str = "refund_fail"
    REFUND_PAID: str = "refund_paid"
    LOCKED: str = "locked"


class PayoutStatuses:
    PROCESS: str = "process"
    CHECK: str = "check"
    PAID: str = "paid"
    FAIL: str = "fail"
    CANCEL: str = "cancel"
    SYSTEM_FAIL: str = "system_fail"