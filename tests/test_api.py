import os
from unittest import mock

import pytest

from swx.api import API
from swx.errors import APIException, ExcMissingToken, ResponseError
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
                token("valid-token").
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
