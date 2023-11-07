from unittest import mock

from swx.api import API
from swx.models.anythingdb import Category, CategoryList
from tests.common import make_json_response
from tests.test_api_pagination import assert_pagination

test_category01 = {
    "name": "ElectronicBoards",
    "description": "My category",
    "model": {
        "name": "RaspberryPiModel",
        "version": 1
    },
    "created": "2021-11-17T03:15:40Z",
    "modified": "2021-11-17T03:15:40Z"
}

test_category02 = {
    "name": "ElectronicComponents",
    "description": "My electronic components category",
    "model": None,
    "created": "2021-11-19T11:19:09Z",
    "modified": "2021-11-21T20:33:51Z"
}

test_category03 = {
    "name": "Category03",
    "model": None,
    "created": "2023-10-23T08:12:02Z",
    "modified": "2023-11-06T14:03:13Z"
}

test_category04 = {
    "name": "Category04",
    "model": None,
    "created": "2023-02-20T21:54:23Z",
    "modified": "2023-07-01T16:34:52Z"
}

categories = [
    test_category01,
    test_category02,
    test_category03,
    test_category04,
]
categories.sort(key=lambda x: x['name'])


def test_get():
    """
    Tests a successful request to get a Category.
    """
    expected_resp = make_json_response(200, test_category01)

    with mock.patch("swx.api.requests.request", return_value=expected_resp) as m:
        cat = (API(host="test-api.swx.altairone.com").
               set_token("valid-token").
               spaces("space01").
               categories("category01").
               get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/categories/category01",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)

    assert cat == Category.parse_obj(test_category01)
    assert type(cat) == Category


def test_list():
    """
    Tests a successful request to list Categories.
    """
    expected_resp_payload = {
        "paging": {
            "next_cursor": "",
            "previous_cursor": ""
        },
        "data": [test_category01, test_category02]
    }

    expected_resp = make_json_response(200, expected_resp_payload)

    with mock.patch("swx.api.requests.request", return_value=expected_resp) as m:
        cat = (API(host="test-api.swx.altairone.com").
               set_token("valid-token").
               spaces("space01").
               categories().
               get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/categories",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=None,
                              timeout=3)

    assert cat == CategoryList.parse_obj(expected_resp_payload)
    assert type(cat) == CategoryList

    # Test pagination
    pagination_function = (API(host="test-api.swx.altairone.com").
                           set_token("valid-token").
                           spaces("space01").
                           categories().
                           get)

    for i in range(1, 10):
        assert_pagination(pagination_function,
                          "https://test-api.swx.altairone.com/spaces/space01/categories",
                          categories, i, {'foo': 'bar'},
                          lambda x: x['name'], Category)
