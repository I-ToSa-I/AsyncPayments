from pydantic import BaseModel, Field
from typing import Optional, Union, List


class Balance(BaseModel):
    currency: str
    balance: Union[int, float]


class AppInfo(BaseModel):
    name: str
    feePercents: Union[int, float]
    balances: List[Balance]


class Transfer(BaseModel):
    id: int
    tgUserId: int
    currency: str
    amount: Union[int, float]
    description: str


class Withdrawal(BaseModel):
    network: str
    address: str
    currency: str
    amount: Union[int, float]
    withdrawalId: str
    status: str
    comment: str
    txHash: str
    txLink: str


class FeeWithdraw(BaseModel):
    fee: Optional[float] = None
    currency: str


class Fee(BaseModel):
    networkCode: str
    feeWithdraw: FeeWithdraw


class WithdrawalFees(BaseModel):
    code: str
    minWithdraw: float
    fees: List[Fee]


class MultiCheque(BaseModel):
    id: int
    currency: str
    total: int
    perUser: int
    users: int
    password: str
    description: str
    sendNotifications: bool
    captchaEnabled: bool
    refProgramPercents: int
    refRewardPerUser: float
    state: str
    link: str
    disabledLanguages: list
    enabledCountries: list
    forPremium: int
    forNewUsersOnly: int
    linkedWallet: int
    tgResources: Optional[list] = None
    activations: Optional[int] = None
    refRewards: Optional[int] = None


class MultiChequesList(BaseModel):
    total: int
    limit: int
    offset: int
    results: List[MultiCheque]


class InvoicePayment(BaseModel):
    userId: int
    paymentNum: int
    paymentAmount: int
    comment: str
    paid: str


class Invoice(BaseModel):
    id: str
    amount: Union[float, int]
    minPayment: Optional[Union[float, int]] = None
    totalActivations: int
    activationsLeft: int
    description: Optional[str] = None
    hiddenMessage: Optional[str] = None
    payload: Optional[str] = None
    callbackUrl: Optional[str] = None
    commentsEnabled: Union[bool, int]
    currency: str
    created: Optional[str] = None
    paid: Optional[str] = None
    status: str
    expiredIn: int
    link: str
    payments: Optional[List[InvoicePayment]] = []


class InvoicesList(BaseModel):
    total: int
    limit: int
    offset: int
    results: List[Invoice]


class Currency(BaseModel):
    currency: str
    name: str
    minTransfer: Union[float, int]
    minCheque: Union[float, int]
    minInvoice: Union[float, int]
    minWithdraw: Union[float, int]
    feeWithdraw: dict


class Subscriptions:
    class Interval(BaseModel):
        interval: str
        amount: Union[float, int]
        status: str
        code: str

    class tgResource(BaseModel):
        id: int
        type_: str = Field(alias="type")
        resourceId: str
        name: str
        linkedChat: str


class Subscription(BaseModel):
    id: int
    name: str
    description: str
    currency: str
    link: str
    interval: Subscriptions.Interval
    referralPercent: int
    returnUrl: str
    tgResource: Subscriptions.tgResource


class SubscriptionsList(BaseModel):
    total: int
    limit: int
    offset: int
    results: List[Subscription]


class SubscriptionCheck(BaseModel):
    subscriptionId: int
    subscriptionCode: str
    userId: int
    amount: Union[float, int]
    currency: str
    interval: str
    refFee: Union[float, int]
    isRefPay: bool
    totalAmount: Union[float, int]
    paymentStart: str
    paymentEnd: str
    autoRenewal: bool
    transactions: list


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