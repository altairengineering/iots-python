from typing import List

from requests import Response


class APIException(Exception):
    pass


class ResponseError(APIException):
    """ Client or server error response. """

    def __init__(self, error, *attr):
        super().__init__(*attr)
        if isinstance(error, Response):
            self._http_response = error
        else:
            self.error = error
            self._http_response = error.http_response()

    def http_response(self) -> Response:
        return self._http_response


class ExceptionList(APIException):
    def __init__(self, msg: str, exceptions: List[Exception], *attr):
        super().__init__(msg, *attr)
        self.exceptions = exceptions
