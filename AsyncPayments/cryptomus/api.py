from ..requests import RequestsClient
from typing import Optional, List
from .models import Balance, Balances, CreatePayment, GenerateStaticWallet, GenerateQrCode, BlockStaticWallet, RefundPaymentsOnBlockedAddress, \
                    PaymentInfo, ListOfServices, PaymentHistory, Payout, PayoutHistory, ListOfServicesPayout, TransferWallet, RecurringPayment, \
                    ListOfRecurringPayments, ExchangeRatesList, Discount
import base64
import json
import hashlib


class AsyncCryptomus(RequestsClient):
    API_HOST: str = "https://cryptomus.com/gateway"

    def __init__(self, payment_api_key: str, merchant_id: str, payout_api_key: str) -> None:
        """
        Initialize Cryptomus API client
        :param payment_api_key: Your payment API key
        :param merchant_id: Your merchant ID
        :param payout_api_key: Your payout API key
        """
        super().__init__()
        self.__payment_api_key = payment_api_key
        self.__merchant_id = merchant_id
        self.__payout_api_key = payout_api_key
        self.__headers = {
            "Content-Type": "application/json",
            "merchant": self.__merchant_id,
        }
        self.__base_url = "https://api.cryptomus.com/v1"
        self.__post_method = "POST"
        self.__get_method = "GET"
        self.__payment_name = "cryptomus"
        self.check_values()

    def check_values(self):
        if not self.__merchant_id or not self.__payment_api_key or not self.__payout_api_key:
            raise ValueError('No Payment API key, merchant ID or Payout API key specified')
        
    def __generate_sign(self, data: Optional[dict] = None, is_for_payouts: Optional[bool] = False) -> dict:
        if data:
            data_encoded = base64.b64encode(json.dumps(data).encode()).decode()
        else:
            data_encoded = ""

        if is_for_payouts:
            return hashlib.md5((data_encoded + self.__payout_api_key).encode()).hexdigest()
        return hashlib.md5((data_encoded + self.__payment_api_key).encode()).hexdigest()

    async def get_balance(self) -> Balances:
        """Get list of your balances.

        Docs: https://doc.cryptomus.com/ru/business/balance"""

        self.__headers["sign"] = self.__generate_sign()
        response = await self._request(self.__payment_name, self.__post_method, f'{self.__base_url}/balance', headers=self.__headers)        
        
        return Balances(merchant=[Balance(**balance) for balance in response['result'][0]['balance']['merchant']], 
                        user=[Balance(**balance) for balance in response['result'][0]['balance']['user']])

    async def create_payment(self, amount: str, currency: str, order_id: str, network: Optional[str] = None, url_return: Optional[str] = None,
                             url_success: Optional[str] = None, url_callback: Optional[str] = None, is_payment_multiple: Optional[bool] = True,
                             lifetime: Optional[int] = 3600, to_currency: Optional[str] = None, subtract: Optional[int] = 0,
                             accuracy_payment_percent: Optional[int] = 0, additional_data: Optional[str] = None, currencies: Optional[list] = None,
                             except_currencies: Optional[list] = None, course_source: Optional[str] = None, from_referral_code: Optional[str] = None,
                             discount_percent: Optional[int] = None, is_refresh: Optional[bool] = False) -> CreatePayment:
        
        """Create payment.
        
        :param amount: Amount to be paid. If there are pennies in the amount, then send them with a separator '.'. Example: 10.28
        :param currency: Currency code.
        :param order_id: Order ID in your system. The parameter should be a string consisting of alphabetic characters, numbers, underscores, and dashes. It should not contain any spaces or special characters. The order_id must be unique within the merchant invoices/static wallets/recurrence payments. When we find an existing invoice with order_id, we return its details, a new invoice will not be created.
        :param network: Blockchain network code.
        :param url_return: Before paying, the user can click on the button on the payment form and return to the store page at this URL.
        :param url_success: After successful payment, the user can click on the button on the payment form and return to this URL.
        :param url_callback: Url to which webhooks with payment status will be sent.
        :param is_payment_multiple: Whether the user is allowed to pay the remaining amount. This is useful when the user has not paid the entire amount of the invoice for one transaction, and you want to allow him to pay up to the full amount. If you disable this feature, the invoice will finalize after receiving the first payment and you will receive funds to your balance.
        :param lifetime: Min: 300. Max: 43200. The lifespan of the issued invoice (in seconds).
        :param to_currency: The parameter is used to specify the target currency for converting the invoice amount. When creating an invoice, you provide an amount and currency, and the API will convert that amount to the equivalent value in the to_currency. For example, to create an invoice for 20 USD in bitcoin: amount: 20, currency: USD, to_currency: BTC. The API will convert 20 USD amount to its equivalent in BTC based on the current exchange rate and the user will pay in BTC. The to_currency should always be the cryptocurrency code, not a fiat currency code.
        :param subtract: Min: 0. Max: 100. Percentage of the payment commission charged to the client. If you have a rate of 1%, then if you create an invoice for 100 USDT with subtract = 100 (the client pays 100% commission), the client will have to pay 101 USDT.
        :param accuracy_payment_percent: Min: 0. Max: 5. Acceptable inaccuracy in payment. For example, if you pass the value 5, the invoice will be marked as Paid even if the client has paid only 95% of the amount. The actual payment amount will be credited to the balance.
        :param additional_data: Max: 255. Additional information for you (not shown to the client).
        :param currencies: List of allowed currencies for payment. This is useful if you want to limit the list of coins that your customers can use to pay invoices.
        :param except_currencies: List of excluded currencies for payment.
        :param course_source: Min: 4. Max: 20. The service from which the exchange rates are taken for conversion in the invoice.
        :param from_referral_code: The merchant who makes the request connects to a referrer by code. For example, you are an application that generates invoices via the Cryptomus API and your customers are other stores. They enter their api key and merchant id in your application, and you send requests with their credentials and passing your referral code. Thus, your clients become referrals on your Cryptomus account and you will receive income from their turnover.
        :param discount_percent: Min: -99. Max: 100. Positive numbers: Allows you to set a discount. To set a 5% discount for the payment, you should pass a value: 5. Negative numbers: Allows you to set custom additional commission. To set an additional commission of 10% for the payment, you should pass a value: -10. The discount percentage when creating an invoice is taken into account only if the invoice has a specific cryptocurrency.
        :param is_refresh: Using this parameter, you can update the lifetime and get a new address for the invoice if the lifetime has expired. To do that, you need to pass all required parameters, and the invoice with passed order_id will be refreshed. Only address, payment_status and expired_at are changed. No other fields are changed, regardless of the parameters passed.
        
        Docs: https://doc.cryptomus.com/business/payments/creating-invoice
        """

        url = f"{self.__base_url}/payment"
        params = {
            "amount": amount,
            "currency": currency,
            "order_id": order_id,
            "network": network,
            "url_return": url_return,
            "url_success": url_success,
            "url_callback": url_callback,
            "is_payment_multiple": is_payment_multiple,
            "lifetime": lifetime,
            "to_currency": to_currency,
            "subtract": subtract,
            "accuracy_payment_percent": accuracy_payment_percent,
            "additional_data": additional_data,
            "currencies": currencies,
            "except_currencies": except_currencies,
            "course_source": course_source,
            "from_referral_code": from_referral_code,
            "discount_percent": discount_percent,
            "is_refresh": is_refresh,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)

        return CreatePayment(**response['result'])
    
    async def payment_info(self, uuid: Optional[str] = None, order_id: Optional[str] = None) -> PaymentInfo:
        """Payment information.

        :param uuid: Invoice uuid.
        :param order_id: Invoice order ID.

        Docs: https://doc.cryptomus.com/business/payments/payment-information
        """
        url = f"{self.__base_url}/payment/info"
        params = {
            "uuid": uuid,
            "order_id": order_id,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)

        return PaymentInfo(**response['result'])

    async def generate_static_wallet(self, currency: str, network: str, order_id: str, url_callback: Optional[str] = None, 
                                     from_referral_code: Optional[str] = None) -> GenerateStaticWallet:
        """Creating a Static wallet.
        
        :param currency: Currency code.
        :param network: Blockchain network code.
        :param order_id: Order ID in your system. The parameter should be a string consisting of alphabetic characters, numbers, underscores, and dashes. It should not contain any spaces or special characters. The order_id must be unique within the merchant invoices/static wallets/recurrence payments. When we find an existing invoice with order_id, we return its details, a new invoice will not be created.
        :param url_callback: URL, to which the webhook will be sent after each top-up of the wallet
        :param from_referral_code: The merchant who makes the request connects to a referrer by code.
        
        
        Docs: https://doc.cryptomus.com/business/payments/creating-static
        """
        url = f"{self.__base_url}/wallet"
        params = {
            "currency": currency,
            "network": network,
            "order_id": order_id,
            "url_callback": url_callback,
            "from_referral_code": from_referral_code,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)

        return GenerateStaticWallet(**response['result'])

    async def generate_qr_code_for_wallet(self, wallet_address_uuid: str) -> GenerateQrCode:
        """Generate a QR-code for the static wallet address.

        :param wallet_address_uuid: Uuid of a static wallet.

        Docs: https://doc.cryptomus.com/business/payments/qr-code-pay-form
        """
        url = f"{self.__base_url}/wallet/qr"
        params = {
            "wallet_address_uuid": wallet_address_uuid,
        }
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)

        return GenerateQrCode(**response['result'])
    
    async def generate_qr_code_for_invoice(self, merchant_payment_uuid: str) -> GenerateQrCode:
        """Generate a QR-code for the invoice address.

        :param merchant_payment_uuid: Invoice uuid.

        Docs: https://doc.cryptomus.com/business/payments/qr-code-pay-form
        """
        url = f"{self.__base_url}/payment/qr"
        params = {
            "merchant_payment_uuid": merchant_payment_uuid,
        }
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)

        return GenerateQrCode(**response['result'])
    
    async def block_static_wallet(self, uuid: Optional[str] = None, order_id: Optional[str] = None, is_force_refund: Optional[bool] = False) -> BlockStaticWallet:
        """Block static wallet.
        
        :param uuid: Uuid of a static wallet.
        :param order_id: Order ID of a static wallet.
        :param is_force_refund: Refund all incoming payments to sender’s address.
        
        Docs: https://doc.cryptomus.com/business/payments/block-wallet
        """
        url = f"{self.__base_url}/wallet/block-address"
        params = {
            "uuid": uuid,
            "order_id": order_id,
            "is_force_refund": is_force_refund,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)

        return BlockStaticWallet(**response['result'])
    
    async def refund_payments_on_blocked_address(self, address: str, uuid: Optional[str] = None, order_id: Optional[str] = None) -> RefundPaymentsOnBlockedAddress:
        """Refund payments on blocked address.

        :param address: Uuid of a static wallet.
        :param uuid: Order ID of a static wallet.
        :param order_id: Refund all blocked funds to this address.

        Docs: https://doc.cryptomus.com/business/payments/refundblocked
        """
        url = f"{self.__base_url}/blocked-address-refund"
        params = {
            "address": address,
            "uuid": uuid,
            "order_id": order_id,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)

        return RefundPaymentsOnBlockedAddress(**response['result'])

    async def refund(self, address: str, is_subtract: bool, uuid: Optional[str] = None, order_id: Optional[str] = None) -> bool:
        """Refund.
        
        :param address: The address to which the refund should be made.
        :param is_subtract: Whether to take a commission from the merchant's balance or from the refund amount. True - take the commission from merchant balance. False - reduce the refundable amount by the commission amount.
        :param uuid: Invoice uuid.
        :param order_id: Invoice order ID.

        Docs: https://doc.cryptomus.com/business/payments/refund
        """
        url = f"{self.__base_url}/payment/refund"
        params = {
            "address": address,
            "is_subtract": is_subtract,
            "uuid": uuid,
            "order_id": order_id,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)

        return True if response['state'] == 0 else False

    async def resend_webhook(self, uuid: Optional[str] = None, order_id: Optional[str] = None) -> bool:
        """Resend webhook.
        
        :param uuid: Invoice uuid.
        :param order_id: Invoice order ID.

        Docs: https://doc.cryptomus.com/business/payments/resend-webhook
        """
        url = f"{self.__base_url}/payment/resend"
        params = {
            "uuid": uuid,
            "order_id": order_id,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)

        return True if response['state'] == 0 else False
    
    async def test_webhook_payment(self, url_callback: str, currency: str, network: str, status: str, uuid: Optional[str] = None, 
                                   order_id: Optional[str] = None) -> bool:
        """Testing payment webhook.
        
        :param url_callback: Url to which webhooks with payment status will be sent.
        :param currency: Invoice currency code.
        :param network: Invoice network code.
        :param status: Payment status.
        :param uuid: uuid of the invoice.
        :param order_id: Order ID of the invoice.

        Docs: https://doc.cryptomus.com/business/payments/testing-webhook
        """
        url = f"{self.__base_url}/test-webhook/payment"
        params = {
            "url_callback": url_callback,
            "currency": currency,
            "network": network,
            "status": status,
            "uuid": uuid,
            "order_id": order_id,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)

        return True if response['state'] == 0 else False
    
    async def test_webhook_wallet(self, url_callback: str, currency: str, network: str, status: str, uuid: Optional[str] = None, 
                                   order_id: Optional[str] = None) -> bool:
        """Testing wallet webhook.
        
        :param url_callback: Url to which webhooks with payment status will be sent.
        :param currency: Invoice currency code.
        :param network: Invoice network code.
        :param status: Payment status.
        :param uuid: uuid of the invoice.
        :param order_id: Order ID of the invoice.

        Docs: https://doc.cryptomus.com/business/payments/testing-webhook
        """
        url = f"{self.__base_url}/test-webhook/wallet"
        params = {
            "url_callback": url_callback,
            "currency": currency,
            "network": network,
            "status": status,
            "uuid": uuid,
            "order_id": order_id,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)

        return True if response['state'] == 0 else False
    
    async def test_webhook_payout(self, url_callback: str, currency: str, network: str, status: str, uuid: Optional[str] = None, 
                                   order_id: Optional[str] = None) -> bool:
        """Testing payout webhook.
        
        :param url_callback: Url to which webhooks with payment status will be sent.
        :param currency: Payout currency code.
        :param network: Payout network code.
        :param status: Payout status.
        :param uuid: uuid of the Payout.
        :param order_id: Order ID of the Payout.

        Docs: https://doc.cryptomus.com/business/payments/testing-webhook
        """
        url = f"{self.__base_url}/test-webhook/payout"
        params = {
            "url_callback": url_callback,
            "currency": currency,
            "network": network,
            "status": status,
            "uuid": uuid,
            "order_id": order_id,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)

        return True if response['state'] == 0 else False
        
    async def list_of_services(self) -> List[ListOfServices]:
        """List of services.

        Docs: https://doc.cryptomus.com/business/payments/list-of-services
        """
        url = f"{self.__base_url}/payment/services"
        self.__headers["sign"] = self.__generate_sign()

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)

        return [ListOfServices(**service) for service in response["result"]]
    
    async def payment_history(self, date_from: Optional[str] = None, date_to: Optional[str] = None, cursor: Optional[str] = None) -> PaymentHistory:
        """Payment history.

        :param date_from: Filtering by creation date, from. Format: YYYY-MM-DD H:mm:ss
        :param date_to: Filtering by creation date, to. Format: YYYY-MM-DD H:mm:ss
        :param cursor: Cursor to page.
        
        Docs: https://doc.cryptomus.com/business/payments/payment-history
        """
        url = f"{self.__base_url}/payment/list"
        if cursor:
            url += f"?cursor={cursor}"
        params = {
            "date_from": date_from,
            "date_to": date_to,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, json=params, headers=self.__headers)

        return PaymentHistory(**response['result'])

    async def create_payout(self, amount: str, currency: str, order_id: str, address: str, is_subtract: bool, network: str, 
                            url_callback: Optional[str] = None, to_currency: Optional[str] = None, 
                            course_source: Optional[str] = None, from_currency: Optional[str] = None, 
                            priority: Optional[str] = None, memo: Optional[str] = None) -> Payout:
        """Creating a payout.
        
        :param amount: Payout amount.
        :param currency: Currency code for the payout. If Currency is fiat, the to_currency parameter is required.
        :param order_id: Order ID in your system. The parameter should be a string consisting of alphabetic characters, numbers, underscores, and dashes. It should not contain any spaces or special characters. The order_id must be unique within the merchant payouts. When we find an existing payout with order_id, we return its details, a new payout will not be created.
        :param address: The address of the wallet to which the withdrawal will be made.
        :param is_subtract: Defines where the withdrawal fee will be deducted. True - from your balance. False - from payout amount, the payout amount will be decreased.
        :param network: Blockchain network code. Not required when the currency/to_currency parameters is a cryptocurrency and has only one network, for example BTC.
        :param url_callback: URL to which webhooks with payout status will be sent.
        :param to_currency: Cryptocurrency code in which the payout will be made. It is used when the currency parameter is fiat.
        :param course_source: The service from which the exchange rates are taken for conversion in the invoice. The parameter is applied only if the currency is fiat, otherwise the default value is taken from the merchant's settings. Available values: Binance, BinanceP2p, Exmo, Kucoin, Garantexio.
        :param from_currency: Allows to automatically convert the withdrawal amount and use the from_currency balance. Only USDT is available.
        :param priority: The parameter for selecting the withdrawal priority. The cost of the withdrawal fee depends on the selected parameter. This parameter is applied only in case of using the BTC, ETH, POLYGON, and BSC networks. Available values: recommended, economy, high, highest.
        :param memo: Additional identifier for TON, used to specify a particular recipient or target.

        Docs: https://doc.cryptomus.com/business/payouts/creating-payout
        """
        url = f"{self.__base_url}/payout"
        params = {
            "amount": amount,
            "currency": currency,
            "order_id": order_id,
            "address": address,
            "is_subtract": is_subtract,
            "network": network,
            "url_callback": url_callback,
            "to_currency": to_currency,
            "course_source": course_source,
            "from_currency": from_currency,
            "priority": priority,
            "memo": memo,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params, True)

        response = await self._request(self.__payment_name, self.__post_method, url, json=params, headers=self.__headers)

        return Payout(**response['result'])
    
    async def payout_info(self, uuid: Optional[str] = None, order_id: Optional[str] = None) -> Payout:
        """Payout information.
        
        :param uuid: Payout uuid.
        :param order_id: Payout order ID.

        Docs: https://doc.cryptomus.com/business/payouts/payout-information
        """
        url = f"{self.__base_url}/payout/info"
        params = {
            "uuid": uuid,
            "order_id": order_id,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params, True)

        response = await self._request(self.__payment_name, self.__post_method, url, json=params, headers=self.__headers)

        return Payout(**response['result'])
    
    async def payout_history(self, date_from: Optional[str] = None, date_to: Optional[str] = None, cursor: Optional[str] = None) -> PayoutHistory:
        """Payout history.
        
        :param date_from: Filtering by creation date, from. Format: YYYY-MM-DD H:mm:ss.
        :param date_to: Filtering by creation date, to. Format: YYYY-MM-DD H:mm:ss.
        :param cursor: Cursor to page.

        Docs: https://doc.cryptomus.com/business/payouts/payout-history
        """
        url = f"{self.__base_url}/payout/list"
        if cursor:
            url += f"?cursor={cursor}"
        params = {
            "date_from": date_from,
            "date_to": date_to,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params, True)

        response = await self._request(self.__payment_name, self.__post_method, url, json=params, headers=self.__headers)

        return PayoutHistory(**response['result'])

    async def list_of_services_payout(self) -> List[ListOfServicesPayout]:
        """List of services.
        
        Docs: https://doc.cryptomus.com/business/payouts/list-of-services
        """
        url = f"{self.__base_url}/payout/services"
        self.__headers["sign"] = self.__generate_sign(dict(), True)

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)

        return [ListOfServicesPayout(**service) for service in response["result"]]
    
    async def transfer_to_personal_wallet(self, amount: str, currency: str) -> TransferWallet:
        """Transfer to personal wallet.
        
        :param amount: Amount to transfer.
        :param currency: Currency code. Only cryptocurrency code is allowed..

        Docs: https://doc.cryptomus.com/business/payouts/transfer-to-personal
        """
        url = f"{self.__base_url}/transfer/to-personal"
        params = {
            "amount": amount,
            "currency": currency,
        }
        self.__headers["sign"] = self.__generate_sign(params, True)

        response = await self._request(self.__payment_name, self.__post_method, url, json=params, headers=self.__headers)

        return TransferWallet(**response['result'])
    


    async def transfer_to_business_wallet(self, amount: str, currency: str) -> TransferWallet:
        """Transfer to business wallet.
        
        :param amount: Amount to transfer.
        :param currency: Currency code. Only cryptocurrency code is allowed..

        Docs: https://doc.cryptomus.com/business/payouts/transfer-to-personal
        """
        url = f"{self.__base_url}/transfer/to-business"
        params = {
            "amount": amount,
            "currency": currency,
        }
        self.__headers["sign"] = self.__generate_sign(params, True)

        response = await self._request(self.__payment_name, self.__post_method, url, json=params, headers=self.__headers)

        return TransferWallet(**response['result'])
    
    async def creating_recurring_payment(self, amount: str, currency: str, name: str, period: str, to_currency: Optional[str] = None,
                                         order_id: Optional[str] = None, url_callback: Optional[str] = None, discount_days: Optional[str] = None,
                                         discount_amount: Optional[str] = None, additional_data: Optional[str] = None) -> RecurringPayment:
        """Creating recurring payment.
        
        :param amount: Recurring payment amount.
        :param currency: Currency code.
        :param name: Recurring payment name.
        :param period: Recurring payment period. Available: weekly, monthly, three_month.
        :param to_currency: Currency code for accepting payments. The parameter is used to specify the target currency for converting the recurrent payment amount. For example, to create an recurrent payment for 20 USD in bitcoin: amount: 20, currency: USD, to_currency: BTC. The API will convert 20 USD amount to its equivalent in BTC based on the current exchange rate and the user will pay in BTC. The to_currency should always be the cryptocurrency code, not a fiat currency code.
        :param order_id: Order ID in your system.
        :param url_callback: Url to which webhooks with payment status will be sent.
        :param discount_days: Discount period days (required with 'discount_amount').
        :param discount_amount: Discount amount (required with 'discount_days').Here the amount in the currency of the parameter ‘currency’.
        :param additional_data: Additional recurring payment details.

        Docs: https://doc.cryptomus.com/business/recurring/creating
        """
        url = f"{self.__base_url}/recurrence/create"
        params = {
            "amount": amount,
            "currency": currency,
            "name": name,
            "period": period,
            "to_currency": to_currency,
            "order_id": order_id,
            "url_callback": url_callback,
            "discount_days": discount_days,
            "discount_amount": discount_amount,
            "additional_data": additional_data,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, json=params, headers=self.__headers)

        return RecurringPayment(**response['result'])

    async def recurring_payment_info(self, uuid: Optional[str] = None, order_id: Optional[str] = None) -> RecurringPayment:
        """Payment information.
        
        :param uuid: Recurrence uuid.
        :param order_id: Recurrence order ID.

        Docs: https://doc.cryptomus.com/business/recurring/info"""
        url = f"{self.__base_url}/recurrence/info"
        params = {
            "uuid": uuid,
            "order_id": order_id,
        }
        self._delete_empty_fields(params)
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, json=params, headers=self.__headers)

        return RecurringPayment(**response['result'])

    async def list_of_recurring_payments(self, cursor: Optional[str] = None) -> ListOfRecurringPayments:
        """List of recurring payments.
        
        Docs: https://doc.cryptomus.com/business/recurring/list
        """
        url = f"{self.__base_url}/recurrence/list"
        if cursor:
            url += f"?cursor={cursor}"
        self.__headers["sign"] = self.__generate_sign()

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)

        return ListOfRecurringPayments(**response['result'])

    async def cancel_recurring_payment(self, uuid: Optional[str] = None, order_id: Optional[str] = None) -> RecurringPayment:
        """Cancel recurring payment
        
        :param uuid: Recurrence uuid.
        :param order_id: Order ID in your system.

        Docs: https://doc.cryptomus.com/business/recurring/cancel
        """
        url = f"{self.__base_url}/recurrence/cancel"
        params = {
            "uuid": uuid,
            "order_id": order_id,
        }
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, json=params, headers=self.__headers)

        return RecurringPayment(**response['result'])

    async def exchange_rates_list(self, currency: str) -> List[ExchangeRatesList]:
        """Exchange rates list.
        
        Docs: https://doc.cryptomus.com/business/exchange-rates/list
        """
        url = f"{self.__base_url}/exchange-rate/{currency}/list"
        self.__headers["sign"] = self.__generate_sign()

        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)

        return [ExchangeRatesList(**rate) for rate in response["result"]]

    async def list_of_discounts(self) -> List[Discount]:
        """List of discounts.
        
        Docs: https://doc.cryptomus.com/business/discount/list
        """
        url = f"{self.__base_url}/payment/discount/list"
        self.__headers["sign"] = self.__generate_sign()

        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)

        return [Discount(**discount) for discount in response["result"]]
    
    async def set_discount_to_payment_method(self, currency: str, network: str, discount_percent: int) -> Discount:
        """Set discount to payment method. 
        
        :param currency: Currency code.
        :param network: Blockchain network code.
        :param discount_percent: Discount percent.

        Docs: https://doc.cryptomus.com/business/discount/set
        """
        url = f"{self.__base_url}/payment/discount/set"
        params = {
            "currency": currency,
            "network": network,
            "discount_percent": discount_percent,
        }
        self.__headers["sign"] = self.__generate_sign(params)

        response = await self._request(self.__payment_name, self.__post_method, url, json=params, headers=self.__headers)

        return Discount(**response["result"])