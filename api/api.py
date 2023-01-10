import os

from .obj import APIObject
from .category import Category, Categories
from .category import Thing, Things


def get_host():
    """
    Returns the default SmartWorks host URL from the `SWX_API_URL` environment
    variable. If the variable is not found, None is returned.
    """
    return os.getenv("SWX_API_URL")


class API:
    """
    This is the top-level class used as an abstraction of the SmartWorks API.
    """

    def __init__(self, host: str = ""):
        host = host if host else get_host()
        if not host:
            raise ValueError("empty host")

        if not host.startswith("http://") and not host.startswith("https://"):
            host = "https://" + host
        self.host = host

    def category(self, name: str) -> Category:
        return self._get(Category(name))

    def categories(self) -> Categories:
        return self._get(Categories())

    def thing(self, thing_id: str) -> Thing:
        return self._get(Thing(thing_id))

    def things(self) -> Things:
        return self._get(Things())

    def _get(self, obj: APIObject):
        return obj._with_stack([self])
