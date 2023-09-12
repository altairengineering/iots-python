from unittest import mock

from swx.api import API
from swx.models.anythingdb import Properties
from tests.common import make_json_response


def test_get():
    """
    Tests a successful request to get a property value.
    """
    expected_resp_payload = {"temperature": 21.7}

    expected_resp = make_json_response(200, expected_resp_payload)

    with mock.patch("swx.api.requests.request", return_value=expected_resp) as m:
        prop = (API(host="test-api.swx.altairone.com").
                set_token("valid-token").
                spaces("space01").
                things("thing01").
                properties("temperature").
                get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/properties/temperature",
                              params={'foo': 'bar'},
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Prefer': 'preview=2023.1',
                              },
                              data=None,
                              timeout=3)

    assert prop.dict() == expected_resp_payload
    assert type(prop) == Properties


def test_list():
    """
    Tests a successful request to list the property values of a Thing.
    """
    expected_resp_payload = {
        "temperature": 21.7,
        "humidity": 78
    }

    expected_resp = make_json_response(200, expected_resp_payload)

    with mock.patch("swx.api.requests.request", return_value=expected_resp) as m:
        prop = (API(host="test-api.swx.altairone.com").
                set_token("valid-token").
                spaces("space01").
                things("thing01").
                properties().
                get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/properties",
                              params={'foo': 'bar'},
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Prefer': 'preview=2023.1',
                              },
                              data=None,
                              timeout=3)

    assert prop == expected_resp_payload
    assert type(prop) == Properties


def test_update_one():
    """
    Tests a successful request to update one property value.
    """
    expected_resp_payload = {"temperature": 17.5}

    expected_resp = make_json_response(201, expected_resp_payload)

    with mock.patch("swx.api.requests.request", return_value=expected_resp) as m:
        prop = (API(host="test-api.swx.altairone.com").
                set_token("valid-token").
                spaces("space01").
                things("thing01").
                properties("temperature").
                update(17.5, params={'foo': 'bar'}))

    m.assert_called_once_with("POST",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/properties/temperature",
                              params={'foo': 'bar'},
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json',
                                  'Prefer': 'preview=2023.1',
                              },
                              data={"temperature": 17.5},
                              timeout=3)

    assert prop == expected_resp_payload
    assert type(prop) == Properties


def test_update_multiple():
    """
    Tests a successful request to update multiple property values.
    """
    new_values = {
        "temperature": 17.5,
        "humidity": 78
    }
    expected_resp_payload = new_values

    expected_resp = make_json_response(201, expected_resp_payload)

    with mock.patch("swx.api.requests.request", return_value=expected_resp) as m:
        prop = (API(host="test-api.swx.altairone.com").
                set_token("valid-token").
                spaces("space01").
                things("thing01").
                properties().
                update(new_values, params={'foo': 'bar'}))

    m.assert_called_once_with("POST",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/properties",
                              params={'foo': 'bar'},
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json',
                                  'Prefer': 'preview=2023.1',
                              },
                              data=new_values,
                              timeout=3)

    assert prop == expected_resp_payload
    assert type(prop) == Properties
