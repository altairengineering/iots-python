from dataclasses import dataclass
from typing import Callable
from urllib.parse import urljoin

import requests

from .errors import OAuth2Error, TokenRevokeError

API_TOKEN_ENDPOINT = "/oauth2/token"
API_REVOKE_ENDPOINT = "/oauth2/revoke"

DEFAULT_TIMEOUT = 3


@dataclass
class Token:
    """ This class represents a SmartWorks token. """
    host: str = ''
    access_token: str = ''
    expires_in: int = 0
    id_token: str = ''
    refresh_token: str = ''
    scope: str = ''
    token_type: str = ''
    _revoke: Callable = None

    def revoke(self):
        """ Revokes this token. """
        if self._revoke is None:
            raise TokenRevokeError()
        self._revoke()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.revoke()


def get_token(host: str, client_id: str, client_secret: str, scopes: list) -> Token:
    """
    Requests an OAuth 2.0 Bearer Token from SmartWorks using the
    client_credentials grant.
    If the request fails, an OAuth2Error will be raised.

    :param host:            Host URL.
    :param client_id:       Client ID.
    :param client_secret:   Client Secret.
    :param scopes:          List of scopes to request.
    :return:                Token instance.
    """
    payload = f'grant_type=client_credentials&' \
              f'client_id={client_id}&' \
              f'client_secret={client_secret}&' \
              f'scope={" ".join(scopes)}'

    url = urljoin(host, API_TOKEN_ENDPOINT)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=payload, headers=headers, timeout=DEFAULT_TIMEOUT)

    if response.status_code >= 400:
        raise OAuth2Error.parse(response.json())

    token = Token(**response.json())
    token._revoke = lambda: revoke_token(token.host, token.access_token, client_id, client_secret)
    token.host = host

    return token


def revoke_token(host: str, access_token: str, client_id: str, client_secret: str = ""):
    """
    Revokes the given SmartWork's OAuth2 Bearer Token.
    If the request fails, an OAuth2Error will be raised.

    :param host:          Host URL
    :param access_token:  Access Token to revoke.
    :param client_id:     Client ID of the client that requested the token.
    :param client_secret: Client Secret of the client that requested the token.
    """
    payload = f'token={access_token}&' \
              f'client_id={client_id}'

    if client_secret:
        payload += f'&client_secret={client_secret}'

    url = urljoin(host, API_REVOKE_ENDPOINT)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, headers=headers, data=payload,
                             timeout=DEFAULT_TIMEOUT)

    if response.status_code >= 400:
        raise OAuth2Error.parse(response.json())
