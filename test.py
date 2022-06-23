import json
from typing import List
import requests
from django.conf import settings

# ./manage.py shell < test.py
# ["account-info",
#          "operation-history",
#          "operation-details",
#          "incoming-transfers",
#          "payment-p2p",
#          "payment-shop"]


class YooMoneyError(Exception):
    """Basic class"""


class InvalidToken(YooMoneyError):

    message = "Token is not valid, or does not have the appropriate rights"

    def __init__(self, ):
        super().__init__(self.message)


class IllegalParamType(YooMoneyError):

    message = "Invalid parameter value 'type'"

    def __init__(self, ):
        super().__init__(self.message)


class IllegalParamStartRecord(YooMoneyError):

    message = "Invalid parameter value 'start_record'"
    def __init__(self, ):

        super().__init__(self.message)


class IllegalParamRecords(YooMoneyError):

    message = "Invalid parameter value 'records'"

    def __init__(self, ):
        super().__init__(self.message)


class IllegalParamLabel(YooMoneyError):

    message = "Invalid parameter value 'label'"

    def __init__(self, ):
        super().__init__(self.message)


class IllegalParamFromDate(YooMoneyError):

    message = "Invalid parameter value 'from_date'"

    def __init__(self, ):
        super().__init__(self.message)


class IllegalParamTillDate(YooMoneyError):

    message = "Invalid parameter value 'till_date'"

    def __init__(self, ):
        super().__init__(self.message)


class IllegalParamOperationId(YooMoneyError):

    message = "Invalid parameter value 'operation_id'"

    def __init__(self, ):
        super().__init__(self.message)


class TechnicalError(YooMoneyError):

    message = "Technical error, try calling the operation again later"

    def __init__(self, ):
        super().__init__(self.message)


class InvalidRequest(YooMoneyError):

    message = "Required query parameters are missing or have incorrect or invalid values"

    def __init__(self, ):
        super().__init__(self.message)


class UnauthorizedClient(YooMoneyError):

    message = "Invalid parameter value 'client_id' or 'client_secret', or the application" \
              " does not have the right to request authorization (for example, YooMoney blocked it 'client_id')"

    def __init__(self, ):
        super().__init__(self.message)


class InvalidGrant(YooMoneyError):

    message = "In issue 'access_token' denied. YooMoney did not issue a temporary token, " \
              "the token is expired, or this temporary token has already been issued " \
              "'access_token' (repeated request for an authorization token with the same temporary token)"

    def __init__(self, ):
        super().__init__(self.message)


class EmptyToken(YooMoneyError):

    message = "Response token is empty. Repeated request for an authorization token"

    def __init__(self, ):
        super().__init__(self.message)


CLIENT_ID = "31B8EB7BA78BD618A38458465652441CF50D61E2D897ADF30A125C4BC6C9462D"
REDIRECT_URL = "http://127.0.0.1"
SCOPE = ["account-info",
         "operation-history",
         "operation-details",
         "incoming-transfers"]


class YooMoneyAuth:
    def __init__(self, client_id: str, redirect_uri: str, scope: List[str]):
        self.client_id = client_id
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
        url = "https://yoomoney.ru/oauth/token?code={code}&client_id={client_id}&" \
              "grant_type=authorization_code&redirect_uri={redirect_uri}"\
            .format(code=code,
                    client_id=self.client_id,
                    redirect_uri=self.redirect_uri)
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


