import os

import requests

from .errors import ExcMissingToken, ResponseError
from .spaces import _SpacesMethod
from .auth.token import get_token, revoke_token


class API(_SpacesMethod):
    """
    The top-level class used as an abstraction of the SmartWorks API.
    """

    def __init__(self, host: str = "", token: str = "", beta: bool = True):
        """
        Creates a new API instance.

        :param host: (optional) SmartWorks API host name
            (e.g. https://api.swx.altairone.com). If not set, it will try to
            get the host from the `SWX_API_URL` environment variable.
            If the host is not set and the environment variable does not exist,
            it will raise a ValueError.
        :param token: (optional) Access token used for API authentication.
            It can also be set using :func:`~API.set_token` or setting the
            client credentials with :func:`~API.get_token`.
        :param beta: (optional) If True, a special header will be added to all
            the requests made to the SmartWorks API to use features in beta
            stage.
        """
        host = host if host else os.getenv("SWX_API_URL")
        if not host:
            raise ValueError("empty host")

        if not host.startswith("http://") and not host.startswith("https://"):
            host = "https://" + host

        self.host = host
        self._token = token
        self._beta = beta
        self.headers = {}
        if beta:
            self.headers['Prefer'] = "preview=2023.1"

    def set_token(self, token: str):
        """
        Sets the bearer token used for API authentication.

        :param token: Access token.
        """
        self._token = token
        return self

    def get_token(self, client_id: str, client_secret: str, scopes: list):
        """
        Returns a :class:`CredentialsAPI` instance that automatically requests
        an OAuth 2.0 Bearer Token from SmartWorks using the client_credentials
        grant. If the request fails, an OAuth2Error will be raised.

        This method can be used as a context manager to automatically revoke
        the access token after the `with` block. Example:

        .. code-block:: python

            with API().get_token(client_id, client_secret, ["thing"]) as api:
                categories = api.categories()

        :param client_id:       Client ID.
        :param client_secret:   Client Secret.
        :param scopes:          List of scopes to request.
        :return:                :class:`CredentialsAPI` instance.
        """
        api = CredentialsAPI(self.host, client_id, client_secret, scopes,
                             self._beta)
        api.headers = self.headers
        return api

    def make_request(self, method: str, path: str, body=None, params=None,
                     headers: dict = None, auth: bool = True) -> requests.Response:
        """
        Makes a request to the API server.

        :param method: HTTP request method used (`GET`, `OPTIONS`, `HEAD`,
            `POST`, `PUT`, `PATCH`, or `DELETE`).
        :param path: Request URL. It can be a relative path or a full URL (the
            host used must be the same as the host in this :class:`API` instance).
        :param body: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the request.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP headers to send.
        :param auth: (optional) If True (default), the authentication token will
            be sent in the request. An exception will be raised if no token is set.
        :return: A :class:`request.Response`. If the response returns with a
            status code >= 400, a :class:`~.errors.ResponseError` exception will
            be raised.
        """
        if headers is None:
            headers = {}

        headers.update(self.headers)

        if auth:
            if not self._token:
                raise ExcMissingToken

            headers['Authorization'] = f'Bearer {self._token}'

        if isinstance(body, dict):
            headers['Content-Type'] = 'application/json'

        resp = requests.request(method, self.host + path, params=params,
                                headers=headers, data=body, timeout=3)

        if resp.status_code >= 400:
            raise ResponseError.parse(resp.json())

        return resp


class CredentialsAPI(API):
    """
    An API instance that handles authentication using the OAuth2 Client
    Credentials flow by getting and revoking access tokens.
    """

    def __init__(self, host: str, client_id: str, client_secret: str, scopes: list, beta: bool = True):
        """
        Creates a new CredentialsAPI instance.

        :param host: (optional) SmartWorks API host name
            (e.g. https://api.swx.altairone.com). If not set, it will try to
            get the host from the `SWX_API_URL` environment variable.
            If the host is not set and the environment variable does not exist,
            it will raise a ValueError.
        :param client_id:       Client ID.
        :param client_secret:   Client Secret.
        :param scopes:          List of scopes to request.
        :param beta: (optional) If True, a special header will be added to all
            the requests made to the SmartWorks API to use features in beta
            stage.
        """
        super().__init__(host, beta=beta)
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes

        self.renew_token()

    def __enter__(self):
        if not self._token:
            self.renew_token()
        return self

    def __exit__(self, *exc):
        self.revoke_token()

    def renew_token(self):
        """
        Revokes the old access token and gets a new one.
        """
        self.revoke_token()
        token = get_token(self.host, self.client_id, self.client_secret, self.scopes)
        self._token = token.access_token

    def revoke_token(self):
        """
        Revokes the access token.
        """
        if self._token:
            revoke_token(self.host, self._token, self.client_id, self.client_secret)
            self._token = None
