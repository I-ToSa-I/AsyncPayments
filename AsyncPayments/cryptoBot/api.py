from AsyncPayments.requests import RequestsClient
from typing import Optional, Union, List

from .models import Invoice, MeInfo, Transfer, Balance, Check, ExchangeRate, Currency


class AsyncCryptoBot(RequestsClient):
    API_HOST: str = "https://t.me/Cryptobot"

    def __init__(self, token: str, is_testnet: bool = False) -> None:
        """
        Initialize CryptoBot API client
        :param token: Your Token
        :param is_testnet: Optional. True - Testnet is on. False - Testnet is off. Default to False.
        """
        super().__init__()
        self.__token = token
        self.__headers = {
            'Crypto-Pay-API-Token': self.__token,
        }
        if is_testnet:
            self.__base_url = "https://testnet-pay.crypt.bot/api"
        else:
            self.__base_url = "https://pay.crypt.bot/api"
        self.__post_method = "POST"
        self.__payment_name = "cryptoBot"
        self.check_values()

    def check_values(self):
        if not self.__token:
            raise ValueError('No Token specified')

    async def get_me(self) -> MeInfo:
        """Use this method to test your app's authentication token. Requires no parameters. On success, returns basic information about an app.

        Docs: https://help.crypt.bot/crypto-pay-api#getMe"""

        url = f'{self.__base_url}/getMe/'

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)

        return MeInfo(**response['result'])

    async def create_invoice(self, amount: Union[int, float], currency_type: Optional[str] = None,
                             asset: Optional[str] = None, fiat: Optional[str] = None,
                             accepted_assets: Optional[list] = None, description: Optional[str] = None,
                             hidden_message: Optional[str] = None, paid_btn_name: Optional[str] = None,
                             paid_btn_url: Optional[str] = None, payload: Optional[str] = None,
                             allow_comments: Optional[bool] = True, allow_anonymous: Optional[bool] = True,
                             expires_in: Optional[int] = 3600) -> Invoice:
        """Use this method to create a new invoice.

        Docs: https://help.crypt.bot/crypto-pay-api#createInvoice

        :param amount: Amount of the invoice in float. For example: 125.50
        :param currency_type: Optional. Type of the price, can be “crypto” or “fiat”. Defaults to crypto.
        :param asset: Optional. Required if currency_type is “crypto”. Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC”.
        :param fiat: Optional. Required if currency_type is “fiat”. Fiat currency code. Supported fiat currencies: “USD”, “EUR”, “RUB”, “BYN”, “UAH”, “GBP”, “CNY”, “KZT”, “UZS”, “GEL”, “TRY”, “AMD”, “THB”, “INR”, “BRL”, “IDR”, “AZN”, “AED”, “PLN” and “ILS".
        :param accepted_assets: Optional. List of cryptocurrency alphabetic codes separated comma. Assets which can be used to pay the invoice. Available only if currency_type is “fiat”. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet). Defaults to all currencies.
        :param description: Optional. Description for the invoice. User will see this description when they pay the invoice. Up to 1024 characters.
        :param hidden_message: Optional. Text of the message which will be presented to a user after the invoice is paid. Up to 2048 characters.
        :param paid_btn_name: Optional. Label of the button which will be presented to a user after the invoice is paid. Supported names:
viewItem – “View Item”
openChannel – “View Channel”
openBot – “Open Bot”
callback – “Return”
        :param paid_btn_url: Optional. Required if paid_btn_name is specified. URL opened using the button which will be presented to a user after the invoice is paid. You can set any callback link (for example, a success link or link to homepage). Starts with https or http.
        :param payload: Optional. Any data you want to attach to the invoice (for example, user ID, payment ID, ect). Up to 4kb.
        :param allow_comments: Optional. Allow a user to add a comment to the payment. Defaults to True.
        :param allow_anonymous: Optional. Allow a user to pay the invoice anonymously. Defaults to True.
        :param expires_in: Optional. You can set a payment time limit for the invoice in seconds. Values between 1-2678400 are accepted. Defaults to 3600
        """

        if allow_comments is True:
            allow_comments = "true"
        else:
            allow_comments = "false"
            
        if allow_anonymous is True:
            allow_anonymous = "true"
        else:
            allow_anonymous = "false"

        url = f'{self.__base_url}/createInvoice/'

        if accepted_assets and type(accepted_assets) == list:
            accepted_assets = ",".join(map(str, accepted_assets))

        params = {
            "asset": asset,
            "amount": amount,
            "description": description,
            "hidden_message": hidden_message,
            "paid_btn_name": paid_btn_name,
            "paid_btn_url": paid_btn_url,
            "payload": payload,
            "allow_comments": allow_comments,
            "allow_anonymous": allow_anonymous,
            "expires_in": expires_in,
            "fiat": fiat,
            "currency_type": currency_type,
            "accepted_assets": accepted_assets,
        }

        self._delete_empty_fields(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers,
                                       params=params)

        return Invoice(**response['result'])

    async def delete_invoice(self, invoice_id: int) -> bool:
        """Use this method to delete invoices created by your app. Returns True on success.

        Docs: https://help.crypt.bot/crypto-pay-api#deleteInvoice

        :param invoice_id: Invoice ID"""

        url = f'{self.__base_url}/deleteInvoice/'
        params = {
            "invoice_id": invoice_id,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers,
                                       params=params)

        return bool(response['result'])

    async def create_check(self, amount: Union[float, int], asset: str) -> Check:
        """Use this method to create a new check.

        Docs: https://help.crypt.bot/crypto-pay-api#createCheck

        :param amount: Amount of the invoice in float. For example: 125.50
        :param asset: Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet).
        """


        url = f'{self.__base_url}/createCheck/'

        params = {
            "amount": amount,
            "asset": asset,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers,
                                       params=params)

        return Check(**response['result'])

    async def delete_check(self, check_id: int) -> bool:
        """Use this method to delete checks created by your app. Returns True on success.

        Docs: https://help.crypt.bot/crypto-pay-api#deleteCheck

        :param check_id: Check ID"""

        url = f'{self.__base_url}/deleteCheck/'

        params = {
            "check_id": check_id,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers,
                                       params=params)

        return bool(response['result'])

    async def transfer(self, user_id: int, asset: str, amount: Union[float, int], spend_id: str,
                       comment: Optional[str] = None, disable_send_notification: Optional[bool] = False) -> Transfer:
        """Use this method to send coins from your app's balance to a user. This method must first be enabled in the security settings of your app. Open @CryptoBot (@CryptoTestnetBot for testnet), go to CryptoPay → MyApps, choose an app, then go to Security -> Transfers... and tap Enable.

        Docs: https://help.crypt.bot/crypto-pay-api#transfer

        :param user_id: User ID in Telegram. User must have previously used @CryptoBot (@CryptoTestnetBot for testnet).
        :param asset: Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet).
        :parameter amount: Amount of the transfer in float. The minimum and maximum amount limits for each of the supported assets roughly correspond to 1-25000 USD. Use get_exchange_rates() to convert amounts. For example: 125.50
        :param spend_id: Random UTF-8 string unique per transfer for idempotent requests. The same spend_id can be accepted only once from your app. Up to 64 symbols.
        :param comment: Optional. Comment for the transfer. Users will see this comment in the notification about the transfer. Up to 1024 symbols.
        :param disable_send_notification: Optional. Pass true to not send to the user the notification about the transfer. Defaults to false.
        """

        url = f'{self.__base_url}/transfer/'

        params = {
            "user_id": user_id,
            "asset": asset,
            "amount": amount,
            "spend_id": spend_id,
            "comment": comment,
            "disable_send_notification": disable_send_notification,
        }

        self._delete_empty_fields(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers,
                                       params=params)

        return Transfer(**response['result'])

    async def get_invoices(self, asset: Optional[str] = None, fiat: Optional[str] = None,
                           invoice_ids: Optional[list] = None, status: Optional[str] = None,
                           offset: Optional[int] = None, count: Optional[int] = None) -> Union[Invoice, List[Invoice]]:
        """Use this method to get invoices created by your app.

        Docs: https://help.crypt.bot/crypto-pay-api#getInvoices

        :param asset: Optional. Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet). Defaults to all currencies.
        :param fiat: Optional. Fiat currency code. Supported fiat currencies: “USD”, “EUR”, “RUB”, “BYN”, “UAH”, “GBP”, “CNY”, “KZT”, “UZS”, “GEL”, “TRY”, “AMD”, “THB”, “INR”, “BRL”, “IDR”, “AZN”, “AED”, “PLN” and “ILS". Defaults to all currencies.
        :param invoice_ids: Optional. List of invoice IDs.
        :param status: Optional. Status of invoices to be returned. Available statuses: “active” and “paid”. Defaults to all statuses.
        :param offset: Optional. Offset needed to return a specific subset of invoices. Defaults to 0.
        :param count: Optional. Number of invoices to be returned. Values between 1-1000 are accepted. Defaults to 100.
        """

        url = f"{self.__base_url}/getInvoices"

        if invoice_ids and type(invoice_ids) == list:
            invoice_ids = ",".join(map(str, invoice_ids))

        params = {
            "asset": asset,
            "invoice_ids": invoice_ids,
            "fiat": fiat,
            "status": status,
            "offset": offset,
            "count": count,
        }

        self._delete_empty_fields(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers,
                                       params=params)

        if len(response["result"]["items"]) > 0:
            if invoice_ids and isinstance(invoice_ids, int):
                return Invoice(**response["result"]["items"][0])
            return [Invoice(**invoice) for invoice in response["result"]["items"]]

    async def get_transfers(self, asset: Optional[str] = None, transfer_ids: Optional[list] = None,
                            offset: Optional[int] = None, count: Optional[int] = None) -> Union[Transfer, List[Transfer]]:
        """Use this method to get transfers created by your app.

        Docs: https://help.crypt.bot/crypto-pay-api#getTransfers

        :param asset: Optional. Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet). Defaults to all currencies.
        :param transfer_ids: Optional. List of transfer IDs.
        :param offset: Optional. Offset needed to return a specific subset of transfers. Defaults to 0.
        :param count: Optional. Number of transfers to be returned. Values between 1-1000 are accepted. Defaults to 100.
        """
        url = f"{self.__base_url}/getTransfers"

        if transfer_ids and type(transfer_ids) == list:
            transfer_ids = ",".join(map(str, transfer_ids))

        params = {
            "asset": asset,
            "transfer_ids": transfer_ids,
            "offset": offset,
            "count": count,
        }

        self._delete_empty_fields(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers,
                                       params=params)

        if len(response["result"]["items"]) > 0:
            if transfer_ids and isinstance(transfer_ids, int):
                return Transfer(**response["result"]["items"][0])
            return [Transfer(**transfer) for transfer in response["result"]["items"]]

    async def get_checks(self, asset: Optional[str] = None, check_ids: Optional[list] = None,
                         status: Optional[str] = None, offset: Optional[int] = None,
                         count: Optional[int] = None) -> Union[Check, List[Check]]:
        """Use this method to get checks created by your app.

        Docs: https://help.crypt.bot/crypto-pay-api#getChecks

        :param asset: Optional. Cryptocurrency alphabetic code. Supported assets: “USDT”, “TON”, “BTC”, “ETH”, “LTC”, “BNB”, “TRX” and “USDC” (and “JET” for testnet). Defaults to all currencies.
        :param check_ids: Optional. List of check IDs.
        :param status: Optional. Status of check to be returned. Available statuses: “active” and “activated”. Defaults to all statuses.
        :param offset: Optional. Offset needed to return a specific subset of check. Defaults to 0.
        :param count: Optional. Number of check to be returned. Values between 1-1000 are accepted. Defaults to 100.
        """
        url = f"{self.__base_url}/getChecks"

        if check_ids and type(check_ids) == list:
            check_ids = ",".join(map(str, check_ids))

        params = {
            "asset": asset,
            "check_ids": check_ids,
            "status": status,
            "offset": offset,
            "count": count,
        }

        self._delete_empty_fields(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers,
                                       params=params)

        if len(response["result"]["items"]) > 0:
            if check_ids and isinstance(check_ids, int):
                return Check(**response["result"]["items"][0])
            return [Check(**check) for check in response["result"]["items"]]

    async def get_balance(self) -> List[Balance]:
        """Use this method to get balances of your app.

        Docs: https://help.crypt.bot/crypto-pay-api#getBalance"""
        url = f"{self.__base_url}/getBalance"
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)

        return [Balance(**balance) for balance in response["result"]]

    async def get_exchange_rates(self) -> List[ExchangeRate]:
        """Use this method to get exchange rates of supported currencies.

        Docs: https://help.crypt.bot/crypto-pay-api#getExchangeRates"""
        url = f"{self.__base_url}/getExchangeRates"
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)

        return [ExchangeRate(**rate) for rate in response["result"]]

    async def get_currencies(self) -> List[Currency]:
        """Use this method to get a list of supported currencies.

        Docs: https://help.crypt.bot/crypto-pay-api#getCurrencies"""
        url = f"{self.__base_url}/getCurrencies"

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)

        return [Currency(**currency) for currency in response["result"]]