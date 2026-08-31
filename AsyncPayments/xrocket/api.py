from ..requests import RequestsClient
from typing import Optional, List
from .models import (AppInfo, Balance, Health, Invoice, InvoicesList, InvoicePayments, InvoicePaymentAddress, Cheque, ChequesList, Payout, PayoutsList,
                     MassPayouts, Withdrawal, WithdrawalsList, WithdrawalQuotas, WithdrawalLink, Currency, Rate)
from urllib.parse import urlencode


class AsyncXRocket(RequestsClient):
    API_HOST: str = "https://t.me/tonRocketBot"

    def __init__(self, apiKey: str, is_testnet: bool = False) -> None:
        """
        Initialize XRocket API client
        :param apiKey: Your API key
        """
        super().__init__()
        self.__api_key = apiKey
        self.__headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.__api_key}",
        }
        if is_testnet:
            self.__base_url = "https://pay.api.testnet.xrocket.exchange/api/v1"
            self.__base_url_without_api_version = "https://pay.api.testnet.xrocket.exchange"
        else:
            self.__base_url = "https://pay.api.xrocket.exchange/api/v1"
            self.__base_url_without_api_version = "https://pay.api.xrocket.exchange"
        self.__post_method = "POST"
        self.__get_method = "GET"
        self.__put_method = "PUT"
        self.__delete_method = "DELETE"
        self.__payment_name = "xrocket"
        self.check_values()

    def check_values(self):
        if not self.__api_key:
            raise ValueError('No API key specified')
        
    async def get_app_info(self) -> AppInfo:
        """Returns information about your application.
        
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/app-controller-get-app"""
        url = f"{self.__base_url}/app-info"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return AppInfo(**response)
    
    async def get_balances(self) -> List[Balance]:
        """Get balances of your application.
                
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/app-controller-get-app-balances"""
        url = f"{self.__base_url}/balances"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return [Balance(**balance) for balance in response['balances']]
    
    async def check_health(self) -> Health:
        """Health check.
                        
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/health-controller-health"""
        url = f"{self.__base_url_without_api_version}/health"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return Health(**response)
    
    async def create_invoice(self, priceCurrency: str, priceAmount: Optional[str] = None, minPayment: Optional[int] = None,
                             numPayments: Optional[int] = 1, payoutCurrency: Optional[str] = None, payCurrencies: Optional[List[str]] = None,
                             clientInvoiceId: Optional[str] = None, description: Optional[str] = None, expiresIn: Optional[int] = None,
                             callback: Optional[dict] = None, url: Optional[dict] = None, customer: Optional[dict] = None, 
                             isFeePaidByUser: Optional[bool] = False, data: Optional[dict] = None, platformId: Optional[str] = None) -> Invoice:
        """Create invoice.
        
        :param priceCurrency: Required. Invoice price currency (crypto or fiat).
        :param priceAmount: Optional. Fixed invoice amount. Pass either priceAmount or minPayment, never both and never neither — omitting both fails with missing_invoice_amount, passing both with amount_conflict. The value is range-checked against the per-asset limits.
        :param minPayment: Optional. Minimum payment for an open-amount invoice (the payer chooses the amount). Mutually exclusive with priceAmount — exactly one of the two is required.
        :param numPayments: Optional. Num payments for invoice.
        :param payoutCurrency: Optional. Invoice payout crypto currency.
        :param payCurrencies: Optional. Currencies the payer may use. Multi-currency invoices are not implemented yet: if provided, this array must contain exactly one code equal to priceCurrency, otherwise the request fails with not_implemented.
        :param clientInvoiceId: Optional. Client Invoice ID as assigned by the client.
        :param description: Optional. Description for invoice.
        :param expiresIn: Optional. Invoice lifetime in seconds from creation. Pass 0 for an invoice that never expires; expiresAt is then null. Omitting the field does not mean "never expires" — it falls back to a default of 3600000 seconds (~41 days), so always send an explicit value.
        :param callback: Optional. Webhook URL for this invoice; overrides the application-wide webhook URL. {"callbackUrl": <str>, "payload": <dict>}
        :param url: Optional. User redirect urls. {"successUrl": <str>, "cancelUrl": <str>}.
        :param customer: Optional. Customer info. {"id": <str>, "email": <str>, "telegramId": <str>, telegramUsername": <str>}
        :param isFeePaidByUser: Optional. If true, the user pays a commission.
        :param data: Optional. Custom user data passed through and returned in callbacks/webhooks (max size 4KB).
        :param platformId: Optional. Platform identifier.

        Docs: https://docs.xrocket.exchange/api/pay/reference/http/invoice-controller-create-invoice"""
        params = {
            "priceCurrency": priceCurrency,
            "priceAmount": priceAmount,
            "minPayment": minPayment,
            "numPayments": numPayments,
            "payoutCurrency": payoutCurrency,
            "payCurrencies": payCurrencies,
            "clientInvoiceId": clientInvoiceId,
            "description": description,
            "expiresIn": expiresIn,
            "callback": callback,
            "url": url,
            "customer": customer,
            "isFeePaidByUser": isFeePaidByUser,
            "data": data,
            "platformId": platformId,
        }
        self._delete_empty_fields(params)
        request_url = f"{self.__base_url}/invoices"
        response = await self._request(self.__payment_name, self.__post_method, request_url, headers=self.__headers, json=params)
        return Invoice(**response)

    async def get_list_invoices(self, asset: Optional[str] = None, fiat: Optional[str] = None, ids: Optional[List[str]] = None, 
                                status: Optional[str] = None, cursor: Optional[str] = None, limit: Optional[int] = None) -> InvoicesList:
        """Get list of invoices.
        
        :param asset: Optional. Filtering invoices by asset.
        :param fiat: Optional. Filtering invoices by fiat.
        :param ids: Optional. Filtering invoices by ids.
        :param status: Optional. Filtering invoices by status.
        :param cursor: Optional. Cursor for pagination.
        :param limit: Optional. Limit. Possible values: <= 1000.
                                
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/invoice-controller-get-invoices"""
        params = {
            "asset": asset,
            "fiat": fiat,
            "ids": ids,
            "status": status,
            "cursor": cursor,
            "limit": limit,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/invoices?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return InvoicesList(**response)
    
    async def get_invoice_info(self, invoiceId: Optional[str] = None, clientInvoiceId: Optional[str] = None) -> Invoice:
        """Get invoice info.
        
        :param invoiceId: xRocket Invoice ID. Either invoiceId or clientInvoiceId is required. If both are passed, invoiceId will be used.
        :param clietnInvoiceId: Client Invoice ID assigned by the client. Either invoiceId or clientInvoiceId is required.
        
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/invoice-controller-get-invoice"""
        params = {
            "invoiceId": invoiceId,
            "clientInvoiceId": clientInvoiceId,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/invoice?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return Invoice(**response)
    
    async def get_invoice_payments(self, invoiceId: Optional[str] = None, clientInvoiceId: Optional[str] = None,
                                   cursor: Optional[str] = None, limit: Optional[int] = None) -> InvoicePayments:
        """Returns payments of an invoice in the same format as the payment_status_changed webhook. Either invoiceId (xRocket) or clientInvoiceId (client-assigned) is required. If both are passed, invoiceId will be used.
        
        :param invoiceId: xRocket Invoice ID. Either invoiceId or clientInvoiceId is required. If both are passed, invoiceId will be used.
        :param clietnInvoiceId: Client Invoice ID assigned by the client. Either invoiceId or clientInvoiceId is required.
        :param cursor: Cursor for pagination.
        :param limit: Limit. Possible values: <= 1000.
        
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/invoice-controller-get-invoice"""
        params = {
            "invoiceId": invoiceId,
            "clientInvoiceId": clientInvoiceId,
            "cursor": cursor,
            "limit": limit,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/invoice/payments?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return InvoicePayments(**response)

    async def delete_invoice(self, invoiceId: Optional[str] = None, clientInvoiceId: Optional[str] = None) -> bool:
        """Delete invoice. Either invoiceId (xRocket) or clientInvoiceId (client-assigned) is required. If both are passed, invoiceId will be used.
        
        :param invoiceId: xRocket Invoice ID. Either invoiceId or clientInvoiceId is required. If both are passed, invoiceId will be used.
        :param clientInvoiceId: Client Invoice ID assigned by the client. Either invoiceId or clientInvoiceId is required.

        Docs: https://docs.xrocket.exchange/api/pay/reference/http/invoice-controller-delete-invoice"""
        params = {
            "invoiceId": invoiceId,
            "clientInvoiceId": clientInvoiceId,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/invoice?{urlencode(params)}"
        return await self._request(self.__payment_name, self.__delete_method, url, headers=self.__headers)
    
    async def create_invoice_payment_address(self, payNetwork: str, invoiceId: Optional[str] = None, 
                                             clientInvoiceId: Optional[str] = None) -> InvoicePaymentAddress:
        """Create invoice payment address.
                
        :param payNetwork: Required. Network code for payment.
        :param invoiceId: Optional. xRocket Invoice ID. Either invoiceId or clientInvoiceId is required. If both are passed, invoiceId will be used.
        :param clientInvoiceId: Optional. Client Invoice ID assigned by the client. Either invoiceId or clientInvoiceId is required.

        Docs: https://docs.xrocket.exchange/api/pay/reference/http/invoice-payment-controller-create-invoice-payment-address"""
        params = {
            "invoiceId": invoiceId,
            "clientInvoiceId": clientInvoiceId,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/invoices/payments/address?{urlencode(params)}"
        response =  await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json={ "payNetwork": payNetwork })
        return InvoicePaymentAddress(**response)
    
    async def create_cheque(self, asset: str, amount: str, clientChequeId: Optional[str] = None, password: Optional[str] = None,
                            description: Optional[str] = None, callback: Optional[dict] = None, url: Optional[dict] = None,
                            targetType: Optional[str] = None, target: Optional[str] = None) -> Cheque:
        """Issue a personal cheque to perform an accept-type payout. The amount is reserved from the application balance and can be redeemed by the recipient or cancelled before redemption. When targetType and target are set, only the addressed user is allowed to redeem the cheque.
                        
        :param asset: Required. Unique cheque ID in your system to prevent double spends. Possible values: <= 50 characters.
        :param amount: Required. Currency of transfer.
        :param clientChequeId: Optional. Cheque amount.
        :param password: Optional. Cheque password, the recipient has to enter it to redeem the cheque. Possible values: <= 100 characters.
        :param description: Optional. Description for cheque. Possible values: <= 1000 characters.
        :param callback: Optional. Webhook settings for cheque activation updates. {"callbackUrl": <str>, "payload": <dict>}
        :param url: Optional. User redirect urls after cheque activation. {"successUrl": <str>, "cancelUrl": <str>}
        :param targetType: Optional. Target type for cheque, has to be passed together with target. Possible values: [user_id, telegram_user_id, telegram_username].
        :param target: Optional. Target for cheque, has to be passed together with targetType. Possible values: <= 100 characters.

        Docs: https://docs.xrocket.exchange/api/pay/reference/http/cheque-controller-create-cheque"""
        
        params = {
            "asset": asset,
            "amount": amount,
            "clientChequeId": clientChequeId,
            "password": password,
            "description": description,
            "callback": callback,
            "url": url,
            "targetType": targetType,
            "target": target,
        }
        self._delete_empty_fields(params)
        request_url = f"{self.__base_url}/cheques"
        response =  await self._request(self.__payment_name, self.__post_method, request_url, headers=self.__headers, json=params)
        return Cheque(**response)
    
    async def get_list_cheques(self, fromDate: Optional[str] = None, toDate: Optional[str] = None, targetType: Optional[str] = None, 
                               target: Optional[str] = None, state: Optional[str] = None, cursor: Optional[str] = None, 
                               limit: Optional[int] = None) -> ChequesList:
        """List personal cheques issued for accept-type transfers. Use this to monitor pending, redeemed, or cancelled cheques. Cancelled cheques are excluded from the list.
        
        :param fromDate: Optional. From date (ISO 8601).
        :param toDate: Optional. To date (ISO 8601).
        :param targetType: Optional. Target type for cheque, has to be passed together with target. Possible values: [user_id, telegram_user_id, telegram_username].
        :param target: Optional. Target identifier for cheque (depends on targetType), has to be passed together with targetType.
        :param state: Optional. Cheque state. Possible values: [active, completed, draft, error].
        :param cursor: Optional. Cursor for pagination.
        :param limit: Optional. Limit. Possible values: >= 1 and <= 1000.
                                
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/cheque-controller-get-cheques"""
        params = {
            "fromDate": fromDate,
            "toDate": toDate,
            "targetType": targetType,
            "target": target,
            "state": state,
            "cursor": cursor,
            "limit": limit,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/cheques?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return ChequesList(**response)
    
    async def get_cheque_info(self, chequeId: Optional[str] = None, clientChequeId: Optional[str] = None) -> Cheque:
        """Fetch details of a personal cheque used for an accept-type payout, including status and reserved amount. A cancelled cheque is returned with the deleted flag set.
        
        :param chequeId: xRocket Cheque ID. Either chequeId or clientChequeId is required. If both are passed, chequeId will be used.
        :param clientChequeId: Client Cheque ID assigned by the client. Either chequeId or clientChequeId is required.
        
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/cheque-controller-get-cheque"""
        params = {
            "chequeId": chequeId,
            "clientChequeId": clientChequeId,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/cheque?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return Cheque(**response)
    
    async def update_cheque(self, description: str, chequeId: Optional[str] = None, clientChequeId: Optional[str] = None) -> Cheque:
        """Modify an active unredeemed cheque. Only description can be updated, pass an empty string to clear it. The cheque must be in active state, not cancelled and not yet redeemed.
        
        :param description: Cheque description (set empty string to clear description).
        :param chequeId: xRocket Cheque ID. Either chequeId or clientChequeId is required. If both are passed, chequeId will be used.
        :param clientChequeId: Client Cheque ID assigned by the client. Either chequeId or clientChequeId is required.
        
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/cheque-controller-get-cheque"""
        params = {
            "chequeId": chequeId,
            "clientChequeId": clientChequeId,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/cheques?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__put_method, url, headers=self.__headers, json={ "description": description })
        return Cheque(**response)
    
    async def delete_cheque(self, chequeId: Optional[str] = None, clientChequeId: Optional[str] = None) -> bool:
        """Cancel an unredeemed personal cheque. Upon cancellation, the reserved funds are released back to the application balance.
        
        :param chequeId: xRocket Cheque ID. Either chequeId or clientChequeId is required. If both are passed, chequeId will be used.
        :param clientChequeId: Client Cheque ID assigned by the client. Either chequeId or clientChequeId is required.

        Docs: https://docs.xrocket.exchange/api/pay/reference/http/cheque-controller-delete-cheque"""
        params = {
            "chequeId": chequeId,
            "clientChequeId": clientChequeId,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/cheques?{urlencode(params)}"
        return await self._request(self.__payment_name, self.__delete_method, url, headers=self.__headers)
    
    async def create_payout(self, clientPayoutId: str, target: str, targetType: str, asset: str, amount: str, 
                                   description: Optional[str] = None, callback: Optional[dict] = None) -> Payout:
        """Payout funds to user.
                            
        :param clientPayoutId: Required. Unique payout ID in your system to prevent double spends.
        :param target: Required. Target.
        :param targetType: OptRequiredional. Target type. Possible values: [user_id, telegram_user_id, telegram_username].
        :param asset: Required. Asset of transfer.
        :param amount: Required. Payout amount.
        :param description: Optional. Payout description.
        :param callback: Optional. Webhook settings for payout status updates. {"callbackUrl": <str>, "payload": <dict>}

        Docs: https://docs.xrocket.exchange/api/pay/reference/http/payout-controller-payout"""
        
        params = {
            "clientPayoutId": clientPayoutId,
            "target": target, 
            "targetType": targetType,
            "asset": asset,
            "amount": amount,
            "description": description,
            "callback": callback,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/payouts"
        response =  await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)
        return Payout(**response)
    
    async def get_list_payouts(self, fromDate: Optional[str] = None, toDate: Optional[str] = None, 
                               cursor: Optional[str] = None, limit: Optional[int] = None) -> PayoutsList:
        """Get payouts list.
        
        :param fromDate: Optional. From date (ISO 8601).
        :param toDate: Optional. To date (ISO 8601).
        :param cursor: Optional. Cursor for pagination.
        :param limit: Optional. Limit. Possible values: >= 1 and <= 1000.
                                
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/payout-controller-get-list-payouts"""
        params = {
            "fromDate": fromDate,
            "toDate": toDate,
            "cursor": cursor,
            "limit": limit,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/payouts?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return PayoutsList(**response)
    
    async def get_payout_info(self, payoutId: Optional[str] = None, clientPayoutId: Optional[str] = None) -> Payout:
        """Get payout info.
        
        :param payoutId: xRocket Payout ID. Either payoutId or clientPayoutId is required. If both are passed, payoutId will be used.
        :param clientPayoutId: Client Payout ID assigned by the client. Either payoutId or clientPayoutId is required.
        
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/cheque-controller-get-cheque"""
        params = {
            "payoutId": payoutId,
            "clientPayoutId": clientPayoutId,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/payout?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return Payout(**response)
    
    async def create_mass_payouts(self, asset: str, payouts: list) -> MassPayouts:
        """Create mass payouts (Telegram users only).
                            
        :param asset: Required. Asset of transfer.
        :param payouts: Required. List of payouts to process. Between 1 and 500 entries per request. Example - [{ "target": "87209764", "targetType": "telegram_user_id", "amount": "1.23", "clientPayoutId": "abc-def", "description": "Monthly payroll", "callback": { "callbackUrl": "https://example.com/webhooks/payout", "payload": {} } }]

        Docs: https://docs.xrocket.exchange/api/pay/reference/http/mass-payouts-controller-create-mass-payouts"""
        
        params = {
            "asset": asset,
            "payouts": payouts,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/mass-payouts"
        response =  await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)
        return MassPayouts(**response)
    
    async def create_withdrawal_to_external_wallet(self, clientWithdrawalId: str, network: str, address: str, asset: str, amount: str,
                                                   comment: Optional[str] = None, callback: Optional[dict] = None) -> Withdrawal:
        """Withdrawal funds from application to external wallet.
                       
        :param clientWithdrawalId: Required. Unique withdrawal ID in your system to prevent double spends.
        :param network: address: Required. Network code. Possible values: [TON, BSC, ETH, BTC, TRX, SOL].
        :param address: Required. Withdrawal address.
        :param asset: Required. Asset code.
        :param amount: Required. Withdrawal amount.            
        :param comment: Optional. Withdrawal comment.
        :param callback: Optional. Webhook settings for withdrawal status updates. {"callbackUrl": <str>, "payload": <dict>}.

        Docs: https://docs.xrocket.exchange/api/pay/reference/http/withdrawal-controller-create-withdrawal"""
        
        params = {
            "clientWithdrawalId": clientWithdrawalId,
            "network": network,
            "address": address,
            "asset": asset,
            "amount": amount,
            "comment": comment,
            "callback": callback,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/withdrawals"
        response =  await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)
        return Withdrawal(**response)
    
    async def get_list_withdrawals(self, fromDate: Optional[str] = None, toDate: Optional[str] = None, status: Optional[str] = None,
                                   cursor: Optional[str] = None, limit: Optional[int] = None) -> WithdrawalsList:
        """Get application withdrawals.
        
        :param fromDate: Optional. From date (ISO 8601).
        :param toDate: Optional. To date (ISO 8601).
        :param status: Optional. Possible values: [CREATED, COMPLETED, FAIL].
        :param cursor: Optional. Cursor for pagination.
        :param limit: Optional. Limit. Possible values: >= 1 and <= 1000.
                                
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/withdrawal-controller-get-withdrawals"""
        params = {
            "fromDate": fromDate,
            "toDate": toDate,
            "status": status,
            "cursor": cursor,
            "limit": limit,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/withdrawals?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return WithdrawalsList(**response)
    
    async def get_withdrawal_info(self, withdrawalId: Optional[str] = None, clientWithdrawalId: Optional[str] = None) -> Withdrawal:
        """Get withdrawal info.
        
        :param withdrawalId: xRocket Withdrawal ID. Either withdrawalId or clientWithdrawalId is required. If both are passed, withdrawalId will be used.
        :param clientWithdrawalId: Client Withdrawal ID assigned by the client. Either withdrawalId or clientWithdrawalId is required.
        
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/withdrawal-controller-get-withdrawal"""
        params = {
            "withdrawalId": withdrawalId,
            "clientWithdrawalId": clientWithdrawalId,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/withdrawal?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return Withdrawal(**response)
    
    async def get_withdrawal_quotas(self, network: str, asset: str) -> WithdrawalQuotas:
        """Get application withdrawal quotas.
        
        :param network: Network code. Possible values: [TON, BSC, ETH, BTC, TRX, SOL].
        :param asset: Asset code.
        
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/withdrawal-controller-get-withdrawal-fees"""
        params = {
            "network": network,
            "asset": asset,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/withdrawal-quotas?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return WithdrawalQuotas(**response)
    
    async def create_withdrawal_link(self, network: str, address: str, asset: str, amount: str,
                                     comment: Optional[str] = None, platform: Optional[str] = None) -> WithdrawalLink:
        """Create withdrawal link.

        :param network: address: Required. Network code. Possible values: [TON, BSC, ETH, BTC, TRX, SOL].
        :param address: Required. Withdrawal address.
        :param asset: Required. Asset code.
        :param amount: Required. Withdrawal amount.            
        :param comment: Optional. Withdrawal comment.
        :param platform: Optional. Platform identifier (optional, use only if provided by xRocket).

        Docs: https://docs.xrocket.exchange/api/pay/reference/http/withdrawal-links-controller-create-withdrawal-link"""
        
        params = {
            "network": network,
            "address": address,
            "asset": asset,
            "amount": amount,
            "comment": comment,
            "platform": platform,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/withdrawal-link"
        response =  await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)
        return WithdrawalLink(**response)
    
    async def get_available_currencies(self, kind: Optional[str] = None) -> Currency:
        """Get available currencies.
                
        :param kind: Currency kind. Possible values: [crypto, fiat].
        
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/currencies-controller-get-currencies"""
        params = {
            "kind": kind,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/currencies?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return [Currency(**currency) for currency in response]
    
    async def get_currencies_rates(self, base: Optional[str] = None, assets: Optional[list] = None) -> Currency:
        """Get currencies rates.
                
        :param base: Fiat currency.
        :param assets: Asset codes. Example - ["BTC", "USDT"]
        
        Docs: https://docs.xrocket.exchange/api/pay/reference/http/rate-controller-get-rates"""
        params = {
            "base": base,
            "assets": ",".join(assets),
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/rates?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return [Rate(**rate) for rate in response]
