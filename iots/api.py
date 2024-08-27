import json
from typing import Union, List

import requests
from pydantic import BaseModel

from .apis.spaces import _SpacesMethods
from .models.exceptions import APIException
from .security import (
    AccessToken,
    OAuth2ClientCredentials,
    SecurityStrategyWithTokenExchange,
)


class API(_SpacesMethods):
    """
    The top-level class used as an abstraction of the AnythingDB - API reference.
    """

    def __init__(self, host: str = "https://api.swx.altairone.com",
                 security_strategy: Union[AccessToken, OAuth2ClientCredentials] = None,
                 verify: bool = True):
        """
        Creates a new API instance.

        :param host: (optional) Host name of the AnythingDB - API reference.
        :param security_strategy: (optional) The security strategy for the API client.
        :param verify: (optional) Whether to verify the server's TLS certificate.
        """
        if not host.startswith("http://") and not host.startswith("https://"):
            host = "https://" + host

        self.host = host
        self._verify = verify
        self.headers = {}
        self._raise_errors = True

        self._security_strategy = security_strategy
        if self._security_strategy:
            self.with_security(self._security_strategy)

    def with_security(self, security_strategy: Union[AccessToken, OAuth2ClientCredentials]):
        """
        Sets the security strategy for the API client. If the provided security
        strategy requires token exchange and retrieval, the method will retrieve
        the access token automatically.

        :param security_strategy: The security strategy to be set for the API client.
        :type security_strategy: Union[AccessToken, OAuth2ClientCredentials]
        :return: The modified API client with the specified security strategy.
        """
        self._security_strategy = security_strategy

        if isinstance(self._security_strategy, SecurityStrategyWithTokenExchange):
            self._security_strategy.set_token_url_host(self.host)
            self._security_strategy.set_verify_tls_certificate(self._verify)
            self._security_strategy.get_token()

        return self

    def set_token(self, token: str):
        """
        Sets an already exchanged access token as a bearer token security
        strategy.

        :return: The modified API client.
        """
        return self.with_security(AccessToken(token))

    def set_credentials(self, client_id: str, client_secret: str,
                        scopes: List[str],
                        token_url: str = '/oauth2/token',
                        revoke_token_url: str = '/oauth2/revoke',
                        refresh_threshold: int = 10):
        """
        Configure an OAuth2 security strategy using the Client Credentials flow.

        :param client_id: The client ID for OAuth2 client credentials authentication.
        :param client_secret: The client secret for OAuth2 client credentials authentication.
        :param scopes: The list of scopes to be requested during token exchange.
        :param token_url: The URL for token exchange.
        :param revoke_token_url: The URL for revoking access tokens (optional).
        :param refresh_threshold: The number of seconds before token expiration to trigger token refresh.
        :return: The modified API client.
        """
        return self.with_security(OAuth2ClientCredentials(client_id, client_secret,
                                                          scopes, token_url,
                                                          revoke_token_url,
                                                          refresh_threshold))

    def revoke_token(self):
        """ Revokes the access token. """
        if isinstance(self._security_strategy, OAuth2ClientCredentials):
            self._security_strategy.revoke_token()

    def make_request(self, method: str, url: str, body=None, params=None,
                     headers: dict = None, timeout: float = 3, auth: bool = True,
                     verify=None) -> requests.Response:
        """
        Makes a request to the API server.

        :param method: HTTP request method used (`GET`, `OPTIONS`, `HEAD`,
            `POST`, `PUT`, `PATCH`, or `DELETE`).
        :param url: Request URL. It can be a relative path or a full URL (the
            host used must be the same as the host in this :class:`API` instance).
        :param body: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the request.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP headers to send.
        :param timeout: (optional) How many seconds to wait for the server to
            send data before giving up, as a float, or a `(connect timeout,
            read timeout)` tuple.
        :param auth: (optional) If True (default), the authentication token will
            be sent in the request. An exception will be raised if no token is set.
        :param verify: (optional) If set as a boolean, it will override the API
            verify value.
        :return: An instance of :class:`request.Response`.
        """
        if headers is None:
            headers = {}

        headers.update(self.headers)

        # TODO: Handle request Content-Type
        if isinstance(body, dict):
            headers['Content-Type'] = 'application/json'
            body = json.dumps(body)
        elif isinstance(body, BaseModel):
            headers['Content-Type'] = 'application/json'
            body = body.json()

        if url.lower().startswith('http://') or url.lower().startswith('https://'):
            url = url
        else:
            url = self.host + url

        req = requests.Request(method, url, params=params,
                               headers=headers, data=body)

        if auth:
            if not self._security_strategy:
                raise APIException("No security strategy has been set")
            self._security_strategy.apply(req)

        if verify is None:
            verify = self._verify

        return requests.request(req.method, req.url, params=req.params,
                                headers=req.headers, data=req.data,
                                timeout=timeout, verify=verify)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if self._security_strategy:
            self._security_strategy.clean()
