from unittest import mock

import pytest

from iots.api import API
from iots.models.models import (ActionCreateRequest, ActionListResponse,
                                ActionResponse, ActionUpdateRequest)
from .common import make_response, to_json
from .test_api_pagination import assert_pagination

request_mock_pkg = 'iots.api.requests.request'

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
    expected_resp = make_response(201, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  set_token("valid-token").
                  spaces("space01").
                  things("thing01").
                  actions("delay").
                  create(action_req, params={'foo': 'bar'}))

    m.assert_called_once_with("POST",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/actions/delay",
                              params={'foo': 'bar'},
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json',
                              },
                              data=to_json(action_req),
                              timeout=3)

    assert action == ActionResponse.parse_obj(expected_resp_payload)
    assert isinstance(action, ActionResponse)


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

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  set_token("valid-token").
                  spaces("space01").
                  things("thing01").
                  actions("delay").
                  get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/actions/delay",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3)

    assert action == ActionListResponse.parse_obj(expected_resp_payload)
    assert isinstance(action, ActionListResponse)

    # Test pagination
    expected_delay_actions = [
        test_action01,
        test_action02,
    ]
    expected_delay_actions.sort(key=lambda x: x['delay']['timeRequested'])

    pagination_function = (API(host="test-api.swx.altairone.com").
                           set_token("valid-token").
                           spaces("space01").
                           things("thing01").
                           actions("delay").
                           get)

    for limit in range(1, 10):
        assert_pagination(pagination_function,
                          "https://test-api.swx.altairone.com/spaces/space01/things/thing01/actions/delay",
                          expected_delay_actions, limit, {'foo': 'bar'},
                          lambda x: x['delay']['timeRequested'], ActionResponse)


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

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        actions = (API(host="test-api.swx.altairone.com").
                   set_token("valid-token").
                   spaces("space01").
                   things("thing01").
                   actions().
                   get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01/actions",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3)

    assert actions == ActionListResponse.parse_obj(expected_resp_payload)
    assert isinstance(actions, ActionListResponse)

    # Test pagination
    expected_actions = [
        test_action01,
        test_action02,
        test_action03,
    ]
    expected_actions.sort(key=lambda x: x[list(x)[0]]['timeRequested'])

    pagination_function = (API(host="test-api.swx.altairone.com").
                           set_token("valid-token").
                           spaces("space01").
                           things("thing01").
                           actions().
                           get)

    for limit in range(1, 10):
        assert_pagination(pagination_function,
                          "https://test-api.swx.altairone.com/spaces/space01/things/thing01/actions",
                          expected_actions, limit, {'foo': 'bar'},
                          lambda x: x[list(x)[0]]['timeRequested'], ActionResponse)


def test_get_action():
    """
    Tests a successful request to get an Action value.
    """
    expected_resp = make_response(200, test_action02)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  set_token("valid-token").
                  spaces("space01").
                  things("thing01").
                  actions("delay", "01EDCB9FMD0Q3QR0YV4TWY4S3E").
                  get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01"
                              "/actions/delay/01EDCB9FMD0Q3QR0YV4TWY4S3E",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3)

    assert action == ActionResponse.parse_obj(test_action02)
    assert isinstance(action, ActionResponse)


@pytest.mark.parametrize("action_req", [
    ActionUpdateRequest.parse_obj({"delay": {"status": "completed"}}),
    {"delay": {"status": "completed"}},
])
def test_put_action(action_req):
    """
    Tests a successful request to update an Action value.
    """
    expected_resp_payload = test_action02
    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  set_token("valid-token").
                  spaces("space01").
                  things("thing01").
                  actions("delay", "01EDCB9FMD0Q3QR0YV4TWY4S3E").
                  update(action_req, params={'foo': 'bar'}))

    m.assert_called_once_with("PUT",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01"
                              "/actions/delay/01EDCB9FMD0Q3QR0YV4TWY4S3E",
                              params={'foo': 'bar'},
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': 'Bearer valid-token',
                              },
                              data=to_json(action_req),
                              timeout=3)

    assert action == ActionResponse.parse_obj(expected_resp_payload)
    assert isinstance(action, ActionResponse)


def test_delete_action():
    """
    Tests a successful request to delete an Action value.
    """
    expected_resp = make_response(204)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        (API(host="test-api.swx.altairone.com").
         set_token("valid-token").
         spaces("space01").
         things("thing01").
         actions("delay", "01EDCB9FMD0Q3QR0YV4TWY4S3E").
         delete(params={'foo': 'bar'}))

    m.assert_called_once_with("DELETE",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01"
                              "/actions/delay/01EDCB9FMD0Q3QR0YV4TWY4S3E",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3)
