import os
from unittest import mock

import pytest

from swx.api import API
from swx.errors import APIException, ExcMissingToken, ResponseError
from swx.token import Token
from tests.common import make_json_response


def test_create_successfully():
    """ Creates an API instance successfully. """
    api = API(host="test-api.swx.altairone.com")
    assert api.host == "https://test-api.swx.altairone.com"


def test_default_host():
    """
    Creates an API instance taking the host from the default environment
    variable.
    """
    os.environ["SWX_API_URL"] = "https://test-api.swx.altairone.com"
    api = API()
    assert api.host == "https://test-api.swx.altairone.com"


def test_missing_host():
    """
    Creates an API instance taking the host from the default environment
    variable, but the variable is not set.
    """
    os.environ.pop("SWX_API_URL")
    with pytest.raises(ValueError):
        API()


def test_set_token():
    """
    Sets a token in an API instance.
    """
    api = API(host="api.swx.mock").set_token("valid-token")
    assert api._token == "valid-token"


def test_get_token():
    """
    Creates an API instance that handles authentication using OAuth2 credentials
    and revokes the token.
    """
    expected_token = Token(
        host="https://api.swx.mock",
        access_token="valid-token",
        expires_in=604799,
        scope="app function",
        token_type="bearer"
    )

    client_id = "test-client-id"
    client_secret = "test-client-secret"
    scopes = ["app", "function"]

    with mock.patch("swx.api.get_token", return_value=expected_token) as mock_get_token:
        api = API(host="api.swx.mock").get_token(
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes)

    assert api._token == expected_token.access_token

    with mock.patch("swx.api.revoke_token", return_value=None) as mock_revoke_token:
        api.revoke_token()

    assert api._token is None

    mock_get_token.assert_called_once_with("https://api.swx.mock", client_id, client_secret, scopes)
    mock_revoke_token.assert_called_once_with("https://api.swx.mock", "valid-token", client_id, client_secret)


def test_get_token_with():
    """
    Creates an API instance that handles authentication using OAuth2 credentials
    and revokes the token automatically using a context manager (with).
    """
    expected_token = Token(
        host="https://api.swx.mock",
        access_token="valid-token",
        expires_in=604799,
        scope="app function",
        token_type="bearer"
    )

    client_id = "test-client-id"
    client_secret = "test-client-secret"
    scopes = ["app", "function"]

    with mock.patch("swx.api.get_token", return_value=expected_token) as mock_get_token:
        with mock.patch("swx.api.revoke_token", return_value=None) as mock_revoke_token:
            with API(host="api.swx.mock").get_token(client_id=client_id,
                                                    client_secret=client_secret,
                                                    scopes=scopes) as api:
                assert api._token == expected_token.access_token

    assert api._token is None

    mock_get_token.assert_called_once_with("https://api.swx.mock", client_id, client_secret, scopes)
    mock_revoke_token.assert_called_once_with("https://api.swx.mock", "valid-token", client_id, client_secret)


def test_make_request():
    """
    Makes an authenticated request to the API successfully.
    """
    req_payload = {"foo": "bar"}
    expected_resp_payload = {
        "key1": 123,
        "key2": "hey!"
    }

    expected_resp = make_json_response(200, expected_resp_payload)

    with mock.patch("requests.request", return_value=expected_resp) as m:
        resp = (API(host="test-api.swx.altairone.com").
                set_token("valid-token").
                make_request("POST", "/info", body=req_payload))

    m.assert_called_once_with("POST",
                              "https://test-api.swx.altairone.com/info",
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json'
                              },
                              data=req_payload,
                              timeout=3)

    assert resp.status_code == 200
    assert resp.json() == expected_resp_payload


def test_make_request_unauthenticated():
    """
    Makes an unauthenticated request to the API.
    """
    expected_resp_payload = {
        "error": {
            "message": "missing token",
            "status": 401
        }
    }

    expected_resp = make_json_response(401, expected_resp_payload)

    with mock.patch("swx.api.requests.request", return_value=expected_resp) as m:
        with pytest.raises(ResponseError) as e:
            API(host="test-api.swx.altairone.com").make_request("GET", "/info", auth=False)

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/info",
                              headers={},
                              data=None,
                              timeout=3)

    assert e.value.status_code == 401
    assert e.value.json() == expected_resp_payload


def test_make_request_missing_token():
    """
    Makes an authenticated request to the API, but the token is not set.
    """
    with pytest.raises(APIException) as e:
        API(host="test-api.swx.altairone.com").make_request("POST", "/info")

    assert e.value == ExcMissingToken
