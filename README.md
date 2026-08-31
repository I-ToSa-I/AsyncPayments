# AsyncPayments
![PyPiAsyncPaymentsPackage](https://img.shields.io/badge/pypi-AsyncPayments-red)
![PyPiAsyncPaymentsPackageVersion](https://img.shields.io/pypi/v/AsyncPayments)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/AsyncPayments?color=brightgreen)

> Add payment acceptance to your projects.
## Installing
    pip install AsyncPayments
## Last version
    v1.7
## Code example

```python
import asyncio
from contextlib import AsyncExitStack

from AsyncPayments.ruKassa import AsyncRuKassa
from AsyncPayments.lolz import AsyncLolzteamMarketPayment
from AsyncPayments.aaio import AsyncAaio
from AsyncPayments.cryptoBot import AsyncCryptoBot
from AsyncPayments.crystalPay import AsyncCrystalPay
from AsyncPayments.freeKassa import AsyncFreeKassa
from AsyncPayments.cryptomus import AsyncCryptomus
from AsyncPayments.xrocket import AsyncXRocket
from AsyncPayments.yoomoney import AsyncYoomoney
from AsyncPayments.apays import AsyncAPays
from AsyncPayments.platega import AsyncPlatega
from AsyncPayments.rollypay import AsyncRollyPay
from AsyncPayments.pay2328io import Async2328io

async def main():
    async with AsyncExitStack() as stack:
        ruKassa = await stack.enter_async_context(AsyncRuKassa(api_token="ApiToken", shop_id=1, email="Email", password="Password"))
        lolz = await stack.enter_async_context(AsyncLolzteamMarketPayment(token="Token"))
        aaio = await stack.enter_async_context(AsyncAaio(apikey="ApiKey", shopid="ShopID", secretkey="SecretKey"))
        cryptoBot = await stack.enter_async_context(AsyncCryptoBot(token="CryptoPayToken", is_testnet=False))
        crystalPay = await stack.enter_async_context(AsyncCrystalPay(login="Login", secret="Secret", salt="Salt"))
        freeKassa = await stack.enter_async_context(AsyncFreeKassa(apiKey="ApiKey", shopId=1))
        cryptomus = await stack.enter_async_context(AsyncCryptomus(payment_api_key="PaymentApiKey", merchant_id="MerchantID", payout_api_key="PayoutApiKey"))
        xrocket = await stack.enter_async_context(AsyncXRocket(apiKey="ApiKey", is_testnet=False))
        yoomoney = await stack.enter_async_context(AsyncYoomoney(access_token="AccessToken"))
        apays = await stack.enter_async_context(AsyncAPays(client_id=1, secret_key="SecretKey"))
        platega = await stack.enter_async_context(AsyncPlatega(merchant_id=1, secret_key="SecretKey"))
        rolly = await stack.enter_async_context(AsyncRollyPay(api_key="ApiKey", terminal_id="TerminalID"))
        pay2328io = await stack.enter_async_context(Async2328io(api_key="ApiKey", project_uuid="ProjectUUID"))

        balance_rolly = await rolly.get_balance()
        balance_2328io = await pay2328io.get_balance()
        balance_freekassa = await freeKassa.get_balance()
        balance_rukassa = await ruKassa.get_balance()
        balance_lolz = await lolz.get_me()
        balance_aaio = await aaio.get_balance()
        balance_crypto_bot = await cryptoBot.get_balance()
        balance_crystal_pay = await crystalPay.get_balance_list()
        balance_cryptomus = await cryptomus.get_balance()
        balance_xrocket = await xrocket.get_balances()
        balance_yoomoney = await yoomoney.account_info()

        print("RollyPay:")
        print("Available USDT: ", balance_rolly.available_usdt)
        print("Hold USDT: ", balance_rolly.hold_usdt)
        print('--------------')
        print("2328.io:")
        for balance in balance_2328io:
            print(f"Available {balance.currency_code}: {balance.balance} {balance.currency_code} ({balance.balance_usd}$, lock: {balance.locked_balance} {balance.currency_code})")
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
        for balance in balance_xrocket:
            print(f"Available {balance.asset}: {balance.balance} {balance.asset} ({balance.available} {balance.asset}, holds: {balance.holds} {balance.asset})")
        print('--------------')
        print('YooMoney:')
        print(f"Account: {balance_yoomoney.account}")
        print(f"Available: {balance_yoomoney.balance}")
            
        print('------------------------------------------')

        order_rolly = await rolly.create_payment("1500.00", "RUB", "orderId")
        order_2328io = await pay2328io.create_payment(150.0, "RUB", "orderId", "https://example.com")
        order_freeKassa = await freeKassa.create_order(1, "example@gmail.com", "0.0.0.0", 150, "RUB")
        order_ruKassa = await ruKassa.create_payment(15)
        order_lolz = await lolz.create_invoice(15, "paymentId", "comment", "https://example.com", 1)
        order_aaio = await aaio.create_payment_url(15, "orderId")
        order_crypto_bot = await cryptoBot.create_invoice(15, currency_type="crypto", asset="USDT")
        order_crystal_pay = await crystalPay.create_payment(15)
        order_cryptomus = await cryptomus.create_payment("15", "RUB", "orderId")
        order_xrocket = await xrocket.create_invoice("USDT", "15")
        order_yoomoney = await yoomoney.quick_pay("walletNumber", 15, label="labelOfOperation")
        order_apays = await apays.create_order("orderId", 15)
        order_platega = await platega.create_order(2, 15, "RUB", "description")

        print("RollyPay", order_rolly.pay_url)
        print("2328.io", order_2328io.url)
        print("FreeKassa", order_freeKassa.location)
        print("RuKassa: ", order_ruKassa.url)
        print("Lolz: ":, order_lolz.url)
        print("Aaio: ", order_aaio)
        print("CryptoBot: ", order_crypto_bot.pay_url)
        print("CrystalPay: ", order_crystal_pay.url)
        print("Cryptomus: ", order_cryptomus.url)
        print("XRocket: ", order_xrocket.links.telegramBotLink)
        print("YooMoney: ", order_yoomoney)
        print("APays: ", order_apays.url)
        print("Platega: ", order_platega.redirect)

        print('------------------------------------------')

        info_rolly = await rolly.get_payment("paymentId")
        info_2328io = await pay2328io.get_payment(order_id="orderId")
        info_freeKassa = await freeKassa.get_orders("orderId")
        info_ruKassa = await ruKassa.get_info_payment("orderId")
        info_lolz = await lolz.get_invoice(payment_id="paymentId")
        info_aaio = await aaio.get_order_info("orderId")
        info_crypto_bot = await cryptoBot.get_invoices(invoice_ids=["orderId"], count=1)
        info_crystal_pay = await crystalPay.get_payment_info("orderId")
        info_cryptomus = await cryptomus.payment_info(order_id="orderId")
        info_xrocket = await xrocket.get_invoice_info(invoiceId='orderId')
        info_yoomoney = await yoomoney.operation_history(label="labelOfOperation", records=1)
        info_apays = await apays.get_order("orderId")
        info_platega = await platega.get_order("orderId")

        print("RollyPay:")
        print("Amount: ", info_rolly.amount)
        print("Status: ", info_rolly.status)
        print('--------------')
        print("2328.io:")
        print("Amount: ", info_2328io.amount)
        print("Status: ", info_2328io.payment_status)
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
        print("Amount: ", info_xrocket.priceAmount)
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
RollyPay:
Available USDT:  -1.57842382
Hold USDT:  0.00000000
--------------
2328.io:
Available AVAX: 0.00 AVAX (0.00$, lock: 0.00 AVAX)
Available BNB: 0.00 BNB (0.00$, lock: 0.00 BNB)
Available BTC: 0.00 BTC (0.00$, lock: 0.00 BTC)
Available DOGE: 0.00 DOGE (0.00$, lock: 0.00 DOGE)
Available ETH: 0.00 ETH (0.00$, lock: 0.00 ETH)
...
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
Available GRAM: 0 GRAM (0 GRAM, holds: 0 GRAM)
Available XROCK: 0 XROCK (0 XROCK, holds: 0 XROCK)
Available DUST: 0 DUST (0 DUST, holds: 0 DUST)
Available BOLT: 0 BOLT (0 BOLT, holds: 0 BOLT)
Available TGR: 0 TGR (0 TGR, holds: 0 TGR)
...
--------------
YooMoney:
Account: 4100112252967685
Available balance: 236.24
------------------------------------------
RollyPay: https://pay.rollypay.io/pay/J8_RVO33btNdxTFHzKjGn3GFeZ3lDgBiwBNXO0J-apI
2328.io: https://pay.2328.io/b3436fa5-6fd4-4c3f-9a46-1a627ad6efb3
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
RollyPay:
Amount:  1500.00
Status:  created
--------------
2328.io:
Amount:  150.00
Status:  check
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
Amount:  15
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
> Cryptomus: https://doc.cryptomus.com/business <br>
> XRocket: https://pay.xrocket.tg/api/#/ <br>
> YooMoney: https://yoomoney.ru/docs/wallet <br>
> APays: https://docs.apays.io/lets-start/api/how-to-start <br>
> Platega: https://docs.platega.io/авторизация-1678262m0 <br>
> RollyPay: https://docs.rollypay.io/ <br>
> 2328.io: https://doc.2328.io/ <br>

## Developer Links
> Zelenka (Lolzteam): https://lzt.market/tosa <br>
> GitHub: https://github.com/I-ToSa-I <br>
> Telegram: https://t.me/ToSa_LZT
