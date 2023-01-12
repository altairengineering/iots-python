from unittest import TestCase, mock

from api.api import API
from models.anythingdb import ActionResponse, ActionListResponse
from tests.common import make_json_response

test_action01 = {
    "delay": {
        "input": {
            "delay": 5
        },
        "status": "pending",
        "timeRequested": "2022-06-02 15:37:46+0000",
        "href": "/beta/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/actions/delay/01EDCAQE78A7CP6REXV5J8BAKR"
    }
}

test_action02 = {
    "delay": {
        "input": {
            "delay": 7
        },
        "status": "pending",
        "timeRequested": "2022-06-02 15:39:54+0000",
        "href": "/beta/spaces/altair/things/01FPSXTMN4CEGX09HF5RQ4RMY6/actions/delay/01EDCB9FMD0Q3QR0YV4TWY4S3E"
    }
}


class TestAPIActions(TestCase):
    def test_get(self):
        """
        Tests a successful request to get an action info.
        """
        expected_resp = make_json_response(200, test_action01)

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

        assert action == ActionResponse.parse_obj(test_action01)
        assert type(action) == ActionResponse

    def test_list(self):
        """
        Tests a successful request to list the actions of a Thing.
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
