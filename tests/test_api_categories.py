from unittest import mock

import pytest

from iots.api import API
from iots.models.models import (CategoryCreate, Category, CategoryList,
                                CategoryUpdate)
from .common import make_response, to_json
from .test_api_pagination import assert_pagination

request_mock_pkg = 'iots.api.requests.request'

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

# Payload of a request to create/update a Category
test_category_request_payload = test_category01.copy()
del test_category_request_payload['created']
del test_category_request_payload['modified']


@pytest.mark.parametrize("category_req", [
    CategoryCreate.parse_obj(test_category_request_payload),
    test_category_request_payload,
])
def test_create(category_req):
    """
    Tests a successful request to create a Category.
    """
    expected_resp_payload = test_category01

    expected_resp = make_response(201, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  set_token("valid-token").
                  spaces("space01").
                  categories().
                  create(category_req, params={'foo': 'bar'}))

    m.assert_called_once_with("POST",
                              "https://test-api.swx.altairone.com/spaces/space01/categories",
                              params={'foo': 'bar'},
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json',
                              },
                              data=to_json(category_req),
                              timeout=3,
                              verify=True)

    assert action == Category.parse_obj(expected_resp_payload)
    assert isinstance(action, Category)


def test_get():
    """
    Tests a successful request to get a Category.
    """
    expected_resp = make_response(200, test_category01)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        cat = (API(host="test-api.swx.altairone.com").
               set_token("valid-token").
               spaces("space01").
               categories("category01").
               get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/categories/category01",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3,
                              verify=True)

    assert cat == Category.parse_obj(test_category01)
    assert isinstance(cat, Category)


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

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        cat = (API(host="test-api.swx.altairone.com").
               set_token("valid-token").
               spaces("space01").
               categories().
               get(params={'foo': 'bar'}))

    m.assert_called_once_with("GET",
                              "https://test-api.swx.altairone.com/spaces/space01/categories",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3,
                              verify=True)

    assert cat == CategoryList.parse_obj(expected_resp_payload)
    assert isinstance(cat, CategoryList)

    # Test pagination
    pagination_function = (API(host="test-api.swx.altairone.com").
                           set_token("valid-token").
                           spaces("space01").
                           categories().
                           get)

    for limit in range(1, 10):
        assert_pagination(pagination_function,
                          "https://test-api.swx.altairone.com/spaces/space01/categories",
                          categories, limit, {'foo': 'bar'},
                          lambda x: x['name'], Category)


@pytest.mark.parametrize("category_req", [
    CategoryUpdate.parse_obj(test_category_request_payload),
    test_category_request_payload,
])
def test_update(category_req):
    """
    Tests a successful request to update a Category.
    """
    expected_resp_payload = test_category_request_payload.copy()
    expected_resp_payload["created"] = "2024-01-15T11:19:09Z"
    expected_resp_payload["modified"] = "2024-03-21T20:33:51Z"

    expected_resp = make_response(200, expected_resp_payload)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        action = (API(host="test-api.swx.altairone.com").
                  set_token("valid-token").
                  spaces("space01").
                  categories("ElectronicBoards").
                  update(category_req, params={'foo': 'bar'}))

    m.assert_called_once_with("PUT",
                              "https://test-api.swx.altairone.com/spaces/space01/categories/ElectronicBoards",
                              params={'foo': 'bar'},
                              headers={
                                  'Authorization': 'Bearer valid-token',
                                  'Content-Type': 'application/json',
                              },
                              data=to_json(category_req),
                              timeout=3,
                              verify=True)

    assert action == Category.parse_obj(expected_resp_payload)
    assert isinstance(action, Category)


def test_delete():
    """
    Tests a successful request to delete a Category.
    """
    expected_resp = make_response(204)

    with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
        (API(host="test-api.swx.altairone.com").
         set_token("valid-token").
         spaces("space01").
         categories("ElectronicBoards").
         delete(params={'foo': 'bar'}))

    m.assert_called_once_with("DELETE",
                              "https://test-api.swx.altairone.com/spaces/space01/categories/ElectronicBoards",
                              params={'foo': 'bar'},
                              headers={'Authorization': 'Bearer valid-token'},
                              data=[],
                              timeout=3,
                              verify=True)
