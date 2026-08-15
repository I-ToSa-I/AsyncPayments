from ..requests import RequestsClient
from typing import Optional, List
from .models import (Balance, CryptoPairPrice, Direction, ConversionPrice, ConvertInfo, CreatePayment, PaymentInfo, PaymentList, CreatePayout,
                     CalculatePayout, PayoutInfo, CreateStaticWallet, StaticWalletInfo, StaticWalletList, StatusStaticWallet, StaticWalletTransactions)
import json
import hmac
import hashlib
import base64

class Async2328io(RequestsClient):
    API_HOST: str = "https://2328.io/"

    def __init__(self, api_key: str, project_uuid: str) -> None:
        """
        Initialize 2328io API client
        :param api_key: Your 2328io API Key.
        :param terminal_id: Your 2328io Project UUID.
        """
        super().__init__()
        self.__api_key = api_key
        self.__project_uuid = project_uuid
        self.__headers = {
            "project": project_uuid,
            "Content-Type": "application/json",
        }
        self.__base_url = "https://api.2328.io/api/v1"
        self.__get_method = "GET"
        self.__post_method = "POST"
        self.__payment_name = "2328io"
        self.check_values()

    def check_values(self):
        if not self.__api_key or not self.__project_uuid:
            raise ValueError('No ApiKey or ProjectUUID specified')
    
    def __create_sign(self, data: Optional[dict] = None) -> str:
        if data:
            body = json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        else:
            body = b""
        b64 = base64.b64encode(body).decode()
        return hmac.new(self.__api_key.encode(), b64.encode(), hashlib.sha256).hexdigest()
    
    async def get_balance(self) -> List[Balance]:
        """Get the list of merchant accounts with their balances per currency.
        
        Docs: https://doc.2328.io/en/docs/balance"""
        url = f"{self.__base_url}/balance"
        self.__headers["sign"] = self.__create_sign()
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return [Balance(**balance) for balance in response['result']]
    
    async def get_exchange_rates(self) -> dict:
        """The exchange rates endpoint returns a matrix of current exchange rates between all supported currencies — both fiat (USD, EUR, RUB, etc.) and crypto (BTC, ETH, USDT, etc.).
                
        Docs: https://doc.2328.io/en/docs/exchange-rates"""
        url = f"{self.__base_url}/exchange-rates"
        self.__headers["sign"] = self.__create_sign()
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return response['result']

    async def get_crypto_pair_prices(self) -> List[CryptoPairPrice]:
        """Returns all supported pairs — direct coin→USDT pairs and synthetic cross-pairs via USDT (e.g. TRX→TON). Price already includes the platform markup.
                        
        Docs: https://doc.2328.io/en/docs/exchange-rates#crypto-pair-prices"""
        url = f"{self.__base_url}/prices"
        self.__headers["sign"] = self.__create_sign()
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return [CryptoPairPrice(**pair) for pair in response]
    
    async def get_directions(self) -> List[Direction]:
        """Returns all supported currency + network pairs with their current statuses, limits, and estimated withdrawal fees. Use it to dynamically build a currency selector UI and show users the withdrawal cost upfront.
        
        Docs: https://doc.2328.io/en/docs/directions"""
        url = f"{self.__base_url}/directions"
        self.__headers["sign"] = self.__create_sign()
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return [Direction(**direction) for direction in response['result']]
    
    async def get_conversion_price(self, from_currency: str, to_currency: str, amount: float, amount_type: str) -> ConversionPrice:
        """Returns an indicative quote for a conversion at the current market price — the effective rate and the resulting amounts. Nothing is debited or reserved; call it as often as you need before executing.
                
        :param from_currency: Required. Uppercase source asset code. A usable route and balance must exist; the displayed catalog is not a guarantee of an active market.
        :param to_currency: Required. Uppercase target asset code; must differ from from_currency and have a tradable direct or bridge route.
        :param amount: Required. Amount to convert, greater than 0.
        :param amount_type: Required. Which side amount refers to. Values: "from", "to".
                
        Docs: https://doc.2328.io/en/docs/converts#get-conversion-price"""
        url = f"{self.__base_url}/convert/price"
        params = {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "amount_type": amount_type
        }
        self.__headers["sign"] = self.__create_sign(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return ConversionPrice(**response['result'])
    
    async def execute_convert(self, from_currency: str, to_currency: str, amount: float, amount_type: str) -> ConvertInfo:
        """Executes a conversion at the current market price and updates your merchant balance. There is no separate "commit a quote" step — call this directly with the amount you want to convert.
                
        :param from_currency: Required. Uppercase source asset code. A usable route and balance must exist; the displayed catalog is not a guarantee of an active market.
        :param to_currency: Required. Uppercase target asset code; must differ from from_currency and have a tradable direct or bridge route.
        :param amount: Required. Amount to convert, greater than 0.
        :param amount_type: Required. Which side amount refers to. Values: "from", "to".
                
        Docs: https://doc.2328.io/en/docs/converts#get-conversion-price"""
        url = f"{self.__base_url}/convert"
        params = {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "amount_type": amount_type
        }
        self.__headers["sign"] = self.__create_sign(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return ConvertInfo(**response['result'])
    
    async def create_payment(self, amount: float, currency: str, order_id: str, url_callback: str, to_currency: Optional[str] = None, 
                             network: Optional[str] = None, url_return: Optional[str] = None, url_success: Optional[str] = None,
                             invite_code: Optional[str] = None, fee_split: Optional[float] = None, price_markup: Optional[float] = None,
                             description: Optional[str] = None, ttl_seconds: Optional[int] = None) -> CreatePayment:
        """Creates a payment session and returns a URL for the customer to pay.
                    
        :param amount: Required. Payment amount in the currency, e.g. 100.00.
        :param currency: Required. Fiat currency (USD, EUR, RUB, …) or an enabled cryptocurrency. Use /v1/directions as the live source of truth. TON is accepted as a legacy input alias for canonical GRAM.
        :param order_id: Required. Your order ID, e.g. ORDER-12345 (up to 128 chars).
        :param url_callback: Required. Public HTTP(S) URL for webhook notifications, e.g. https://your-site.com/webhook. Private, loopback, and otherwise unsafe targets are rejected.
        :param to_currency: Optional. Preselected enabled cryptocurrency; TON is normalized to GRAM.
        :param network: Optional. Canonical network code (required if to_currency is set or currency is a cryptocurrency).
        :param url_return: Optional. Redirect URL after payment, e.g. https://your-site.com/return.
        :param url_success: Optional. Alternative to url_return.
        :param invite_code: Optional. Referrer code.
        :param fee_split: Optional. Share of the merchant fee passed to the payer, 0–100 (%). 0 = merchant pays fully, 100 = payer pays fully. Overrides the project-level setting. Example: 30 (payer covers 30% of the fee).
        :param price_markup: Optional. Markup or discount on the invoice amount, −99 to 100 (%). Overrides the project-level setting. Example: 5 (+5%) or -10 (10% discount).
        :param description: Optional. Optional invoice description (max 200 chars). Shown to the payer on the payment page. Example: Premium plan — Order #12345.
        :param ttl_seconds: Optional. Invoice lifetime in seconds, from 300 (5 minutes) to 86400 (24 hours). After this period the invoice expires and can no longer be paid. Default: 3600 (1 hour). Example: 3600.
                
        Docs: https://doc.2328.io/en/docs/payments#create-payment"""
        url = f"{self.__base_url}/payment"
        params = {
            "amount": amount,
            "currency": currency,
            "order_id": order_id,
            "url_callback": url_callback,
            "to_currency": to_currency,
            "network": network,
            "url_return": url_return,
            "url_success": url_success,
            "invite_code": invite_code,
            "fee_split": fee_split,
            "price_markup": price_markup,
            "description": description,
            "ttl_seconds": ttl_seconds,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__create_sign(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return CreatePayment(**response['result'])
    
    async def get_payment(self, uuid: Optional[str] = None, order_id: Optional[str] = None) -> PaymentInfo:
        """Get the current payment status by uuid or order_id.
        At least one of `uuid` or `order_id` is required.
        
        :param uuid: Payment UUID (from result.uuid on creation).
        :param order_id: Your order ID.
       
        Docs: https://doc.2328.io/en/docs/payments#payment-info"""
        url = f"{self.__base_url}/payment/info"
        params = {
            "uuid": uuid,
            "order_id": order_id,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__create_sign(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return PaymentInfo(**response['result'])
    
    async def get_payment_list(self, status: Optional[str] = None, date_from: Optional[str] = None,
                               date_to: Optional[str] = None, page: Optional[int] = 1, per_page: Optional[int] = 15) -> PaymentList:
        """Get a list of all payments with filtering and pagination.
        
        :param status: Optional. Filter by list-supported payment status. aml_lock can appear in payment info/webhooks but is not accepted by this list filter.
        :param date_from: Optional. Start date (YYYY-MM-DD), e.g. 2026-01-01.
        :param date_to: Optional. End date (YYYY-MM-DD), e.g. 2026-01-31.
        :param page: Optional. Page number, default 1.
        :param per_page: Optional. Items per page, default 15, max 5000.
        
        Docs: https://doc.2328.io/en/docs/payments#payment-list"""
        url = f"{self.__base_url}/payment/list"
        params = {
            "status": status,
            "date_from": date_from,
            "date_to": date_to,
            "page": page,
            "per_page": per_page,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__create_sign(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return PaymentList(**response['result'])
    
    async def create_payout(self, currency: str, network: str, amount: str, to_address: str, order_id: Optional[str] = None,
                            url_callback: Optional[str] = None, memo: Optional[str] = None, from_currency: Optional[str] = None,
                            fee_option: Optional[str] = None) -> CreatePayout:
        """Creates a withdrawal request from your merchant balance.
                
        :param currency: Required. Withdrawal currency.
        :param network: Required. Network code.
        :param amount: Required. Withdrawal amount.
        :param to_address: Required. Recipient blockchain address.
        :param order_id: Optional. Idempotency key — unique within a project. A repeated POST with the same order_id does not create a new payout — the existing one is returned instead.
        :param url_callback: Optional. URL for payout webhooks. Omit to disable webhooks for this payout.
        :param memo: Optional. Destination tag / memo. Currently used only by TON and SOL networks; max 255 chars.
        :param from_currency: Optional. Source balance to debit and auto-convert into currency at the moment of payout. Lets you pay out in volatile assets (BTC, ETH, …) while keeping your balance in a stable coin like USDT — you don't have to hold the volatile crypto yourself. Pass "USDT" to debit the USDT balance.
        :param fee_option: Optional. How fees are charged. deduct (default) — network + platform fees subtracted from amount, the recipient gets amount - fees. add — fees added on top, the merchant is debited amount + fees, the recipient receives exactly amount.
        
        Docs: https://doc.2328.io/en/docs/payouts#create-payout"""
        url = f"{self.__base_url}/payout"
        params = {
            "currency": currency,
            "network": network,
            "amount": amount,
            "to_address": to_address,
            "order_id": order_id,
            "url_callback": url_callback,
            "memo": memo,
            "from_currency": from_currency,
            "fee_option": fee_option,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__create_sign(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return CreatePayout(**response['result'])
    
    async def calculate_payout(self, currency: str, network: str, amount: str, order_id: Optional[str] = None, 
                               from_currency: Optional[str] = None, fee_option: Optional[str] = None) -> CalculatePayout:
        """Estimates withdrawal amounts and fees without creating a payout or debiting your balance. Use it to show users the exact amount they will receive (or pay) before they confirm.
                
        :param currency: Required. Withdrawal currency.
        :param network: Required. Network code.
        :param amount: Required. Withdrawal amount.
        :param order_id: Optional. Idempotency key — unique within a project. A repeated POST with the same order_id does not create a new payout — the existing one is returned instead.
        :param from_currency: Optional. Source balance to debit and auto-convert into currency at the moment of payout. Lets you pay out in volatile assets (BTC, ETH, …) while keeping your balance in a stable coin like USDT — you don't have to hold the volatile crypto yourself. Pass "USDT" to debit the USDT balance.
        :param fee_option: Optional. How fees are charged. deduct (default) — network + platform fees subtracted from amount, the recipient gets amount - fees. add — fees added on top, the merchant is debited amount + fees, the recipient receives exactly amount.
        
        Docs: https://doc.2328.io/en/docs/payouts#calculate-payout"""
        url = f"{self.__base_url}/payout/calc"
        params = {
            "currency": currency,
            "network": network,
            "amount": amount,
            "order_id": order_id,
            "from_currency": from_currency,
            "fee_option": fee_option,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__create_sign(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return CalculatePayout(**response['result'])
        
    async def get_payout(self, uuid: str) -> PayoutInfo:
        """Get the status of a payout request.
                
        :param uuid: Required. Payout UUID (from result.uuid on creation)
        
        Docs: https://doc.2328.io/en/docs/payouts#payout-status"""
        url = f"{self.__base_url}/payout/status/{uuid}"
        self.__headers["sign"] = self.__create_sign()
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return PayoutInfo(**response['result'])
    
    async def create_static_wallet(self, currency: str, network: str, order_id: str, url_callback: str, label: Optional[str] = None,
                                   invite_code: Optional[str] = None) -> CreateStaticWallet:
        """Create static wallet.
                        
        :param currency: Required. Cryptocurrency (USDT, BTC, ETH, etc.).
        :param network: Required. Network code.
        :param order_id: Required. Your order/user ID (up to 255 chars).
        :param url_callback: Required. URL for webhook notifications.
        :param label: Optional. Wallet label (up to 255 chars).
        :param invite_code: Optional. Referrer code.
        
        
        Docs: https://doc.2328.io/en/docs/static-wallets#create-static-wallet"""
        url = f"{self.__base_url}/static-wallet"
        params = {
            "currency": currency,
            "network": network,
            "order_id": order_id,
            "url_callback": url_callback,
            "label": label,
            "invite_code": invite_code,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__create_sign(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return CreateStaticWallet(**response['result'])
    
    async def get_static_wallet(self, uuid: Optional[str] = None, address: Optional[str] = None) -> StaticWalletInfo:
        """Get static wallet information by uuid or address.
        At least one of `uuid` or `address` is required.
                        
        :param uuid: Static wallet UUID.
        :param address: Blockchain wallet address.
        
        Docs: https://doc.2328.io/en/docs/static-wallets#wallet-info"""
        url = f"{self.__base_url}/static-wallet/info"
        params = {
            "uuid": uuid,
            "address": address,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__create_sign(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return StaticWalletInfo(**response['result'])
    
    async def get_static_wallet_list(self, status: Optional[str] = None, currency: Optional[str] = None,
                                     network: Optional[str] = None, order_id: Optional[str] = None,
                                     page: Optional[int] = 1, per_page: Optional[int] = 20) -> StaticWalletList:
            """Get static wallet list.
                            
            :param status: Optional. Filter by status (active, inactive).
            :param currency: Optional. Filter by currency.
            :param network: Optional. Filter by network.
            :param order_id: Optional. Filter by order_id.
            :param page: Optional. Page number (default: 1).
            :param per_page: Optional. Items per page (default: 20, max: 100).
            
            Docs: https://doc.2328.io/en/docs/static-wallets#wallet-list"""
            url = f"{self.__base_url}/static-wallet/list"
            params = {
                "status": status,
                "currency": currency,
                "network": network,
                "order_id": order_id,
                "page": page,
                "per_page": per_page,
            }
            self._delete_empty_fields(params)
            self.__headers["sign"] = self.__create_sign(params)
            response = await self._request(
                self.__payment_name,
                self.__post_method,
                url,
                headers=self.__headers,
                data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
            )
            return StaticWalletList(**response['result'])
    
    async def enable_static_wallet(self, uuid: str) -> StatusStaticWallet:
        """Enable a static wallet accepts new payments.
                        
        :param uuid: Required. Static wallet UUID.
        
        Docs: https://doc.2328.io/en/docs/static-wallets#enable--disable-wallet"""
        url = f"{self.__base_url}/static-wallet/enable"
        params = {
            "uuid": uuid,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__create_sign(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return StatusStaticWallet(**response['result'])
    
    async def disable_static_wallet(self, uuid: str) -> StatusStaticWallet:
        """Disable a static wallet accepts new payments.
                        
        :param uuid: Required. Static wallet UUID.
        
        Docs: https://doc.2328.io/en/docs/static-wallets#enable--disable-wallet"""
        url = f"{self.__base_url}/static-wallet/disable"
        params = {
            "uuid": uuid,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__create_sign(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return StatusStaticWallet(**response['result'])
    
    async def get_static_wallet_transactions(self, uuid: str, date_from: Optional[str] = None,
                                             date_to: Optional[str] = None, page: Optional[int] = 1,
                                             per_page: Optional[int] = 15) -> StaticWalletTransactions:
        """Get a list of all deposits received by a static wallet.
                        
        :param uuid: Required. Static wallet UUID.
        :param date_from: Optional. Start date (YYYY-MM-DD).
        :param date_to: Optional. End date (YYYY-MM-DD).
        :param page: Optional. Page number (default: 1).
        :param per_page: Optional. Items per page (default: 15, max: 5000).
        
        Docs: https://doc.2328.io/en/docs/static-wallets#wallet-transactions"""
        url = f"{self.__base_url}/static-wallet/transactions"
        params = {
            "uuid": uuid,
            "date_from": date_from,
            "date_to": date_to,
            "page": page,
            "per_page": per_page,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__create_sign(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return StaticWalletTransactions(**response['result'])