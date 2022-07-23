from rest_framework.response import Response


class ValidationCheck:
    def __init__(self, is_ok=False, response=Response()):
        self._is_ok = is_ok
        self._response_on_invalid = response

    @property
    def is_ok(self):
        return self._is_ok

    @property
    def false_response(self):
        return self._response_on_invalid
