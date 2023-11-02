from dataclasses import dataclass
from typing import Callable, Union
from urllib.parse import urljoin

import requests

from ..consts import DEFAULT_SWX_API_HOST
from ..errors import OAuth2Error, TokenRevokeError

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

    def __str__(self):
        return self.access_token


def get_token(client_id: str, client_secret: str, scopes: list, host: str = "") -> Token:
    """
    Requests an OAuth 2.0 Bearer Token from SmartWorks using the
    client_credentials grant.
    If the request fails, an OAuth2Error will be raised.

    :param client_id:       Client ID.
    :param client_secret:   Client Secret.
    :param scopes:          List of scopes to request.
    :param host:            API Host URL. Defaults to https://api.swx.altairone.com.
    :return:                :class:`Token` instance.
    """
    payload = f'grant_type=client_credentials&' \
              f'client_id={client_id}&' \
              f'client_secret={client_secret}&' \
              f'scope={" ".join(scopes)}'

    if host == '':
        host = DEFAULT_SWX_API_HOST

    url = urljoin(host, API_TOKEN_ENDPOINT)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=payload, headers=headers, timeout=DEFAULT_TIMEOUT)

    if response.status_code >= 400:
        raise OAuth2Error.parse(response.json())

    token = Token(**response.json())
    token._revoke = lambda: revoke_token(token.access_token,
                                         client_id, client_secret, token.host)
    token.host = host

    return token


def revoke_token(access_token: Union[str, Token], client_id: str,
                 client_secret: str = "", host: str = ""):
    """
    Revokes the given SmartWork's OAuth2 Bearer Token.
    If the request fails, an OAuth2Error will be raised.

    :param access_token:  Access Token to revoke.
    :param client_id:     Client ID of the client that requested the token.
    :param client_secret: Client Secret of the client that requested the token.
    :param host:          API Host URL. If access_token is a :class:`Token`,
                          it defaults to the token hostm otherwise it defaults
                          to https://api.swx.altairone.com.
    """
    payload = f'token={access_token}&' \
              f'client_id={client_id}'

    if client_secret:
        payload += f'&client_secret={client_secret}'

    url = urljoin(host or DEFAULT_SWX_API_HOST, API_REVOKE_ENDPOINT)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, headers=headers, data=payload,
                             timeout=DEFAULT_TIMEOUT)

    if response.status_code >= 400:
        raise OAuth2Error.parse(response.json())
