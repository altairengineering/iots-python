import json
from unittest import mock
from unittest.mock import call

import pytest

from iots.api import API
from iots.models.exceptions import APIException
from .common import make_response

request_mock_pkg = 'iots.api.requests.request'


def test_create_successfully():
    """ Creates an API instance successfully. """
    api = API(host="test-api.swx.altairone.com")
    assert api.host == "https://test-api.swx.altairone.com"


def test_missing_host():
    """ Creates an API instance that will use the default host. """
    api = API()
    assert api.host == "https://api.swx.altairone.com"


def test_set_token():
    """ Sets a token in an API instance. """
    api = API(host="api.swx.mock").set_token("valid-token")
    assert api._security_strategy._token == "valid-token"


def test_set_credentials():
    """
    Creates an API instance that handles authentication using OAuth2 credentials
    and revokes the token.
    """
    expected_token = {
        'access_token': "valid-token",
        'expires_in': 604799,
        'scope': "app function",
        'token_type': "bearer",
    }
    expected_token_resp = make_response(200, expected_token)

    client_id = "test-client-id"
    client_secret = "test-client-secret"
    scopes = ["app", "function"]

    with mock.patch(request_mock_pkg, return_value=expected_token_resp) as mock_get_token:
        api = API(host="api.swx.mock").set_credentials(
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
            token_url='/auth/token')

    assert api._security_strategy._token == expected_token['access_token']

    with mock.patch(request_mock_pkg, return_value=make_response(200)) as mock_revoke_token:
        api.revoke_token()

    assert api._security_strategy._token == ''

    mock_get_token.assert_called_once_with('POST',
                                           'https://api.swx.mock/auth/token',
                                           data={
                                               'grant_type': 'client_credentials',
                                               'client_id': 'test-client-id',
                                               'client_secret': 'test-client-secret',
                                               'scope': 'app function',
                                           })

    mock_revoke_token.assert_called_once_with('POST',
                                              'https://api.swx.mock/oauth2/revoke',
                                              data={
                                                  'token': 'valid-token',
                                                  'client_id': 'test-client-id',
                                                  'client_secret': 'test-client-secret',
                                              })


def test_get_token_with():
    """
    Creates an API instance that handles authentication using OAuth2 credentials
    and revokes the token automatically using a context manager (with).
    """
    expected_token = {
        'access_token': "valid-token",
        'expires_in': 604799,
        'scope': "app function",
        'token_type': "bearer",
    }
    expected_token_resp = make_response(200, expected_token)

    client_id = "test-client-id"
    client_secret = "test-client-secret"
    scopes = ["app", "function"]

    with mock.patch(request_mock_pkg, side_effect=[expected_token_resp, make_response(200)]) as m:
        with API().set_credentials(client_id=client_id,
                                   client_secret=client_secret,
                                   scopes=scopes,
                                   token_url='/auth/token',
                                   revoke_token_url='/auth/revoke') as api:
            assert api._security_strategy._token == expected_token['access_token']

            m.assert_called_with('POST',
                                 'https://api.swx.altairone.com/auth/token',
                                 data={
                                     'grant_type': 'client_credentials',
                                     'client_id': 'test-client-id',
                                     'client_secret': 'test-client-secret',
                                     'scope': 'app function',
                                 })

    assert api._security_strategy._token == ''

    m.assert_called_with('POST',
                         'https://api.swx.altairone.com/auth/revoke',
                         data={
                             'token': 'valid-token',
                             'client_id': 'test-client-id',
                             'client_secret': 'test-client-secret',
                         })

    assert m.call_count == 2


def test_make_request():
    """ Makes an authenticated request to the API successfully. """
    req_payload = {"foo": "bar"}
    expected_resp_payload = {
        "key1": 123,
        "key2": "hey!"
    }

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        resp = (API(host="test-api.swx.altairone.com").
                set_token("valid-token").
                make_request("POST", "/info", body=req_payload))

    m.assert_called_once_with("POST",
                              "https://test-api.swx.altairone.com/info",
                              params={},
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': 'Bearer valid-token',
                              },
                              data=json.dumps(req_payload),
                              timeout=3)

    assert resp.status_code == 200
    assert resp.json() == expected_resp_payload


def test_make_request_get_token():
    """
    Makes an authenticated request to the API successfully using OAuth2
    Client Credentials.
    """
    expected_token = {
        'access_token': "valid-token",
        'expires_in': 604799,
        'scope': "app function",
        'token_type': "bearer",
    }
    expected_token_resp = make_response(200, expected_token)

    client_id = "test-client-id"
    client_secret = "test-client-secret"
    scopes = ["app", "function"]

    req_payload = {"foo": "bar"}
    expected_resp_payload = {
        "key1": 123,
        "key2": "hey!"
    }

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, side_effect=[expected_token_resp, expected_resp]) as m:
        resp = (API(host="test-api.swx.altairone.com").
                set_credentials(client_id=client_id,
                                client_secret=client_secret,
                                scopes=scopes).
                make_request("POST", "/info", body=req_payload))

    m.assert_has_calls([
        call('POST',
             'https://test-api.swx.altairone.com/oauth2/token',
             data={
                 'grant_type': 'client_credentials',
                 'client_id': 'test-client-id',
                 'client_secret': 'test-client-secret',
                 'scope': 'app function',
             }),
        call("POST",
             "https://test-api.swx.altairone.com/info",
             params={},
             headers={
                 'Content-Type': 'application/json',
                 'Authorization': 'Bearer valid-token',
             },
             data=json.dumps(req_payload),
             timeout=3),
    ])

    assert resp.status_code == 200
    assert resp.json() == expected_resp_payload


def test_make_request_unauthenticated():
    """ Makes a request to the API with invalid authentication. """
    expected_resp_payload = {
        "error": {
            "message": "missing token",
            "status": 401
        }
    }

    expected_resp = make_response(401, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        resp = (API(host="test-api.swx.altairone.com").
                set_token("invalid-token").
                make_request("GET", "/info", auth=True))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/info",
                              params={},
                              headers={'Authorization': 'Bearer invalid-token'},
                              data=[],
                              timeout=3)

    assert resp.status_code == 401
    assert resp.json() == expected_resp_payload


def test_make_request_missing_token():
    """ Makes an authenticated request to the API, but the token is not set. """
    with pytest.raises(APIException) as e:
        API(host="test-api.swx.altairone.com").make_request("POST", "/info")

    assert str(e.value) == "No security strategy has been set"
