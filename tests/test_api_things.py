from unittest import mock

from swx.api import API
from swx.models.anythingdb import Thing, ThingList
from tests.common import make_json_response

test_thing01 = {
    "uid": "01FPSXTMN4CEGX09HF5RQ4RMY6",
    "id": "https://api.swx.altairone.com/beta/spaces/space01/things/01FPSXTMN4CEGX09HF5RQ4RMY6",
    "categories": [
        "category1",
        "category2"
    ],
    "title": "SmartWorks Device",
    "description": "My connected SmartWorks device",
    "@type": [
        "Light",
        "OnOffSwitch"
    ],
    "model": {
        "name": "RaspberryPiModel",
        "version": 1
    },
    "properties": {
        "cpu": {
            "title": "CPU %",
            "description": "Device CPU usage in percent",
            "type": "number",
            "unit": "percent",
            "readOnly": False
        },
        "disk": {
            "title": "Disk %",
            "description": "Device Disk usage in percent",
            "type": "number",
            "unit": "percent",
            "readOnly": False
        },
        "memory": {
            "title": "Memory %",
            "description": "Device Memory usage in percent",
            "type": "number",
            "unit": "percent",
            "readOnly": False
        }
    },
    "actions": {
        "delay": {
            "title": "Delay",
            "description": "Change sending frequency",
            "input": {
                "properties": {
                    "input": {
                        "maximum": 100,
                        "minimum": 3,
                        "type": "number"
                    }
                }
            }
        },
        "reboot": {
            "title": "Reboot",
            "description": "Reboot device"
        }
    },
    "events": {
        "highCPU": {
            "title": "High CPU",
            "description": "The CPU usage is over 50%",
            "data": {
                "type": "number",
                "unit": "percent"
            }
        }
    },
    "created": "2021-12-13T09:38:11Z",
    "modified": "2021-12-13T09:38:11Z"
}

test_thing02 = {
    "name": "RaspberryPiModel",
    "description": "My Raspberry Pi Model",
    "created": "2021-11-17T10:08:31Z",
    "modified": "2021-11-17T10:08:31Z"
}


def test_get():
    """
    Tests a successful request to get a Thing.
    """
    expected_resp = make_json_response(200, test_thing01)

    with mock.patch("swx.api.requests.request", return_value=expected_resp) as m:
        cat = (API(host="test-api.swx.altairone.com").
               set_token("valid-token").
               spaces("space01").
               things("thing01").
               get())

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01",
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)

    assert cat == Thing.parse_obj(test_thing01)
    assert type(cat) == Thing


def test_list():
    """
    Tests a successful request to list Things.
    """
    expected_resp_payload = {
        "paging": {
            "next_cursor": "",
            "previous_cursor": ""
        },
        "data": [test_thing01, test_thing02]
    }

    expected_resp = make_json_response(200, expected_resp_payload)

    with mock.patch("swx.api.requests.request", return_value=expected_resp) as m:
        cat = (API(host="test-api.swx.altairone.com").
               set_token("valid-token").
               spaces("space01").
               things().
               get())

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things",
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)

    assert cat == ThingList.parse_obj(expected_resp_payload)
    assert type(cat) == ThingList
