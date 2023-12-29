import ssl
import certifi

from typing import Optional
from aiohttp import ClientSession, TCPConnector

from .exceptions import BadRequest

class RequestsClient:

    def __init__(self) -> None:
        self._session: Optional[ClientSession] = None

    def _getsession(self):

        if isinstance(self._session, ClientSession) and not self._session.closed:
            return self._session

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)

        self._session = ClientSession(connector=connector)

        return self._session

    async def _request(self,
                       payment: str,
                       method: str,
                       url: str,
                       **kwargs) -> dict:

        session = self._getsession()

        async with session.request(method, url, **kwargs) as response:

            response = await response.json()

        await self._session.close()

        return await self._checkexception(payment, response)

    async def _checkexception(self, payment: str,
                              response: dict) -> dict:
        if payment == "aaio":
            if response['type'] == 'error':
                raise BadRequest("[AAIO] " + response['message'])
        elif payment == "crystalPay":
            if response['error']:
                raise BadRequest("[CrystalPay] " + response['errors'][0])
        elif payment == "cryptoBot":
            if not response['ok']:
                raise BadRequest("[CryptoBot] " + response['error']['name'])
        elif payment == "lolz":
            if response.get("error"):
                raise BadRequest("[Lolzteam Market] " + response['error_description'])
            if response.get("errors"):
                raise BadRequest("[Lolzteam Market] " + response['errors'][0])

        return response