from pydantic import BaseModel, Field
from typing import Optional, Union, List


class Balance(BaseModel):
    currency: Optional[str] = None
    balance: Optional[Union[int, float]] = None


class AppInfo(BaseModel):
    name: Optional[str] = None
    feePercents: Optional[Union[int, float]] = None
    balances: Optional[List[Balance]] = None


class Transfer(BaseModel):
    id: Optional[int] = None
    tgUserId: Optional[int] = None
    currency: Optional[str] = None
    amount: Optional[Union[int, float]] = None
    description: Optional[str] = None


class Withdrawal(BaseModel):
    network: Optional[str] = None
    address: Optional[str] = None
    currency: Optional[str] = None
    amount: Optional[Union[int, float]] = None
    withdrawalId: Optional[str] = None
    status: Optional[str] = None
    comment: Optional[str] = None
    txHash: Optional[str] = None
    txLink: Optional[str] = None


class FeeWithdraw(BaseModel):
    fee: Optional[float] = None
    currency: Optional[str] = None


class Fee(BaseModel):
    networkCode: Optional[str] = None
    feeWithdraw: Optional[FeeWithdraw] = None


class WithdrawalFees(BaseModel):
    code: Optional[str] = None
    minWithdraw: Optional[float] = None
    fees: Optional[List[Fee]] = None


class MultiCheque(BaseModel):
    id: Optional[int] = None
    currency: Optional[str] = None
    total: Optional[int] = None
    perUser: Optional[int] = None
    users: Optional[int] = None
    password: Optional[str] = None
    description: Optional[str] = None
    sendNotifications: Optional[bool] = None
    captchaEnabled: Optional[bool] = None
    refProgramPercents: Optional[int] = None
    refRewardPerUser: Optional[float] = None
    state: Optional[str] = None
    link: Optional[str] = None
    disabledLanguages: Optional[list] = None
    enabledCountries: Optional[list] = None
    forPremium: Optional[int] = None
    forNewUsersOnly: Optional[int] = None
    linkedWallet: Optional[int] = None
    tgResources: Optional[list] = None
    activations: Optional[int] = None
    refRewards: Optional[int] = None


class MultiChequesList(BaseModel):
    total: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    results: Optional[List[MultiCheque]] = None


class InvoicePayment(BaseModel):
    userId: Optional[int] = None
    paymentNum: Optional[int] = None
    paymentAmount: Optional[int] = None
    comment: Optional[str] = None
    paid: Optional[str] = None


class Invoice(BaseModel):
    id: Optional[str] = None
    amount: Optional[Union[float, int]] = None
    minPayment: Optional[Union[float, int]] = None
    totalActivations: Optional[int] = None
    activationsLeft: Optional[int] = None
    description: Optional[str] = None
    hiddenMessage: Optional[str] = None
    payload: Optional[str] = None
    callbackUrl: Optional[str] = None
    commentsEnabled: Optional[Union[bool, int]] = None
    currency: Optional[str] = None
    created: Optional[str] = None
    paid: Optional[str] = None
    status: Optional[str] = None
    expiredIn: Optional[int] = None
    link: Optional[str] = None
    payments: Optional[List[InvoicePayment]] = []


class InvoicesList(BaseModel):
    total: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    results: Optional[List[Invoice]] = None


class Currency(BaseModel):
    currency: Optional[str] = None
    name: Optional[str] = None
    minTransfer: Optional[Union[float, int]] = None
    minCheque: Optional[Union[float, int]] = None
    minInvoice: Optional[Union[float, int]] = None
    minWithdraw: Optional[Union[float, int]] = None
    feeWithdraw: Optional[dict] = None


class Subscriptions:
    class Interval(BaseModel):
        interval: Optional[str] = None
        amount: Optional[Union[float, int]] = None
        status: Optional[str] = None
        code: Optional[str] = None

    class tgResource(BaseModel):
        id: Optional[int] = None
        type_: Optional[str] = Field(alias="type", default=None)
        resourceId: Optional[str] = None
        name: Optional[str] = None
        linkedChat: Optional[str] = None


