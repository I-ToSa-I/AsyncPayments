from AsyncPayments.requests import RequestsClient
from typing import Optional, Union, List
from .models import Balance, Order, Orders, CreateOrder, Currency, WithdrawalCurrency, Store, Withdrawal, Withdrawals, CreateWithdrawal

import json
import hashlib
import time
import hmac


class AsyncFreeKassa(RequestsClient):
    API_HOST: str = "https://freekassa.com/"

    def __init__(self, apiKey: str, shopId: int) -> None:
        """
        Initialize FreeKassa API client
        :param apiKey: Your api key
        :param shopId: Your shop id
        """
        super().__init__()
        self.__apiKey = apiKey
        self.__shopId = shopId
        self.__headers = {
            'Content-Type': 'application/json',
        }
        self.__base_url = "https://api.freekassa.com/v1"
        self.__post_method = "POST"
        self.__payment_name = "freeKassa"
        self.check_values()

    def check_values(self):
        if not self.__shopId or not self.__apiKey:
            raise ValueError('No ShopID or ApiKey specified')

    def __generate_sign(self, data: dict) -> str:
        data = dict(sorted(data.items()))
        return hmac.new(self.__apiKey.encode(), '|'.join(map(str, data.values())).encode(), hashlib.sha256).hexdigest()

    async def get_balance(self) -> List[Balance]:
        """Get balance or your store.
        
        Docs: https://docs.freekassa.com/#operation/getBalance
        """
        url = f"{self.__base_url}/balance"
        
        params = {
            "shopId": self.__shopId,
            "nonce": time.time_ns(),
        }
        params['signature'] = self.__generate_sign(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))
        
        return [Balance(**balance) for balance in response['balance']]
    
    async def get_orders(self, orderId: Optional[int] = None, paymentId: Optional[str] = None, 
                         orderStatus: Optional[int] = None, dateFrom: Optional[str] = None, 
                         dateTo: Optional[str] = None, page: Optional[int] = None) -> Orders:
        """Get orders of your store.
        
        Docs: https://docs.freekassa.com/#operation/getOrders
        
        :param orderId: Optional. Freekassa Order Number. Example: orderId=123456789.
        :param paymentId: Optional. The order number in your store. Example: paymentId=987654321.
        :param orderStatus: Optional. Order status. Example: orderStatus=1.
        :param dateFrom: Optional. Date from. Example: dateFrom=2021-01-01 13:45:21.
        :param dateTo: Optional. Date by. Example: dateTo=2021-01-02 13:45:21.
        :param page: Optional. Page number.
        """
        url = f"{self.__base_url}/orders"
        params = {
            "shopId": self.__shopId,
            "nonce": time.time_ns(),
            "orderId": orderId,
            "paymentId": paymentId,
            "orderStatus": orderStatus,
            "dateFrom": dateFrom,
            "dateTo": dateTo,
            "page": page,
        }
        self._delete_empty_fields(params)
        params['signature'] = self.__generate_sign(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return Orders(pages=int(response['pages']), orders=[Order(**order) for order in response["orders"]])
    
    async def create_order(self, i: int, email: str, ip: str, amount: Union[int, float], currency: str, 
                           tel: Optional[str] = None, paymentId: Optional[str] = None, 
                           successUrl: Optional[str] = None, failureUrl: Optional[str] = None, 
                           notificationUrl: Optional[str] = None) -> CreateOrder:
        """Create an order and receive a payment link.
        
        Docs: https://docs.freekassa.com/#operation/createOrder
        
        :param i: Required. Payment system ID. Example: i=6.
        :param email: Required. Buyer's email address. Example: email=user@site.ru.
        :param ip: Required. Buyer's IP address. Example: ip=0.0.0.0.
        :param amount: Required. Payment amount. Example: amount=100.23.
        :param currency: Required. Payment currency. Example: currency=RUB.
        :param tel: Optional. The payer's phone number is required in some payment methods. Example: tel=+79261231212.
        :param paymentId: Optional. Payment system ID. Example: paymentId=987654321.
        :param successUrl: Optional. Redefining the success url (to enable this parameter, contact support).  Example: successUrl=https://site.ru/success.
        :param failureUrl: Optional. Redefining the error URL (to enable this parameter, contact support). Example: failureUrl=https://site.ru/error.
        :param notificationUrl: Optional. Redefining the notification url (to enable this option, contact support). Example: notificationUrl=https://site.ru/notify.
        """
        url = f"{self.__base_url}/orders/create"
        params = {
            "shopId": self.__shopId,
            "nonce": time.time_ns(),
            "i": i,
            "email": email,
            "ip": ip,
            "amount": amount,
            "currency": currency,
            "tel": tel,
            "paymentId": paymentId,
            "success_url": successUrl,
            "failure_url": failureUrl,
            "notification_url": notificationUrl,
        }
        self._delete_empty_fields(params)
        params['signature'] = self.__generate_sign(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))
        return CreateOrder(**response)
    
    async def get_list_of_currencies(self) -> List[Currency]:
        """Get list of all available currencies for payments.
        
        Docs: https://docs.freekassa.com/#operation/getCurrencies
        """
        url = f"{self.__base_url}/currencies"
        params = {
            "shopId": self.__shopId,
            "nonce": time.time_ns(),
        }
        params["signature"] = self.__generate_sign(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))
        
        return [Currency(**currency) for currency in response['currencies']]
    
    
    async def check_currency_status(self, paymentId: int) -> bool:
        """Check the availability of the payment system for payment.
        
        Docs: https://docs.freekassa.com/#operation/currencyStatus
        
        :return: True - Payment is available. False - Payment is not available.
        """
        url = f"{self.__base_url}/currencies/{paymentId}/status"
        params = {
            "shopId": self.__shopId,
            "nonce": time.time_ns(),
        }
        params["signature"] = self.__generate_sign(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))
        
        return response['type'] == "success"
            
    async def get_list_of_currencies_for_withdrawal(self) -> List[WithdrawalCurrency]:
        """Get list of all available currencies for withdrawal.
        
        Docs: https://docs.freekassa.com/#operation/getWithdrawalsCurrencies
        """
        url = f"{self.__base_url}/withdrawals/currencies"
        params = {
            "shopId": self.__shopId,
            "nonce": time.time_ns(),
        }
        params["signature"] = self.__generate_sign(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))
        
        return [WithdrawalCurrency(**currency) for currency in response['currencies']]
    
    async def get_list_of_your_stores(self) -> List[Store]:
        """Get list of your stores.
        
        Docs: https://docs.freekassa.com/#operation/getShops
        """
        url = f"{self.__base_url}/shops"
        params = {
            "shopId": self.__shopId,
            "nonce": time.time_ns(),
        }
        params["signature"] = self.__generate_sign(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))
        
        return [Store(**store) for store in response['shops']]
            
    async def get_withdrawals(self, orderId: Optional[int] = None, paymentId: Optional[str] = None, 
                         orderStatus: Optional[int] = None, dateFrom: Optional[str] = None, 
                         dateTo: Optional[str] = None, page: Optional[int] = None) -> Withdrawals:
        """Get list of withdrawals.
        
        Docs: https://docs.freekassa.com/#operation/getWithdrawals
        
        :param orderId: Optional. Freekassa Order Number. Example: orderId=123456789.
        :param paymentId: Optional. The order number in your store. Example: paymentId=987654321.
        :param orderStatus: Optional. Order status. Example: orderStatus=1.
        :param dateFrom: Optional. Date from. Example: dateFrom=2021-01-01 13:45:21.
        :param dateTo: Optional. Date by. Example: dateTo=2021-01-02 13:45:21.
        :param page: Optional. Page number.
        """
        url = f"{self.__base_url}/withdrawals"
        params = {
            "shopId": self.__shopId,
            "nonce": time.time_ns(),
            "orderId": orderId,
            "paymentId": paymentId,
            "orderStatus": orderStatus,
            "dateFrom": dateFrom,
            "dateTo": dateTo,
            "page": page,
        }
        self._delete_empty_fields(params)
        params['signature'] = self.__generate_sign(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))
        
        return Withdrawals(pages=int(response['pages']), withdrawals=[Withdrawal(**withdrawal) for withdrawal in response["orders"]])
    
    async def create_withdrawal(self, i: int, account: str, amount: Union[int, float], currency: str, 
                                paymentId: Optional[str] = None) -> CreateWithdrawal:
        """Create withdrawal.
        
        Docs: https://docs.freekassa.com/#operation/createWithdrawal
        
        :param i: Required. Payment system ID. Example: i=6.
        :param account: Required. A wallet for crediting funds (when paying to FKWallet, withdrawal is made only to your account). Example: account=5500000000000004.
        :param amount: Required. Payment amount. Example: amount=100.23.
        :param currency: Required. Payment currency. Example: currency=RUB.
        :param paymentId: Optional. Payment system ID. Example: paymentId=987654321.
        """
        url = f"{self.__base_url}/withdrawals/create"
        params = {
            "shopId": self.__shopId,
            "nonce": time.time_ns(),
            "i": i,
            "account": account,
            "amount": amount,
            "currency": currency,
            "paymentId": paymentId,
        }
        self._delete_empty_fields(params)
        params['signature'] = self.__generate_sign(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))
        return CreateWithdrawal(**response['data'])
    