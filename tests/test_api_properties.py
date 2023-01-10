import json
from unittest import TestCase, mock

from requests import Response

from api.api import API
from models.property import PropertiesResp


class TestAPIProperties(TestCase):
    def test_get(self):
        """
        Tests a successful request to get a property value.
        """
        expected_status_code = 200
        expected_resp_payload = {
            "temperature": 21.7
        }

        resp = Response()
        resp.status_code = expected_status_code
        resp._content = json.dumps(expected_resp_payload).encode('utf-8')

        with mock.patch("api.api.requests.request", return_value=resp) as m:
            prop = (API(host="test-api.swx.altairone.com").
                    things("thing01").
                    properties("temperature").
                    get())

        m.assert_called_once_with("GET",
                                  "https://test-api.swx.altairone.com/things/thing01/properties/temperature",
                                  headers={'Authorization': 'Bearer valid-token'},
                                  data=None,
                                  timeout=3)

        assert prop == expected_resp_payload
        assert type(prop) == PropertiesResp

    def test_list(self):
        """
        Tests a successful request to list the property values of a Thing.
        """
        expected_status_code = 200
        expected_resp_payload = {
            "temperature": 21.7,
            "humidity": 78
        }

        resp = Response()
        resp.status_code = expected_status_code
        resp._content = json.dumps(expected_resp_payload).encode('utf-8')

        with mock.patch("api.api.requests.request", return_value=resp) as m:
            prop = (API(host="test-api.swx.altairone.com").
                    things("thing01").
                    properties().
                    get())

        m.assert_called_once_with("GET",
                                  "https://test-api.swx.altairone.com/things/thing01/properties",
                                  headers={'Authorization': 'Bearer valid-token'},
                                  data=None,
                                  timeout=3)

        assert prop == expected_resp_payload
        assert type(prop) == PropertiesResp
