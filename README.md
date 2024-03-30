# AsyncPayments
> Add payment acceptance to your projects.
## Installing
    pip install AsyncPayments
## Version
    v1.4.2
## Code example
```python
import asyncio

from AsyncPayments.ruKassa import AsyncRuKassa
from AsyncPayments.lolz import AsyncLolzteamMarketPayment
from AsyncPayments.aaio import AsyncAaio
from AsyncPayments.cryptoBot import AsyncCryptoBot
from AsyncPayments.crystalPay import AsyncCrystalPay

ruKassa = AsyncRuKassa("Api-Token", 1, "Email", "Password") # 1 - ShopID
lolz = AsyncLolzteamMarketPayment("Token")
aaio = AsyncAaio("ApiKey", "ShopId", "SecretKey")
cryptoBot = AsyncCryptoBot("Token")
crystalPay = AsyncCrystalPay("Login", "Secret", "Salt")

async def main():
    balance_rukassa = await ruKassa.get_balance()
    balance_lolz = await lolz.get_me()
    balance_aaio = await aaio.get_balance()
    balance_crypto_bot = await cryptoBot.get_balance()
    balance_crystal_pay = await crystalPay.get_balance()
    
    print("RuKassa:")
    print("RUB: ", balance_rukassa.balance_rub)
    print("USD: ", balance_rukassa.balance_usd)
    print('--------------')
    print("Lolz:")
    print('ID: ', balance_lolz.user_id)
    print('Никнейм: ', balance_lolz.username)
    print('Доступно: ', balance_lolz.balance)
    print('В холде: ', balance_lolz.hold)
    print('--------------')
    print("Aaio:")
    print('Доступно: ', balance_aaio.balance)
    print('В холде: ', balance_aaio.hold)
    print('Реферальный: ', balance_aaio.referral)
    print('--------------')
    print("CryptoBot:")
    for balance in balance_crypto_bot:
        print(f"Доступно {balance.currency_code}: ", balance.available, f" (В холде: {balance.onhold})")
    print('--------------')
    print("CrystalPay:")
    for currency, balance in balance_crystal_pay:
        print(f"Доступно {currency}:", balance.amount, f" {balance.currency}")
    
    print('------------------------------------------')
    
    order_ruKassa = await ruKassa.create_payment(15)
    order_lolz = lolz.get_payment_link(15, comment="orderId")
    order_aaio = await aaio.create_payment_url(15, "orderId")
    order_crypto_bot = await cryptoBot.create_invoice(15, currency_type="crypto", asset="USDT")
    order_crystal_pay = await crystalPay.create_payment(15)
    
    print("RuKassa: ", order_ruKassa.url)
    print('Lolz: ', order_lolz)
    print('Aaio: ', order_aaio)
    print('CryptoBot: ', order_crypto_bot.pay_url)
    print('CrystalPay: ', order_crystal_pay.url)
    
    print('------------------------------------------')
    
    info_ruKassa = await ruKassa.get_info_payment("orderId")
    info_lolz = await lolz.check_status_payment(50, "orderId")
    info_aaio = await aaio.get_order_info("orderId")
    info_crypto_bot = await cryptoBot.get_invoices(
        invoice_ids=["orderId"], count=1
    )
    info_crystal_pay = await crystalPay.get_payment_info("orderId")
    
    print('RuKassa:')
    print("Сумма: ", info_ruKassa.amount)
    print("Статус: ", info_ruKassa.status)
    print('--------------')
    print("Lolz:")
    print("Сумма: ", 15)
    print("Статус: ", info_lolz)
    print('--------------')
    print("Aaio:")
    print("Сумма: ", info_aaio.amount)
    print("Статус: ", info_aaio.status)
    print('--------------')
    print("CryptoBot:")
    print("Сумма: ", info_crypto_bot.amount)
    print("Статус: ", info_crypto_bot.status)
    print('--------------')
    print("CrystalPay:")
    print("Сумма: ", info_crystal_pay.amount)
    print("Статус:", info_crystal_pay.state)
    

asyncio.run(main())
```
## Output
```Python
RuKassa:
RUB:  34.0
USD:  234.1
--------------
Lolz:
ID:  4810752
Никнейм:  ToSa
Доступно:  5233.0
В холде:  234.0
--------------
Aaio:
Доступно:  1235.0
В холде:  0.0
Реферальный:  0.0
--------------
CryptoBot:
Доступно USDT:  15.0  (В холде: 0.0)
Доступно TON:  0.0  (В холде: 0.0)
Доступно BTC:  0.00000023  (В холде: 0.0)
Доступно LTC:  0.0  (В холде: 0.0)
Доступно ETH:  0.0  (В холде: 0.0)
Доступно BNB:  0.0  (В холде: 0.0)
Доступно TRX:  0.0  (В холде: 0.0)
Доступно USDC:  0.0  (В холде: 0.0)
--------------
CrystalPay:
Доступно BITCOIN: 0.0  BTC
Доступно BITCOINCASH: 0.0  BCH
Доступно BNBCRYPTOBOT: 0.0  BNB
Доступно BNBSMARTCHAIN: 0.0  BNB
Доступно BTCBANKER: 0.0  RUB
Доступно BTCCHATEX: 0.0  RUB
Доступно BTCCRYPTOBOT: 0.0  BTC
Доступно CARDRUBP2P: 0.0  RUB
Доступно CARDTRYP2P: 0.0  TRY
Доступно DASH: 0.0  DASH
Доступно DOGECOIN: 0.0  DOGE
Доступно ETHBANKER: 0.0  RUB
Доступно ETHCRYPTOBOT: 0.0  ETH
Доступно ETHEREUM: 0.0  ETH
Доступно LITECOIN: 0.0  LTC
Доступно LTCBANKER: 0.0  RUB
Доступно LZTMARKET: 184.0  RUB
Доступно POLYGON: 0.0  MATIC
Доступно TONCRYPTOBOT: 0.09825723  TON
Доступно TRON: 0.0  TRX
Доступно USDCTRC: 0.0  USDC
Доступно USDTBANKER: 0.0  RUB
Доступно USDTCHATEX: 0.0  RUB
Доступно USDTCRYPTOBOT: 0.144637  USDT
Доступно USDTTRC: 0.0  USDT
------------------------------------------
RuKassa:  https://pay.ruks.pro/?hash=435fc3cee737f9dac2b34c9ba9311eae
Lolz:  https://lzt.market/balance/transfer?user_id=4810752&hold=0&amount=15&comment=orderId
Aaio:  https://aaio.io/merchant/pay?merchant_id=f398c75d-b775-412c-9674-87939692c083&amount=15&order_id=orderId&currency=RUB&sign=6ad5dc2164059a255921ad216c7e5ffd0d2abcaec9af7415636fc12df938582f
CryptoBot:  https://t.me/CryptoBot?start=IVYOJWPOZh15
CrystalPay:  https://pay.crystalpay.io/?i=715297022_MxRoixNnSrMSBD
------------------------------------------
RuKassa:
Сумма:  50
Статус:  WAIT
--------------
Lolz:
Сумма:  15
Статус:  False
--------------
Aaio:
Сумма:  299.0
Статус:  in_process
--------------
CryptoBot:
Сумма:  15
Статус:  active
--------------
CrystalPay:
Сумма:  15.0
Статус: notpayed

```

## Docs
> Lolzteam Market: https://lzt-market.readme.io/reference/ <br>
> Aaio: https://wiki.aaio.io <br>
> CryptoBot: https://help.crypt.bot/crypto-pay-api <br>
> CrystalPay: https://docs.crystalpay.io <br>
> RuKassa: https://lk.rukassa.is/api/v1 <br>

## Developer Links
> Zelenka (Lolzteam): https://zelenka.guru/tosa <br>
> GitHub: https://github.com/I-ToSa-I <br>
> Telegram: https://t.me/ToSa_LZT
