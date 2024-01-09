from AsyncPayments.requests import RequestsClient
from typing import Optional, Union
from .models import CreatePayment, CassaInfo, PayoffCreate, Balances, TickersRate, PaymentsMethods, PayoffRequest, \
                    PaymentInfo, GeneralStats

import json
import hashlib



class AsyncCrystalPay(RequestsClient):
    API_HOST: str = "https://crystalpay.io"

    def __init__(self, login: str, secret: str, salt: str) -> None:
        """
        Initialize CrystalPay API client
        :param login: Your Login
        :param secret: Your Secret
        :param salt: Your Salt
        """
        super().__init__()
        self.__login = login
        self.__secret = secret
        self.__salt = salt
        self.__headers = {
            'Content-Type': 'application/json',
        }
        self.__base_url = "https://api.crystalpay.io/v2"
        self.__post_method = "POST"
        self.__payment_name = "crystalPay"
        self.check_values()

    def check_values(self):
        if not self.__login or not self.__secret or not self.__salt:
            raise ValueError('No Secret, Login or Salt specified')

    async def get_cassa_info(self, hide_empty: Optional[bool]= False) -> CassaInfo:
        """Get cash info.

        Docs: https://docs.crystalpay.io/api/kassa/poluchenie-informacii-o-kasse

        :param hide_empty: Hide empty balances"""

        url = f'{self.__base_url}/me/info/'

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "hide_empty": hide_empty,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return CassaInfo(**response)

    async def get_balance(self) -> Balances:
        """Get cash balance.

        Docs: https://docs.crystalpay.io/api/balans/poluchenie-balansa-kassy"""

        url = f'{self.__base_url}/balance/info/'

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return Balances(**response['balances'])

    async def get_payment_methods(self) -> PaymentsMethods:
        """Get payment methods.

        Docs: https://docs.crystalpay.io/api/metody-oplaty/poluchenie-informacii-o-metodakh-oplaty"""

        url = f'{self.__base_url}/method/list/'

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return PaymentsMethods(**response['methods'])

    async def edit_payment_method(self, method: str, extra_commission_percent: Union[int, float], enabled: bool) -> bool:
        """Edit payment method

        Dosc: https://docs.crystalpay.io/api/metody-oplaty/izmenenie-nastroek-metoda-oplaty

        :param method: Payment method, for example: LZTMARKET, BITCOIN
        :param extra_commission_percent: Additional cash desk commission for payment method, in percent
        :param enabled: Enable/Disable payment method

        :return: True if successful, else exception BadRequest
        """

        url = f'{self.__base_url}/method/edit/'

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "method": method,
            "extra_commission_percent": extra_commission_percent,
            "enabled": enabled,
        }

        await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return True

    async def create_payment(
            self, amount: Union[int, float], amount_currency: Optional[str] = "RUB", required_methods: Optional[str] = None,
            type: Optional[str] = "purchase", description: Optional[str] = None, redirect_url: Optional[str] = None,
            callback_url: Optional[str] = None, extra: Optional[str] = None, payer_details: Optional[str] = None,
            lifetime: Optional[int] = 60) -> CreatePayment:
        """Generate payment url.

        Docs: https://docs.crystalpay.io/api/oplata/vystavlenie-schyota

        :param amount: Order amount.
        :param amount_currency: Currency. Default to 'RUB', for example: USD, BTC, ETH
        :param required_methods: Pre-selected payment method, for example: LZTMARKET, BITCOIN
        :param type: Invoice type. possible options: purchase, topup
        :param description: The description or purpose of the payment is displayed to the payer on the payment page, for example: Account purchase #12345678
        :param redirect_url: Redirect link after payment
        :param callback_url: Link for HTTP Callback notification after successful payment
        :param extra: Any internal data, for example: Payment ID in your system
        :param payer_details: Payer email
        :param lifetime: Invoice lifetime in minutes, maximum - 4320. Default to 60"""

        url = f'{self.__base_url}/invoice/create/'

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "amount": amount,
            "amount_currency": amount_currency,
            "required_methods": required_methods,
            "type": type,
            "description": description,
            "redirect_url": redirect_url,
            "callback_url": callback_url,
            "extra": extra,
            "payer_details": payer_details,
            "lifetime": lifetime,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return CreatePayment(**response)

    async def get_payment_info(self, invoice_id: str) -> PaymentInfo:
        """Get info about payment.

        Docs: https://docs.crystalpay.io/api/oplata/poluchenie-informacii-o-schyote

        :param invoice_id: Invoice ID"""

        url = f'{self.__base_url}/invoice/info/'

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "id": invoice_id,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return PaymentInfo(**response)

    async def create_payoff(self, amount: Union[int, float], method: str, wallet: str, subtract_from: str,
                            amount_currency: Optional[str] = None, callback_url: Optional[str] = None,
                            extra: Optional[str] = None) -> PayoffCreate:
        """Create payoff request.

        Docs: https://docs.crystalpay.io/api/vyvod/sozdanie-zayavki

        :param amount: Payoff amount, for example: 10, 0.0015
        :param amount_currency: The currency of the amount is automatically converted into the currency of the withdrawal method, for example: RUB, USD, BTC
        :param method: Payoff method, for example: LZTMARKET, BITCOIN
        :param wallet: Recipient's wallet details
        :param subtract_from: Where to write off the commission amount, possible options: balance, amount
        :param callback_url: Link for HTTP Callback notification after output is complete
        :param extra: Any internal data, for example: Payment ID in your system

        More about subtract_from:

        amount - The commission will be deducted from the withdrawal amount. The amount will be credited to your wallet.
        balance - The commission will be deducted from the balance. The exact amount will be sent to your wallet."""

        url = f'{self.__base_url}/payoff/create/'

        signature = hashlib.sha1(str.encode(f"{amount}:{method}:{wallet}:{self.__salt}")).hexdigest()

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "signature": signature,
            "amount": amount,
            "amount_currency": amount_currency,
            "method": method,
            "wallet": wallet,
            "subtract_from": subtract_from,
            "callback_url": callback_url,
            "extra": extra,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return PayoffCreate(**response)

    async def submit_payoff(self, payoff_id: str) -> PayoffRequest:
        """Submit payoff request

        Docs: https://docs.crystalpay.io/api/vyvod/podtverzhdenie-zayavki

        :param payoff_id: Payoff ID"""

        signature = hashlib.sha1(str.encode(f"{payoff_id}:{self.__salt}")).hexdigest()

        url = f"{self.__base_url}/payoff/submit/"

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "signature": signature,
            "id": payoff_id,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return PayoffRequest(**response)


    async def cancel_payoff(self, payoff_id: str) -> PayoffRequest:
        """Cancel payoff request

        Docs: https://docs.crystalpay.io/api/vyvod/otmena-zayavki

        :param payoff_id: Payoff ID"""

        signature = hashlib.sha1(str.encode(f"{payoff_id}:{self.__salt}")).hexdigest()

        url = f"{self.__base_url}/payoff/cancel/"

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "signature": signature,
            "id": payoff_id,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return PayoffRequest(**response)

    async def get_payoff(self, payoff_id: str) -> PayoffRequest:
        """Get info about payoff request

        Docs: https://docs.crystalpay.io/api/vyvod/poluchenie-informacii-o-zayavke

        :param payoff_id: Payoff ID"""

        url = f"{self.__base_url}/payoff/info/"

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "id": payoff_id,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return PayoffRequest(**response)

    async def get_tickers_list(self) -> list:
        """Get a list of available currencies

        Dosc: https://docs.crystalpay.io/api/valyuty/poluchenie-spiska-dostupnykh-valyut"""

        url = f"{self.__base_url}/ticker/list/"

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return list(response['tickers'])

    async def get_tickers_rate(self, tickers: list) -> TickersRate:
        """Get the exchange rate against RUB

        Docs: https://docs.crystalpay.io/api/valyuty/poluchenie-kursa-valyut

        :param tickers: Array of currencies, for example: [“BTC”, “LTC”]"""

        url = f"{self.__base_url}/ticker/get/"

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "tickers": tickers,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return TickersRate(**response)

    async def get_history_payments(self, page: int, items: int) -> list:
        """Get payment history

        Docs: https://docs.crystalpay.io/api/otchyoty/poluchenie-istorii-platezhei

        :param page: Page number, for example: 1, 2, 3
        :param items: Number of elements per page, maximum - 100"""

        url = f"{self.__base_url}/history/payments/"

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "page": page,
            "items": items,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return list(response['payments'])

    async def get_payoff_history(self, page: int, items: int) -> list:
        """Getting withdrawal history

        Docs: https://docs.crystalpay.io/api/otchyoty/poluchenie-istorii-vyvodov

        :param page: Page number, for example: 1, 2, 3
        :param items: Number of elements per page, maximum - 100"""

        url = f"{self.__base_url}/history/payoffs/"

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "page": page,
            "items": items,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return list(response['payoffs'])

    async def get_general_stats(self) -> GeneralStats:
        """Get general statistics

        Dosc: https://docs.crystalpay.io/api/otchyoty/poluchenie-obshei-statistiki"""

        url = f"{self.__base_url}/history/summary/"

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return GeneralStats(**response)