import requests
from typing import List
from .exceptions import *


class YooMoneyAuth:
    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 redirect_uri: str,
                 scope: List[str]):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def get_auth_url(self):
        """
        Send POST request to get an url that user have to visit to confirm
        app access and copy 'code=XXXXXXX' from response url to paste it for
        the auth_by_code method
        """
        url = "https://yoomoney.ru/oauth/authorize?client_id={client_id}"\
              "&response_type=code&redirect_uri={redirect_uri}&scope={scope}"\
              .format(client_id=self.client_id,
                      redirect_uri=self.redirect_uri,
                      scope='%20'.join([str(elem) for elem in self.scope]))
        response = requests.post(url, headers=self.headers)

        if response.status_code == 200:
            return response.url

    def auth_by_code(self, code: str):
        """
        Send POST request to get an access token for further use
        """
        url = "https://yoomoney.ru/oauth/token?code={code}&"\
              "client_id={client_id}&grant_type=authorization_code"\
              "&redirect_uri={redirect_uri}&client_secret={client_secret}"\
            .format(code=code,
                    client_id=self.client_id,
                    redirect_uri=self.redirect_uri,
                    client_secret=self.client_secret)
        response = requests.post(url, headers=self.headers)

        if "error" in response.json():
            error = response.json()["error"]
            if error == "invalid_request":
                raise InvalidRequest()
            elif error == "unauthorized_client":
                raise UnauthorizedClient()
            elif error == "invalid_grant":
                raise InvalidGrant()

        if response.json()['access_token'] == "":
            raise EmptyToken()

        return response.json()['access_token']
