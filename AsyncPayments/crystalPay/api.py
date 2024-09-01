from AsyncPayments.requests import RequestsClient
from typing import Optional, Union, List
from .models import CreatePayment, CassaInfo, PayoffCreate, TickersRate, PayoffRequest, \
                    PaymentInfo, BalancesList, Balance, Methods, Method, SwapPair, \
                    CreateSwap, SwapInfo, CreateTransfer, TransferInfo, Stats

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
        self.__base_url = "https://api.crystalpay.io/v3"
        self.__post_method = "POST"
        self.__payment_name = "crystalPay"
        self.check_values()

    def check_values(self):
        if not self.__login or not self.__secret or not self.__salt:
            raise ValueError('No Secret, Login or Salt specified')

    async def get_cassa_info(self, hide_empty: Optional[bool]= False) -> CassaInfo:
        """Get cash info.

        Docs: https://docs.crystalpay.io/metody-api/me-kassa/poluchenie-informacii-o-kasse"""

        url = f'{self.__base_url}/me/info/'

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "hide_empty": hide_empty,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return CassaInfo(**response)

    async def get_balance_list(self, hide_empty: Optional[bool] = False) -> BalancesList:
        """Get balances list.

        Docs: https://docs.crystalpay.io/metody-api/balance-balansy/poluchenie-spiska-balansov
        
        :param hide_empty: Optional. Hide empty balances. Defaults to False"""

        url = f'{self.__base_url}/balance/list/'

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "hide_empty": hide_empty,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))
        if response['items']:
            return BalancesList(**response['items'])
        else:
            return []
    
    async def get_balance(self, method: str) -> Balance:
        """Get balance of the method.

        Docs: https://docs.crystalpay.io/metody-api/balance-balansy/poluchenie-balansa
        
        :param method: Internal name of the account/method."""

        url = f'{self.__base_url}/balance/get/'

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "method": method,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))
        return Balance(**response)
    
    async def get_payment_methods(self, compact: Optional[bool] = False) -> Methods:
        """Get list of a methods.

        Docs: https://docs.crystalpay.io/metody-api/method-metody/poluchenie-spiska-metodov
        
        :param compact: Displaying only basic information."""

        url = f'{self.__base_url}/method/list/'

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "compact": compact,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return Methods(**response['items'])
    
    
    async def get_payment_method(self, method: str) -> Method:
        """Get info about a method.

        Docs: https://docs.crystalpay.io/metody-api/method-metody/poluchenie-metoda
        
        :param compact: The internal name of the method."""

        url = f'{self.__base_url}/method/get/'

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "method": method,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return Method(**response)
        

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
            _type: Optional[str] = "purchase", description: Optional[str] = None, redirect_url: Optional[str] = None,
            callback_url: Optional[str] = None, extra: Optional[str] = None, payer_details: Optional[str] = None,
            lifetime: Optional[int] = 60) -> CreatePayment:
        """Generate payment url.

        Docs: https://docs.crystalpay.io/metody-api/invoice-platezhi/sozdanie-invoisa

        :param amount: Order amount.
        :param amount_currency: Currency. Default to 'RUB', for example: USD, BTC, ETH
        :param required_methods: Pre-selected payment method, for example: LZTMARKET, BITCOIN
        :param _type: Invoice type. possible options: purchase, topup
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
            "type": _type,
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

        Docs: https://docs.crystalpay.io/metody-api/invoice-platezhi/poluchenie-informacii-ob-invoise

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
                            extra: Optional[str] = None, wallet_extra: Optional[str] = None) -> PayoffCreate:
        """Create payoff request.

        Docs: https://docs.crystalpay.io/metody-api/payoff-vyvody/sozdanie-vyvoda

        :param amount: Payoff amount, for example: 10, 0.0015
        :param amount_currency: The currency of the amount is automatically converted into the currency of the withdrawal method, for example: RUB, USD, BTC
        :param method: Payoff method, for example: LZTMARKET, BITCOIN
        :param wallet: Recipient's wallet details
        :param subtract_from: Where to write off the commission amount, possible options: balance, amount
        :param callback_url: Link for HTTP Callback notification after output is complete
        :param extra: Any internal data, for example: Payment ID in your system
        :param wallet_extra: Optional. Additional information about the recipient's details.

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
            "wallet_extra": wallet_extra,
            "subtract_from": subtract_from,
            "callback_url": callback_url,
            "extra": extra,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return PayoffCreate(**response)

    async def submit_payoff(self, payoff_id: str) -> PayoffRequest:
        """Submit payoff request

        Docs: https://docs.crystalpay.io/metody-api/payoff-vyvody/podtverzhdenie-vyvoda

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

        Docs: https://docs.crystalpay.io/metody-api/payoff-vyvody/otmena-vyvoda

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

        Docs: https://docs.crystalpay.io/metody-api/payoff-vyvody/poluchenie-informacii-o-vyvode

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

    async def get_tickers_rate(self, tickers: list, base_currency: Optional[str] = "RUB") -> TickersRate:
        """Get the exchange rate against 

        Docs: https://docs.crystalpay.io/api/valyuty/poluchenie-kursa-valyut

        :param tickers: Array of currencies, for example: [“BTC”, “LTC”]
        :param base_currency: Base currency, RUB by default."""

        url = f"{self.__base_url}/ticker/get/"

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "tickers": tickers,
            "base_currency": base_currency,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return TickersRate(**response)

    async def get_list_swap_pairs(self, page: Optional[int] = 1, items: Optional[int] = 20, source: Optional[str] = None,
                                      target: Optional[str] = None) -> List[SwapPair]:
        """Getting a list of swap pairs.

        Docs: https://docs.crystalpay.io/metody-api/swap-obmeny/obmennye-pary/poluchenie-spiska-obmennykh-par

        :param page: Optional. Page Number. Default is 1.
        :param items: Optional. Number of items per page. Default is 20.
        :param source: Optional. The original currency, deducted during the exchange. Filter by source.
        :param target: Optional. The currency received is credited during the exchange. Filter by target.
        """

        url = f"{self.__base_url}/swap/pair/list/"

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "page": page,
            "items": items,
            "source": source,
            "target": target,
        }
        self._delete_empty_fields(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return [SwapPair(**swapPair) for swapPair in response['items'].values()]
    
    async def get_swap_pair(self, pair_id: int) -> SwapPair:
        """Get a swap pair.

        Docs: https://docs.crystalpay.io/metody-api/swap-obmeny/obmennye-pary/poluchenie-obmennoi-pary

        :param pair_id: ID of the swap pair.
        """

        url = f"{self.__base_url}/swap/pair/get/"

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "pair_id": pair_id,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return SwapPair(**response)
    
    async def create_swap(self, pair_id: int, amount: int, amount_type: str) -> CreateSwap:
        """Create swap.

        Docs: https://docs.crystalpay.io/metody-api/swap-obmeny/sozdanie-obmena

        :param pair_id: ID of the swap pair.
        :param amount: Amount of the swap.
        :param amount_type: Type of the amount. source - The amount specified in the original currency. target - The amount specified in the received currency.
        """
        
        url = f"{self.__base_url}/swap/create/"
        signature = hashlib.sha1(str.encode(f"{amount}:{pair_id}:{self.__salt}")).hexdigest()

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "pair_id": pair_id,
            "amount": amount,
            "amount_type": amount_type,
            "signature": signature,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return CreateSwap(**response)
    
    async def swap_submit(self, swap_id: str) -> SwapInfo:
        """Submit swap request.

        Docs: https://docs.crystalpay.io/metody-api/swap-obmeny/podtverzhdenie-obmena

        :param swap_id: ID of the swap.
        """
        
        url = f"{self.__base_url}/swap/submit/"
        signature = hashlib.sha1(str.encode(f"{swap_id}:{self.__salt}")).hexdigest()

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "id": swap_id,
            "signature": signature,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return SwapInfo(**response)
    
    async def swap_cancel(self, swap_id: str) -> SwapInfo:
        """Cancel swap request.

        Docs: https://docs.crystalpay.io/metody-api/swap-obmeny/otmena-obmena

        :param swap_id: ID of the swap.
        """
        
        url = f"{self.__base_url}/swap/cancel/"
        signature = hashlib.sha1(str.encode(f"{swap_id}:{self.__salt}")).hexdigest()

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "id": swap_id,
            "signature": signature,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return SwapInfo(**response)
    
    async def get_swap_info(self, swap_id: str) -> SwapInfo:
        """Get swap info.

        Docs: https://docs.crystalpay.io/metody-api/swap-obmeny/poluchenie-informacii-ob-obmene

        :param swap_id: ID of the swap.
        """
        
        url = f"{self.__base_url}/swap/info/"
        

        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "id": swap_id,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return SwapInfo(**response)
    
    async def create_transfer(self, method: str, amount: str, receiver: str, 
                              description: Optional[str] = None) -> CreateTransfer:
        """Create a transfer.

        Docs: https://docs.crystalpay.io/metody-api/transfer-perevody/sozdanie-perevoda

        :param method: The internal name of the method.
        :param amount: Amount of the transfer.
        :param receiver: The recipient's cashier's login.
        :param description: Optional. Description of the transfer.
        """
        
        url = f"{self.__base_url}/transfer/create/"
        signature = hashlib.sha1(str.encode(f"{amount}:{method}:{receiver}:{self.__salt}")).hexdigest()
        
        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "method": method,
            "amount": amount,
            "receiver": receiver,
            "signature": signature,
            "description": description,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return CreateTransfer(**response)
    
    async def submit_transfer(self, transfer_id: str) -> TransferInfo:
        """Submit the transfer.

        Docs: https://docs.crystalpay.io/metody-api/transfer-perevody/podtverzhdenie-perevoda

        :param transfer_id: ID of the transfer.
        """
        
        url = f"{self.__base_url}/transfer/submit/"
        signature = hashlib.sha1(str.encode(f"{transfer_id}:{self.__salt}")).hexdigest()
        
        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "id": transfer_id,
            "signature": signature,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return TransferInfo(**response)
    
    async def cancel_transfer(self, transfer_id: str) -> TransferInfo:
        """Cancel the transfer.

        Docs: https://docs.crystalpay.io/metody-api/transfer-perevody/otmena-perevoda

        :param transfer_id: ID of the transfer.
        """
        
        url = f"{self.__base_url}/transfer/submit/"
        signature = hashlib.sha1(str.encode(f"{transfer_id}:{self.__salt}")).hexdigest()
        
        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "id": transfer_id,
            "signature": signature,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return TransferInfo(**response)

    async def get_transfer_info(self, transfer_id: str) -> TransferInfo:
        """Get info about the transfer.

        Docs: https://docs.crystalpay.io/metody-api/transfer-perevody/poluchenie-informacii-o-perevode

        :param transfer_id: ID of the transfer.
        """
        
        url = f"{self.__base_url}/transfer/info/"
        
        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "id": transfer_id,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return TransferInfo(**response)
    
    async def get_history_payments(self, page: Optional[int] = 1, items: Optional[int] = 20, period: Optional[int] = 1, 
                                   export_csv: Optional[bool] = False) -> List[PaymentInfo]:
        """Get payments history.

        Docs: https://docs.crystalpay.io/metody-api/report-otchyoty-i-statistika/invoice-platezhi/poluchenie-istorii

        :param page: Optional. Page number. Default is 1.
        :param items: Optional. Number of items per page. Default is 20.
        :param period: Optional. The period from the current date, in days. Default is 1.
        :param export_csv: Optional. Export as a csv format table. Default is False.
        """
        
        url = f"{self.__base_url}/report/invoice/history/"
        
        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "page": page,
            "items": items,
            "period": period,
            "export_csv": export_csv,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        if response["items"]:
            return [PaymentInfo(**payment) for payment in response['items']]
        else:
            return []
    
    async def get_stats_payments(self, period: Optional[int] = 1, 
                                 export_pdf: Optional[bool] = False) -> Stats:
        """Get payments stats.

        Docs: https://docs.crystalpay.io/metody-api/report-otchyoty-i-statistika/invoice-platezhi/poluchenie-statistiki

        :param period: Optional. The period from the current date, in days. Default is 1.
        :param export_pdf: Optional. Export as a pdf format. Default is False.
        """
        
        url = f"{self.__base_url}/report/invoice/summary/"
        
        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "period": period,
            "export_pdf": export_pdf,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return Stats(**response)
    
    async def get_history_payoffs(self, page: Optional[int] = 1, items: Optional[int] = 20, period: Optional[int] = 1, 
                                   export_csv: Optional[bool] = False) -> List[PayoffRequest]:
        """Get payoffs history.

        Docs: https://docs.crystalpay.io/metody-api/report-otchyoty-i-statistika/payoff-vyvody/poluchenie-istorii

        :param page: Optional. Page number. Default is 1.
        :param items: Optional. Number of items per page. Default is 20.
        :param period: Optional. The period from the current date, in days. Default is 1.
        :param export_csv: Optional. Export as a csv format table. Default is False.
        """
        
        url = f"{self.__base_url}/report/payoff/history/"
        
        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "page": page,
            "items": items,
            "period": period,
            "export_csv": export_csv,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        if response['items']:
            return [PayoffRequest(**payment) for payment in response['items']]
        else:
            return []
    
    async def get_stats_payoffs(self, period: Optional[int] = 1, 
                                 export_pdf: Optional[bool] = False) -> Stats:
        """Get payoff stats.

        Docs: https://docs.crystalpay.io/metody-api/report-otchyoty-i-statistika/payoff-vyvody/poluchenie-statistiki

        :param period: Optional. The period from the current date, in days. Default is 1.
        :param export_pdf: Optional. Export as a pdf format. Default is False.
        """
        
        url = f"{self.__base_url}/report/payoff/summary/"
        
        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "period": period,
            "export_pdf": export_pdf,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))

        return Stats(**response)
    
    
    async def get_history_swaps(self, page: Optional[int] = 1, items: Optional[int] = 20, period: Optional[int] = 1, 
                                   export_csv: Optional[bool] = False) -> List[SwapInfo]:
        """Get swaps history.

        Docs: https://docs.crystalpay.io/metody-api/report-otchyoty-i-statistika/swap-obmeny/poluchenie-istorii

        :param page: Optional. Page number. Default is 1.
        :param items: Optional. Number of items per page. Default is 20.
        :param period: Optional. The period from the current date, in days. Default is 1.
        :param export_csv: Optional. Export as a csv format table. Default is False.
        """
        
        url = f"{self.__base_url}/report/swap/history/"
        
        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "page": page,
            "items": items,
            "period": period,
            "export_csv": export_csv,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))
        
        if response["items"]:
            return [SwapInfo(**payment) for payment in response['items']]
        else:
            return []
    
    async def get_history_transfers(self, page: Optional[int] = 1, items: Optional[int] = 20, period: Optional[int] = 1, 
                                   export_csv: Optional[bool] = False) -> List[TransferInfo]:
        """Get swaps history.

        Docs: https://docs.crystalpay.io/metody-api/report-otchyoty-i-statistika/transfer-perevody/poluchenie-istorii

        :param page: Optional. Page number. Default is 1.
        :param items: Optional. Number of items per page. Default is 20.
        :param period: Optional. The period from the current date, in days. Default is 1.
        :param export_csv: Optional. Export as a csv format table. Default is False.
        """
        
        url = f"{self.__base_url}/report/transfer/history/"
        
        params = {
            "auth_login": self.__login,
            "auth_secret": self.__secret,
            "page": page,
            "items": items,
            "period": period,
            "export_csv": export_csv,
        }

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=json.dumps(params))
        
        if response["items"]:
            return [TransferInfo(**payment) for payment in response['items']]
        else:
            return []
    