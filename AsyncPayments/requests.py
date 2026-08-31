import ssl
import certifi
from typing import Optional
from aiohttp import ClientSession, TCPConnector, ClientResponse
from .exceptions.exceptions import (BadRequest, RequestError, MissingScopeError, IncorrectTokenError, UnexpectedError, UnauthorizedClient, 
                                    InvalidGrant, EmptyToken)


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
    
    def _delete_empty_fields(self, params: dict) -> None:
        for key, value in params.copy().items():
            if value is None:
                params.pop(key)
                
    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
            
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _request_for_authorize_yoomoney(self, method: str, url: str, **kwargs) -> ClientResponse:
        session = self._getsession()
        return await session.request(method, url, **kwargs)
    
    async def _request(self, payment: str, method: str, url: str, **kwargs) -> dict:
        session = self._getsession()
        async with session.request(method, url, **kwargs) as response:
            if response.status in [200, 201]:
                if payment == "ruKassa":
                    response = await response.json(content_type="text/html")
                elif payment == "yoomoney_quick-pay":
                    response = response.url
                elif payment == "xrocket" and method == "DELETE" and response.content_length == 0:
                    response = True
                else:
                    response = await response.json()
            else:
                try:
                    response_json = await response.json()
                    if response_json:
                        return await self._checkexception(payment, response_json)
                    else:
                        raise RequestError(
                            f"{payment}. Response status: {response.status}. Text: {await response.text()}"
                        )
                except (BadRequest, RequestError, MissingScopeError, IncorrectTokenError, UnexpectedError, UnauthorizedClient, InvalidGrant, EmptyToken):
                    raise
                except Exception:
                    raise RequestError(
                        f"{payment}. Response status: {response.status}. Text: {await response.text()}"
                    )
            return response

    async def _checkexception(self, payment: str, response: dict) -> dict:
        if payment == "aaio":
            if response.get("type") == "error":
                raise BadRequest("[AAIO] " + response["message"])
        elif payment == "crystalPay":
            if response.get("error"):
                raise BadRequest("[CrystalPay] " + response["errors"][0])
        elif payment == "cryptoBot":
            if not response.get("ok"):
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
        elif payment == "cryptomus":
            if response.get('state') != 0:
                if response.get("errors"):
                    raise BadRequest("[Cryptomus] " + str(response.get("errors")))
                else:
                    raise BadRequest("[Cryptomus] " + str(response.get("message")))
            else:
                raise BadRequest("[Cryptomus] " + response.get("message"))
        elif payment == "xrocket":
            raise BadRequest(
                f"[XRocket] Status code: {response.get('status')}. Error type: {response.get('type')}. Title: {response.get('title')}. " \
                f"Detail: {response.get('detail')}. Instance: {response.get('instance')}. Kind: {response.get('kind')}"
            )
        elif payment == "yoomoney":
            if response.get("error"):
                raise BadRequest("[YooMoney] " + response.get("error_description") + ". Error code: " + response['error'])
        elif payment == "2328io":
            if response.get("state") == 1:
                raise BadRequest("[2328.io] " + str(response.get("errors")))
        else:
            # RollyPay
            if response.get("error"):
                raise BadRequest("[RollyPay] " + response['error'])

        return response
