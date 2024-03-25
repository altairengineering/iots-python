import time
from unittest import mock

import pytest
from requests import Request

from iots.models.exceptions import ResponseError
from .common import make_response

from iots.security import AccessToken, OAuth2ClientCredentials
from iots.models.exceptions import ResponseError

request_mock_pkg = 'iots.security.requests.request'


def test_bearer_security():
    """
    Tests the AccessToken security strategy.
    """
    bearer_strategy = AccessToken("valid-token")
    assert bearer_strategy._token == "valid-token"

    req = Request()
    bearer_strategy.apply(req)
    assert req.headers["Authorization"] == "Bearer valid-token"

    bearer_strategy.clean()
    assert bearer_strategy._token == ''


def test_oauth2_security():
    """
    Tests the OAuth2ClientCredentials security strategy.
    """
    expected_token = {
        'access_token': "valid-token",
        'expires_in': 2,
        'scope': "foo bar",
        'token_type': "bearer",
    }
    expected_token_resp = make_response(200, expected_token)

    client_id = "test-client-id"
    client_secret = "test-client-secret"
    scopes = ["foo", "bar"]

    oauth2_strategy = OAuth2ClientCredentials(
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes,
        token_url='/auth/token',
        revoke_token_url='/auth/revoke',
        refresh_threshold=1)
    assert oauth2_strategy._token == ''

    oauth2_strategy.set_token_url_host('https://test-api.com')

    # Apply token
    with mock.patch(request_mock_pkg, return_value=expected_token_resp) as m:
        req = Request()
        oauth2_strategy.apply(req)
        assert oauth2_strategy._token == "valid-token"
        assert req.headers["Authorization"] == "Bearer valid-token"

    m.assert_called_once_with('POST',
                              'https://test-api.com/auth/token',
                              data={
                                  'grant_type': 'client_credentials',
                                  'client_id': 'test-client-id',
                                  'client_secret': 'test-client-secret',
                                  'scope': 'foo bar',
                              })

    # Revoke token
    with mock.patch(request_mock_pkg, return_value=make_response(200)) as m:
        oauth2_strategy.clean()
        assert oauth2_strategy._token == ''

    m.assert_called_once_with('POST',
                              'https://test-api.com/auth/revoke',
                              data={
                                  'token': 'valid-token',
                                  'client_id': 'test-client-id',
                                  'client_secret': 'test-client-secret',
                              })

    # Get token
    with mock.patch(request_mock_pkg, return_value=expected_token_resp) as m:
        oauth2_strategy.get_token()
        assert oauth2_strategy._token == "valid-token"

    m.assert_called_once_with('POST',
                              'https://test-api.com/auth/token',
                              data={
                                  'grant_type': 'client_credentials',
                                  'client_id': 'test-client-id',
                                  'client_secret': 'test-client-secret',
                                  'scope': 'foo bar',
                              })

    # Reuse token before it expires
    req = Request()
    oauth2_strategy.apply(req)
    assert oauth2_strategy._token == "valid-token"
    assert req.headers["Authorization"] == "Bearer valid-token"

    # Wait until token has expired (or is closed to expire, based on the threshold)
    time.sleep(1)
    with mock.patch(request_mock_pkg, return_value=expected_token_resp) as m:
        req = Request()
        oauth2_strategy.apply(req)
        assert oauth2_strategy._token == "valid-token"
        assert req.headers["Authorization"] == "Bearer valid-token"

    m.assert_called_once_with('POST',
                              'https://test-api.com/auth/token',
                              data={
                                  'grant_type': 'client_credentials',
                                  'client_id': 'test-client-id',
                                  'client_secret': 'test-client-secret',
                                  'scope': 'foo bar',
                              })


def test_oauth2_security_get_token_error():
    """
    Tests getting a token with invalid credentials using the
    OAuth2ClientCredentials security strategy.
    """
    expected_error_payload = {
        "error": "invalid_client",
        "error_description": "Client authentication failed"
    }
    expected_token_resp = make_response(401, expected_error_payload)

    client_id = "test-client-id"
    client_secret = "test-client-secret"
    scopes = ["foo", "bar"]

    oauth2_strategy = OAuth2ClientCredentials(
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes,
        token_url='https://test-api.com/auth/token')

    # Apply token
    with mock.patch(request_mock_pkg, return_value=expected_token_resp):
        with pytest.raises(ResponseError) as e:
            req = Request()
            oauth2_strategy.apply(req)
            assert oauth2_strategy._token == ''
            assert req.headers["Authorization"] == "Bearer valid-token"

    assert "Failed to refresh token: {" in str(e.value)
    assert e.value.http_response().status_code == 401
    assert e.value.http_response().json() == expected_error_payload


def test_oauth2_security_revoke_token_error():
    """
    Tests getting a token with invalid credentials using the
    OAuth2ClientCredentials security strategy.
    """
    expected_error_payload = {
        "error": "some_error",
        "error_description": "Cannot revoke token"
    }
    expected_token_resp = make_response(400, expected_error_payload)

    client_id = "test-client-id"
    client_secret = "test-client-secret"
    scopes = ["foo", "bar"]

    oauth2_strategy = OAuth2ClientCredentials(
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes,
        revoke_token_url='')
    oauth2_strategy._token = 'valid-token'

    # No-op since revoke_token_url was not set
    oauth2_strategy.revoke_token()
    oauth2_strategy._token = ''

    # Apply token
    oauth2_strategy._token = 'valid-token'
    oauth2_strategy.revoke_token_url = 'https://test-api.com/auth/revoke'
    with mock.patch(request_mock_pkg, return_value=expected_token_resp):
        with pytest.raises(ResponseError) as e:
            oauth2_strategy.revoke_token()
            assert oauth2_strategy._token == 'valid-token'

    assert "Failed to revoke token: {" in str(e.value)
    assert e.value.http_response().status_code == 400
    assert e.value.http_response().json() == expected_error_payload
