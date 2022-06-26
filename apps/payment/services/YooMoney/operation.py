import requests
from typing import TypeGuard


class Operation:
    def __init__(self,
                 operation_id: str,
                 amount: int,
                 withdraw_amount: int,
                 datetime: str,
                 sha1_hash: str,
                 test_notification: TypeGuard = True,
                 unaccepted: TypeGuard = False,
                 sender: str = "",
                 codepro: TypeGuard = False,
                 label: str = "",
                 notification_type: str = "card-incoming",
                 currency: str = "643"):
        pass
