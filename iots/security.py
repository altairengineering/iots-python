import time
from abc import ABC, abstractmethod
from typing import List

import requests
from requests import Request

from .models.exceptions import ResponseError


class SecurityStrategy(ABC):
    """
    Abstract base class for defining security strategies in an API client.

    Subclasses of SecurityStrategy are responsible for applying security
    measures such as authentication and authorization to API requests.

    Methods:
     - `apply(request)`: Apply security measures to the given request.
     - `clean()`: Clean sensitive information from the security strategy.

    This class serves as a template for implementing different security
    strategies, allowing flexibility in handling various authentication
    mechanisms such as Bearer tokens, Basic authentication, OAuth2, etc.

    The :meth:`apply` method should be implemented by subclasses to apply
    the specific security measures required for the given request. It may involve
    adding headers, parameters, or performing other actions necessary to authenticate
    and authorize the request.

    The :meth:`clean` method should be implemented by subclasses to perform any
    necessary cleanup tasks such as revoking tokens or cleaning sensitive data
    from the security strategy when it is no longer needed.
    """

    @abstractmethod
    def apply(self, request: Request):
        """
        Apply security measures to the given request.

        :param request: The request object to which security measures will be applied.
        :type request: Request

        This method is implemented by subclasses to apply the specific
        security measures required for the given request. It may involve
        adding headers, parameters, or performing other actions necessary
        to authenticate and authorize the request.
        """
        pass

    @abstractmethod
    def clean(self):
        """
        Clean sensitive information from the security strategy.

        This method should be implemented by subclasses to perform any
        necessary cleanup tasks such as revoking tokens or cleaning
        sensitive data from the security strategy when it is no longer needed.
        """
        pass


class SecurityStrategyWithTokenExchange(SecurityStrategy):
    """
    Abstract base class for defining security strategies in an API client
    that require token exchange and revocation logic with a server.

    Subclasses of SecurityStrategyWithTokenExchange extend SecurityStrategy
    and provide additional methods for token exchange and revocation with
    a token server.

    Methods:
     - `apply(request)`: Apply security measures to the given request.
     - `clean()`: Clean sensitive information from the security strategy.
     - `set_token_url_host(token_url_host)`: Set the host URL for token exchange.
     - `set_verify_tls_certificate(verify)`: Set whether to verify the authentication server's TLS certificate.
     - `get_token()`: Exchange and retrieve a token from the server.
     - `revoke_token()`: Revoke the currently held token.

    This class serves as a template for implementing security strategies
    that involve exchanging tokens with a token server, such as OAuth2 or
    other token-based authentication mechanisms.
    """

    @abstractmethod
    def set_token_url_host(self, token_url_host: str):
        """
        Set the host URL for token exchange.

        This method should be implemented by subclasses to set the host URL
        where tokens can be exchanged with the server.

        :param token_url_host: The host URL for token exchange.
        """
        pass

    @abstractmethod
    def set_verify_tls_certificate(self, verify: bool):
        """
        Set whether to verify the authentication server's TLS certificate.

        This method should be implemented by subclasses to set the host URL
        where tokens can be exchanged with the server.

        :param verify: Whether to verify the server's TLS certificate.
        """
        pass

    @abstractmethod
    def get_token(self):
        """
        Exchange and retrieve a token from the server.

        This method should be implemented by subclasses to exchange credentials
        with the token server and retrieve a token.

        :return: The retrieved token.
        """
        pass

    @abstractmethod
    def revoke_token(self):
        """
        Revoke the currently held token.

        This method should be implemented by subclasses to revoke the currently
        held token from the token server, if supported by the security strategy.
        """
        pass


class AccessToken(SecurityStrategy):
    """
    Security strategy for handling Bearer token authentication.

    This class is a concrete implementation of SecurityStrategy, specifically
    designed to handle authentication using a Bearer token. It applies the Bearer
    token to the Authorization header of the request.

    Methods:
     - `apply(request)`: Apply security measures to the given request.
     - `clean()`: Clean sensitive information from the security strategy.

    :param token: The Bearer token used for authentication.
    :type token: str
    """

    def __init__(self, token: str):
        """
        Initialize a AccessToken instance with the provided Bearer token.

        :param token: The Bearer token used for authentication.
        """
        self._token = token

    def apply(self, request: Request):
        """
        Apply security measures by adding the Bearer token to the request header.

        :param request: The request object to which security measures will be applied.
        """
        if self._token:
            request.headers['Authorization'] = f'Bearer {self._token}'

    def clean(self):
        """
        Clean sensitive information from the security strategy.

        This method clears the stored Bearer token, ensuring sensitive
        information is removed from memory.
        """
        self._token = ''


