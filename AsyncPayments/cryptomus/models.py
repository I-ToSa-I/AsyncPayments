from pydantic import BaseModel, Field
from typing import Optional, Union, List


class Balances(BaseModel):
    merchant: Optional[list] = None
    user: Optional[list] = None


class Balance(BaseModel):
    uuid: Optional[str] = None
    balance: Optional[str] = None
    currency_code: Optional[str] = None
    balance_usd: Optional[str] = None


class CreatePayment(BaseModel):
    uuid: Optional[str] = None
    order_id: Optional[str] = None
    amount: Optional[str] = None
    payment_amount: Optional[Union[str, int]] = None
    payment_amount_usd: Optional[Union[str, int]] = None
    payer_amount: Optional[Union[str, int]] = None
    payer_amount_exchange_rate: Optional[Union[str, int]] = None
    discount_percent: Optional[Union[str, int]] = None
    discount: Optional[str] = None
    payer_currency: Optional[Union[str, int]] = None
    currency: Optional[str] = None
    comments: Optional[Union[str, dict, list]] = None
    merchant_amount: Optional[Union[str, int]] = None
    network: Optional[str] = None
    address: Optional[str] = None
    from_: Optional[str] = Field(alias="from", default=None)
    txid: Optional[str] = None
    payment_status: Optional[str] = None
    url: Optional[str] = None
    expired_at: Optional[int] = None
    status: Optional[str] = None
    is_final: Optional[bool] = None
    aditional_data: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    commission: Optional[Union[str, int]] = None
    address_qr_code: Optional[str] = None
    mercuryo_payment_link: Optional[str] = None


class GenerateStaticWallet(BaseModel):
    wallet_uuid: Optional[str] = None
    uuid: Optional[str] = None
    address: Optional[str] = None
    network: Optional[str] = None
    currency: Optional[str] = None
    url: Optional[str] = None
    

class GenerateQrCode(BaseModel):
    image: Optional[str] = None


class BlockStaticWallet(BaseModel):
    uuid: Optional[str] = None
    status: Optional[str] = None


class RefundPaymentsOnBlockedAddress(BaseModel):
    commission: Optional[str] = None
    amount: Optional[str] = None


class PaymentInfo(BaseModel):
    uuid: Optional[str] = None
    order_id: Optional[str] = None
    amount: Optional[str] = None
    payment_amount: Optional[str] = None
    payer_amount: Optional[str] = None
    discount_percent: Optional[Union[int, float, str]] = None
    discount: Optional[str] = None
    payer_currency: Optional[str] = None
    currency: Optional[str] = None
    merchant_amount: Optional[str] = None
    network: Optional[str] = None
    address: Optional[str] = None
    from_: Optional[str] = Field(alias="from", default=None)
    txid: Optional[str] = None
    payment_status: Optional[str] = None
    url: Optional[str] = None
    expired_at: Optional[int] = None
    status: Optional[str] = None
    is_final: Optional[bool] = None
    additional_data: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ServiceInfo:
    class ServiceLimit(BaseModel):
        min_amount: Optional[str] = None
        max_amount: Optional[str] = None


    class ServiceCommission(BaseModel):
        fee_amount: Optional[str] = None
        percent: Optional[str] = None


class ListOfServices(BaseModel):
    network: Optional[str] = None
    currency: Optional[str] = None
    is_available: Optional[bool] = None
    limit: Optional[ServiceInfo.ServiceLimit] = None
    commission: Optional[ServiceInfo.ServiceCommission] = None


class HistoryPaginate(BaseModel):
    count: Optional[int] = None
    hasPages: Optional[bool] = None
    nextCursor: Optional[str] = None
    previousCursor: Optional[str] = None
    perPage: Optional[int] = None


class PaymentHistory(BaseModel):
    items: Optional[List[PaymentInfo]] = None
    paginate: Optional[HistoryPaginate] = None


class PayoutHistoryItem(BaseModel):
    uuid: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    network: Optional[str] = None
    address: Optional[str] = None
    txid: Optional[str] = None
    status: Optional[str] = None
    is_final: Optional[bool] = None
    balance: Optional[Union[str, int]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class PayoutHistory(BaseModel):
    merchant_uuid: Optional[str] = None
    items: Optional[List[PayoutHistoryItem]] = None
    paginate: Optional[HistoryPaginate] = None


class Payout(BaseModel):
    uuid: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    network: Optional[str] = None
    address: Optional[str] = None
    txid: Optional[str] = None
    status: Optional[str] = None
    is_final: Optional[bool] = None
    balance: Optional[Union[str, int]] = None
    payer_currency: Optional[str] = None
    payer_amount: Optional[Union[str, int]] = None


class ListOfServicesPayout(BaseModel):
    network: Optional[str] = None
    currency: Optional[str] = None
    is_available: Optional[bool] = None
    limit: Optional[ServiceInfo.ServiceLimit] = None
    commission: Optional[ServiceInfo.ServiceCommission] = None


class TransferWallet(BaseModel):
    user_wallet_transaction_uuid: Optional[str] = None
    user_wallet_balance: Optional[str] = None
    merchant_transaction_uuid: Optional[str] = None
    merchant_balance: Optional[str] = None


class RecurringPayment(BaseModel):
    uuid: Optional[str] = None
    name: Optional[str] = None
    order_id: Optional[str] = None
    amount: Optional[str] = None
    currency: Optional[str] = None
    payer_currency: Optional[str] = None
    payer_amount_usd: Optional[str] = None
    payer_amount: Optional[str] = None
    url_callback: Optional[str] = None
    period: Optional[str] = None
    status: Optional[str] = None
    url: Optional[str] = None
    last_pay_off: Optional[str] = None
    additional_data: Optional[str] = None


class ListOfRecurringPayments(BaseModel):
    merchant_uuid: Optional[str] = None
    items: Optional[List[RecurringPayment]] = None
    paginate: Optional[HistoryPaginate] = None


class ExchangeRatesList(BaseModel):
    from_: Optional[str] = Field(alias="from", default=None)
    to: Optional[str] = None
    course: Optional[str] = None


class Discount(BaseModel):
    currency: Optional[str] = None
    network: Optional[str] = None
    discount: Optional[Union[str, int, float]] = None


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