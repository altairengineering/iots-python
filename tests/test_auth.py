from unittest import mock, TestCase

import pytest
from requests.exceptions import MissingSchema

from auth.token import Token, get_token, revoke_token, DEFAULT_TIMEOUT
from errors import OAuth2Error, TokenRevokeError
from tests.common import make_json_response


class TestToken(TestCase):
    def test_get_and_revoke_token_successfully(self):
        """ Tests a successful token request and revoking. """
        expected_resp_payload = {
            "host": "https://api.swx.mock",
            "access_token": "valid-token",
            "expires_in": 604799,
            "scope": "app function",
            "token_type": "bearer"
        }

        expected_resp = make_json_response(200, expected_resp_payload)

        with mock.patch("auth.token.requests.post", return_value=expected_resp) as m:
            actual_token = get_token("https://api.swx.mock", "client-id", "client-secret",
                                     ["app", "function"])

        expected_req_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        expected_req_payload = 'grant_type=client_credentials&' \
                               'client_id=client-id&' \
                               'client_secret=client-secret&' \
                               'scope=app function'

        m.assert_called_once_with("https://api.swx.mock/oauth2/token",
                                  headers=expected_req_headers,
                                  data=expected_req_payload,
                                  timeout=DEFAULT_TIMEOUT)
        assert actual_token.access_token == expected_resp_payload["access_token"]
        assert actual_token.expires_in == expected_resp_payload["expires_in"]
        assert actual_token.scope == expected_resp_payload["scope"]
        assert actual_token.token_type == expected_resp_payload["token_type"]

        # Tests Token.revoke()
        expected_resp = make_json_response(204)

        with mock.patch("auth.token.requests.post", return_value=expected_resp) as m:
            actual_token.revoke()

        expected_req_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        expected_req_payload = 'token=valid-token&' \
                               'client_id=client-id&' \
                               'client_secret=client-secret'

        m.assert_called_once_with("https://api.swx.mock/oauth2/revoke",
                                  headers=expected_req_headers,
                                  data=expected_req_payload,
                                  timeout=DEFAULT_TIMEOUT)

    def test_get_token_invalid_request_data(self):
        """ Tests a failing token request due to invalid request data. """
        expected_resp_payload = {
            "error": {
                "details": {
                    "error_description": "Client authentication failed",
                },
                "message": "invalid_client",
                "status": 401
            }
        }

        expected_resp = make_json_response(401, expected_resp_payload)

        with mock.patch("auth.token.requests.post", return_value=expected_resp) as m:
            with pytest.raises(OAuth2Error) as e:
                get_token("https://api.swx.mock", "client-id", "invalid-client-secret",
                          ["app", "function"])

        expected_req_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        expected_req_payload = 'grant_type=client_credentials&' \
                               'client_id=client-id&' \
                               'client_secret=invalid-client-secret&' \
                               'scope=app function'

        m.assert_called_once_with("https://api.swx.mock/oauth2/token",
                                  headers=expected_req_headers,
                                  data=expected_req_payload,
                                  timeout=DEFAULT_TIMEOUT)

        assert e.value.status_code == 401
        assert e.value.json() == expected_resp_payload

    def test_get_token_network_error(self):
        """ Tests a failing token request due to an invalid url. """
        with pytest.raises(MissingSchema):
            get_token("", "client-id", "client-secret", ["app", "function"])

    def test_revoke_token_successfully(self):
        """ Tests a successful revoke token request. """
        expected_resp = make_json_response(204)

        with mock.patch("auth.token.requests.post", return_value=expected_resp) as m:
            revoke_token("https://api.swx.mock", "some-access-token", "client-id", "client-secret")

        expected_req_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        expected_req_payload = 'token=some-access-token&' \
                               'client_id=client-id&' \
                               'client_secret=client-secret'

        m.assert_called_once_with("https://api.swx.mock/oauth2/revoke",
                                  headers=expected_req_headers,
                                  data=expected_req_payload,
                                  timeout=DEFAULT_TIMEOUT)

    def test_revoke_token_without_secret_successfully(self):
        """
        Tests a successful revoke token request without client secret
        (authorization code).
        """
        expected_resp = make_json_response(200)

        with mock.patch("auth.token.requests.post", return_value=expected_resp) as m:
            revoke_token("https://api.swx.mock", "some-access-token", "client-id")

        expected_req_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        expected_req_payload = 'token=some-access-token&' \
                               'client_id=client-id'

        m.assert_called_once_with("https://api.swx.mock/oauth2/revoke",
                                  headers=expected_req_headers,
                                  data=expected_req_payload,
                                  timeout=DEFAULT_TIMEOUT)

    def test_revoke_token_invalid_request_data(self):
        """
        Tests a failing revoke token request due to invalid request data.
        """
        expected_resp_payload = {
            "error": {
                "details": {
                    "error_description": "Client authentication failed (e.g., unknown "
                                         "client, no client authentication included, "
                                         "or unsupported authentication method)"
                },
                "message": "invalid_client",
                "status": 401
            }
        }

        expected_resp = make_json_response(401, expected_resp_payload)

        with mock.patch("auth.token.requests.post", return_value=expected_resp) as m:
            with pytest.raises(OAuth2Error) as e:
                revoke_token("https://api.swx.mock", "some-access-token", "client-id", "invalid-client-secret")

        expected_req_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        expected_req_payload = 'token=some-access-token&' \
                               'client_id=client-id&' \
                               'client_secret=invalid-client-secret'

        m.assert_called_once_with("https://api.swx.mock/oauth2/revoke",
                                  headers=expected_req_headers,
                                  data=expected_req_payload,
                                  timeout=DEFAULT_TIMEOUT)

        assert e.value.status_code == 401
        assert e.value.json() == expected_resp_payload

    def test_token_revoke_not_defined(self):
        """
        Tests calling the Token.revoke() method with a Token that has not
        been properly obtained.
        """
        with pytest.raises(TokenRevokeError):
            Token().revoke()

    @mock.patch("auth.token.requests.post")
    def test_get_token_successfully_with_context_manager(self, m: mock.Mock):
        """
        Tests a successful token request and revoke using a Context Manager.
        """
        expected_resp_payload = {
            "host": "https://api.swx.mock",
            "access_token": "valid-token",
            "expires_in": 604799,
            "scope": "app function",
            "token_type": "bearer"
        }

        expected_resp_token = make_json_response(200, expected_resp_payload)
        expected_resp_revoke = make_json_response(204)

        m.side_effect = [expected_resp_token, expected_resp_revoke]

        with get_token("https://api.swx.mock", "client-id", "client-secret", ["app", "function"]) as actual_token:
            assert actual_token.host == expected_resp_payload["host"]
            assert actual_token.access_token == expected_resp_payload["access_token"]
            assert actual_token.expires_in == expected_resp_payload["expires_in"]
            assert actual_token.scope == expected_resp_payload["scope"]
            assert actual_token.token_type == expected_resp_payload["token_type"]

        expected_req_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        expected_req_payload = 'grant_type=client_credentials&' \
                               'client_id=client-id&' \
                               'client_secret=client-secret&' \
                               'scope=app function'

        m.assert_has_calls([
            mock.call("https://api.swx.mock/oauth2/token",
                      headers=expected_req_headers,
                      data=expected_req_payload,
                      timeout=DEFAULT_TIMEOUT),
            mock.call("https://api.swx.mock/oauth2/revoke",
                      data='token=valid-token&'
                           'client_id=client-id&'
                           'client_secret=client-secret',
                      headers={'Content-Type': 'application/x-www-form-urlencoded'},
                      timeout=3),
        ])