class OAuth2ClientCredentials(SecurityStrategyWithTokenExchange):
    """
    Security strategy for handling OAuth2 client credentials authentication.

    This class is a concrete implementation of SecurityStrategyWithTokenExchange,
    specifically designed to handle authentication using OAuth2 client credentials.
    It exchanges client credentials for an access token and applies it to the
    Authorization header of the request.

    Methods:
     - `apply_security(request)`: Apply security measures to the given request.
     - `clean()`: Clean sensitive information from the security strategy.
     - `set_token_url_host(token_url_host)`: Set the host URL for token exchange.
     - `set_verify_tls_certificate(verify)`: Set whether to verify the authentication server's TLS certificate.
     - `get_token()`: Exchange and retrieve an access token from the token server.
     - `revoke_token()`: Revoke the currently held access token, if supported.

    :param client_id: The client ID for OAuth2 client credentials authentication.
    :type client_id: str
    :param client_secret: The client secret for OAuth2 client credentials authentication.
    :type client_secret: str
    :param scopes: The list of scopes to be requested during token exchange.
    :type scopes: List[str]
    :param token_url: The URL for token exchange.
    :type token_url: str
    :param revoke_token_url: The URL for revoking access tokens (optional).
    :type revoke_token_url: str
    :param refresh_threshold: The number of seconds before token expiration to trigger token refresh.
    :type refresh_threshold: int
    """

    def __init__(self, client_id: str, client_secret: str,
                 scopes: List[str],
                 token_url: str = 'https://api.swx.altairone.com/oauth2/token',
                 revoke_token_url: str = '',
                 refresh_threshold: int = 10,
                 verify: bool = True):
        """
        Initialize OAuth2ClientCredentials with the provided parameters.

        :param client_id: The client ID for OAuth2 client credentials authentication.
        :param client_secret: The client secret for OAuth2 client credentials authentication.
        :param scopes: The list of scopes to be requested during token exchange.
        :param token_url: The URL for token exchange.
        :param revoke_token_url: The URL for revoking access tokens (optional).
        :param refresh_threshold: The number of seconds before token expiration to trigger token refresh.
        :param verify: Whether to verify the server's TLS certificate.
        """
        super().__init__()
        self._token = ''
        self.client_id = client_id
        self._client_secret = client_secret
        self.token_url_host = ''
        self.token_url = token_url
        self.revoke_token_url = revoke_token_url
        self.scopes = scopes
        self.expires_in = 0
        self.expires_at = 0
        self.refresh_threshold = refresh_threshold
        self.verify = verify

    def set_token_url_host(self, token_url_host: str):
        """
        Set the host URL for token exchange.

        :param token_url_host: The host URL for token exchange.
        """
        self.token_url_host = token_url_host.rstrip('/')

    def set_verify_tls_certificate(self, verify: bool):
        """
        Set whether to verify the authentication server's TLS certificate.

        :param verify: Whether to verify the server's TLS certificate.
        """
        self.verify = verify

    def get_token(self):
        """
        Exchange and retrieve an access token from the token server.

        This method exchanges client credentials for an access token with
        the token server and stores the token for subsequent use.
        """
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self._client_secret
        }
        if self.scopes:
            data['scope'] = ' '.join(self.scopes)

        token_url = self.token_url
        if token_url.startswith('/'):
            token_url = self.token_url_host.rstrip('/') + token_url

        response = requests.request('POST', token_url, data=data,
                                    verify=self.verify)
        response_json = response.json()
        if 'access_token' in response_json:
            self._token = response_json['access_token']
            self.expires_in = response_json.get('expires_in', 3600)
            self.expires_at = time.time() + self.expires_in
        else:
            raise ResponseError(response, f"Failed to refresh token: {response.content.decode('utf-8')}")

    def revoke_token(self):
        """
        Revoke the currently held access token, if supported.

        This method revokes the currently held access token from the token server,
        if a token revocation URL is provided and the token is still valid.
        """
        if self._token and self.revoke_token_url:
            data = {
                'token': self._token,
                'client_id': self.client_id,
                'client_secret': self._client_secret
            }

            revoke_token_url = self.revoke_token_url
            if revoke_token_url.startswith('/'):
                revoke_token_url = self.token_url_host.rstrip('/') + revoke_token_url

            response = requests.request('POST', revoke_token_url,
                                        data=data, verify=self.verify)
            if response.status_code == 200:
                self._token = ''
                self.expires_in = 0
                self.expires_at = 0
            else:
                raise ResponseError(response, f"Failed to revoke token: {response.content.decode('utf-8')}")
        else:
            self._token = ''

    def apply(self, request: Request):
        """
        Apply security measures by adding the OAuth2 access token to the request header.

        If the access token is not present or close to expiration, it is refreshed before applying.

        :param request: The request object to which security measures will be applied.
        """
        if not self._token or time.time() + self.refresh_threshold >= self.expires_at:
            self.get_token()
        request.headers['Authorization'] = f'Bearer {self._token}'

    def clean(self):
        """
        Clean sensitive information from the security strategy.

        This method revokes the currently held access token, if supported,
        ensuring sensitive information is removed from memory.
        """
        self.revoke_token()
