from AsyncPayments.requests import RequestsClient
from .models import Order, OrderMethod, WithdrawalMethod, CreateWithdrawalInfo, Withdrawal, Balance
from typing import Optional, Union, List
from urllib.parse import urlencode

import hashlib


class AsyncAaio(RequestsClient):
    API_HOST: str = "https://aaio.so"

    def __init__(self,
            apikey: str,
            shopid: Optional[str] = None,
            secretkey: Optional[str] = None,
            ) -> None:
        '''
        Initialize Aaio API client
        :param apikey: Your API Key
        :param shopid: Your Shop ID
        :param secretkey: Your Secretkey №1
        '''
        super().__init__()
        self.__api_key = apikey
        self.__shop_id = shopid
        self.__secret_key = secretkey
        self.__headers = {
            "Accept": "application/json",
            "X-Api-Key": self.__api_key
        }
        self.__post_method = "POST"
        self.__payment_name = "aaio"
        self.check_values()

    def check_values(self):
        if not self.__secret_key or not self.__shop_id:
            raise ValueError('No SecretKey or ShopID specified')

    def __create_sign(self, amount: Union[float, int], currency: str, order_id: str) -> str:
        params_for_sing = ':'.join(map(
            str,
            [self.__shop_id, amount, currency, self.__secret_key, order_id])
        )

        return hashlib.sha256(params_for_sing.encode('utf-8')).hexdigest()

    async def create_payment_url(
            self,
            amount: float,
            order_id: Union[int, str],
            currency: Optional[str] = 'RUB',
            method: Optional[str] = None,
            desc: Optional[str] = None,
            email: Optional[str] = None,
            lang: Optional[str] = None,
            referal: Optional[str] = None,
            us_key: Optional[str] = None,
    ) -> str:

        """Generate payment url.

        Docs: https://wiki.aaio.so/priem-platezhei/sozdanie-zakaza

        :param amount: Order amount.
        :param order_id: Order number, which unique in your system, up to 16 characters, without spaces (aA-zZ, 0-9, :, -, _, [, ] , |)
        :param currency: Currency. Default to 'RUB' (RUB, UAH, EUR, USD)
        :param method: Payment Aaio system code name
        :param desc: Order description
        :param email: Buyer mail
        :param lang: Interface language. Default to 'ru' (ru, en)
        :param referal: Referral code
        :param us_key: Parameter that you want to get in the notification"""

        params = {
            'merchant_id': self.__shop_id,
            'amount': amount,
            'order_id': order_id,
            'currency': currency,
            'method': method,
            'desc': desc,
            'email': email,
            'lang': lang,
            'referal': referal,
            'us_key': us_key,
            'sign': self.__create_sign(amount, currency, order_id),
        }

        self._delete_empty_fields(params)
        
        headers = self.__headers
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        response = await self._request(self.__payment_name, self.__post_method, f"{self.API_HOST}/merchant/get_pay_url", headers=headers, data=urlencode(params))
        
        return response['url']

    async def get_balance(self) -> Balance:
        """Get available, referal and hold balance.

        Docs: https://wiki.aaio.so/api/poluchenie-balansa"""

        url = f'{self.API_HOST}/api/balance'

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)

        return Balance(**response)

    async def get_order_info(self,
                           order_id: Union[int, str]
                           ) -> Order:

        """Get information about an order by OrderID.

        Docs: https://wiki.aaio.so/api/informaciya-o-zakaze

        :param order_id: OrderID (in your system)"""

        url = f'{self.API_HOST}/api/info-pay'

        params = {
            'merchant_id': self.__shop_id,
            'order_id': order_id,
        }

        self._delete_empty_fields(params)

        response = await self._request(self.__payment_name, self.__post_method, url, data=params, headers=self.__headers)

        return Order(**response)

    async def get_withdrawal_methods(self,
                                method: Optional[str] = None
                                ) -> Union[List[WithdrawalMethod], WithdrawalMethod]:

        """Get available methods for withdrawal.

        If method is None -> return dict with all methods.

        If a specific method -> return info about only this method.

        Docs: https://wiki.aaio.so/api/dostupnye-metody-dlya-vyvoda-sredstv

        :param method: Specific method. Default is None"""

        url = f'{self.API_HOST}/api/methods-payoff'

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)

        if method is not None:
            return WithdrawalMethod(**response['list'][method])
        return [WithdrawalMethod(**method) for method in response["list"].values()]

    async def get_order_methods(self,
                           method: Optional[str] = None
                           ) -> Union[List[OrderMethod], OrderMethod]:

        """Get available methods for order.

        If method is None -> return dict with all methods.

        If a specific method -> return info about only this method.

        Docs: https://wiki.aaio.so/api/dostupnye-metody-dlya-sozdaniya-zakaza

        :param method: Specific method. Default is None"""

        url = f'{self.API_HOST}/api/methods-pay'

        params = {
            'merchant_id': self.__shop_id,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, data=params, headers=self.__headers)

        if method is not None:
            return OrderMethod.model_validate(response['list'][method])
        return [OrderMethod(**method) for method in response["list"].values()]

    async def get_withdrawal_info(self,
                                my_id: Union[int, str],
                                ) -> Withdrawal:

        """Get information about a withdrawal by WithdrawalID.

        Docs: https://wiki.aaio.so/api/informaciya-o-zayavke-na-vyvod-sredstv

        :param my_id: WithdrawalID (in your system)"""

        url = f'{self.API_HOST}/api/info-payoff'

        params = {
            'my_id': my_id,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, data=params, headers=self.__headers)

        return Withdrawal(**response)

    async def create_withdrawal(self,
                               my_id: Union[int, str],
                               method: str,
                               amount: float,
                               wallet: str,
                               commission_type: Optional[int] = 0
                               ) -> CreateWithdrawalInfo:

        """Create withdrawal.

        Docs: https://wiki.aaio.so/api/vyvod-sredstv

        :param my_id: WithdrawalID (in your system)
        :param method: Specific method for withdrawal
        :param amount: Withdrawal amount
        :param wallet: Wallet or number for withdrawal (Without +, " ", and separators)
        :param commission_type: Withdrawal commission type. Default to 0 (from the payment amount)"""

        url = f'{self.API_HOST}/api/create-payoff'

        params = {
            'my_id': my_id,
            'method': method,
            'amount': amount,
            'wallet': wallet,
            'commission_type': commission_type,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, data=params, headers=self.__headers)

        return CreateWithdrawalInfo(**response)