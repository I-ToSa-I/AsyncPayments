from pydantic import BaseModel
from typing import Optional, List


class Shop(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    created_at: Optional[str] = None


class ShopKey(BaseModel):
    test: Optional[bool] = None
    access: Optional[str] = None


class ShopInfo(BaseModel):
    shop: Optional[Shop] = None
    key: Optional[ShopKey] = None


class Balance(BaseModel):
    chain: Optional[str] = None
    asset: Optional[str] = None
    decimals: Optional[int] = None
    confirmed: Optional[str] = None
    pending: Optional[str] = None
    seen: Optional[str] = None


class FiatCurrency(BaseModel):
    code: Optional[str] = None
    symbol: Optional[str] = None
    scale: Optional[int] = None


class CryptoCurrency(BaseModel):
    code: Optional[str] = None
    scale: Optional[int] = None


class Currencies(BaseModel):
    fiat: Optional[List[FiatCurrency]] = None
    crypto: Optional[List[CryptoCurrency]] = None


class InvoiceItem(BaseModel):
    name: Optional[str] = None
    quantity: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[str] = None
    amount: Optional[str] = None


class InvoicePayment(BaseModel):
    deposit_id: Optional[str] = None
    status: Optional[str] = None
    chain: Optional[str] = None
    asset: Optional[str] = None
    amount: Optional[str] = None
    tx_hash: Optional[str] = None
    value: Optional[str] = None
    late: Optional[bool] = None
    created_at: Optional[str] = None
    confirmed_at: Optional[str] = None


class Invoice(BaseModel):
    id: Optional[str] = None
    number: Optional[int] = None
    title: Optional[str] = None
    shop_id: Optional[str] = None
    test: Optional[bool] = None
    status: Optional[str] = None
    currency: Optional[str] = None
    currency_kind: Optional[str] = None
    amount: Optional[str] = None
    amount_paid: Optional[str] = None
    amount_pending: Optional[str] = None
    amount_due: Optional[str] = None
    amount_overpaid: Optional[str] = None
    reference: Optional[str] = None
    pay_url: Optional[str] = None
    paid_late: Optional[bool] = None
    paid_manually: Optional[bool] = None
    expires_at: Optional[str] = None
    paid_at: Optional[str] = None
    created_at: Optional[str] = None
    description: Optional[str] = None
    return_url: Optional[str] = None
    expired_at: Optional[str] = None
    cancelled_at: Optional[str] = None
    items: Optional[List[InvoiceItem]] = None
    payments: Optional[List[InvoicePayment]] = None


class InvoiceList(BaseModel):
    invoices: Optional[List[Invoice]] = None
    next_cursor: Optional[str] = None


class WebhookData(BaseModel):
    invoice: Optional[Invoice] = None
    payment: Optional[dict] = None
    payout: Optional[dict] = None


class WebhookEvent(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None
    created_at: Optional[str] = None
    shop_id: Optional[str] = None
    test: Optional[bool] = None
    data: Optional[WebhookData] = None
