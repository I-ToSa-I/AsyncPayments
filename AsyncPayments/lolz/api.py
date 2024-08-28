from AsyncPayments.requests import RequestsClient
from typing import Optional, Union
from .models import User, Payments
from AsyncPayments.exceptions import MissingScopeError

import json
import random
import math
import time
import secrets
import base64


class AsyncLolzteamMarketPayment(RequestsClient):
    API_HOST: str = "https://lzt.market"

    def __init__(self, token: str) -> None:
        """
        Initialize LolzteamMarket API client
        :param token: Your Lolzteam Token
        """
        super().__init__()
        self.__token = token
        jwt_payload = json.loads(
            base64.b64decode(token.split(".")[1] + "==").decode("utf-8")
        )
        self.__user_id = jwt_payload["sub"]
        if jwt_payload.get("scope"):
            if "market" not in jwt_payload["scope"]:
                raise MissingScopeError(
                    '"Market" scope is not provided in your token. You need to recreate token with "Market" scope.'
                )
        self.__headers = {
            "Authorization": f"Bearer {self.__token}",
            "Accept": "application/json",
        }
        self.__base_url = "https://api.lzt.market"
        self.__get_method = "GET"
        self.__payment_name = "lolz"

    async def get_me(self) -> User:
        """Get info about your account on Zelenka (Lolzteam).

        Docs: https://lzt-market.readme.io/reference/marketprofilesettingsgetinfo"""

        url = f"{self.__base_url}/me"

        response = await self._request(
            self.__payment_name, self.__get_method, url, headers=self.__headers
        )

        return User(**response["user"])

    def __get_random_string(self):
        return f"{time.time()}_{secrets.token_hex(random.randint(5, 10))}"

    def get_payment_link(
        self,
        amount: Union[int, float],
        comment: Optional[str] = None,
        is_hold: Optional[bool] = False,
        is_amount_ceiling: Optional[bool] = False,
    ) -> str:
        """Get a link to transfer funds to the Lolzteam market.

        :param amount: Amount to transfer
        :param comment: Comment on the translation. If not specified: a random unique set of characters is generated.
        :param is_hold: If True: The page will have funds holding enabled by default. The user will be able to turn it off. *If you use this link for payment: ask your users not to enable hold!!! Defaults to False
        :param is_amount_ceiling: If True: The transfer amount will be rounded up. Defaults to False

        :return: Link to transfer (String)"""

        if is_amount_ceiling:
            amount = math.ceil(amount)

        if not comment:
            comment = self.__get_random_string()

        return f"https://lzt.market/balance/transfer?user_id={self.__user_id}&hold={int(is_hold)}&amount={amount}&comment={comment}"

    async def get_history_payments(
        self,
        operation_type: Optional[str] = None,
        pmin: Optional[int] = None,
        pmax: Optional[int] = None,
        page: Optional[int] = 1,
        operation_id_lt: Optional[int] = None,
        receiver: Optional[str] = None,
        sender: Optional[str] = None,
        startDate: Optional[str] = None,
        endDate: Optional[str] = None,
        wallet: Optional[str] = None,
        comment: Optional[str] = None,
        is_hold: Optional[bool] = None,
        show_payment_stats: Optional[bool] = None,
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
        :param show_payment_stats: Optional. Display payment stats for selected period (outgoing value, incoming value).
        """

        url = f"{self.__base_url}/user/{self.__user_id}/payments"

        params = {
            "type": operation_type,
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
            "show_payment_stats": show_payment_stats,
        }

        self._delete_empty_fields(params)

        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
            params=params,
        )
        if type(response.get("payments")) is list and len(response.get("payments")) == 0:
            response["payments"] = {}
        return Payments(**response)

    async def check_status_payment(self, pay_amount: int, comment: str) -> bool:
        """Displays whether the transfer is paid or not.

        :param pay_amount: The amount indicated in the transaction.
        :param comment: Comment indicated in the transaction.

        :return: True if payment has been received. Otherwise False"""
        payments = (
            await self.get_history_payments(
                operation_type="receiving_money",
                comment=comment,
                pmin=pay_amount,
                pmax=pay_amount,
            )
        ).payments
        if payments.values():
            return True
        return False
