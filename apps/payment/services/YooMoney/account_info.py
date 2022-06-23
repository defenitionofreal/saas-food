import requests


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
