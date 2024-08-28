from AsyncPayments.requests import RequestsClient
from typing import Optional, Union, List
from .models import Balance, Transaction, Payout, CreatePayout, PayoutOnCreate
from urllib.parse import urlencode

import hashlib


class AsyncPayOK(RequestsClient):
    API_HOST: str = "https://payok.io/"

    def __init__(self, apiKey: str, secretKey: str, apiId: int, shopId: int) -> None:
        """
        Initialize PayOK API client
        :param apiKey: Your api key
        :param secretKey: Your secret key
        :param apiId: Your api id
        :param shopId: Your shop id
        """
        super().__init__()
        self.__apiKey = apiKey
        self.__secretKey = secretKey
        self.__apiId = apiId
        self.__shopId = shopId
        self.__base_url = "https://payok.io/api"
        self.__post_method = "POST"
        self.__payment_name = "payok"
        self.check_values()

    def check_values(self):
        if not self.__secretKey or not self.__apiKey or not self.__apiId or not self.__shopId:
            raise ValueError('No SecretKey, ApiKey, ShopID or ApiID specified')

    async def get_balance(self) -> Balance:
        """Get your balance.
        
        Docs: https://payok.io/cabinet/documentation/doc_api_balance
        """
        url = f"{self.__base_url}/balance"
        
        params = {
            "API_ID": self.__apiId,
            "API_KEY": self.__apiKey,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, data=params)
        
        return Balance(**response)

    async def get_transactions(self, payment: Optional[int] = None, 
                               offset: Optional[int] = None) -> Union[Transaction, List[Transaction]]:
        """Get list of transactions.
        
        Docs: https://payok.io/cabinet/documentation/doc_api_transaction
        
        :param payment: Optional. Payment ID in your system.
        :param offset: Optional. Indentation, skipping the specified number of lines.
        """
        url = f"{self.__base_url}/transaction"
        
        params = {
            "API_ID": self.__apiId,
            "API_KEY": self.__apiKey,
            "shop": self.__shopId,
            "payment": payment,
            "offset": offset,
        }
        self._delete_empty_fields(params)
        response = await self._request(self.__payment_name, self.__post_method, url, data=params)
        if payment:
            return Transaction(**response['1'])
        
        return [Transaction(**transaction) for transaction in response.values()]
        
    async def get_payouts(self, payout_id: Optional[int] = None, offset: Optional[int] = None):
        """Get list of payouts.
        
        Docs: https://payok.io/cabinet/documentation/doc_api_payout
        
        :param payout_id: Payment ID in the Payok system.
        :param offset: Indentation, skipping the specified number of lines.
        """
        url = f"{self.__base_url}/payout"
        params = {
            "API_ID": self.__apiId,
            "API_KEY": self.__apiKey,
            "payout_id": payout_id,
            "offset": offset,
        }
        self._delete_empty_fields(params)
        response = await self._request(self.__payment_name, self.__post_method, url, data=params)
        
        if payout_id:
            return Payout(**response['1'])
        
        return [Payout(**payout) for payout in response.values()]

    async def create_payout(
        self,
        amount: float,
        method: str,
        reciever: str,
        commission_type: str,
        sbp_bank: Optional[str] = None,
        webhook_url: Optional[str] = None
        ) -> CreatePayout:
        """
        Create payout.
        
        Docs: https://payok.io/cabinet/documentation/doc_api_payout_create
        
        :param amount: Payment amount.
        :param method: Special value of the payment method, list of values.
        :param reciever: Details of the payee.
        :param commission_type: The bank for the payment of SBP.
        :param sbp_bank: Type of commission calculation: balance - Commission from the balance sheet, payment - Commission from the payment.
        :param webhook_url: URL for sending a Webhook when the payment status changes.
        """
        url = f"{self.__base_url}/payout_create"
        params = {
            "API_ID": self.__apiId,
            "API_KEY": self.__apiKey,
            "amount": amount,
            "method": method,
            "reciever": reciever,
            "commission_type": commission_type,
            "sbp_bank": sbp_bank,
            "webhook_url": webhook_url
        }
        self._delete_empty_fields(params)
        response = await self._request(self.__payment_name, self.__post_method, url, data=params)
        
        return CreatePayout(remain_balance=response['remain_balance'], payout=PayoutOnCreate(**response['data']))
        
    
    async def create_pay(
        self,
        amount: float,
        payment: Union[int, str],
        currency: Optional[str] = "RUB",
        desc: Optional[str] = 'Description',
        email: Optional[str] = None,
        success_url: Optional[str] = None,
        method: Optional[str] = None,
        lang: Optional[str] = None,
        custom: Optional[str] = None
    ) -> str:
        """Create payform url.
        
        Docs: https://payok.io/cabinet/documentation/doc_payform.php
        
        :param payment: Order number, unique in your system, up to 16 characters. (a-z0-9-_)
        :param amount : Order amount.
        :param currency : ISO 4217 currency. Default is "RUB".
        :param desc : Product name or description.
        :param email : Email Buyer mail. Defaults to None.
        :param success_url: Link to redirect after payment.
        :param method: Payment method
        :param lang: Interface language. RU or EN
        :param custom: Parameter that you want to pass in the notification.
        """

        params = {
            'amount': amount,
            'payment': payment,
            'shop': self.__shopId,
            'currency': currency,
            'desc': desc,
            'email': email,
            'success_url': success_url,
            'method': method,
            'lang': lang,
            'custom': custom
        }

        self._delete_empty_fields(params)

        sign_params = '|'.join(map(
            str,
            [amount, payment, self.__shopId, currency, desc, self.__secretKey]
        )).encode('utf-8')
        sign = hashlib.md5(sign_params).hexdigest()
        params['sign'] = sign

        url = f'{self.API_HOST}/pay?' + urlencode(params)
        return url
