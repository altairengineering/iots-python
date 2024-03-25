from unittest import mock

import pytest

from iots.api import API
from iots.models.models import (EventCreateRequest, EventListResponse,
                                EventResponse)
from .common import make_response, to_json
from .test_api_pagination import assert_pagination

request_mock_pkg = 'iots.api.requests.request'

test_event01 = {
    "highCPU": {
        "data": 61,
        "timestamp": "2020-04-02 15:22:37+0000",
        "href": "/beta/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/events/highCPU/01EDCEZDTJX50SQTCJST5EW5NX"
    }
}

test_event02 = {
    "highCPU": {
        "data": 85,
        "timestamp": "2020-04-02 15:26:42+0000",
        "href": "/beta/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/events/highCPU/01EDCGYKV4YQ1CY3QHHSX8J843"
    }
}

test_event03 = {
    "lowDiskSpace": {
        "data": 95,
        "timestamp": "2020-04-03 07:12:55+0000",
        "href": "/beta/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/events/lowDiskSpace/01GPX7BR5X3YT5Y65ZMT24YT1N"
    }
}


@pytest.mark.parametrize("event_req", [
    EventCreateRequest.parse_obj({"highCPU": {"data": 75}}),
    {"highCPU": {"data": 75}},
])
def test_create(event_req):
    """
    Tests a successful request to create an Event value.
    """
    expected_resp_payload = test_event01
    expected_resp = make_response(201, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        event = (API(host="test-api.swx.altairone.com").
                 set_token("valid-token").
                 spaces("space01").
                 things("thing01").
                 events("delay").
                 create(event_req, params={'foo': 'bar'}))

    m.assert_called_once_with("POST",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/events/delay",
                              params={'foo': 'bar'},
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json',
                              },
                              data=to_json(event_req),
                              timeout=3)

    assert event == EventResponse.parse_obj(expected_resp_payload)
    assert isinstance(event, EventResponse)


def test_list_event():
    """
    Tests a successful request to list the history values of an Event.
    """
    expected_resp_payload = {
        "paging": {
            "next_cursor": "",
            "previous_cursor": ""
        },
        "data": [test_event01, test_event02]
    }

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        event = (API(host="test-api.swx.altairone.com").
                 set_token("valid-token").
                 spaces("space01").
                 things("thing01").
                 events("highCPU").
                 get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/events/highCPU",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3)

    assert event == EventListResponse.parse_obj(expected_resp_payload)
    assert isinstance(event, EventListResponse)

    # Test pagination
    expected_high_cpu_events = [
        test_event01,
        test_event02,
    ]
    expected_high_cpu_events.sort(key=lambda x: x['highCPU']['timestamp'])

    pagination_function = (API(host="test-api.swx.altairone.com").
                           set_token("valid-token").
                           spaces("space01").
                           things("thing01").
                           events("highCPU").
                           get)

    for limit in range(1, 10):
        assert_pagination(pagination_function,
                          "https://test-api.swx.altairone.com/spaces/space01/things/thing01/events/highCPU",
                          expected_high_cpu_events, limit, {'foo': 'bar'},
                          lambda x: x['highCPU']['timestamp'], EventResponse)


def test_list_all():
    """
    Tests a successful request to list all the Event values of a Thing.
    """
    expected_resp_payload = {
        "paging": {
            "next_cursor": "",
            "previous_cursor": ""
        },
        "data": [test_event01, test_event02, test_event03]
    }

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        events = (API(host="test-api.swx.altairone.com").
                  set_token("valid-token").
                  spaces("space01").
                  things("thing01").
                  events().
                  get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/events",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3)

    assert events == EventListResponse.parse_obj(expected_resp_payload)
    assert isinstance(events, EventListResponse)

    # Test pagination
    expected_events = [
        test_event01,
        test_event02,
        test_event03,
    ]
    expected_events.sort(key=lambda x: x[list(x)[0]]['timestamp'])

    pagination_function = (API(host="test-api.swx.altairone.com").
                           set_token("valid-token").
                           spaces("space01").
                           things("thing01").
                           events().
                           get)

    for limit in range(1, 10):
        assert_pagination(pagination_function,
                          "https://test-api.swx.altairone.com/spaces/space01/things/thing01/events",
                          expected_events, limit, {'foo': 'bar'},
                          lambda x: x[list(x)[0]]['timestamp'], EventResponse)


def test_get_event():
    """
    Tests a successful request to get an Event value.
    """
    expected_resp = make_response(200, test_event02)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        event = (API(host="test-api.swx.altairone.com").
                 set_token("valid-token").
                 spaces("space01").
                 things("thing01").
                 events("highCPU", "01EDCEZDTJX50SQTCJST5EW5NX").
                 get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01"
                              "/events/highCPU/01EDCEZDTJX50SQTCJST5EW5NX",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3)

    assert event == EventResponse.parse_obj(test_event02)
    assert isinstance(event, EventResponse)
