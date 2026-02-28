from typing import List
from ..requests import RequestsClient
from ..exceptions import InvalidRequest, InvalidGrant, EmptyToken, UnauthorizedClient

class Authorize(RequestsClient):
    def __init__(self, client_id: str, redirect_uri: str, client_secret: str, scope: List[str]):
        super().__init__()
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.client_secret = client_secret
        self.scope = scope
    
    async def authorize(self):
        url = "https://yoomoney.ru/oauth/authorize?client_id={client_id}&response_type=code" \
              "&redirect_uri={redirect_uri}&scope={scope}".format(client_id=self.client_id,
                                                                  redirect_uri=self.redirect_uri,
                                                                  scope='%20'.join([str(elem) for elem in self.scope]),
                                                                  )

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = await self._request_for_authorize_yoomoney("POST", url, headers=headers)
        if response.status == 200:
            print("Visit this website and confirm the application authorization request:")
            print(response.url)

        code = str(input("Enter redirected url (https://yourredirect_uri?code=XXXXXXXXXXXXX) or just code: "))
        try:
            code = code[code.index("code=") + 5:].replace(" ","")
        except:
            pass

        url = "https://yoomoney.ru/oauth/token?code={code}&client_id={client_id}&" \
              "grant_type=authorization_code&redirect_uri={redirect_uri}&client_secret={client_secret}".format(code=str(code), client_id=self.client_id, 
                                                                                                               redirect_uri=self.redirect_uri, 
                                                                                                               client_secret=self.client_secret
                                                                                                               )
        response = await self._request("yoomoney", "POST", url, headers=headers)
        
        if "error" in response:
            error = response["error"]
            if error == "invalid_request":
                raise InvalidRequest("Required query parameters are missing or have incorrect or invalid values.")
            elif error == "unauthorized_client":
                raise UnauthorizedClient("Invalid parameter value 'client_id' or 'client_secret', or the application" \
              " does not have the right to request authorization (for example, YooMoney blocked it 'client_id').")
            elif error == "invalid_grant":
                raise InvalidGrant("In issue 'access_token' denied. YuMoney did not issue a temporary token, " \
              "the token is expired, or this temporary token has already been issued " \
              "'access_token' (repeated request for an authorization token with the same temporary token).")

        if response['access_token'] == "":
            raise EmptyToken("Response token is empty. Repeated request for an authorization token.")

        print("Your access token:")
        print(response['access_token'])