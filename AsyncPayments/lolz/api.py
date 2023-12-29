import json
import random
import math
import time
import secrets

from typing import Optional
from AsyncPayments.requests import RequestsClient
from .models import *


class AsyncLolzteamMarketPayment(RequestsClient):
    API_HOST = "https://lzt.market"

    def __init__(self, token: str, user_id: int, user_nickname: str) -> None:
        """
        Initialize LolzteamMarket API client
        :param token: Your Lolzteam Token
        :param user_id: Your Lolzteam User ID
        :param user_nickname: Your Lolzteam User nickname
        """
        super().__init__()
        self.__token = token
        self.__user_id = user_id
        self.__nickname = user_nickname
        self.__headers = {
            'Authorization': f'Bearer {self.__token}',
            "Accept": "application/json"
        }
        self.__base_url = "https://api.lzt.market"

    async def get_me(self) -> User:
        """Get info about your account on Zelenka (Lolzteam).

        Docs: https://lzt-market.readme.io/reference/marketprofilesettingsgetinfo"""

        if not self.__token :
            raise Exception('Не указан Token')

        url = f'{self.__base_url}/me'


        response = await self._request("lolz", "GET", url, headers=self.__headers)

        return User(**response['user'])

    def __get_random_string(self):
        return f'{time.time()}_{secrets.token_hex(random.randint(5, 10))}'

    def get_payment_link(self, amount: Union[int, float], comment: Optional[str] = None, is_hold: Optional[bool] = False,
                         is_amount_ceiling: Optional[bool] = False) -> str:
        """Get a link to transfer funds to the Lolzteam market.

        :param amount: Amount to transfer
        :param comment: Comment on the translation. If not specified: a random unique set of characters is generated.
        :param is_hold: If True: The page will have funds holding enabled by default. The user will be able to turn it off. *If you use this link for payment: ask your users not to enable hold!!! Defaults to False
        :param is_amount_ceiling: If True: The transfer amount will be rounded up. Defaults to False

        :return: Link to transfer (String)"""

        if not self.__nickname:
            raise Exception('Не указан Nickname')

        if is_amount_ceiling:
            amount = math.ceil(amount)

        if not comment:
            comment = self.__get_random_string()

        return f'https://lzt.market/balance/transfer?username={self.__nickname}&hold={int(is_hold)}&amount={amount}&comment={comment}'

    async def get_history_payments(self, type: Optional[str] = None, pmin: Optional[int] = None,
                                   pmax: Optional[int] = None, page: Optional[int] = 1,
                                   operation_id_lt: Optional[int] = None, receiver: Optional[str] = None,
                                   sender: Optional[str] = None, startDate: Optional[str] = None,
                                   endDate: Optional[str] = None, wallet: Optional[str] = None,
                                   comment: Optional[str] = None, is_hold: Optional[bool] = None,
                                   show_payment_stats: Optional[bool] = None
                                   ) -> Payments:
        """Displays list of your payments.

        Docs: https://lzt-market.readme.io/reference/paymentslisthistory

        :param type: Optional. Type of operation. It can only be: "income", "cost", "refilled_balance", "withdrawal_balance", "paid_item", "sold_item", "money_transfer", "receiving_money", "internal_purchase", "claim_hold".
        :param pmin: Optional. Minimal price of account (Inclusive).
        :param pmax: Optional. Maximum price of account (Inclusive).
        :param page: Optional. The number of the page to display results from.
        :param operation_id_lt: Optional. ID of the operation from which the result begins.
        :param receiver: Optional. Username of user, which receive money from you.
        :param sender: Optional. Username of user, which sent money to you.
        :param startDate: Optional. Start date of operation (RFC 3339 date format).
        :param endDate: Optional. End date of operation (RFC 3339 date format).
        :param wallet: Optional. Wallet, which used for money payouts.
        :param comment: Optional. Comment for money transfers.
        :param is_hold: Optional. Display hold operations.
        :param show_payment_stats: Optional. Display payment stats for selected period (outgoing value, incoming value)."""

        if not self.__token or not self.__user_id:
            raise Exception('Не указан Token или User ID')

        url = f'{self.__base_url}/user/{self.__user_id}/payments'

        params = {
            "type": type,
            "pmin": pmin,
            "pmax": pmax,
            "page": page,
            "operation_id_lt": operation_id_lt,
            "receiver": receiver,
            "sender": sender,
            "startDate": startDate,
            "endDate": endDate,
            "wallet": wallet,
            "comment": comment,
            "is_hold": is_hold,
            "show_payment_stats": show_payment_stats
        }

        for key, value in params.copy().items():
            if isinstance(value, bool):
                params[key] = str(value).lower()
            if value is None:
                del params[key]

        response = await self._request("lolz", "GET", url, headers=self.__headers, data=json.dumps(params))

        return Payments(**response)

    async def check_status_payment(self, pay_amount: int, comment: str) -> bool:
        """Displays whether the transfer is paid or not.

        :param pay_amount: The amount indicated in the transaction.
        :param comment: Comment indicated in the transaction.

        :return: True if payment has been received. Otherwise False"""

        if not self.__token or not self.__user_id:
            raise Exception('Не указан Token или User ID')

        payments = (await self.get_history_payments(type="receiving_money")).payments

        for payment in payments.values():
            if 'Перевод денег от' in payment['label']['title'] and pay_amount == payment['incoming_sum'] and comment == \
                    payment['data']['comment']:
                return True

        return False