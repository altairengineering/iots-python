from unittest import mock

import pytest

from api.api import API
from models.anythingdb import (ActionCreateRequest, ActionUpdateRequest,
                               ActionResponse, ActionListResponse)
from tests.common import make_json_response, to_dict

test_action01 = {
    "delay": {
        "input": 5,
        "status": "pending",
        "timeRequested": "2022-06-02 15:37:46+0000",
        "href": "/beta/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/actions/delay/01EDCAQE78A7CP6REXV5J8BAKR"
    }
}

test_action02 = {
    "delay": {
        "input": 7,
        "status": "completed",
        "timeRequested": "2022-06-02 15:39:54+0000",
        "timeCompleted": "2022-06-01 15:45:32+0000",
        "href": "/beta/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/actions/delay/01EDCB9FMD0Q3QR0YV4TWY4S3E"
    }
}

test_action03 = {
    "reboot": {
        "status": "pending",
        "timeRequested": "2022-06-02 15:56:12+0000",
        "href": "/beta/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/actions/delay/01EDCCZYATJW1Z3D4T4BA4S2QH"
    }
}


@pytest.mark.parametrize("action_req", [
    ActionCreateRequest.parse_obj({"delay": {"input": 5}}),
    {"delay": {"input": 5}},
])
def test_create(action_req):
    """
    Tests a successful request to create an Action value.
    """
    expected_resp_payload = test_action01
    expected_resp = make_json_response(201, expected_resp_payload)

    with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  token("valid-token").
                  spaces("space01").
                  things("thing01").
                  actions("delay").
                  create(action_req))

    m.assert_called_once_with("POST",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/actions/delay",
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json'
                              },
                              data=to_dict(action_req),
                              timeout=3)

    assert action == ActionResponse.parse_obj(expected_resp_payload)
    assert type(action) == ActionResponse


def test_list_action():
    """
    Tests a successful request to list the history values of an Action.
    """
    expected_resp_payload = {
        "paging": {
            "next_cursor": "",
            "previous_cursor": ""
        },
        "data": [test_action01, test_action02]
    }

    expected_resp = make_json_response(200, expected_resp_payload)

    with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  token("valid-token").
                  spaces("space01").
                  things("thing01").
                  actions("delay").
                  get())

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/actions/delay",
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)

    assert action == ActionListResponse.parse_obj(expected_resp_payload)
    assert type(action) == ActionListResponse


def test_list_all():
    """
    Tests a successful request to list all the Action values of a Thing.
    """
    expected_resp_payload = {
        "paging": {
            "next_cursor": "",
            "previous_cursor": ""
        },
        "data": [test_action01, test_action02, test_action03]
    }

    expected_resp = make_json_response(200, expected_resp_payload)

    with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
        actions = (API(host="test-api.swx.altairone.com").
                   token("valid-token").
                   spaces("space01").
                   things("thing01").
                   actions().
                   get())

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/actions",
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)

    assert actions == ActionListResponse.parse_obj(expected_resp_payload)
    assert type(actions) == ActionListResponse


def test_get_action():
    """
    Tests a successful request to get an Action value.
    """
    expected_resp = make_json_response(200, test_action02)

    with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  token("valid-token").
                  spaces("space01").
                  things("thing01").
                  actions("delay", "01EDCB9FMD0Q3QR0YV4TWY4S3E").
                  get())

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01"
                              "/actions/delay/01EDCB9FMD0Q3QR0YV4TWY4S3E",
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)

    assert action == ActionResponse.parse_obj(test_action02)
    assert type(action) == ActionResponse


@pytest.mark.parametrize("action_req", [
    ActionUpdateRequest.parse_obj({"delay": {"status": "completed"}}),
    {"delay": {"status": "completed"}},
])
def test_put_action(action_req):
    """
    Tests a successful request to update an Action value.
    """
    expected_resp_payload = test_action02
    expected_resp = make_json_response(200, expected_resp_payload)

    with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  token("valid-token").
                  spaces("space01").
                  things("thing01").
                  actions("delay", "01EDCB9FMD0Q3QR0YV4TWY4S3E").
                  update(action_req))

    m.assert_called_once_with("PUT",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01"
                              "/actions/delay/01EDCB9FMD0Q3QR0YV4TWY4S3E",
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json'
                              },
                              data=to_dict(action_req),
                              timeout=3)

    assert action == ActionResponse.parse_obj(expected_resp_payload)
    assert type(action) == ActionResponse


def test_delete_action():
    """
    Tests a successful request to delete an Action value.
    """
    expected_resp = make_json_response(204)

    with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
        (API(host="test-api.swx.altairone.com").
         token("valid-token").
         spaces("space01").
         things("thing01").
         actions("delay", "01EDCB9FMD0Q3QR0YV4TWY4S3E").
         delete())

    m.assert_called_once_with("DELETE",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01"
                              "/actions/delay/01EDCB9FMD0Q3QR0YV4TWY4S3E",
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)
