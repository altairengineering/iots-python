from unittest import mock

import pytest

from api.api import API
from models.anythingdb import EventCreateRequest, EventResponse, EventListResponse
from tests.common import make_json_response, to_dict

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
    expected_resp = make_json_response(201, expected_resp_payload)

    with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
        event = (API(host="test-api.swx.altairone.com").
                 token("valid-token").
                 spaces("space01").
                 things("thing01").
                 events("delay").
                 create(event_req))

    m.assert_called_once_with("POST",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/events/delay",
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json'
                              },
                              data=to_dict(event_req),
                              timeout=3)

    assert event == EventResponse.parse_obj(expected_resp_payload)
    assert type(event) == EventResponse


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

    expected_resp = make_json_response(200, expected_resp_payload)

    with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
        event = (API(host="test-api.swx.altairone.com").
                 token("valid-token").
                 spaces("space01").
                 things("thing01").
                 events("delay").
                 get())

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/events/delay",
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)

    assert event == EventListResponse.parse_obj(expected_resp_payload)
    assert type(event) == EventListResponse


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

    expected_resp = make_json_response(200, expected_resp_payload)

    with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
        events = (API(host="test-api.swx.altairone.com").
                  token("valid-token").
                  spaces("space01").
                  things("thing01").
                  events().
                  get())

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/events",
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)

    assert events == EventListResponse.parse_obj(expected_resp_payload)
    assert type(events) == EventListResponse


def test_get_event():
    """
    Tests a successful request to get an Event value.
    """
    expected_resp = make_json_response(200, test_event02)

    with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
        event = (API(host="test-api.swx.altairone.com").
                 token("valid-token").
                 spaces("space01").
                 things("thing01").
                 events("delay", "01EDCB9FMD0Q3QR0YV4TWY4S3E").
                 get())

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01"
                              "/events/delay/01EDCB9FMD0Q3QR0YV4TWY4S3E",
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)

    assert event == EventResponse.parse_obj(test_event02)
    assert type(event) == EventResponse
