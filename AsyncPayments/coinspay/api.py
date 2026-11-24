from ..requests import RequestsClient
from ..exceptions import BadRequest
from typing import Optional, List, Union
from decimal import Decimal, InvalidOperation
from urllib.parse import quote
from .models import ShopInfo, Balance, Currencies, Invoice, InvoiceList, WebhookEvent
import json
import hmac
import hashlib
import re
import time


class AsyncCoinsPay(RequestsClient):
    API_HOST: str = "https://coinspay.app/"

    def __init__(self, api_key: str, webhook_secret: Optional[str] = None) -> None:
        """
        Initialize CoinsPay API client
        :param api_key: Your CoinsPay API key: cpk_live_... or cpk_test_... (a test key creates test invoices).
        :param webhook_secret: Optional. Webhook secret of the shop, needed only for parse_webhook().
        """
        super().__init__()
        self.__api_key = api_key
        self.__webhook_secret = webhook_secret
        self.__base_url = "https://coinspay.app/api/v1"
        self.__get_method = "GET"
        self.__post_method = "POST"
        self.__payment_name = "coinspay"
        self.check_values()

    def check_values(self):
        if not self.__api_key:
            raise ValueError('No ApiKey specified')

    def __headers(self, idempotency_key: Optional[str] = None) -> dict:
        headers = {
            "Authorization": f"Bearer {self.__api_key}",
            "Content-Type": "application/json",
        }
        if idempotency_key is not None:
            headers["Idempotency-Key"] = idempotency_key
        return headers

    @staticmethod
    def __amount(value: Union[str, int, float, Decimal]) -> str:
        if isinstance(value, bool):
            raise ValueError("Amount must be a number")
        try:
            amount = Decimal(str(value))
        except (InvalidOperation, ValueError):
            raise ValueError(f"Invalid amount: {value!r}")
        if not amount.is_finite() or amount <= 0:
            raise ValueError(f"Invalid amount: {value!r}")
        return format(amount, "f")

    async def get_shop(self) -> ShopInfo:
        """The shop of the API key and the key itself: test or live, access.
        Handy to check a key before saving it.

        Docs: https://coinspay.app/docs"""
        url = f"{self.__base_url}/shop"
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers(),
        )
        return ShopInfo(**response)

    async def get_balances(self) -> List[Balance]:
        """Balances of the shop per network and asset. Needs a live key with full access:
        test and invoices-only keys raise BadRequest.

        Docs: https://coinspay.app/docs"""
        url = f"{self.__base_url}/balances"
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers(),
        )
        return [Balance(**balance) for balance in response['balances']]

    async def get_currencies(self) -> Currencies:
        """Fiat and crypto currencies an invoice can be priced in.

        Docs: https://coinspay.app/docs/invoices"""
        url = f"{self.__base_url}/currencies"
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers(),
        )
        return Currencies(**response)

    async def create_invoice(self, amount: Union[str, int, float, Decimal], currency: str, title: Optional[str] = None,
                             reference: Optional[str] = None, description: Optional[str] = None,
                             return_url: Optional[str] = None, auto_return: Optional[bool] = None,
                             lifetime_minutes: Optional[int] = None, stablecoins_only: Optional[bool] = None,
                             buyer_pays_fee: Optional[bool] = None, buyer_pays_network: Optional[bool] = None,
                             idempotency_key: Optional[str] = None) -> Invoice:
        """Creates an invoice and returns it; send the buyer to invoice.pay_url.
        The buyer picks the coin and the network on the payment page.

        :param amount: Required. Invoice amount, e.g. "150.00".
        :param currency: Required. Fiat (USD, EUR, RUB, ...) or crypto code, see get_currencies().
        :param title: Optional. What is paid for, shown on the payment page (up to 200 chars).
        :param reference: Optional. Your order ID (up to 190 chars); find the invoice later with get_invoices(reference=...).
        :param description: Optional. Longer text for the payment page (up to 1000 chars).
        :param return_url: Optional. Where the "Back to the shop" button leads, e.g. https://t.me/your_bot.
        :param auto_return: Optional. Send the buyer to return_url right after the payment.
        :param lifetime_minutes: Optional. How long the invoice can be paid, from 15 to 43200 minutes (30 days).
        :param stablecoins_only: Optional. Offer only stablecoins (USDT, USDC, ...) on the payment page.
        :param buyer_pays_fee: Optional. Add the CoinsPay fee to the amount the buyer pays.
        :param buyer_pays_network: Optional. Add the network fee to the amount the buyer pays.
        :param idempotency_key: Optional. 8-128 printable chars, e.g. your order ID. A repeated request with the same key
            returns the same invoice instead of a second one; the same key with a different body is refused.

        Docs: https://coinspay.app/docs/invoices"""
        url = f"{self.__base_url}/invoices"
        params = {
            "amount": self.__amount(amount),
            "currency": currency,
            "title": title,
            "reference": reference,
            "description": description,
            "return_url": return_url,
            "auto_return": auto_return,
            "lifetime_minutes": lifetime_minutes,
            "stablecoins_only": stablecoins_only,
            "buyer_pays_fee": buyer_pays_fee,
            "buyer_pays_network": buyer_pays_network,
        }
        self._delete_empty_fields(params)
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers(idempotency_key),
            data=json.dumps(params, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        )
        return Invoice(**response['invoice'])

    async def get_invoice(self, invoice_id: str) -> Invoice:
        """Get an invoice with its payments. Check status, amount and reference here
        before you deliver the order: a webhook is only a hint to look.

        :param invoice_id: Invoice ID (invoice.id).

        Docs: https://coinspay.app/docs/invoices"""
        url = f"{self.__base_url}/invoices/{quote(invoice_id, safe='')}"
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers(),
        )
        return Invoice(**response['invoice'])

    async def get_invoices(self, status: Optional[str] = None, reference: Optional[str] = None,
                           limit: Optional[int] = None, cursor: Optional[str] = None) -> InvoiceList:
        """List invoices, newest first. Without the payments; get_invoice() returns them.

        :param status: Optional. open, paid, expired or cancelled.
        :param reference: Optional. Your order ID given on creation.
        :param limit: Optional. Invoices per page.
        :param cursor: Optional. next_cursor of the previous page.

        Docs: https://coinspay.app/docs/invoices"""
        url = f"{self.__base_url}/invoices"
        params = {
            "status": status,
            "reference": reference,
            "limit": str(limit) if limit is not None else None,
            "cursor": cursor,
        }
        self._delete_empty_fields(params)
        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers(),
            params=params,
        )
        return InvoiceList(**response)

    async def cancel_invoice(self, invoice_id: str) -> Invoice:
        """Cancels an open invoice. An invoice that is no longer open raises BadRequest (INVOICE_NOT_OPEN).

        :param invoice_id: Invoice ID (invoice.id).

        Docs: https://coinspay.app/docs/invoices"""
        url = f"{self.__base_url}/invoices/{quote(invoice_id, safe='')}/cancel"
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers(),
            data=b"{}",
        )
        return Invoice(**response['invoice'])

    def parse_webhook(self, body: Union[bytes, str], signature: Optional[str], tolerance: int = 300) -> WebhookEvent:
        """Checks the x-cpay-signature header of a webhook and returns the event.
        Raises BadRequest if the signature does not hold.

        Pass the raw request body, before json.loads(): the signature covers the bytes.
        Then confirm the invoice with get_invoice(event.data.invoice.id) before you deliver the order.

        :param body: Required. Raw request body.
        :param signature: Required. Value of the x-cpay-signature header.
        :param tolerance: Optional. Allowed clock difference in seconds, default 300.

        Docs: https://coinspay.app/docs/webhooks"""
        if not self.__webhook_secret:
            raise ValueError('No WebhookSecret specified')
        if isinstance(body, str):
            body = body.encode("utf-8")
        if not signature:
            raise BadRequest("[CoinsPay] Webhook signature is missing")

        timestamp = None
        signatures = []
        for piece in signature.split(","):
            key, _, value = piece.strip().partition("=")
            if key == "t":
                timestamp = value
            elif key == "v1":
                signatures.append(value)
        if (timestamp is None or not re.fullmatch(r"[0-9]{1,15}", timestamp) or not signatures
                or not all(re.fullmatch(r"[0-9a-f]{64}", item) for item in signatures)):
            raise BadRequest("[CoinsPay] Webhook signature is malformed")
        if abs(time.time() - int(timestamp)) > tolerance:
            raise BadRequest("[CoinsPay] Webhook signature is too old")

        expected = hmac.new(self.__webhook_secret.encode("utf-8"), f"{timestamp}.".encode("ascii") + body,
                            hashlib.sha256).hexdigest()
        if not any(hmac.compare_digest(expected, item) for item in signatures):
            raise BadRequest("[CoinsPay] Webhook signature does not match")
        return WebhookEvent(**json.loads(body))
