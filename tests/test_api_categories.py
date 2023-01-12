from unittest import TestCase, mock

from api.api import API
from models.anythingdb import Category, CategoryList
from tests.common import make_json_response

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


class TestAPICategories(TestCase):
    def test_get(self):
        """
        Tests a successful request to get a Category.
        """
        expected_resp = make_json_response(200, test_category01)

        with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
            cat = (API(host="test-api.swx.altairone.com").
                   token("valid-token").
                   spaces("space01").
                   categories("category01").
                   get())

        m.assert_called_once_with("GET",
                                  "https://test-api.swx.altairone.com/spaces/space01/categories/category01",
                                  headers={'Authorization': 'Bearer valid-token'},
                                  data=None,
                                  timeout=3)

        assert cat == Category.parse_obj(test_category01)
        assert type(cat) == Category

    def test_list(self):
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

        with mock.patch("api.api.requests.request", return_value=expected_resp) as m:
            cat = (API(host="test-api.swx.altairone.com").
                   token("valid-token").
                   spaces("space01").
                   categories().
                   get())

        m.assert_called_once_with("GET",
                                  "https://test-api.swx.altairone.com/spaces/space01/categories",
                                  headers={'Authorization': 'Bearer valid-token'},
                                  data=None,
                                  timeout=3)

        assert cat == CategoryList.parse_obj(expected_resp_payload)
        assert type(cat) == CategoryList
