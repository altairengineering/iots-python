from unittest import TestCase, mock

from api.api import API
from models.property import PropertiesResp
from tests.common import make_json_response


class TestAPIProperties(TestCase):
    def test_get(self):
        """
        Tests a successful request to get a property value.
        """
        expected_resp_payload = {"temperature": 21.7}

        expected_resp = make_json_response(200, expected_resp_payload)

        with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
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
        expected_resp_payload = {
            "temperature": 21.7,
            "humidity": 78
        }

        expected_resp = make_json_response(200, expected_resp_payload)

        with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
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
