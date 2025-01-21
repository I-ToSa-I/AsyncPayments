from ..requests import RequestsClient
from typing import Optional, List
from .models import AppInfo, Transfer, Withdrawal, WithdrawalFees, MultiCheque, MultiChequesList, Invoice, InvoicesList, Currency, \
                    Subscription, SubscriptionsList, SubscriptionCheck, Subscriptions
from urllib.parse import urlencode


class AsyncXRocket(RequestsClient):
    API_HOST: str = "https://t.me/tonRocketBot"

    def __init__(self, apiKey: str) -> None:
        """
        Initialize XRocket API client
        :param apiKey: Your API key
        """
        super().__init__()
        self.__api_key = apiKey
        self.__headers = {
            "Content-Type": "application/json",
            "Rocket-Pay-Key": self.__api_key,
        }
        self.__base_url = "https://pay.xrocket.tg"
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
        
        Docs: https://pay.xrocket.tg/api/#/app/AppsController_getAppInfo"""
        url = f"{self.__base_url}/app/info"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return AppInfo(**response['data'])

    async def transfer(self, tgUserId: int, currency: str, amount: float, transferId: str, description: Optional[str] = "") -> Transfer:
        """Make transfer of funds to another user.
        
        :param tgUserId: Telegram user ID. If we dont have this user in DB, we will fail transaction with error: 400 - User not found.
        :param currency: Currency of transfer, info with function get_available_currencies().
        :param amount: Transfer amount. 9 decimal places, others cut off.
        :param transferId: Unique transfer ID in your system to prevent double spends.
        :description: Transfer description.

        Docs: https://pay.xrocket.tg/api/#/app/AppsController_transfer"""
        url = f"{self.__base_url}/app/transfer"
        params = {
            "tgUserId": tgUserId,
            "currency": currency,
            "amount": amount,
            "transferId": transferId,
            "description": description,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)
        return Transfer(**response['data'])
    
    async def withdrawal(self, network: str, address: str, currency: str, amount: float, withdrawalId: str, comment: Optional[str] = "") -> Withdrawal:
        """Make withdrawal of funds to external wallet.
        
        :param network: Network code.
        :param address: Withdrawal address.
        :param currency: Currency code.
        :param amount: Withdrawal amount. 9 decimal places, others cut off.
        :param withdrawalId: Unique withdrawal ID in your system to prevent double spends.
        :param comment: Withdrawal comment.

        Docs: https://pay.xrocket.tg/api/#/app/AppsController_withdrawal"""
        url = f"{self.__base_url}/app/withdrawal"
        params = {
            "network": network,
            "address": address,
            "currency": currency,
            "amount": amount,
            "withdrawalId": withdrawalId,
            "comment": comment,
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)
        return Withdrawal(**response['data'])
    
    async def withdrawal_status(self, withdrawalId: str) -> Withdrawal:
        """Returns withdrawal status.
        
        Docs: https://pay.xrocket.tg/api/#/app/AppsController_getWithdrawalStatus"""
        url = f"{self.__base_url}/app/withdrawal/status/{withdrawalId}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return Withdrawal(**response['data'])
    
    async def withdrawal_fees(self, currency: Optional[str] = None) -> List[WithdrawalFees]:
        """Returns withdrawal fees.
        
        Docs: https://pay.xrocket.tg/api/#/app/AppsController_getWithdrawalFees"""
        url = f"{self.__base_url}/app/withdrawal/fees"
        params = {
            "currency": currency,
        }
        self._delete_empty_fields(params)
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers, json=params)
        return [WithdrawalFees(**withdrawalFee) for withdrawalFee in response['data']]
    
    async def create_multi_cheque(self, currency: str, chequePerUser: float, usersNumber: int, refProgram: int, password: Optional[str] = None,
                                  description: Optional[str] = None, sendNotifications: Optional[bool] = True, enableCaptcha: Optional[bool] = True,
                                  telegramResourcesIds: Optional[List[str]] = [], forPremium: Optional[bool] = False, linkedWallet: Optional[bool] = False,
                                  disabledLanguages: Optional[List[str]] = [], enabledCountries: Optional[List[str]] = []) -> MultiCheque:
        """Create multi-cheque.

        :param currency: Currency of transfer, info with function get_available_currencies().
        :param chequePerUser: Cheque amount for one user. 9 decimal places, others cut off.
        :param usersNumber: Number of users to save multicheque. 0 decimal places.
        :param refProgram: Referral program percentage (%). 0 decimal places.
        :param password: Password for cheque.
        :param description: Description for cheque.
        :param sendNotifications: Send notifications about activations.
        :param enableCaptcha: Enable captcha.
        :param telegramResourcesIds: IDs of telegram resources (groups, channels, private groups).
        :param forPremium: Only users with Telegram Premium can activate this cheque.
        :param linkedWallet: Only users with linked wallet can activate this cheque.
        :param disabledLanguages: Disable languages.
        :param enabledCountries: Enabled countries (AsyncPayments.xrocket.models.CountriesName).
        
        Docs: https://pay.xrocket.tg/api/#/multi-cheque/ChequesController_createCheque"""
        url = f"{self.__base_url}/multi-cheque"
        params = {
            "currency": currency,
            "chequePerUser": chequePerUser,
            "usersNumber": usersNumber,
            "refProgram": refProgram,
            "password": password,
            "description": description,
            "sendNotifications": sendNotifications,
            "enableCaptcha": enableCaptcha,
            "telegramResourcesIds": telegramResourcesIds,
            "forPremium": forPremium,
            "linkedWallet": linkedWallet,
            "disabledLanguages": disabledLanguages,
            "enabledCountries": enabledCountries,
        }
        self._delete_empty_fields(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)
        return MultiCheque(**response['data'])
    
    async def multi_cheques_list(self, limit: Optional[int] = 100, offset: Optional[int] = 0) -> MultiChequesList:
        """Get list of multi-cheques.
        
        :param limit: Limit of cheques.
        :param offset: Offset.

        Docs: https://pay.xrocket.tg/api/#/multi-cheque/ChequesController_getCheques"""
        params = {
            "limit": limit,
            "offset": offset,
        }
        url = f"{self.__base_url}/multi-cheque?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return MultiChequesList(**response['data'])
    
    async def get_multi_cheque_info(self, cheque_id: int) -> MultiCheque:
        """Get multi-cheque info.
        
        :param cheque_id: ID of cheque.

        Docs: https://pay.xrocket.tg/api/#/multi-cheque/ChequesController_getCheque"""
        url = f"{self.__base_url}/multi-cheque/{cheque_id}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return MultiCheque(**response['data'])
    
    async def edit_multi_cheque(self, cheque_id: int, password: Optional[str] = None, description: Optional[str] = None,
                                sendNotifications: Optional[bool] = None, enableCaptcha: Optional[bool] = None, 
                                telegramResourcesIds: Optional[List[str]] = None, forPremium: Optional[bool] = None,
                                linkedWallet: Optional[bool] = None, disabledLanguages: Optional[List[str]] = None,
                                enabledCountries: Optional[List[str]] = None) -> MultiCheque:
        """Edit multi-cheque.
        
        :param cheque_id: ID of cheque.
        :param password: Password for cheque.
        :param description: Description for cheque.
        :param sendNotifications: Send notifications about activations.
        :param enableCaptcha: Enable captcha.
        :param telegramResourcesIds: IDs of telegram resources (groups, channels, private groups).
        :param forPremium: Only users with Telegram Premium can activate this cheque.
        :param linkedWallet: Only users with linked wallet can activate this cheque.
        :param disabledLanguages: Disable languages.
        :param enabledCountries: Enabled countries (AsyncPayments.xrocket.models.CountriesName).
        
        
        Docs: https://pay.xrocket.tg/api/#/multi-cheque/ChequesController_editCheque"""
        params = {
            "password": password,
            "description": description,
            "sendNotifications": sendNotifications,
            "enableCaptcha": enableCaptcha,
            "telegramResourcesIds": telegramResourcesIds,
            "forPremium": forPremium,
            "linkedWallet": linkedWallet,
            "disabledLanguages": disabledLanguages,
            "enabledCountries": enabledCountries,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/multi-cheque/{cheque_id}"
        response = await self._request(self.__payment_name, self.__put_method, url, headers=self.__headers, json=params)
        return MultiCheque(**response['data'])
    
    async def delete_multi_cheque(self, cheque_id: int) -> bool:
        """Delete multi-cheque.
        
        :param cheque_id: ID of cheque.

        Docs: https://pay.xrocket.tg/api/#/multi-cheque/ChequesController_deleteCheque"""
        url = f"{self.__base_url}/multi-cheque/{cheque_id}"
        response = await self._request(self.__payment_name, self.__delete_method, url, headers=self.__headers)
        return True if response['success'] else False
    
    async def create_invoice(self, numPayments: int, currency: str, amount: Optional[float] = None, minPayment: Optional[int] = None, 
                             description: Optional[str] = None, hiddenMessage: Optional[str] = None, commentsEnabled: Optional[bool] = None,
                             callbackUrl: Optional[str] = None, payload: Optional[str] = None, expiredIn: Optional[int] = None) -> Invoice:
        """Create invoice.
        
        :param numPayments: Num payments for invoice.
        :param currency: Currency of transfer, info with function get_available_currencies().
        :param amount: Invoice amount. 9 decimal places, others cut off.
        :param minPayment: Min payment only for multi invoice if invoice amount is None.
        :param description: Description for invoice.
        :param hiddenMessage: Hidden message after invoice is paid.
        :param commentsEnabled: Allow comments.
        :param callbackUrl: Url for Return button after invoice is paid.
        :param payload: Any data. Invisible to user, will be returned in callback.
        :param expiredIn: Invoice expire time in seconds, max 1 day, 0 - None expired.

        Docs: https://pay.xrocket.tg/api/#/tg-invoices/InvoicesController_createInvoice"""
        params = {
            "numPayments": numPayments,
            "currency": currency,
            "amount": amount,
            "minPayment": minPayment,
            "description": description,
            "hiddenMessage": hiddenMessage,
            "commentsEnabled": commentsEnabled,
            "callbackUrl": callbackUrl,
            "payload": payload,
            "expiredIn": expiredIn,
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/tg-invoices"
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)
        return Invoice(**response['data'])
    
    async def get_list_invoices(self, limit: Optional[int] = 100, offset: Optional[int] = 0) -> InvoicesList:
        """Get list of invoices.
        
        :param limit: Limit of invoices.
        :param offset: Offset.

        Docs: https://pay.xrocket.tg/api/#/tg-invoices/InvoicesController_getInvoices"""
        params = {
            "limit": limit,
            "offset": offset,
        }
        url = f"{self.__base_url}/tg-invoices?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return InvoicesList(**response['data'])
    
    async def get_invoice_info(self, invoice_id: str) -> Invoice:
        """Get invoice info.
        
        :param invoice_id: ID of invoice.
        
        Docs: https://pay.xrocket.tg/api/#/tg-invoices/InvoicesController_getInvoice"""
        url = f"{self.__base_url}/tg-invoices/{invoice_id}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return Invoice(**response['data'])
    
    async def delete_invoice(self, invoice_id: str) -> bool:
        """Delete invoice.
        
        :param invoice_id: ID of invoice.

        Docs: https://pay.xrocket.tg/api/#/tg-invoices/InvoicesController_deleteInvoice"""
        url = f"{self.__base_url}/tg-invoices/{invoice_id}"
        response = await self._request(self.__payment_name, self.__delete_method, url, headers=self.__headers)
        return True if response['success'] else False

    async def get_challenge(self, challenge_id: str, user_id: str) -> str:
        """Get challenge amount by user id.
        
        :param challenge_id: ID of the challenge.
        :param user_id: Telegram ID of the user.

        Docs: https://pay.xrocket.tg/api/#/challenges/ChallengesController_getTradeAmount
        
        :return: Amount in USD."""
        url = f"{self.__base_url}/challenges/{challenge_id}/users/{user_id}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return response['data']['amountUsd']
    
    async def get_available_currencies(self) -> List[Currency]:
        """Returns available currencies.
        
        Docs: https://pay.xrocket.tg/api/#/currencies/CurrenciesController_getCoins"""
        url = f"{self.__base_url}/currencies/available"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return [Currency(**currency) for currency in response['data']['results']]
    
    async def create_subscription(self, interval: str, amount: float, status: str, referralPercent: int, currency: str, name: Optional[str] = None,
                                  description: Optional[str] = None, tgResource: Optional[str] = None, returnUrl: Optional[str] = None) -> Subscription:
        """Create subscription.
        
        :param interval: Interval for subscription (AsyncPayments.xrocket.models.SubscriptionsIntervals).
        :param amount: Cost subscription for current interval in currency.
        :param status: Status for subscription (AsyncPayments.xrocket.models.SubscriptionsStatuses).
        :param referralPercent: Subscription referral percent.
        :param currency: Subscription currency.
        :param name: Subscription name, view in bot.
        :param description: Subscription description, view in bot.
        :param tgResource: Subscription TG resource.
        :param returlUrl: Return link after payment.
        
        Docs: https://pay.xrocket.tg/api/#/subscriptions/SubscriptionsController_createSubscription"""
        params = {
            "name": name,
            "description": description,
            "currency": currency,
            "interval": [
                {
                "interval": interval,
                "amount": amount,
                "status": status
                }
            ],
            "tgResource": tgResource,
            "referralPercent": referralPercent,
            "returnUrl": returnUrl
        }
        self._delete_empty_fields(params)
        url = f"{self.__base_url}/subscriptions"
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)
        return Subscription(**response['data'])

    async def get_list_subscriptions(self, limit: Optional[int] = 100, offset: Optional[int] = 0) -> SubscriptionsList:
        """Get list of subscription.
        
        :param limit: Limit of subscriptions.
        :param offset: Offset.

        Docs: https://pay.xrocket.tg/api/#/subscriptions/SubscriptionsController_getSubscriptions"""
        params = {
            "limit": limit,
            "offset": offset,
        }
        url = f"{self.__base_url}/subscriptions?{urlencode(params)}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return SubscriptionsList(**response['data'])

    async def get_subscription_info(self, subscription_id: int) -> Subscription:
        """Get subscription info.
        
        :param subscription_id: ID of the subscription.

        Docs: https://pay.xrocket.tg/api/#/subscriptions/SubscriptionsController_getSubscription"""
        url = f"{self.__base_url}/subscriptions/{subscription_id}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return Subscription(**response['data'])
    
    async def delete_subscription(self, subscription_id: int) -> bool:
        """Delete subscription.
        
        :param subscription_id: ID of the subscription.

        Docs: https://pay.xrocket.tg/api/#/subscriptions/SubscriptionsController_deleteSubscription"""
        url = f"{self.__base_url}/subscriptions/{subscription_id}"
        response = await self._request(self.__payment_name, self.__delete_method, url, headers=self.__headers)
        return True if response['success'] else False
    
    async def check_subscription(self, subscription_id: int, user_id: int) -> SubscriptionCheck:
        """Delete subscription.
        
        :param subscription_id: ID of the subscription.
        :param user_id: ID of the user.

        Docs: https://pay.xrocket.tg/api/#/subscriptions/SubscriptionsController_checkSubscription"""
        params = {
            "userId": user_id,
        }
        url = f"{self.__base_url}/subscriptions/check/{subscription_id}"
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, json=params)
        return SubscriptionCheck(**response['data'])
    
    async def get_subscription_interval_info(self, subscription_id: int, interval_code: str) -> Subscriptions.Interval:
        """Get subscription interval info.
        
        :param subscription_id: ID of the subscription.
        :param interval_code: Code of the interval.

        Docs: https://pay.xrocket.tg/api/#/subscriptions/SubscriptionsController_getSubscriptionInterval"""
        url = f"{self.__base_url}/subscriptions/{subscription_id}/interval/{interval_code}"
        response = await self._request(self.__payment_name, self.__get_method, url, headers=self.__headers)
        return Subscriptions.Interval(**response['data'])

    async def edit_subscription_interval(self, subscription_id: int, interval_code: str, status: str) -> Subscriptions.Interval:
        """Edit subscription interval.
        
        :param subscription_id: ID of the subscription.
        :param interval_code: Code of the interval.
        :param status: Status for subscription (AsyncPayments.xrocket.models.SubscriptionsStatuses).

        Docs: https://pay.xrocket.tg/api/#/subscriptions/SubscriptionsController_editSubscriptionInterval"""
        params = {
            "status": status
        }
        url = f"{self.__base_url}/subscriptions/{subscription_id}/interval/{interval_code}"
        response = await self._request(self.__payment_name, self.__put_method, url, headers=self.__headers, json=params)
        return Subscriptions.Interval(**response['data'])
    
    async def delete_subscription_interval(self, subscription_id: int, interval_code: str) -> Subscriptions.Interval:
        """Delete subscription interval.
        
        :param subscription_id: ID of the subscription.
        :param interval_code: Code of the interval.

        Docs: https://pay.xrocket.tg/api/#/subscriptions/SubscriptionsController_deleteSubscriptionInterval"""
        url = f"{self.__base_url}/subscriptions/{subscription_id}/interval/{interval_code}"
        response = await self._request(self.__payment_name, self.__delete_method, url, headers=self.__headers)
        return Subscriptions.Interval(**response['data'])
    
    async def create_subscription_interval(self, subscription_id: int, interval: str, amount: float, status: str) -> Subscriptions.Interval:
        """Create subscription interval.
        
        :param subscription_id: ID of the subscription.
        :param interval: Interval for subscription (AsyncPayments.xrocket.models.SubscriptionsIntervals).
        :param amount: Cost subscription for current interval in currency.
        :param status: Status for subscription (AsyncPayments.xrocket.models.SubscriptionsStatuses).

        Docs: https://pay.xrocket.tg/api/#/subscriptions/SubscriptionsController_creteSubscriptionInterval"""
        params = {
            "interval": interval,
            "amount": amount,
            "status": status,
        }
        url = f"{self.__base_url}/subscriptions/{subscription_id}"
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)
        return Subscriptions.Interval(**response['data'])