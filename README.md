# AsyncPayments
![PyPiAsyncPaymentsPackage](https://img.shields.io/badge/pypi-AsyncPayments-red)
![PyPiAsyncPaymentsPackageVersion](https://img.shields.io/pypi/v/AsyncPayments)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/AsyncPayments?color=brightgreen)

> Add payment acceptance to your projects.
## Installing
    pip install AsyncPayments
## Last version
    v1.5
## Code example

```python
import asyncio

from AsyncPayments.ruKassa import AsyncRuKassa
from AsyncPayments.lolz import AsyncLolzteamMarketPayment
from AsyncPayments.aaio import AsyncAaio
from AsyncPayments.cryptoBot import AsyncCryptoBot
from AsyncPayments.crystalPay import AsyncCrystalPay
from AsyncPayments.freeKassa import AsyncFreeKassa
from AsyncPayments.payok import AsyncPayOK
from AsyncPayments.cryptomus import AsyncCryptomus
from AsyncPayments.xrocket import AsyncXRocket
from AsyncPaymentsTest.yoomoney import AsyncYoomoney
from AsyncPaymentsTest.apays import AsyncAPays
from AsyncPaymentsTest.platega import AsyncPlatega

ruKassa = AsyncRuKassa(api_token="ApiToken", shop_id=1, email="Email", password="Password")
lolz = AsyncLolzteamMarketPayment(token="Token")
aaio = AsyncAaio(apikey="ApiKey", shopid="ShopID", secretkey="SecretKey")
cryptoBot = AsyncCryptoBot(token="CryptoPayToken", is_testnet=False)
crystalPay = AsyncCrystalPay(login="Login", secret="Secret", salt="Salt")
freeKassa = AsyncFreeKassa(apiKey="ApiKey", shopId=1)
payok = AsyncPayOK(apiKey="ApiKey", secretKey="SecretKey", apiId=1, shopId=1)
cryptomus = AsyncCryptomus(payment_api_key="PaymentApiKey", merchant_id="MerchantID", payout_api_key="PayoutApiKey")
xrocket = AsyncXRocket(apiKey="ApiKey")
yoomoney = AsyncYoomoney(access_token="AccessToken")
apays = AsyncAPays(client_id=1, secret_key="SecretKey")
platega = AsyncPlatega(merchant_id=1, secret_key="SecretKey")

async def main():
    balance_payok = await payok.get_balance()
    balance_freekassa = await freeKassa.get_balance()
    balance_rukassa = await ruKassa.get_balance()
    balance_lolz = await lolz.get_me()
    balance_aaio = await aaio.get_balance()
    balance_crypto_bot = await cryptoBot.get_balance()
    balance_crystal_pay = await crystalPay.get_balance_list()
    balance_cryptomus = await cryptomus.get_balance()
    balance_xrocket = await xrocket.get_app_info()
    balance_yoomoney = await yoomoney.account_info()

    print("PayOK:")
    print("Balance: ", balance_payok.balance)
    print("Referral balance: ", balance_payok.ref_balance)
    print('--------------')
    print("FreeKassa:")
    for balance in balance_freekassa:
        print(f"{balance.currency}: ", balance.value)
    print('--------------')
    print("RuKassa:")
    print("RUB: ", balance_rukassa.balance_rub)
    print("USD: ", balance_rukassa.balance_usd)
    print('--------------')
    print("Lolz:")
    print('ID: ', balance_lolz.user_id)
    print('Nickname: ', balance_lolz.username)
    print('Available: ', balance_lolz.balance)
    print('In hold: ', balance_lolz.hold)
    print('--------------')
    print("Aaio:")
    print('Available: ', balance_aaio.balance)
    print('In hold: ', balance_aaio.hold)
    print('Referral balance: ', balance_aaio.referral)
    print('--------------')
    print("CryptoBot:")
    for balance in balance_crypto_bot:
        print(f"Available {balance.currency_code}: ", balance.available, f" (In hold: {balance.onhold})")
    print('--------------')
    print("CrystalPay:")
    for currency, balance in balance_crystal_pay.items():
        print(f"Available {currency}: {balance['amount']} {balance['currency']}")
    print('--------------')
    print("Cryptomus:")
    print("Merchant:\n")
    for balance in balance_cryptomus.merchant:
        print(
            f"Available {balance.currency_code}: {balance.balance} {balance.currency_code} ({balance.balance_usd} USD)")
    print("\nUser:\n")
    for balance in balance_cryptomus.user:
        print(
            f"Available {balance.currency_code}: {balance.balance} {balance.currency_code} ({balance.balance_usd} USD)")
    print('--------------')
    print('XRocket:')
    for bal in balance.balances:
        print(f"Available {bal.currency}: {bal.balance} {bal.currency}")
    print('--------------')
    print('YooMoney:')
    print(f"Account: {balance_yoomoney.account}")
    print(f"Available: {balance_yoomoney.balance}")
        
    print('------------------------------------------')

    order_payok = await payok.create_pay(15, "orderId")
    order_freeKassa = await freeKassa.create_order(1, "example@gmail.com", "0.0.0.0", 150, "RUB")
    order_ruKassa = await ruKassa.create_payment(15)
    order_lolz = await lolz.create_invoice(15, "paymentId", "comment", "https://example.com", 1)
    order_aaio = await aaio.create_payment_url(15, "orderId")
    order_crypto_bot = await cryptoBot.create_invoice(15, currency_type="crypto", asset="USDT")
    order_crystal_pay = await crystalPay.create_payment(15)
    order_cryptomus = await cryptomus.create_payment("15", "RUB", "orderId")
    order_xrocket = await xrocket.create_invoice(1, "TONCOIN", 1)
    order_yoomoney = await yoomoney.quick_pay("walletNumber", 15, label="labelOfOperation")
    order_apays = await apays.create_order("orderId", 15)
    order_platega = await platega.create_order(2, 15, "RUB", "description")

    print("PayOK", order_payok)
    print("FreeKassa", order_freeKassa.location)
    print("RuKassa: ", order_ruKassa.url)
    print("Lolz: ":, order_lolz.url)
    print("Aaio: ", order_aaio)
    print("CryptoBot: ", order_crypto_bot.pay_url)
    print("CrystalPay: ", order_crystal_pay.url)
    print("Cryptomus: ", order_cryptomus.url)
    print("XRocket: ", order_xrocket.link)
    print("YooMoney: ", order_yoomoney)
    print("APays: ", order_apays.url)
    print("Platega: ", order_platega.redirect)

    print('------------------------------------------')

    info_payok = await payok.get_transactions("orderId")
    info_freeKassa = await freeKassa.get_orders("orderId")
    info_ruKassa = await ruKassa.get_info_payment("orderId")
    info_lolz = await lolz.get_invoice(payment_id="paymentId")
    info_aaio = await aaio.get_order_info("orderId")
    info_crypto_bot = await cryptoBot.get_invoices(invoice_ids=["orderId"], count=1)
    info_crystal_pay = await crystalPay.get_payment_info("orderId")
    info_cryptomus = await cryptomus.payment_info(order_id="orderId")
    info_xrocket = await xrocket.get_invoice_info('orderId')
    info_yoomoney = await yoomoney.operation_history(label="labelOfOperation", records=1)
    info_apays = await apays.get_order("orderId")
    info_platega = await platega.get_order("orderId")

    print("PayOK:")
    print("Amount: ", info_payok.amount)
    print("Status: ", info_payok.transaction_status)
    print('--------------')
    print("FreeKassa:")
    print("Amount: ", info_freeKassa.orders[0].amount)
    print("Status: ", info_freeKassa.orders[0].status)
    print('--------------')
    print('RuKassa:')
    print("Amount: ", info_ruKassa.amount)
    print("Status: ", info_ruKassa.status)
    print('--------------')
    print("Lolz:")
    print("Amount: ", info_lolz.amount)
    print("Status: ", info_lolz.status)
    print('--------------')
    print("Aaio:")
    print("Amount: ", info_aaio.amount)
    print("Status: ", info_aaio.status)
    print('--------------')
    print("CryptoBot:")
    print("Amount: ", info_crypto_bot.amount)
    print("Status: ", info_crypto_bot.status)
    print('--------------')
    print("CrystalPay:")
    print("Amount: ", info_crystal_pay.rub_amount)
    print("Status:", info_crystal_pay.state)
    print('--------------')
    print("Cryptomus:")
    print("Amount: ", info_cryptomus.amount)
    print("Status: ", info_cryptomus.payment_status)
    print('--------------')
    print("XRocket:")
    print("Amount: ", info_xrocket.amount)
    print("Status: ", info_xrocket.status)
    print('--------------')
    print("YooMoney:")
    print("Amount: ", info_yoomoney.amount)
    print("Status: ", info_yoomoney.status)
    print('--------------')
    print("APays:")
    print("Status: ", info_apays.order_status)
    print('--------------')
    print("Platega:")
    print("Amount: ", info_platega.paymentDetails['amount'])
    print("Status: ", info_platega.status)

asyncio.run(main())
```
## Output
```Python
PayOK:
Balance: 0
Referral balance: 0.00
--------------
FreeKassa:
RUB:  0.00
USD:  0.00
EUR:  0.00
KZT:  0.00
UAH:  0.00
--------------
RuKassa:
RUB:  34.0
USD:  234.1
--------------
Lolz:
ID:  4810752
Nickname:  ToSa
Available:  5233.0
In hold:  234.0
--------------
Aaio:
Available:  1235.0
In hold:  0.0
Referral balance:  0.0
--------------
CryptoBot:
Available USDT:  15.0  (In hold: 0.0)
Available TON:  0.0  (In hold: 0.0)
Available BTC:  0.00000023  (In hold: 0.0)
Available LTC:  0.0  (In hold: 0.0)
Available ETH:  0.0  (In hold: 0.0)
...
--------------
CrystalPay:
Available BITCOIN: 0 BTC
Available BITCOINCASH: 0 BCH
Available BNBCRYPTOBOT: 0 BNB
Available BNBSMARTCHAIN: 0 BNB
Available BTCCRYPTOBOT: 0 BTC
...
--------------
Cryptomus:
Merchant:

Available VERSE: 0.00000000 VERSE (0.00000000 USD)
Available DAI: 0.00000000 DAI (0.00000000 USD)
Available ETH: 0.00000000 ETH (0.00000000 USD)
Available BCH: 0.00000000 BCH (0.00000000 USD)
Available DASH: 0.00000000 DASH (0.00000000 USD)
...

User:

Available DASH: 0.00000000 DASH (0.00000000 USD)
Available ETH: 0.00000000 ETH (0.00000000 USD)
Available VERSE: 0.00000000 VERSE (0.00000000 USD)
Available CRMS: 0.12041311 CRMS (0.12041311 USD)
Available USDT: 0.00975846 USDT (0.00975097 USD)
...
--------------
XRocket:
Available TONCOIN: 0 TONCOIN
Available XROCK: 0 XROCK
Available SCALE: 0 SCALE
Available BOLT: 0 BOLT
Available TAKE: 0 TAKE
...
--------------
YooMoney:
Account: 4100112252967685
Available balance: 236.24
------------------------------------------
PayOK: https://payok.io//pay?amount=15&payment=4364575733&shop=12452&currency=RUB&desc=Description&sign=af2fdc6796750e3c6910230095ec0ed8
FreeKassa: https://pay.freekassa.com/form/161328352/576046439bd01de60a6e418bad9354a2
RuKassa:  https://pay.ruks.pro/?hash=435fc3cee737f9dac2b34c9ba9311eae
Lolz:  https://lzt.market/invoice/369/
Aaio:  https://aaio.io/merchant/pay?merchant_id=f398c75d-b775-412c-9674-87939692c083&amount=15&order_id=orderId&currency=RUB&sign=6ad5dc2164059a255921ad216c7e5ffd0d2abcaec9af7415636fc12df938582f
CryptoBot:  https://t.me/CryptoBot?start=IVYOJWPOZh15
CrystalPay:  https://pay.crystalpay.io/?i=715308958_rPwTzvsvCmabwl
Cryptomus:  https://pay.cryptomus.com/pay/6c0j685d-2bc1-41a1-954b-b11def3641a4
XRocket:  https://t.me/xrocket?start=inv_NX9RajMus37wbn3
YooMoney:  https://yoomoney.ru/transfer/quickpay?requestId=353635343031333732365f63373363636231323732623835333934353132343264613062373535383033336131343666643235
APays:  https://apays.shop/order?id=77197d6-faa9-467ad-bdea-2534a7258b01
Platega:  https://pay.platega.io?id=61dh392d-67a8-4555-9ac9-f3337f52fd08&mh=b6hba81f-1972-4f46-a90c-0d143df49425
------------------------------------------
PayOK:
Amount:  15
Status:  0
--------------
FreeKassa:
Amount:  150
Status:  0
--------------
RuKassa:
Amount:  50
Status:  WAIT
--------------
Lolz:
Amount:  15
Status:  not_paid
--------------
Aaio:
Amount:  299.0
Status:  in_process
--------------
CryptoBot:
Amount:  15
Status:  active
--------------
CrystalPay:
Amount:  15
Status:  notpayed
--------------
Cryptomus:
Amount:  15.00
Status:  check
--------------
XRocket:
Amount:  1.0
Status:  active
--------------
YooMoney:
Amount:  15
Status:  in_progress
--------------
APays:
Status:  pending
--------------
Platega:
Amount:  15
Status:  PENDING
```

## Docs
> Lolzteam Market: https://lzt-market.readme.io/reference/ <br>
> Aaio: https://wiki.aaio.io <br>
> CryptoBot: https://help.crypt.bot/crypto-pay-api <br>
> CrystalPay: https://docs.crystalpay.io/ <br>
> RuKassa: https://lk.rukassa.pro/api/v1 <br>
> FreeKassa: https://docs.freekassa.com/ <br>
> PayOK: https://payok.io/cabinet/documentation/doc_main.php <br>
> Cryptomus: https://doc.cryptomus.com/business <br>
> XRocket: https://pay.xrocket.tg/api/#/ <br>
> YooMoney: https://yoomoney.ru/docs/wallet <br>
> APays: https://docs.apays.io/lets-start/api/how-to-start <br>
> Platega: https://docs.platega.io/авторизация-1678262m0 <br>

## Developer Links
> Zelenka (Lolzteam): https://lzt.market/tosa <br>
> GitHub: https://github.com/I-ToSa-I <br>
> Telegram: https://t.me/ToSa_LZT
