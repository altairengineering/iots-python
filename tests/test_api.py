import os
from unittest import TestCase, mock

import pytest

from api.api import API
from api.errors import APIException, ExcMissingToken
from errors import ResponseError
from tests.common import make_json_response


class TestAPI(TestCase):
    def test_create_successfully(self):
        """ Creates an API instance successfully. """
        api = API(host="test-api.swx.altairone.com")
        assert api.host == "https://test-api.swx.altairone.com"

    def test_default_host(self):
        """
        Creates an API instance taking the host from the default environment
        variable.
        """
        os.environ["SWX_API_URL"] = "https://test-api.swx.altairone.com"
        api = API()
        assert api.host == "https://test-api.swx.altairone.com"

    def test_missing_host(self):
        """
        Creates an API instance taking the host from the default environment
        variable, but the variable is not set.
        """
        os.environ.pop("SWX_API_URL")
        with pytest.raises(ValueError):
            API()

    def test_make_request(self):
        """
        Makes an authenticated request to the API successfully.
        """
        req_payload = {"foo": "bar"}
        expected_resp_payload = {
            "key1": 123,
            "key2": "hey!"
        }

        expected_resp = make_json_response(200, expected_resp_payload)

        with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
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

    def test_make_request_unauthenticated(self):
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

        with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
            with pytest.raises(ResponseError) as e:
                API(host="test-api.swx.altairone.com").make_request("GET", "/info", auth=False)

        m.assert_called_once_with("GET",
                                  "https://test-api.swx.altairone.com/info",
                                  headers={},
                                  data=None,
                                  timeout=3)

        assert e.value.status_code == 401
        assert e.value.json() == expected_resp_payload

    def test_make_request_missing_token(self):
        """
        Makes an authenticated request to the API, but the token is not set.
        """
        with pytest.raises(APIException) as e:
            API(host="test-api.swx.altairone.com").make_request("POST", "/info")

        assert e.value == ExcMissingToken


class TestAPIObject(TestCase):
    def test_build_url(self):
        """
        Builds the full URL of a chained call successfully.
        """
        api = API(host="test-api.swx.altairone.com")
        prop = api.spaces("space01").categories("cat01").things("thing01").properties("temperature")

        assert prop.build_url() == "https://test-api.swx.altairone.com" \
                                   "/spaces/space01/categories/cat01/things/thing01/properties/temperature"

    def test_build_path(self):
        """
        Builds the URL path of a chained call successfully.
        """
        api = API(host="test-api.swx.altairone.com")

        cat = api.spaces("space01").categories("cat01")
        thing1 = cat.things("thing01")
        thing2 = cat.things("thing02")
        prop_thing1 = thing1.properties("temperature")
        prop_thing2 = thing2.properties("humidity")

        assert cat.build_path() == "/spaces/space01/categories/cat01"
        assert thing1.build_path() == "/spaces/space01/categories/cat01/things/thing01"
        assert thing2.build_path() == "/spaces/space01/categories/cat01/things/thing02"
        assert prop_thing1.build_path() == "/spaces/space01/categories/cat01/things/thing01/properties/temperature"
        assert prop_thing2.build_path() == "/spaces/space01/categories/cat01/things/thing02/properties/humidity"
        assert api.spaces("space01").things("thing01").build_path() == "/spaces/space01/things/thing01"
        assert api.spaces("space01").categories().build_path() == "/spaces/space01/categories"
        assert api.spaces("space01").things().build_path() == "/spaces/space01/things"
        assert api.spaces().build_path() == "/spaces"
        assert thing1.properties().build_path() == "/spaces/space01/categories/cat01/things/thing01/properties"
