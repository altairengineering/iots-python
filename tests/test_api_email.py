import json
from unittest import mock

import pytest

from iots.api import API
from iots.models.models import Email
from .common import make_response, to_json

request_mock_pkg = 'iots.api.requests.request'

test_email_req_1 = {
    "to": [
        "johndoe@altair.com",
        "janedoe@altair.com"
    ],
    "cc": [
        "judydoe@altair.com",
        "johnstiles@altair.com"
    ],
    "bcc": [
        "marymajor@altair.com",
        "richardmiles@altair.com"
    ],
    "subject": "Email Subject Example",
    "body": {
        "html": "<p>Email <b>body</b> content</p>",
        "text": None
    }
}


def test_model():
    assert test_email_req_1 == Email.parse_obj(test_email_req_1).dict(by_alias=True)


@pytest.mark.parametrize("email_req", [
    Email.parse_obj(test_email_req_1),
    test_email_req_1,
])
def test_send(email_req):
    """
    Tests a successful request to send an Email.
    """
    expected_resp = make_response(202, None)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        email_resp = (API(host="test-api.swx.altairone.com").
                      set_token("valid-token").
                      spaces("space01").
                      communications().
                      email().
                      send(email_req, params={'foo': 'bar'}))

    m.assert_called_once_with("POST",
                              "https://test-api.swx.altairone.com/spaces/space01/communications/email",
                              params={'foo': 'bar'},
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json',
                              },
                              data=to_json(email_req),
                              timeout=3,
                              verify=True)
