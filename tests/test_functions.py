from unittest import mock, TestCase
from requests import Response
import functions as api
from errors import ResponseError

token_mocked = mock.Mock(host="https://api.swx.mock")

thing_mocked = mock.Mock(id="01FKGJCB21CSBGQW000000S1T1")
thing_mocked_without_id = mock.Mock(id="")


class TestThings(TestCase):
    def test_get_single_thing(self):
        resp = Response()
        resp.status_code = 200
        with mock.patch("functions.get_info", return_value=resp):
            thing = api.Things(token_mocked, "space01", "", "01FKGJCB21CSBGQW000000S1T1").get()
        assert thing == resp

    def test_get_multiple_things(self):
        resp = Response()
        resp.status_code = 200
        with mock.patch("functions.get_info", return_value=resp):
            thing = api.Things(token_mocked, "space01", "").get()
        assert thing == resp


class TestProperties(TestCase):

    def test_get_property(self):
        resp = Response()
        resp.status_code = 200
        with mock.patch("functions.get_info", return_value=resp):
            with mock.patch("functions.generate_thing_url", return_value="https://api.swx.mock/spaces/space01/things/01FKGJCB21CSBGQW000000S1T1"):
                properties = api.Properties(thing_mocked).get()
        assert properties == resp

    def test_get_property_without_thing_id(self):
        resp = ResponseError(400, "Cannot recover Properties info, ThingID is missing")
        with mock.patch("functions.get_info", return_value=resp):
            properties = api.Properties(thing_mocked_without_id).get()
        assert properties.status_code == resp.status_code

    def test_update_property(self):
        resp = Response()
        resp.status_code = 204
        with mock.patch("functions.post_info", return_value=resp):
            with mock.patch("functions.generate_thing_url", return_value="https://api.swx.mock/spaces/space01/things/01FKGJCB21CSBGQW000000S1T1"):
                properties = api.Properties(thing_mocked, "cpu").update(21)
        assert properties == resp

    def test_update_property_without_thing_id(self):
        resp = ResponseError(400, "Cannot update Properties, ThingID is missing")
        with mock.patch("functions.get_info", return_value=resp):
            properties = api.Properties(thing_mocked_without_id).update({"cpu": 33, "disk": 55})
        assert properties.status_code == resp.status_code
