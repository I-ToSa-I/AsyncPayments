import ssl
import certifi
import json

from typing import Optional
from aiohttp import ClientSession, TCPConnector

from .exceptions.exceptions import BadRequest, RequestError


class RequestsClient:

    def __init__(self) -> None:
        self._session: Optional[ClientSession] = None

    def _getsession(self) -> ClientSession:

        if isinstance(self._session, ClientSession) and not self._session.closed:
            return self._session

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)

        self._session = ClientSession(connector=connector)

        return self._session
    
    def _delete_empty_fields(self, params: dict):
        for key, value in params.copy().items():
            if value is None:
                params.pop(key)

    async def _request(self, payment: str, method: str, url: str, **kwargs) -> dict:

        session = self._getsession()

        async with session.request(method, url, **kwargs) as response:
            if response.status == 200:
                if payment in ["ruKassa"]:
                    response = await response.json(content_type="text/html")
                elif payment in ['payok']:
                    response = await response.json(content_type="text/plain")
                else:
                    response = await response.json()
            else:
                raise RequestError(
                    f"Response status: {response.status}. Text: {await response.text()}"
                )

        await self._session.close()

        return await self._checkexception(payment, response)

    async def _checkexception(self, payment: str, response: dict) -> dict:
        if payment == "aaio":
            if response["type"] == "error":
                raise BadRequest("[AAIO] " + response["message"])
        elif payment == "crystalPay":
            if response["error"]:
                raise BadRequest("[CrystalPay] " + response["errors"][0])
        elif payment == "cryptoBot":
            if not response["ok"]:
                raise BadRequest("[CryptoBot] " + response["error"]["name"])
        elif payment == "lolz":
            if response.get("error"):
                raise BadRequest("[Lolzteam Market] " + response["error_description"])
            if response.get("errors"):
                raise BadRequest("[Lolzteam Market] " + response["errors"][0])
        elif payment == "ruKassa":
            if response.get("error"):
                raise BadRequest("[RuKassa] " + response["message"])
        elif payment == "freeKassa":
            if response["type"] == "error" and not response.get("description"):
                raise BadRequest("[FreeKassa] " + response["message"])
        else:
            # payok
            if response.get("status") and response.pop("status") == "error":
                raise BadRequest("[PayOK] " + response.get("text", response.get("error_text")) + ". Error code: " + response['error_code'])

        return response
