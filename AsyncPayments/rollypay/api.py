from ..requests import RequestsClient
from typing import Optional, List
from .models import (Balance, Rate, CreatePayment, PaymentInfo, PaymentsList, SubscriptionPlan, CreateSubscription, SubscriptionList, 
                     SubscriptionInfo, SubscriptionCharges, SubscriptionStop, Payout)
import json
import uuid

class AsyncRollyPay(RequestsClient):
    API_HOST: str = "https://rollypay.io/"

    def __init__(self, api_key: str, terminal_id: str) -> None:
        """
        Initialize RollyPay API client
        :param api_key: Your RollyPay API Key.
        :param terminal_id: Your RollyPay Terminal ID.
        """
        super().__init__()
        self.__api_key = api_key
        self.__terminal_id = terminal_id
        self.__headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json",
        }
        self.__base_url = "https://rollypay.io/api/v1"
        self.__get_method = "GET"
        self.__post_method = "POST"
        self.__payment_name = "rolly"
        self.check_values()

    def check_values(self):
        if not self.__api_key or not self.__terminal_id:
            raise ValueError('No ApiKey or TerminalID specified')
    
    async def get_balance(self) -> Balance:
        """Get the cash balance.
        
        Docs: https://docs.rollypay.io/api/balance-rate"""
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        url = f"{self.__base_url}/balance?terminal_id={self.__terminal_id}"
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return Balance(**response)
    
    async def get_rate(self, with_terminal_id: Optional[bool] = False) -> Rate:
        """Returns the current USDT/RUB exchange rate.
        
        :param with_terminal_id: If `with_terminal_id` is False, the current rate is returned. If `with_terminal_id` is True, the rate for the specified terminal is returned.

        Docs: https://docs.rollypay.io/api/balance-rate"""
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        url = self.__base_url + (f'/rate?terminal_id={self.__terminal_id}' if with_terminal_id else '/rate')
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return Rate(**response)
    
    async def create_payment(self,
                             amount: str,
                             payment_currency: str,
                             order_id: str,
                             payment_method: Optional[str] = None,
                             description: Optional[str] = None,
                             customer_id: Optional[str] = None,
                             redirect_url: Optional[str] = None,
                             success_redirect_url: Optional[str] = None,
                             fail_redirect_url: Optional[str] = None,
                             metadata: Optional[dict] = None,
                             test: Optional[bool] = False,
                             ) -> CreatePayment:
        """Creates a payment and returns a link to the payment page for the customer.
        
        :param amount: Required. Fiat amount (e.g., "1500.00").
        :param payment_currency: Required. Currency code. Defaults to RUB. The value EUR is permitted only for payment_method: "intl_card".
        :param order_id: Required. Your unique order identifier.
        :param payment_method: Optional. Payment method (e.g., SBP, card, intl_card, crypto). If not provided, the user will be prompted to select one on the payment form.
        :param description: Optional. Payment description for the client.
        :param customer_id: Optional. Your Payer ID.
        :param redirect_url: Optional. URL for client redirection after payment (general). If not specified, the value is taken from the checkout settings.
        :param success_redirect_url: Optional. Redirect URL upon successful payment. Priority: payment parameter → checkout setting.
        :param fail_redirect_url: Optional. Redirect URL for unsuccessful payment (expired/canceled). Priority: payment parameter → checkout setting..
        :param metadata: Optional. Arbitrary data returned in callbacks.
        :param test: Optional. True — create a test (sandbox) payment. Default to False.
        
        Docs: https://docs.rollypay.io/api/payments
        """
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        url = f"{self.__base_url}/payments"
        params = {
            "amount": amount,
            "payment_currency": payment_currency,
            "payment_method": payment_method,
            "order_id": order_id,
            "description": description,
            "customer_id": customer_id,
            "success_redirect_url": success_redirect_url,
            "fail_redirect_url": fail_redirect_url,
            "metadata": metadata,
            "test": test,
        }
        self._delete_empty_fields(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params),
        )
        return CreatePayment(**response)
    
    async def get_payment(self, payment_id: str) -> PaymentInfo:
        """Returns a payment object: status, amount, final exchange rate, commission, payment time, and other payment details.
        
        :param payment_id: Required. Your payment ID.
        
        Docs: https://docs.rollypay.io/api/payments
        """
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        url = f"{self.__base_url}/payments/{payment_id}"
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return PaymentInfo(**response)
    
    async def get_payment_list(self) -> PaymentsList:
        """Returns a list of payments.
        
        Docs: https://docs.rollypay.io/api/payments
        """
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        url = f"{self.__base_url}/payments"
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return PaymentsList(**response)
    
    async def get_subscription_plans(self) -> List[SubscriptionPlan]:
        """Returns only active subscriptions narios connected to this checkout.
                
        Docs: https://docs.rollypay.io/api/recurring
        """
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        url = f"{self.__base_url}/subscription-plans?terminal_id={self.__terminal_id}"
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return [SubscriptionPlan(**item) for item in response["items"]]
    
    async def create_subscription(self, idempotency_key: str, plan_id: str, amount: str, 
                                       merchant_subscription_ref: Optional[str] = None) -> CreateSubscription:
        """Creating a subscription.
                
        Docs: https://docs.rollypay.io/api/recurring
        """
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        self.__headers["Idempotency-Key"] = idempotency_key
        url = f"{self.__base_url}/subscriptions"
        params = {
            "plan_id": plan_id,
            "amount": amount,
            "merchant_subscription_ref": merchant_subscription_ref,
        }
        self._delete_empty_fields(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params)
        )
        return CreateSubscription(**response)
    
    async def get_subscription_list(self) -> SubscriptionList:
        """Returns list of subscriptions.
                
        Docs: https://docs.rollypay.io/api/recurring
        """
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        url = f"{self.__base_url}/subscriptions?terminal_id={self.__terminal_id}"
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return SubscriptionList(**response)
    
    async def get_subscription(self, subscription_id: str) -> SubscriptionList:
        """Get a subscription.
                
        Docs: https://docs.rollypay.io/api/recurring
        """
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        url = f"{self.__base_url}/subscriptions/{subscription_id}"
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return SubscriptionInfo(**response)
    
    async def get_subscription_charges(self, subscription_id: str) -> SubscriptionCharges:
        """Returning subscription charge history.
        
        Docs: https://docs.rollypay.io/api/recurring"""
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        url = f"{self.__base_url}/subscriptions/{subscription_id}/charges"
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return SubscriptionCharges(**response)
    
    async def stop_subscription(self, subscription_id: str) -> SubscriptionStop:
        """Stopping the subscription.
        
        Docs: https://docs.rollypay.io/api/recurring"""
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        url = f"{self.__base_url}/subscriptions/{subscription_id}/stop"
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
        )
        return SubscriptionStop(**response)
    
    async def create_payout(self, amount_usdt: str, wallet_address: str, network: str, 
                            idempotency_key: Optional[str] = None) -> Payout:
        """Creating payout.
                
        Docs: https://docs.rollypay.io/api/payouts"""
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        url = f"{self.__base_url}/payouts?terminal_id={self.__terminal_id}"
        params = {
            "amount_usdt": amount_usdt,
            "wallet_address": wallet_address,
            "network": network,
            "idempotency_key": idempotency_key,
        }
        self._delete_empty_fields(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params),
        )
        return Payout(**response)
    
    async def get_payout_list(self) -> List[Payout]:
        """Returning list of payouts.
                
        Docs: https://docs.rollypay.io/api/payouts"""
        self.__headers["X-Nonce"] = str(uuid.uuid4())
        url = f"{self.__base_url}/payouts?terminal_id={self.__terminal_id}"
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return [Payout(**payout) for payout in response]