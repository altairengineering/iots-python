from unittest import mock

import pytest

from iots.api import API
from iots.models.models import Thing, ThingList, ThingCreate, ThingUpdate, ThingPatch
from .common import make_response, to_json
from .test_api_pagination import assert_pagination

request_mock_pkg = 'iots.api.requests.request'

test_thing01 = {
    "uid": "THING000000000000000000001",
    "id": "https://api.swx.altairone.com/beta/spaces/space01/things/THING000000000000000000001",
    "categories": [
        "category1",
        "category2"
    ],
    "title": "IoT Studio Device",
    "description": "My connected IoT Studio device",
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
    "links": [
        {
            "href": "https://help.altair.com/altair-iot-studio/index.htm",
            "rel": "documentation"
        },
        {
            "href": "/spaces/space01/things/01FPSXTMN4CEGX09HF5RQ4RMY6",
            "rel": "parent"
        }
    ],
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

test_patch_request = [
    {
        "op": "replace",
        "path": "/description",
        "value": "Updated description"
    }
]

# Payload of a request to create/update a Category
test_thing_request_payload = test_thing01.copy()
del test_thing_request_payload['uid']
del test_thing_request_payload['id']
del test_thing_request_payload['created']
del test_thing_request_payload['modified']


@pytest.mark.parametrize("thing_req", [
    ThingCreate.parse_obj(test_thing_request_payload),
    test_thing_request_payload,
])
def test_create(thing_req):
    """
    Tests a successful request to create a Thing.
    """
    expected_resp_payload = test_thing01

    expected_resp = make_response(201, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  set_token("valid-token").
                  spaces("space01").
                  things().
                  create(thing_req, params={'foo': 'bar'}))

    m.assert_called_once_with("POST",
                              "https://test-api.swx.altairone.com/spaces/space01/things",
                              params={'foo': 'bar'},
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json',
                              },
                              data=to_json(thing_req),
                              timeout=3,
                              verify=True)

    assert action == Thing.parse_obj(expected_resp_payload)
    assert isinstance(action, Thing)


def test_get():
    """
    Tests a successful request to get a Thing.
    """
    expected_resp = make_response(200, test_thing01)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        thing_resp = (API(host="test-api.swx.altairone.com").
                      set_token("valid-token").
                      spaces("space01").
                      things("thing01").
                      get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things/thing01",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3,
                              verify=True)

    assert thing_resp == Thing.parse_obj(test_thing01)
    assert isinstance(thing_resp, Thing)


def test_get_by_category():
    """
    Tests a successful request to get a Thing using the Category endpoint.
    """
    expected_resp = make_response(200, test_thing01)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        thing_resp = (API(host="test-api.swx.altairone.com").
                      set_token("valid-token").
                      spaces("space01").
                      categories("category2").
                      things("thing01").
                      get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/categories/category2/things/thing01",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3,
                              verify=True)

    assert thing_resp == Thing.parse_obj(test_thing01)
    assert isinstance(thing_resp, Thing)


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

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        things_resp = (API(host="test-api.swx.altairone.com").
                       set_token("valid-token").
                       spaces("space01").
                       things().
                       get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/things",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3,
                              verify=True)

    assert things_resp == ThingList.parse_obj(expected_resp_payload)
    assert isinstance(things_resp, ThingList)

    # Test pagination
    pagination_function = (API(host="test-api.swx.altairone.com").
                           set_token("valid-token").
                           spaces("space01").
                           things().
                           get)

    for limit in range(1, 10):
        assert_pagination(pagination_function,
                          "https://test-api.swx.altairone.com/spaces/space01/things",
                          things, limit, {'foo': 'bar'},
                          lambda x: x['uid'], Thing)


@pytest.mark.parametrize("thing_req", [
    ThingUpdate.parse_obj(test_thing_request_payload),
    test_thing_request_payload,
])
def test_update(thing_req):
    """
    Tests a successful request to update a Thing.
    """
    expected_resp_payload = test_thing01

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  set_token("valid-token").
                  spaces("space01").
                  things("THING000000000000000000001").
                  update(thing_req, params={'foo': 'bar'}))

    m.assert_called_once_with("PUT",
                              "https://test-api.swx.altairone.com/spaces/space01/things/THING000000000000000000001",
                              params={'foo': 'bar'},
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json',
                              },
                              data=to_json(thing_req),
                              timeout=3,
                              verify=True)

    assert action == Thing.parse_obj(expected_resp_payload)
    assert isinstance(action, Thing)


@pytest.mark.parametrize("thing_req", [
    ThingPatch.parse_obj(test_patch_request),
    test_patch_request,
])
def test_patch(thing_req):
    """
    Tests a successful request to partially update a Thing.
    """
    expected_resp_payload = test_thing01

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  set_token("valid-token").
                  spaces("space01").
                  things("THING000000000000000000001").
                  patch(thing_req, params={'foo': 'bar'}))

    m.assert_called_once_with("PATCH",
                              "https://test-api.swx.altairone.com/spaces/space01/things/THING000000000000000000001",
                              params={'foo': 'bar'},
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json-patch+json',
                              },
                              data=to_json(thing_req),
                              timeout=3,
                              verify=True)

    assert action == Thing.parse_obj(expected_resp_payload)
    assert isinstance(action, Thing)


def test_delete():
    """
    Tests a successful request to delete a Thing.
    """
    expected_resp = make_response(204)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        (API(host="test-api.swx.altairone.com").
         set_token("valid-token").
         spaces("space01").
         things("THING000000000000000000001").
         delete(params={'foo': 'bar'}))

    m.assert_called_once_with("DELETE",
                              "https://test-api.swx.altairone.com/spaces/space01/things/THING000000000000000000001",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3,
                              verify=True)
