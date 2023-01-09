import os
from unittest import TestCase

import pytest

from swx.api import API

TEST_API_HOST = "test-api.swx.altairone.com"


class TestAPI(TestCase):
    def test_create_successfully(self):
        """ Tests creating an API instance successfully. """
        api = API(host=TEST_API_HOST)
        assert api.host == TEST_API_HOST

    def test_default_host(self):
        """
        Tests creating an API instance taking the host from the default
        environment variable.
        """
        os.environ["SWX_API_URL"] = TEST_API_HOST
        api = API()
        assert api.host == TEST_API_HOST

    def test_missing_host(self):
        """
        Tests creating an API instance taking the host from the default
        environment variable.
        """
        os.environ.pop("SWX_API_URL")
        with pytest.raises(ValueError):
            API()
