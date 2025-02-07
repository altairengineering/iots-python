import json
from unittest import mock

import pytest

from iots.api import API
from iots.models.models import Property, Properties
from .common import make_response

request_mock_pkg = 'iots.api.requests.request'


def test_get():
    """
    Tests a successful request to get a property value.
    """
    expected_resp_payload = {"temperature": 21.7}

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        prop = (API(host="test-api.swx.altairone.com").
                set_token("valid-token").
                spaces("space01").
                things("thing01").
                properties("temperature").
                get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/properties/temperature",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3,
                              verify=True)

    assert prop.dict() == expected_resp_payload
    assert isinstance(prop, Property)


def test_list():
    """
    Tests a successful request to list the property values of a Thing.
    """
    expected_resp_payload = {
        "temperature": 21.7,
        "humidity": 78
    }

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        prop = (API(host="test-api.swx.altairone.com").
                set_token("valid-token").
                spaces("space01").
                things("thing01").
                properties().
                get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/properties",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3,
                              verify=True)

    assert prop == expected_resp_payload
    assert isinstance(prop, Properties)


@pytest.mark.parametrize("property_name, value", [
    ("temperature", 17.5),
    ("status", "on"),
    ("enabled", True),
])
def test_update_one(property_name, value):
    """
    Tests a successful request to update one property value.
    """
    expected_resp_payload = {property_name: value}

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        prop = (API(host="test-api.swx.altairone.com").
                set_token("valid-token").
                spaces("space01").
                things("thing01").
                properties(property_name).
                update(value, params={'foo': 'bar'}))

    m.assert_called_once_with("PUT",
                              f"https://test-api.swx.altairone.com/spaces/space01/things/thing01/properties/{property_name}",
                              params={'foo': 'bar'},
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': 'Bearer valid-token',
                              },
                              data=json.dumps({property_name: value}),
                              timeout=3,
                              verify=True)

    assert prop == expected_resp_payload
    assert isinstance(prop, Properties)


def test_update_multiple():
    """
    Tests a successful request to update multiple property values.
    """
    new_values = {
        "temperature": 17.5,
        "humidity": 78
    }
    expected_resp_payload = new_values

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        prop = (API(host="test-api.swx.altairone.com").
                set_token("valid-token").
                spaces("space01").
                things("thing01").
                properties().
                update(new_values, params={'foo': 'bar'}))

    m.assert_called_once_with("PUT",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/properties",
                              params={'foo': 'bar'},
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': 'Bearer valid-token',
                              },
                              data=json.dumps(new_values),
                              timeout=3,
                              verify=True)

    assert prop == expected_resp_payload
    assert isinstance(prop, Properties)
