from ..requests import RequestsClient
from typing import Optional
from .models import AccountInfo, OperationHistory, OperationDetails, RequestPayment, ProcessPayment
from urllib.parse import urlencode


class AsyncYoomoney(RequestsClient):
    API_HOST: str = "https://yoomoney.ru"

    def __init__(self, access_token: str) -> None:
        """
        Initialize Yoomoney API client
        :param apiKey: Your API key
        """
        super().__init__()
        self.__access_token = access_token
        self.__headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {self.__access_token}",
        }
        self.__base_url = "https://yoomoney.ru/api"
        self.__post_method = "POST"
        self.__payment_name = "yoomoney"
        self.__payment_name_quick_pay = "yoomoney_quick-pay"
        self.check_values()

    def check_values(self):
        if not self.__access_token:
            raise ValueError('No access token specified')
        
    async def account_info(self) -> AccountInfo:
        """Obtaining information about the user's account status.
        
        Docs: https://yoomoney.ru/docs/wallet/user-account/account-info"""
        url = f"{self.__base_url}/account-info"
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers)
        return AccountInfo(**response)
    
    async def operation_history(self,
                                operation_type: Optional[str] = None,
                                label: Optional[str] = None,
                                date_from: Optional[str] = None,
                                date_till: Optional[str] = None,
                                start_record: Optional[str] = None,
                                records: Optional[int] = None,
                                details: Optional[bool] = None) -> OperationHistory:
        """This method allows you to view transaction history (in whole or in part) page by page. History entries are displayed in reverse chronological order: from most recent to earliest.
        
        :param operation_type: Optional. A list of transaction types to display. Possible values: deposition — account replenishment (income); payment — payments from the account (expense). Transaction types are listed separated by spaces. If this parameter is omitted, all transactions are displayed.
        :param label: Optional. Filtering payments by label value. Payments that have the specified value for the label parameter of the request-payment call are selected.
        :param date_from: Optional. Print transactions from a given time (transactions equal to or later than from ). If the parameter is omitted, all transactions are printed.
        :param date_till: Optional. Display operations up to the time point (operations earlier than 'till'). If the parameter is omitted, all operations are displayed.
        :param start_record: Optional. If this parameter is present, operations will be displayed starting with the start_record number. Operations are numbered starting from 0.
        :param records: Optional. The number of transaction history records to retrieve. Valid values: 1 to 100, default: 30.
        :param details: Optional. Show detailed operation details. Defaults to false. Displaying operation details requires the operation-details permission.
        
        Docs: https://yoomoney.ru/docs/wallet/user-account/operation-history"""
        url = f"{self.__base_url}/operation-history"
        params = {
            "type": operation_type,
            "label": label,
            "from": date_from,
            "till": date_till,
            "start_record": start_record,
            "records": records,
            "details": details
        }
        self._delete_empty_fields(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=urlencode(params))
        return OperationHistory(**response)
    
    async def operation_details(self, operation_id: Optional[str] = None) -> OperationDetails:
        """Allows you to obtain detailed information about an operation from the history.
        
        :param operation_id: Operation ID. The parameter value should be specified as the value of the operation_id parameter in the operation-history method response or the value of the payment_id field in the process-payment method response if the payer's account history is being requested.

        Docs: https://yoomoney.ru/docs/wallet/user-account/operation-details"""
        url = f"{self.__base_url}/operation-details"
        params = {
            "operation_id": operation_id
        }
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=urlencode(params))
        return OperationDetails(**response)
    
    async def request_payment(self, 
                              to: str,
                              amount: float,
                              amount_due: Optional[float] = None,
                              comment: Optional[str] = None,
                              message: Optional[str] = None,
                              label: Optional[str] = None,
                              ) -> RequestPayment:
        """Create a payment, check the parameters, and verify that the store can accept the payment or transfer funds to the user's YooMoney account.
        
        :param to: Recipient ID (account number, phone number or email).
        :param amount: Amount to be paid (how much the sender will pay).
        :param amount_due: Optional. Amount to be received (will be credited to the recipient's account after payment).
        :param comment: Optional. A comment on the translation is displayed in the sender's history.
        :param message: Optional. A comment on the transfer, displayed to the recipient.
        :param label: Optional. Payment label.
        
        Docs: https://yoomoney.ru/docs/wallet/process-payments/request-payment"""
        url = f"{self.__base_url}/request-payment"
        params = {
            "pattern_id": "p2p",
            "to": to,
            "amount": amount,
            "amount_due": amount_due,
            "comment": comment,
            "message": message,
            "label": label,
        }
        self._delete_empty_fields(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=urlencode(params))
        return RequestPayment(**response)
        
    async def process_payment(self, 
                              request_id: str,
                              money_source: Optional[str] = "wallet",
                              csc: Optional[str] = None,
                              ext_auth_success_uri: Optional[str] = None,
                              ext_auth_fail_uri: Optional[str] = None,
                              ) -> ProcessPayment:
        """Confirmation of a payment previously created using the request_payment() method. Specifying the payment method.
        
        :param request_id: The request ID obtained from the response of the request_payment() method.
        :param money_source: Optional. Requested payment method: wallet — from the user's account. ID of the card linked to the account (the value of the id field in the bank card description). Default: wallet.
        :param csc: Optional. Card Security Code (CVV2/CVC2)—the code of the user's linked bank card. This parameter should only be specified when paying with a linked bank card.
        :param ext_auth_success_uri: Optional. The return page address upon successful 3-D Secure payment authentication. Specified if the app supports 3-D Secure authentication. This parameter is required for this type of authentication.
        :param ext_auth_fail_uri: Optional. The return page address if 3-D Secure payment authentication by bank card is denied. This is specified if the app supports 3-D Secure authentication. This parameter is required for this type of authentication.
        
        Docs: https://yoomoney.ru/docs/wallet/process-payments/process-payment"""
        url = f"{self.__base_url}/process-payment"
        params = {
            "request_id": request_id,
            "money_source": money_source,
            "csc": csc,
            "ext_auth_success_uri": ext_auth_success_uri,
            "ext_auth_fail_uri": ext_auth_fail_uri,
        }
        self._delete_empty_fields(params)
        response = await self._request(self.__payment_name, self.__post_method, url, headers=self.__headers, data=urlencode(params))
        return ProcessPayment(**response)
    
    async def quick_pay(self,
                        receiver: str,
                        sum: float,
                        quickpay_form: Optional[str] = "shop",
                        payment_type: Optional[str] = "SB",
                        label: Optional[str] = None,
                        success_url: Optional[str] = None,
                        ) -> str:
        """A form is a set of fields with information about a transfer. You can place the form in your interface (for example, on a website or blog). When the sender clicks the button, the form data is sent to YuMoney and initiates a transfer instruction to your wallet.
        
        :param receiver: Number of the YooMoney wallet which money from senders is credited to.
        :param sum: Transfer amount (the amount debited from the sender).
        :param quickpay_form: Optional. Form type. Fixed value: button/shop.
        :param payment_type: Optional. Payment method. Possible values: PC for a payment from a YooMoney wallet; AC for a payment from a bank card; SB.
        :param label: Optional. The label that a site or app assigns to a certain transfer. For instance, a code or order identifier may be used for this label.
        :param success_url: Optional. URL where the user is redirected after the transfer.
        
        Docs: https://yoomoney.ru/docs/payment-buttons/using-api/forms"""
        url = "https://yoomoney.ru/quickpay/confirm"
        params = {
            "receiver": receiver,
            "sum": sum,
            "quickpay-form": quickpay_form,
            "paymentType": payment_type,
            "label": label,
            "successURL": success_url,
        }
        self._delete_empty_fields(params)
        response = await self._request(self.__payment_name_quick_pay, self.__post_method, url, headers=self.__headers, data=urlencode(params))
        return response
    
    async def check_yoomoney_payment(self, label: str) -> bool:
        """
        Checking payment in the transaction history by label.

        :param label: Label of operation."""
        operations = await self.operation_history(label=label, records=1)
        if operations.operations:
            return operations.operations[0].label == label
        else:
            return False