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
