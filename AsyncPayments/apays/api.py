from ..requests import RequestsClient
from typing import Optional, Union
from .models import Order, OrderInfo
import hashlib


class AsyncAPays(RequestsClient):
    API_HOST: str = "https://apays.io/"

    def __init__(self, client_id: int, secret_key: str) -> None:
        """
        Initialize APays API client
        :param client_id: Your APays client ID.
        :param secret_key: Your APays secret key.
        """
        super().__init__()
        self.__client_id = client_id
        self.__secret_key = secret_key
        self.__base_url = "https://apays.io/backend"
        self.__get_method = "GET"
        self.__payment_name = "apays"
        self.check_values()

    def check_values(self):
        if not self.__secret_key or not self.__client_id:
            raise ValueError('No SecretKey or ClientID specified')
    
    def __create_sign(self, order_id: str, amount: Union[float, int] = None) -> str:
        if amount:
            data = f"{order_id}:{amount}:{self.__secret_key}"
        else:
            data = f"{order_id}:{self.__secret_key}"
            
        return hashlib.md5(data.encode()).hexdigest()

    async def create_order(
        self,
        order_id: str,
        amount: Union[int, float],
        email: Optional[str] = None,
    ) -> Order:
        """Creates a payment and returns a link for the buyer to pay.
        
        :param order_id: Unique order ID.
        :param amount: Amount in kopecks.
        :param email: Optional. Buyer's email address. If set, it will not be requested.
        
        Docs: https://docs.apays.io/lets-start/api/create-payment
        """
        params = {
            "client_id": self.__client_id,
            "order_id": order_id,
            "amount": amount,
            "sign": self.__create_sign(order_id, amount),
            "email": email,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/create_order"

        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            params=params,
        )
        return Order(**response)
    
    async def get_order(self, order_id: str) -> OrderInfo:
        """Receiving payment.

        :param order_id: Order ID.
        
        Docs: https://docs.apays.io/lets-start/api/check-status-payment
        """
        params = {
            "client_id": self.__client_id,
            "order_id": order_id,
            "sign": self.__create_sign(order_id)
        }
        url = f"{self.__base_url}/get_order"

        response = await self._request(
            self.__payment_name,
            self.__get_method,
            url,
            params=params,
        )
        return OrderInfo(**response)