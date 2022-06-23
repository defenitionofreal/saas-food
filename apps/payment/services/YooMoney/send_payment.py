import requests


class YooMoneyPay:
    """
    Dont need to be authorized for this !
    https://yoomoney.ru/docs/payment-buttons
    ________________________________________
    отправлять на фронте на (yoo_pay.redirected_url)
    """
    def __init__(self,
                 receiver: str,
                 quickpay_form: str,
                 targets: str,
                 paymentType: str,
                 sum: int,
                 formcomment: str = None,
                 shortdest: str = None,
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
        self.formcomment = formcomment
        self.shortdest = shortdest
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

        if self.formcomment != None:
            payload["formcomment"] = self.formcomment
        if self.shortdest != None:
            payload["short-dest"] = self.shortdest
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