class YooMoneyClient:
    def __init__(self, token: str):
        self.base_url = "https://yoomoney.ru/api/"
        self.token = token

    def account_info(self):
        """
        Get simple account information
        """
        method = "account-info"
        url = self.base_url + method
        headers = {'Authorization': 'Bearer ' + str(self.token),
                   'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, headers=headers)
        return response.json()

    # https://yoomoney.ru/docs/payment-buttons/using-api/forms


class YooMoneyPay:
    """
    https://yoomoney.ru/docs/payment-buttons
    """
    def __init__(self,
                 receiver: str,
                 quickpay_form: str,
                 targets: str,
                 paymentType: str,
                 sum: int,
                 label: str = None,
                 successURL: str = None,
                 need_fio: bool = None,
                 need_email: bool = None,
                 need_phone: bool = None,
                 need_address: bool = None):

        self.receiver = receiver
        self.quickpay_form = quickpay_form
        self.targets = targets
        self.paymentType = paymentType
        self.sum = sum
        self.label = label
        self.successURL = successURL
        self.need_fio = need_fio
        self.need_email = need_email
        self.need_phone = need_phone
        self.need_address = need_address

        self.response = self._request()

    def _request(self):
        self.base_url = "https://yoomoney.ru/quickpay/confirm.xml?"
        payload = {"receiver": self.receiver,
                   "quickpay_form": self.quickpay_form,
                   "targets": self.targets,
                   "paymentType": self.paymentType,
                   "sum": self.sum}

        if self.label != None:
            payload["label"] = self.label
        if self.successURL != None:
            payload["successURL"] = self.successURL
        if self.need_fio != None:
            payload["need_fio"] = self.need_fio
        if self.need_email != None:
            payload["need_email"] = self.need_email
        if self.need_phone != None:
            payload["need_phone"] = self.need_phone
        if self.need_address != None:
            payload["need_address"] = self.need_address

        for value in payload:
            self.base_url += str(value).replace("_", "-") + "=" + str(
                payload[value])
            self.base_url += "&"
        self.base_url = self.base_url[:-1].replace(" ", "%20")

        response = requests.post(self.base_url)

        self.redirected_url = response.url

        return response


#yoo_auth = YooMoneyAuth(client_id=CLIENT_ID, redirect_uri=REDIRECT_URL, scope=SCOPE)
#print(yoo_auth.get_auth_url())
# 376856C23C914D8BFE160A30852371C1687606DFE1A2351F17EB7EE6B5761CEC28836851B7D1554DF2E74E248F9911B9B171546A0EB620D6D54A74A844EFDCAF105E1FE47CFBCE730A125010A7B1F0D43C2FE78C936775EE02678D6C113961AE9A665CF6B9B3A0304F3BEA48F72CFBFFC2CDB0CDBF6CB354FC149A51E1EBBA7C
#print(yoo_auth.auth_by_code("376856C23C914D8BFE160A30852371C1687606DFE1A2351F17EB7EE6B5761CEC28836851B7D1554DF2E74E248F9911B9B171546A0EB620D6D54A74A844EFDCAF105E1FE47CFBCE730A125010A7B1F0D43C2FE78C936775EE02678D6C113961AE9A665CF6B9B3A0304F3BEA48F72CFBFFC2CDB0CDBF6CB354FC149A51E1EBBA7C"))
#TOKEN = """410015505324410.6E3E19D46B8688AF80749DB08036EFCBA04D691EDF5A16F1FA9942174A6F19DDC2C8926DE233DC2CC8A56ABB194D31797356B78F5573F5AAF9CF65B0F4082C206E0AD3A40729D839B2B38B052E12275B489B3DB9EF6F388D8FA70E60D9FC72ED637095300EFADCC74A9017E4D95491C5EB6929F4AA3EB264A5B12C8E346710E6"""
#yoo_client = YooMoneyClient(token=TOKEN)

# Номер кошелька ЮMoney, на который нужно зачислять деньги отправителей
#receiver = yoo_client.account_info()["account"]

# https://yoomoney.ru/docs/payment-buttons/using-api/forms
yoo_pay = YooMoneyPay("410015505324410",
                      "shop",
                      "A-123",
                      "AC",
                      2,
                      "A-123",
                      REDIRECT_URL,
                      None,
                      None,
                      None,
                      None)

print(yoo_pay.redirected_url)
