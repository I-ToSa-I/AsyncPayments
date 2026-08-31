from pydantic import BaseModel, Field
from typing import Optional, List


class Balance(BaseModel):
    asset: Optional[str] = None
    balance: Optional[str] = None
    available: Optional[str] = None
    holds: Optional[str] = None


class AppInfo(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None


class Health(BaseModel):
    status: Optional[str] = None
    info: Optional[dict] = None
    error: Optional[dict] = None
    details: Optional[dict] = None


class InvoiceCallback(BaseModel):
    callbackUrl: Optional[str] = None
    payload: Optional[dict] = None
    
    
class InvoiceUrl(BaseModel):
    successUrl: Optional[str] = None
    cancelUrl: Optional[str] = None
    

class InvoiceCustomer(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None
    telegramId: Optional[str] = None
    telegramUsername: Optional[str] = None
    
    
class InvoiceLinks(BaseModel):
    telegramBotLink: Optional[str] = None
    telegramMiniAppLink: Optional[str] = None
    webLink: Optional[str] = None


class Invoice(BaseModel):
    id: Optional[str] = None
    priceAmount: Optional[str] = None
    minPayment: Optional[str] = None
    priceCurrency: Optional[str] = None
    payCurrencies: Optional[List[str]] = None
    clientInvoiceId: Optional[str] = None
    description: Optional[str] = None
    expiresIn: Optional[int] = None
    createdAt: Optional[str] = None
    expiresAt: Optional[str] = None
    status: Optional[str] = None
    callback: Optional[InvoiceCallback] = {}
    url: Optional[InvoiceUrl] = {}
    customer: Optional[InvoiceCustomer] = {}
    links: Optional[InvoiceLinks] = {}


class Pagination(BaseModel):
    total: Optional[int] = None
    next: Optional[str] = None


class InvoicesList(BaseModel):
    items: Optional[List[Invoice]] = None
    pagination: Optional[Pagination] = None
    
    
class PaymentTransaction(BaseModel):
    id: Optional[str] = None
    status: Optional[str] = None
    payAmount: Optional[str] = None
    payCurrency: Optional[str] = None
    receiveAmount: Optional[str] = None
    receiveCurrency: Optional[str] = None
    comment: Optional[str] = None
    payer: Optional[dict] = None
    createdAt: Optional[str] = None
    finalizedAt: Optional[str] = None
    type_: Optional[str] = Field(alias="type", default=None)
    tx: Optional[dict] = None
    
    
class InvoicePayment(BaseModel):
    id: Optional[str] = None
    status: Optional[str] = None
    finalizedAt: Optional[str] = None
    payAmount: Optional[str] = None
    payCurrency: Optional[str] = None
    receiveAmount: Optional[str] = None
    receiveCurrency: Optional[str] = None
    transactions: Optional[List[PaymentTransaction]] = None
    
    
class InvoicePayments(BaseModel):
    items: Optional[List[InvoicePayment]] = None
    pagination: Optional[Pagination] = None


class InvoicePaymentAddress(BaseModel):
    address: Optional[str] = None
    payCurrency: Optional[str] = None
    payNetwork: Optional[str] = None
    expiresAt: Optional[str] = None
    minAmount: Optional[str] = None
    

class Cheque(BaseModel):
    chequeId: Optional[str] = None
    clientChequeId: Optional[str] = None
    asset: Optional[str] = None
    description: Optional[str] = None
    targetType: Optional[str] = None
    target: Optional[str] = None
    links: Optional[dict] = None
    state: Optional[str] = None
    deleted: Optional[bool] = None
    callback: Optional[dict] = None
    url: Optional[dict] = None


class ChequesList(BaseModel):
    items: Optional[List[Cheque]] = None
    pagination: Optional[Pagination] = None


class Payout(BaseModel):
    payoutId: Optional[str] = None
    clientPayoutId: Optional[str] = None
    target: Optional[str] = None
    targetType: Optional[str] = None
    asset: Optional[str] = None
    amount: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    callback: Optional[dict] = None
    
    
class ErrorPayout(BaseModel):
    target: Optional[str] = None
    targetType: Optional[str] = None
    amount: Optional[str] = None
    clientPayoutId: Optional[str] = None
    description: Optional[str] = None
    reason: Optional[dict] = None


class PayoutsList(BaseModel):
    items: Optional[List[Payout]] = None
    pagination: Optional[Pagination] = None


class MassPayouts(BaseModel):
    successPayouts: Optional[List[Payout]] = None
    errorPayouts: Optional[List[ErrorPayout]] = None


class Withdrawal(BaseModel):
    withdrawalId: Optional[str] = None
    network: Optional[str] = None
    address: Optional[str] = None
    asset: Optional[str] = None
    amount: Optional[str] = None
    status: Optional[str] = None
    comment: Optional[str] = None
    txHash: Optional[str] = None
    txLink: Optional[str] = None
    callback: Optional[dict] = None


class WithdrawalsList(BaseModel):
    items: Optional[List[Withdrawal]] = None
    pagination: Optional[Pagination] = None


class WithdrawalQuotas(BaseModel):
    withdrawMinSize: Optional[str] = None
    withdrawFee: Optional[str] = None
    withdrawFeeAsset: Optional[str] = None
    precision: Optional[int] = None


class WithdrawalLink(BaseModel):
    telegramBotLink: Optional[str] = None
    telegramMiniAppLink: Optional[str] = None
    webLink: Optional[str] = None


class CurrencyNetwork(BaseModel):
    code: Optional[str] = None


class Currency(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    kind: Optional[str] = None
    networks: Optional[List[CurrencyNetwork]] = None

class Rate(BaseModel):
    currency: Optional[str] = None
    rate: Optional[str] = None
    