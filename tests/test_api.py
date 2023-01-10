import os
from unittest import TestCase

import pytest
from api.api import API


class TestAPI(TestCase):
    def test_create_successfully(self):
        """ Tests creating an API instance successfully. """
        api = API(host="test-api.swx.altairone.com")
        assert api.host == "https://test-api.swx.altairone.com"

    def test_default_host(self):
        """
        Tests creating an API instance taking the host from the default
        environment variable.
        """
        os.environ["SWX_API_URL"] = "https://test-api.swx.altairone.com"
        api = API()
        assert api.host == "https://test-api.swx.altairone.com"

    def test_missing_host(self):
        """
        Tests creating an API instance taking the host from the default
        environment variable.
        """
        os.environ.pop("SWX_API_URL")
        with pytest.raises(ValueError):
            API()


class TestAPIObject(TestCase):
    def test_build_url(self):
        api = API(host="test-api.swx.altairone.com")
        prop = api.categories("cat01").things("thing01").properties("temperature")

        assert prop.build_url() == "https://test-api.swx.altairone.com" \
                                   "/categories/cat01/things/thing01/properties/temperature"

    def test_build_path(self):
        api = API(host="test-api.swx.altairone.com")

        cat = api.categories("cat01")
        thing1 = cat.things("thing01")
        thing2 = cat.things("thing02")
        prop_thing1 = thing1.properties("temperature")
        prop_thing2 = thing2.properties("humidity")

        assert cat.build_path() == "/categories/cat01"
        assert thing1.build_path() == "/categories/cat01/things/thing01"
        assert thing2.build_path() == "/categories/cat01/things/thing02"
        assert prop_thing1.build_path() == "/categories/cat01/things/thing01/properties/temperature"
        assert prop_thing2.build_path() == "/categories/cat01/things/thing02/properties/humidity"
        assert api.things("thing01").build_path() == "/things/thing01"
        assert api.categories().build_path() == "/categories"
        assert api.things().build_path() == "/things"
        assert thing1.properties().build_path() == "/categories/cat01/things/thing01/properties"
