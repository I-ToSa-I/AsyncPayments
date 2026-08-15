from pydantic import BaseModel
from typing import Optional, List


class Balance(BaseModel):
    terminal_id: Optional[str] = None
    available_usdt: Optional[str] = None
    hold_usdt: Optional[str] = None


class Rate(BaseModel):
    rate: Optional[str] = None
    updated_at: Optional[str] = None


class CreatePayment(BaseModel):
    payment_id: Optional[str] = None
    order_id: Optional[str] = None
    status: Optional[str] = None
    token: Optional[str] = None
    pay_url: Optional[str] = None
    amount: Optional[str] = None
    payment_currency: Optional[str] = None
    qr_content: Optional[str] = None
    h2h_enabled: Optional[bool] = None
    qr_activated: Optional[bool] = None
    redirect_url: Optional[str] = None
    environment: Optional[str] = None
    fee_payer: Optional[str] = None
    created_at: Optional[str] = None
    expires_at: Optional[str] = None


class PaymentInfo(BaseModel):
    payment_id: Optional[str] = None
    order_id: Optional[str] = None
    amount: Optional[str] = None
    payment_currency: Optional[str] = None
    status: Optional[str] = None
    pay_url: Optional[str] = None
    h2h_enabled: Optional[bool] = None
    qr_activated: Optional[bool] = None
    redirect_url: Optional[str] = None
    environment: Optional[str] = None
    fee_payer: Optional[str] = None
    calc_version: Optional[int] = None
    risk_score_initial: Optional[int] = None
    risk_factors: Optional[dict] = {}
    risk_scored_at: Optional[str] = None
    requires_manual_review: Optional[bool] = None
    rate_fallback_used: Optional[bool] = None
    anomaly_detected: Optional[bool] = None
    client_ip: Optional[str] = None
    user_agent: Optional[str] = None
    rate_final: Optional[str] = None
    amount_usdt_net: Optional[str] = None
    platform_fee_percent: Optional[str] = None
    platform_fee_usdt: Optional[str] = None
    paid_at: Optional[str] = None
    created_at: Optional[str] = None
    expires_at: Optional[str] = None
    

class PaymentsList(BaseModel):
    items: Optional[List[PaymentInfo]] = None
    total: Optional[int] = None
    
    
class SubscriptionPlan(BaseModel):
    id: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    version: Optional[int] = None
    interval: Optional[str] = None
    cap_amount_rub: Optional[str] = None
    max_cycles: Optional[str] = None
   
   
class CreateSubscription(BaseModel):
    id: Optional[str] = None
    terminal_id: Optional[str] = None
    plan_id: Optional[str] = None
    merchant_subscription_ref: Optional[str] = None
    provider_state: Optional[str] = None
    billing_status: Optional[str] = None
    plan_code: Optional[str] = None
    plan_version: Optional[int] = None
    merchant_amount_rub: Optional[str] = None
    payer_amount_rub: Optional[str] = None
    interval: Optional[str] = None
    successful_cycles: Optional[int] = None
    consecutive_failures: Optional[int] = None
    pay_url: Optional[str] = None
    created_at: Optional[str] = None
   

class SubscriptionInfo(BaseModel):
    id: Optional[str] = None
    terminal_id: Optional[str] = None
    plan_id: Optional[str] = None
    merchant_subscription_ref: Optional[str] = None
    provider_state: Optional[str] = None
    billing_status: Optional[str] = None
    plan_code: Optional[str] = None
    plan_version: Optional[int] = None
    merchant_amount_rub: Optional[str] = None
    payer_amount_rub: Optional[str] = None
    interval: Optional[str] = None
    successful_cycles: Optional[int] = None
    consecutive_failures: Optional[int] = None
    pay_url: Optional[str] = None
    created_at: Optional[str] = None
    next_charge_at: Optional[str] = None
    created_at: Optional[str] = None
    activated_at: Optional[str] = None
    stopped_at: Optional[str] = None


class SubscriptionCharges(BaseModel):
    id: Optional[str] = None
    payment_id: Optional[str] = None
    status: Optional[str] = None
    validation_status: Optional[str] = None
    cycle_number: Optional[int] = None
    amount_rub: Optional[str] = None
    expected_amount_rub: Optional[str] = None
    scheduled_at: Optional[str] = None
    actual_at: Optional[str] = None
    created_at: Optional[str] = None
    message: Optional[str] = None
    

class SubscriptionStop(BaseModel):
    ok: Optional[bool] = None

   
class SubscriptionList(BaseModel):
    items: Optional[List[SubscriptionInfo]] = None
    total: Optional[int] = None


class Payout(BaseModel):
    id: Optional[str] = None
    terminal_id: Optional[str] = None
    amount_usdt: Optional[str] = None
    wallet_address: Optional[str] = None
    network: Optional[str] = None
    status: Optional[str] = None
    idempotency_key: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    
class PaymentStatuses:
    created: str = "created"
    processing: str = "processing"
    paid: str = "paid"
    canceled: str = "canceled"
    chargeback: str = "chargeback"
    refunded: str = "refunded"
    

class SubscriptionProviderStates:
    new: str = "new"
    active: str = "active"
    stop: str = "stop"
    

class SubscriptionBillingStatuses:
    consent_pending: str = "consent_pending"
    pending: str = "pending"
    enabled: str = "enabled"
    review: str = "review"
    stop_pending: str = "stop_pending"
    stopped: str = "stopped"
    

class PayoutStatuses:
    created: str = "created"
    pending: str = "pending"
    processing: str = "processing"
    completed: str = "completed"
    rejected: str = "rejected"