from unittest import mock

from swx.api import API
from swx.models.anythingdb import Thing, ThingList
from tests.common import make_json_response
from tests.test_api_pagination import assert_pagination

test_thing01 = {
    "uid": "THING000000000000000000001",
    "id": "https://api.swx.altairone.com/beta/spaces/space01/things/THING000000000000000000001",
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
    "uid": "THING000000000000000000002",
    "name": "RaspberryPiModel",
    "description": "My Raspberry Pi Model",
    "created": "2021-11-17T10:08:31Z",
    "modified": "2021-11-17T10:08:31Z"
}

test_thing03 = {
    "uid": "THING000000000000000000003",
    "name": "Thing 3",
    "created": "2023-10-23T08:12:02Z",
    "modified": "2023-11-06T14:03:13Z"
}

test_thing04 = {
    "uid": "THING000000000000000000004",
    "name": "Thing 4",
    "created": "2023-02-20T21:54:23Z",
    "modified": "2023-07-01T16:34:52Z"
}

things = [
    test_thing01,
    test_thing02,
    test_thing03,
    test_thing04,
]


def test_get():
    """
    Tests a successful request to get a Thing.
    """
    expected_resp = make_json_response(200, test_thing01)

    with mock.patch("swx.api.requests.request", return_value=expected_resp) as m:
        thing_resp = (API(host="test-api.swx.altairone.com").
                      set_token("valid-token").
                      spaces("space01").
                      things("thing01").
                      get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)

    assert thing_resp == Thing.parse_obj(test_thing01)
    assert type(thing_resp) == Thing


def test_list():
    """
    Tests a successful request to list Things.
    """
    expected_resp_payload = {
        "paging": {
            "next_cursor": "123",
            "previous_cursor": ""
        },
        "data": [test_thing01, test_thing02]
    }

    expected_resp = make_json_response(200, expected_resp_payload)

    with mock.patch("swx.api.requests.request", return_value=expected_resp) as m:
        things_resp = (API(host="test-api.swx.altairone.com").
                       set_token("valid-token").
                       spaces("space01").
                       things().
                       get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)

    assert things_resp == ThingList.parse_obj(expected_resp_payload)
    assert type(things_resp) == ThingList

    # Test pagination
    pagination_function = (API(host="test-api.swx.altairone.com").
                           set_token("valid-token").
                           spaces("space01").
                           things().
                           get)

    for i in range(1, 10):
        assert_pagination(pagination_function,
                          "https://test-api.swx.altairone.com/spaces/space01/things",
                          things, i, {'foo': 'bar'},
                          lambda x: x['uid'], Thing)
