from pydantic import BaseModel, Field
from typing import Optional, Union, List


class AccountInfo(BaseModel):
    error: Optional[str] = None
    account: Optional[str] = None
    balance: Optional[Union[int, float]] = None
    currency: Optional[str] = None
    account_type: Optional[str] = None
    identified: Optional[bool] = None
    account_status: Optional[str] = None
    balance_details: Optional[dict] = None
    cards_linked: Optional[list] = None
    
    
class Operation(BaseModel):
    operation_id: Optional[str] = None
    status: Optional[str] = None
    datetime: Optional[str] = None
    title: Optional[str] = None
    pattern_id: Optional[str] = None
    direction: Optional[str] = None
    amount: Optional[Union[int, float]] = None
    label: Optional[str] = None
    type_: Optional[str] = Field(alias="type", default=None)
    amount_due: Optional[Union[int, float]] = None
    fee: Optional[Union[int, float]] = None
    recipient: Optional[str] = None
    recipient_type: Optional[str] = None
    message: Optional[str] = None
    comment: Optional[str] = None
    details: Optional[str] = None
    digital_goods: Optional[Union[str, dict]] = None
    spendingCategories: Optional[list] = []
    amount_currency: Optional[str] = None
    group_id: Optional[str] = None
    categories: Optional[list] = None
    showcase_format: Optional[str] = None
    is_sbp_operation: Optional[bool] = None
    
    
class OperationHistory(BaseModel):
    error: Optional[str] = None
    next_record: Optional[str] = None
    operations: Optional[List[Operation]] = []
    
    
class OperationDetails(BaseModel):
    error: Optional[str] = None
    pattern_id: Optional[str] = None
    group_id: Optional[str] = None
    operation_id: Optional[str] = None
    title: Optional[str] = None
    amount: Optional[Union[int, float]] = None
    direction: Optional[str] = None
    datetime: Optional[str] = None
    status: Optional[str] = None
    type_: Optional[str] = Field(alias="type", default=None)
    available_operations: Optional[list] = []
    amount_due: Optional[Union[int, float]] = None
    fee: Optional[Union[int, float]] = None
    recipient: Optional[str] = None
    recipient_type: Optional[str] = None
    message: Optional[str] = None
    comment: Optional[str] = None
    details: Optional[str] = None
    digital_goods: Optional[str] = None
    spendingCategories: Optional[list] = []
    amount_currency: Optional[str] = None
    categories: Optional[list] = None
    showcase_format: Optional[str] = None
    is_sbp_operation: Optional[bool] = None
    
    
class RequestPayment(BaseModel):
    error: Optional[str] = None
    error_description: Optional[str] = None
    status: Optional[str] = None
    money_source: Optional[dict] = {}
    request_id: Optional[str] = None
    contract_amount: Optional[Union[int, float]] = None
    balance: Optional[Union[int, float]] = None
    recipient_account_status: Optional[str] = None
    recipient_account_type: Optional[str] = None
    account_unblock_uri: Optional[str] = None
    ext_action_uri: Optional[str] = None
    
    
class ProcessPayment(BaseModel):
    error: Optional[str] = None
    error_description: Optional[str] = None
    status: Optional[str] = None
    payment_id: Optional[str] = None
    balance: Optional[Union[int, float]] = None
    invoice_id: Optional[str] = None
    payer: Optional[str] = None
    payee: Optional[str] = None
    credit_amount: Optional[Union[int, float]] = None
    account_unblock_uri: Optional[str] = None
    acs_uri: Optional[str] = None
    acs_params: Optional[dict] = {}
    next_retry: Optional[int] = None
    digital_goods: Optional[Union[str, dict]] = None
    