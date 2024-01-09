from AsyncPayments.requests import RequestsClient
from typing import Optional, Union
from .models import Balance, CreatePayment, Payment, CreateWithdrawRequest, CancelWithdrawRequest, WithdrawRequest

import time
import secrets
import random


class AsyncRuKassa(RequestsClient):
    API_HOST: str = "https://ruks.pro"

    def __init__(self, api_token: str, shop_id: int, email: str, password: str) -> None:
        """
        Initialize RuKassa API client
        :param api_token: Your RuKassa API-Token
        :param shop_id: Your RuKassa ShopID
        :param email: Your Email, which you pointed to RuKassa
        :param password: Your Password, which you pointed to RuKassa
        """
        super().__init__()
        self.__token = api_token
        self.__shop_id = shop_id
        self.__email = email
        self.__password = password
        self.__base_url = "https://lk.rukassa.is/api/v1"
        self.__post_method = "POST"
        self.__payment_name = "ruKassa"
        self.check_values()

    def check_values(self):
        if not self.__token or not self.__shop_id or not self.__email or not self.__password:
            raise ValueError('No Api-Token, ShopID, Email or Password specified')

    async def get_balance(self) -> Balance:
        """Get User Balance

        :return: Balance Object"""

        url = f'{self.__base_url}/getBalance'

        params = {
            "email": self.__email,
            "password": self.__password,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, data=params)

        return Balance(**response)

    def __get_random_string(self):
        return f'{time.time()}_{secrets.token_hex(random.randint(5, 10))}'

    async def create_payment(self, amount: Union[int, float], currency: Optional[str] = "RUB",
                             method: Optional[str] = None, data: Optional[str] = None,
                             orderId: Optional[int] = None) -> CreatePayment:
        """Create a payment

        :param amount: Amount of payment.
        :param currency: Optional. In what currency are you specifying the amount parameter? Default RUB. Currencies: RUB, USD
        :param method: Optional. Payment method, if you want payment to be made through a specific method. Methods: card, card_byn, card_kzt, card_uah, card_uzs, qiwi, yandexmoney, payeer, crypta, sbp,
        :param data: Optional. String sent to the server along with a notification of a successful payment.
        :param orderId: Optional. A unique payment number in your system. If not specified, a random string will be generated.

        :return: CreatePayment object
        """

        url = f'{self.__base_url}/create'

        if not orderId:
            orderId = self.__get_random_string()

        params = {
            "shop_id": self.__shop_id,
            "order_id": orderId,
            "amount": amount,
            "token": self.__token,
            "data": data,
            "method": method,
            "currency": currency,
        }

        for key, value in params.copy().items():
            if value is None:
                params.pop(key)

        response = await self._request(self.__payment_name, self.__post_method, url, data=params)

        return CreatePayment(**response)

    async def get_info_payment(self, id: int) -> Payment:
        """
        Get payment information

        :param id: Transaction (entry) number in our system.

        :return: Payment object
        """

        url = f"{self.__base_url}/getPayInfo"

        params = {
            "id": id,
            "shop_id": self.__shop_id,
            "token": self.__token,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, data=params)

        return Payment(**response)

    async def create_withdraw(self, way: str, wallet: str, amount: Union[float, int], orderId: str = None,
                              check_from: Optional[str] = "BASE_RUB", who_fee: Optional[int] = 0,
                              bank: Optional[int] = None) -> CreateWithdrawRequest:
        """
        Create withdraw request

        :param way: Payment system for withdrawal. Systems: CARD, QIWI, YOOMONEY, USDT, SBP.
        :param wallet: The number of the wallet or card where the funds will be sent.
        :param amount: Amount to withdraw.
        :param orderId: ID in the merchant system.
        :param check_from: Account for debiting funds. Default: BASE_RUB. (BASE_RUB, BASE_USD).
        :param who_fee: Where to write off the commission. Default: 0. (0 - from account, 1 - from balance).
        :param bank: Only for SBP. Bank number.

        :return: CreateWithdrawRequest object
        """

        url = f"{self.__base_url}/createWithdraw"

        params = {
            "email": self.__email,
            "password": self.__password,
            "way": way,
            "wallet": wallet,
            "amount": amount,
            "order_id": orderId,
            "from": check_from,
            "who_fee": who_fee,
            "bank": bank,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, data=params)

        return CreateWithdrawRequest(**response)

    async def cancel_withdraw(self, id: int) -> CancelWithdrawRequest:
        """
        Cancel withdraw request

        :param id: Payment ID in our system.

        :return: CancelWithdrawRequest object
        """

        url = f"{self.__base_url}/cancelWithdraw"

        params = {
            "email": self.__email,
            "password": self.__password,
            "id": id,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, data=params)

        return CancelWithdrawRequest(**response)

    async def get_info_withdraw(self, id: int) -> WithdrawRequest:
        """
        Get info about withdraw request

        :param id: The number of the operation (withdrawal) in our system.

        :return: WithdrawRequest object
        """

        url = f"{self.__base_url}/getWithdrawInfo"

        params = {
            "token": self.__token,
            "shop_id": self.__shop_id,
            "id": id,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, data=params)

        return WithdrawRequest(**response)