class Subscription(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None
    link: Optional[str] = None
    interval: Optional[Subscriptions.Interval] = None
    referralPercent: Optional[int] = None
    returnUrl: Optional[str] = None
    tgResource: Optional[Subscriptions.tgResource] = None


class SubscriptionsList(BaseModel):
    total: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    results: Optional[List[Subscription]] = None


class SubscriptionCheck(BaseModel):
    subscriptionId: Optional[int] = None
    subscriptionCode: Optional[str] = None
    userId: Optional[int] = None
    amount: Optional[Union[float, int]] = None
    currency: Optional[str] = None
    interval: Optional[str] = None
    refFee: Optional[Union[float, int]] = None
    isRefPay: Optional[bool] = None
    totalAmount: Optional[Union[float, int]] = None
    paymentStart: Optional[str] = None
    paymentEnd: Optional[str] = None
    autoRenewal: Optional[bool] = None
    transactions: Optional[list] = None


class SubscriptionsStatutes:
    ACTIVE = "ACTIVE"
    ARCHIVE = "ARCHIVE"
    DELETED = "DELETED"


class SubscriptionsIntervals:
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"
    FOREVER = "FOREVER"


class InvoiceStatutes:
    ACTIVE = "active"
    PAID = "paid"
    EXPIRED = "expired"


class CountriesName:
    DZ: str = "DZ"
    AO: str = "AO"
    BJ: str = "BJ"
    BW: str = "BW"
    BF: str = "BF"
    BI: str = "BI"
    CV: str = "CV"
    CM: str = "CM"
    CF: str = "CF"
    TD: str = "TD"
    KM: str = "KM"
    CG: str = "CG"
    CD: str = "CD"
    DJ: str = "DJ"
    EG: str = "EG"
    GQ: str = "GQ"
    ER: str = "ER"
    SZ: str = "SZ"
    ET: str = "ET"
    GA: str = "GA"
    GM: str = "GM"
    GH: str = "GH"
    GN: str = "GN"
    GW: str = "GW"
    CI: str = "CI"
    KE: str = "KE"
    LS: str = "LS"
    LR: str = "LR"
    LY: str = "LY"
    MG: str = "MG"
    MW: str = "MW"
    ML: str = "ML"
    MR: str = "MR"
    MU: str = "MU"
    MA: str = "MA"
    MZ: str = "MZ"
    NA: str = "NA"
    NE: str = "NE"
    NG: str = "NG"
    RW: str = "RW"
    ST: str = "ST"
    SN: str = "SN"
    SC: str = "SC"
    SL: str = "SL"
    SO: str = "SO"
    ZA: str = "ZA"
    SS: str = "SS"
    SD: str = "SD"
    TZ: str = "TZ"
    TG: str = "TG"
    TN: str = "TN"
    UG: str = "UG"
    ZM: str = "ZM"
    ZW: str = "ZW"
    AF: str = "AF"
    AM: str = "AM"
    AZ: str = "AZ"
    BH: str = "BH"
    BD: str = "BD"
    BT: str = "BT"
    BN: str = "BN"
    MM: str = "MM"
    KH: str = "KH"
    CN: str = "CN"
    CY: str = "CY"
    GE: str = "GE"
    IN: str = "IN"
    ID: str = "ID"
    IR: str = "IR"
    IQ: str = "IQ"
    IL: str = "IL"
    JP: str = "JP"
    JO: str = "JO"
    KZ: str = "KZ"
    KW: str = "KW"
    KG: str = "KG"
    LA: str = "LA"
    LB: str = "LB"
    MY: str = "MY"
    MV: str = "MV"
    MN: str = "MN"
    NP: str = "NP"
    KP: str = "KP"
    KR: str = "KR"
    OM: str = "OM"
    PK: str = "PK"
    PS: str = "PS"
    PH: str = "PH"
    QA: str = "QA"
    SA: str = "SA"
    SG: str = "SG"
    LK: str = "LK"
    SY: str = "SY"
    TW: str = "TW"
    TJ: str = "TJ"
    TH: str = "TH"
    TR: str = "TR"
    TM: str = "TM"
    AE: str = "AE"
    UZ: str = "UZ"
    VN: str = "VN"
    YE: str = "YE"
    AL: str = "AL"
    AD: str = "AD"
    AT: str = "AT"
    BY: str = "BY"
    BE: str = "BE"
    BA: str = "BA"
    BG: str = "BG"
    HR: str = "HR"
    CZ: str = "CZ"
    DK: str = "DK"
    EE: str = "EE"
    FI: str = "FI"
    FR: str = "FR"
    DE: str = "DE"
    GR: str = "GR"
    HU: str = "HU"
    IS: str = "IS"
    IE: str = "IE"
    IT: str = "IT"
    XK: str = "XK"
    LV: str = "LV"
    LI: str = "LI"
    LT: str = "LT"
    LU: str = "LU"
    MT: str = "MT"
    MD: str = "MD"
    MC: str = "MC"
    ME: str = "ME"
    NL: str = "NL"
    MK: str = "MK"
    NO: str = "NO"
    PL: str = "PL"
    PT: str = "PT"
    RO: str = "RO"
    RU: str = "RU"
    SM: str = "SM"
    RS: str = "RS"
    SK: str = "SK"
    SI: str = "SI"
    ES: str = "ES"
    SE: str = "SE"
    CH: str = "CH"
    UA: str = "UA"
    GB: str = "GB"
    VA: str = "VA"
    AG: str = "AG"
    BS: str = "BS"
    BB: str = "BB"
    BZ: str = "BZ"
    CA: str = "CA"
    CR: str = "CR"
    CU: str = "CU"
    DM: str = "DM"
    DO: str = "DO"
    SV: str = "SV"
    GD: str = "GD"
    GT: str = "GT"
    HT: str = "HT"
    HN: str = "HN"
    JM: str = "JM"
    MX: str = "MX"
    NI: str = "NI"
    PA: str = "PA"
    KN: str = "KN"
    LC: str = "LC"
    VC: str = "VC"
    TT: str = "TT"
    US: str = "US"
    AR: str = "AR"
    BO: str = "BO"
    BR: str = "BR"
    CL: str = "CL"
    CO: str = "CO"
    EC: str = "EC"
    GY: str = "GY"
    PY: str = "PY"
    PE: str = "PE" 
    SR: str = "SR"
    UY: str = "UY"
    VE: str = "VE"
    AU: str = "AU"
    FJ: str = "FJ"
    KI: str = "KI"
    MH: str = "MH"
    FM: str = "FM"
    NR: str = "NR"
    NZ: str = "NZ"
    PW: str = "PW"
    PG: str = "PG"
    WS: str = "WS"
    SB: str = "SB"
    TO: str = "TO"
    TV: str = "TV"
    VU: str = "VU"