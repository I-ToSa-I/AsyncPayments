# AsyncPayments
![PyPiAsyncPaymentsPackage](https://img.shields.io/badge/pypi-AsyncPayments-red)
![PyPiAsyncPaymentsPackageVersion](https://img.shields.io/pypi/v/AsyncPayments)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/AsyncPayments?color=brightgreen)

> Add payment acceptance to your projects.
## Installing
    pip install AsyncPayments
## Version
    v1.4.6
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

ruKassa = AsyncRuKassa(api_token="ApiToken", shop_id=1, email="Email", password="Password")
lolz = AsyncLolzteamMarketPayment(token="Token")
aaio = AsyncAaio(apikey="ApiKey", shopid="ShopID", secretkey="SecretKey")
cryptoBot = AsyncCryptoBot(token="CryptoPayToken", is_testnet=False)
crystalPay = AsyncCrystalPay(login="Login", secret="Secret", salt="Salt")
freeKassa = AsyncFreeKassa(apiKey="ApiKey", shopId=1)
payok = AsyncPayOK(apiKey="ApiKey", secretKey="SecretKey", apiId=1, shopId=1)
cryptomus = AsyncCryptomus(payment_api_key="PaymentApiKey", merchant_id="MerchantID", payout_api_key="PayoutApiKey")
xrocket = AsyncXRocket(apiKey="ApiKey")


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
    for currency, balance in balance_crystal_pay:
        print(f"Available {currency}: {balance.amount} {balance.currency}")
    print('--------------')
    print("Cryptomus:")
    print("Merchant:\n")
    for balance in balance_cryptomus.merchant:
        print(f"Available {balance.currency_code}: {balance.balance} {balance.currency_code} ({balance.balance_usd} USD)")
    print("\nUser:\n")
    for balance in balance_cryptomus.user:
        print(f"Available {balance.currency_code}: {balance.balance} {balance.currency_code} ({balance.balance_usd} USD)")
    print('--------------')
    print('XRocket:')
    for bal in balance.balances:
        print(f"Available {bal.currency}: {bal.balance} {bal.currency}")
    print('------------------------------------------')

    order_payok = await payok.create_pay(15, "orderId")
    order_freeKassa = await freeKassa.create_order(1, "example@gmail.com", "0.0.0.0", 150, "RUB")
    order_ruKassa = await ruKassa.create_payment(15)
    order_lolz = lolz.get_payment_link(15, comment="orderId")
    order_aaio = await aaio.create_payment_url(15, "orderId")
    order_crypto_bot = await cryptoBot.create_invoice(15, currency_type="crypto", asset="USDT")
    order_crystal_pay = await crystalPay.create_payment(15)
    order_cryptomus = await cryptomus.create_payment("15", "RUB", "orderId")
    order_xrocket = await xrocket.create_invoice(1, "TONCOIN", 1)

    print("PayOK", order_payok)
    print("FreeKassa", order_freeKassa.location)
    print("RuKassa: ", order_ruKassa.url)
    print("Lolz: ":, order_lolz)
    print("Aaio: ", order_aaio)
    print("CryptoBot: ", order_crypto_bot.pay_url)
    print("CrystalPay: ", order_crystal_pay.url)
    print("Cryptomus: ", order_cryptomus.url)
    print("XRocket: ", order_xrocket.link)

    print('------------------------------------------')

    info_payok = await payok.get_transactions("orderId")
    info_freeKassa = await freeKassa.get_orders("orderId")
    info_ruKassa = await ruKassa.get_info_payment("orderId")
    info_lolz = await lolz.check_status_payment(50, "orderId")
    info_aaio = await aaio.get_order_info("orderId")
    info_crypto_bot = await cryptoBot.get_invoices(
        invoice_ids=["orderId"], count=1
    )
    info_crystal_pay = await crystalPay.get_payment_info("orderId")
    info_cryptomus = await cryptomus.payment_info(order_id="orderId")
    info_xrocket = await xrocket.get_invoice_info('orderId')

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
    print("Amount: ", 15)
    print("Status: ", info_lolz)
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
    print("Amount": info_xrocket.amount)
    print("Status": info_xrocket.status)


asyncio.run(main())
```
## Output
```Python
PayOK:
Ba;ance: 0
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
Available BNB:  0.0  (In hold: 0.0)
Available TRX:  0.0  (In hold: 0.0)
Available USDC:  0.0  (In hold: 0.0)
--------------
CrystalPay:
Available BITCOIN: 0 BTC
Available BITCOINCASH: 0 BCH
Available BNBCRYPTOBOT: 0 BNB
Available BNBSMARTCHAIN: 0 BNB
Available BTCCRYPTOBOT: 0 BTC
Available CARDRUBP2P: 0 RUB
Available DASH: 0 DASH
Available DOGECOIN: 0 DOGE
Available ETHCRYPTOBOT: 0 ETH
Available ETHEREUM: 0 ETH
Available LITECOIN: 0 LTC
Available LTCCRYPTOBOT: 0 LTC
Available LZTMARKET: 0 RUB
Available POLYGON: 0 MATIC
Available SBERPAYP2P: 0 RUB
Available SBPP2P: 0 RUB
Available TONCOIN: 0 TON
Available TONCRYPTOBOT: 0 TON
Available TRON: 0 TRX
Available USDCTRC: 0 USDC
Available USDTCRYPTOBOT: 0 USDT
Available USDTTRC: 0 USDT
--------------
Cryptomus:
Merchant:

Available VERSE: 0.00000000 VERSE (0.00000000 USD)
Available DAI: 0.00000000 DAI (0.00000000 USD)
Available ETH: 0.00000000 ETH (0.00000000 USD)
Available BCH: 0.00000000 BCH (0.00000000 USD)
Available DASH: 0.00000000 DASH (0.00000000 USD)
Available BNB: 0.00000000 BNB (0.00000000 USD)
Available XMR: 0.00000000 XMR (0.00000000 USD)
Available SOL: 0.00000000 SOL (0.00000000 USD)
Available DOGE: 0.00000000 DOGE (0.00000000 USD)
Available USDC: 0.00980000 USDC (0.00980031 USD)
Available CGPT: 0.00000000 CGPT (0.00000000 USD)
Available USDT: 0.00315576 USDT (0.00315333 USD)
Available TON: 0.00000000 TON (0.00000000 USD)
Available BUSD: 0.00000000 BUSD (0.00000000 USD)
Available TRX: 0.01116951 TRX (0.00269201 USD)
Available POL: 0.13433365 POL (0.06417564 USD)
Available AVAX: 0.00000000 AVAX (0.00000000 USD)
Available BTC: 0.00000000 BTC (0.00000000 USD)
Available LTC: 0.00000136 LTC (0.00017045 USD)
Available SHIB: 0.00000000 SHIB (0.00000000 USD)
Available HMSTR: 0.00000000 HMSTR (0.00000000 USD)

User:

Available DASH: 0.00000000 DASH (0.00000000 USD)
Available ETH: 0.00000000 ETH (0.00000000 USD)
Available VERSE: 0.00000000 VERSE (0.00000000 USD)
Available CRMS: 0.12041311 CRMS (0.12041311 USD)
Available DAI: 0.00000000 DAI (0.00000000 USD)
Available BUSD: 0.00000000 BUSD (0.00000000 USD)
Available SOL: 0.00000000 SOL (0.00000000 USD)
Available USDT: 0.00975846 USDT (0.00975097 USD)
Available CGPT: 0.00000000 CGPT (0.00000000 USD)
Available BNB: 0.00000000 BNB (0.00000000 USD)
Available BTC: 0.00000000 BTC (0.00000000 USD)
Available USDC: 0.00000000 USDC (0.00000000 USD)
Available DOGE: 0.00000000 DOGE (0.00000000 USD)
Available AVAX: 0.00000000 AVAX (0.00000000 USD)
Available LTC: 0.00000000 LTC (0.00000000 USD)
Available XMR: 0.00000000 XMR (0.00000000 USD)
Available BCH: 0.00000000 BCH (0.00000000 USD)
Available POL: 0.00000000 POL (0.00000000 USD)
Available TON: 0.00000000 TON (0.00000000 USD)
Available TRX: 0.00000000 TRX (0.00000000 USD)
Available SHIB: 0.00000000 SHIB (0.00000000 USD)
Available HMSTR: 0.00000000 HMSTR (0.00000000 USD)
--------------
XRocket:
Available TONCOIN: 0 TONCOIN
Available XROCK: 0 XROCK
Available SCALE: 0 SCALE
Available BOLT: 0 BOLT
Available TAKE: 0 TAKE
Available HEDGE: 0 HEDGE
Available KOTE: 0 KOTE
Available TNX: 0 TNX
Available GRBS: 0 GRBS
Available AMBR: 0 AMBR
Available JBCT: 0 JBCT
Available IVS: 0 IVS
Available LAVE: 0 LAVE
Available DHD: 0 DHD
Available KINGY: 0 KINGY
Available REDX: 0 REDX
Available GGT: 0 GGT
Available PET: 0 PET
Available JETTON: 0 JETTON
Available BNB: 0 BNB
Available USDT: 0 USDT
Available LIFEYT: 0 LIFEYT
Available GEMSTON: 0 GEMSTON
Available BTC: 0 BTC
Available NANO: 0 NANO
Available ANON: 0 ANON
Available ATL: 0 ATL
Available NUDES: 0 NUDES
Available WIF: 0 WIF
Available MARGA: 0 MARGA
Available DUREV: 0 DUREV
Available SOX: 0 SOX
Available UNIC: 0 UNIC
Available VIRUS1: 0 VIRUS1
Available ICTN: 0 ICTN
Available JMT: 0 JMT
Available FID: 0 FID
Available CATS: 0 CATS
Available WALL: 0 WALL
Available NOT: 0 NOT
Available OPEN: 0 OPEN
Available MORFEY: 0 MORFEY
Available MMM: 0 MMM
Available CAVI: 0 CAVI
Available ALENKA: 0 ALENKA
Available TIME: 0 TIME
Available CES: 0 CES
Available KKX: 0 KKX
Available HYDRA: 0 HYDRA
Available GRC: 0 GRC
Available tsTON: 0 tsTON
Available STON: 0 STON
Available DOGS: 0 DOGS
Available TRX: 0 TRX
Available PUNK: 0 PUNK
Available TONNEL: 0 TONNEL
Available DFC: 0 DFC
Available ETH: 0 ETH
Available ARBUZ: 0 ARBUZ
Available UP: 0 UP
Available RAFF: 0 RAFF
Available DRIFT: 0 DRIFT
Available FISH: 0 FISH
Available MEOW: 0 MEOW
Available TINU: 0 TINU
Available BLKC: 0 BLKC
Available PROTON: 0 PROTON
Available GRAM: 0 GRAM
Available WEB3: 0 WEB3
Available MRDN: 0 MRDN
Available LKY: 0 LKY
Available STBL: 0 STBL
Available 1RUSD: 0 1RUSD
Available JVT: 0 JVT
Available DRA: 0 DRA
Available STATHAM: 0 STATHAM
Available SHEEP: 0 SHEEP
Available PLANKTON: 0 PLANKTON
Available MUMBA: 0 MUMBA
Available VWS: 0 VWS
Available LAIKA: 0 LAIKA
Available SAU: 0 SAU
Available GOY: 0 GOY
Available BUFFY: 0 BUFFY
Available PIZZA: 0 PIZZA
Available SOL: 0 SOL
Available SLOW: 0 SLOW
Available THNG: 0 THNG
Available SP: 0 SP
Available AQUAXP: 0 AQUAXP
Available CATI: 0 CATI
Available HMSTR: 0 HMSTR
Available STORM: 0 STORM
Available SPN: 0 SPN
Available JETTY: 0 JETTY
Available MAJOR: 0 MAJOR
Available FTON: 0 FTON
Available CATSTG: 0 CATSTG
Available BUILD: 0 BUILD
Available TRUMP: 0 TRUMP
------------------------------------------
PayOK: https://payok.io//pay?amount=15&payment=4364575733&shop=12452&currency=RUB&desc=Description&sign=af2fdc6796750e3c6910230095ec0ed8
FreeKassa: https://pay.freekassa.com/form/161328352/576046439bd01de60a6e418bad9354a2
RuKassa:  https://pay.ruks.pro/?hash=435fc3cee737f9dac2b34c9ba9311eae
Lolz:  https://lzt.market/balance/transfer?user_id=4810752&hold=0&amount=15&comment=orderId
Aaio:  https://aaio.io/merchant/pay?merchant_id=f398c75d-b775-412c-9674-87939692c083&amount=15&order_id=orderId&currency=RUB&sign=6ad5dc2164059a255921ad216c7e5ffd0d2abcaec9af7415636fc12df938582f
CryptoBot:  https://t.me/CryptoBot?start=IVYOJWPOZh15
CrystalPay:  https://pay.crystalpay.io/?i=715308958_rPwTzvsvCmabwl
Cryptomus:  https://pay.cryptomus.com/pay/6c0j685d-2bc1-41a1-954b-b11def3641a4
XRocket:  https://t.me/xrocket?start=inv_NX9RajMus37wbn3
------------------------------------------
PayOK:
Amount:  15
Status: 0
--------------
FreeKassa:
Amount:  150
Status: 0
--------------
RuKassa:
Amount:  50
Status:  WAIT
--------------
Lolz:
Amount:  15
Status:  False
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
Amount: 15.00
Status:  check
--------------
XRocket:
Amount: 1.0
Status:  active

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

## Developer Links
> Zelenka (Lolzteam): https://lzt.market/tosa <br>
> GitHub: https://github.com/I-ToSa-I <br>
> Telegram: https://t.me/ToSa_LZT
