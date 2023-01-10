import os

import requests

from .category import _CategoriesMethod
from .errors import ExcMissingToken
from .thing import _ThingsMethod


def get_host():
    """
    Returns the default SmartWorks host URL from the `SWX_API_URL` environment
    variable. If the variable is not found, None is returned.
    """
    return os.getenv("SWX_API_URL")


class API(_CategoriesMethod, _ThingsMethod):
    """
    This is the top-level class used as an abstraction of the SmartWorks API.
    """

    def __init__(self, host: str = "", token: str = ""):
        host = host if host else get_host()
        if not host:
            raise ValueError("empty host")

        if not host.startswith("http://") and not host.startswith("https://"):
            host = "https://" + host

        self.host = host
        self._token = token

    def token(self, token: str):
        """
        Set the bearer token used for API authentication.

        :param token: Access token.
        """
        self._token = token
        return self

    def make_request(self, method: str, url: str, headers: dict = None,
                     body=None, auth: bool = True) -> requests.Response:
        """
        Make a request to the API server.

        :param method: HTTP request method used (`GET`, `OPTIONS`, `HEAD`,
            `POST`, `PUT`, `PATCH`, or `DELETE`).
        :param url: Request URL. It can be a relative path or a full URL (the
            host used must be the same as the host in this :class:`API` instance).
        :param headers: (optional) Dictionary of HTTP headers to send.
        :param body: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the request.
        :param auth: (optional) If True (default), the authentication token will
            be sent in the request. An exception will be raised if no token is set.
        :return: A :class:`request.Response`. If the response returns with a
            status code >= 400, a :class:`ResponseError` exception will be raised.
        """
        if headers is None:
            headers = {}

        if auth:
            if not self._token:
                raise ExcMissingToken

            headers['Authorization'] = f'Bearer {self._token}'

        if isinstance(body, dict):
            headers['Content-Type'] = 'application/json'

        if not url.startswith(self.host):
            url = self.host + url

        resp = requests.request(method, url,
                                headers=headers, data=body, timeout=3)

        if resp.status_code >= 400:
            # TODO: Return ResponseError
            raise Exception(f"API error: {resp.status_code} - {resp.text}")

        return resp
