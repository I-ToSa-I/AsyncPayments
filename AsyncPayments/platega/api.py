from ..requests import RequestsClient
from typing import Optional, Union
from .models import Order, OrderInfo, ExchangeRate
from urllib.parse import urlencode
import json

class AsyncPlatega(RequestsClient):
    API_HOST: str = "https://platega.io/"

    def __init__(self, merchant_id: str, secret_key: str) -> None:
        """
        Initialize Platega API client
        :param merchant_id: Your Platega merchant ID.
        :param secret_key: Your Platega secret key.
        """
        super().__init__()
        self.__merchant_id = merchant_id
        self.__secret_key = secret_key
        self.__headers = {
            "X-MerchantId": merchant_id,
            "X-Secret": secret_key,
            "Content-Type": "application/json",
        }
        self.__base_url = "https://app.platega.io"
        self.__get_method = "GET"
        self.__post_method = "POST"
        self.__payment_name = "platega"
        self.check_values()

    def check_values(self):
        if not self.__secret_key or not self.__merchant_id:
            raise ValueError('No SecretKey or MerchantID specified')
        
    async def create_order(
        self,
        payment_method: str,
        amount: Union[int, float],
        currency: str,
        description: str,
        return_url: Optional[str] = None,
        failed_url: Optional[str] = None,
        payload: Optional[str] = None
    ) -> Order:
        """Creates a transaction and returns payment details. The transaction ID is generated automatically by the system—do not pass the id field in the request.
        
        :param payment_method: Payment method number (for example, 2 for QR SBP). 2 - SBP QR; 11 - Card acquiring; 12 - International acquiringInternational card payments; 13 - Cryptocurrency.
        :param amount: Payment amount.
        :param currency: Payment currency (for example, RUB).
        :param description: The purpose (description) of the payment, please always indicate it if possible.
        :param return_url: Redirect upon successful payment.
        :param failed_url: Redirect for unsuccessful payment.
        :param payload: Additional information for initialization on your system.
        
        Docs: https://docs.platega.io/%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5-%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B8-%D0%BD%D0%B0-%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D1%83-27021914e0
        """
        params = {
            "paymentMethod": payment_method,
            "paymentDetails": {
                "amount": amount,
                "currency": currency
            },
            "description": description,
            "return": return_url,
            "failedUrl": failed_url,
            "payload": payload,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/transaction/process"

        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=json.dumps(params),
        )
        return Order(**response)
    
    async def get_order(self, order_id: str) -> OrderInfo:
        """Returns the status and details of the transaction.

        :param order_id: Transaction ID (UUID).
        
        Docs: https://docs.platega.io/%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0-%D1%81%D1%82%D0%B0%D1%82%D1%83%D1%81%D0%B0-%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D1%8B-%D0%BF%D0%BB%D0%B0%D1%82%D0%B5%D0%B6%D0%B0-22645077e0
        """
        url = f"{self.__base_url}/transaction/{order_id}"

        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            headers=self.__headers,
        )
        return OrderInfo(**response)
    
    async def get_rates(self, payment_method: str, currency_from: str, currency_to: str) -> ExchangeRate:
        """Returns the current exchange rate for the specified payment method and currencies.
        
        :param payment_method: Payment method number (for example, 2 for QR SBP). 2 - SBP QR; 11 - Card acquiring; 12 - International acquiringInternational card payments; 13 - Cryptocurrency.
        :param currency_from: Source currency (e.g. RUB).
        :param currency_to: Target currency (e.g. USDT).
        
        Docs: https://docs.platega.io/%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BA%D1%83%D1%80%D1%81%D0%BE%D0%B2-%D0%BF%D0%BE-%D0%BF%D0%BB%D0%B0%D1%82%D0%B5%D0%B6%D0%BD%D0%BE%D0%BC%D1%83-%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D1%83-22645078e0
        """
        params = {
            "merchantId": self.__merchant_id,
            "paymentMethod": payment_method,
            "currencyFrom": currency_from,
            "currencyTo": currency_to,
        }
        url = f"{self.__base_url}/rates/payment_method_rate"

        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=self.__headers,
            data=urlencode(params),
        )
        return ExchangeRate(**response)
    
    async def get_orders(self, date_from: str, date_to: str, page: str, size: str):
        """Method for receiving conversions.
        
        :param date_from: Date from. Example: 2025-01-01T00%3A00%3A00Z.
        :param date_to: Date to. Example: 2025-11-13T23%3A59%3A59Z.
        :param page: Page number. Example: 1.
        :param size: Size. Example: 20.
        
        Docs: https://docs.platega.io/%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BA%D1%83%D1%80%D1%81%D0%BE%D0%B2-%D0%BF%D0%BE-%D0%BF%D0%BB%D0%B0%D1%82%D0%B5%D0%B6%D0%BD%D0%BE%D0%BC%D1%83-%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D1%83-22645078e0
        """
        params = {
            "from": date_from,
            "to": date_to,
            "page": page,
            "size": size,
        }
        url = f"{self.__base_url}/transaction/balance-unlock-operations"
        
        new_headers = self.__headers
        new_headers['accept'] = "text/plain"
        
        response = await self._request(
            self.__payment_name,
            self.__post_method,
            url,
            headers=new_headers,
            data=urlencode(params),
        )
        return response
        