import os

import requests

from .category import _CategoriesMethod
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

    def __init__(self, host: str = ""):
        host = host if host else get_host()
        if not host:
            raise ValueError("empty host")

        if not host.startswith("http://") and not host.startswith("https://"):
            host = "https://" + host
        self.host = host

    def make_request(self, method: str, path: str, headers: dict = None,
                     body=None, auth: bool = True):
        if headers is None:
            headers = {}

        if auth:
            headers['Authorization'] = 'Bearer valid-token'

        if isinstance(body, dict):
            headers['Content-Type'] = 'application/json'

        resp = requests.request(method,
                                self.host + path,
                                headers=headers,
                                data=body,
                                timeout=3)

        if resp.status_code >= 400:
            raise Exception(f"API error: {resp.status_code} - {resp.text}")

        return resp
