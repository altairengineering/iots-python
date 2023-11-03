from dataclasses import dataclass
from typing import overload

from .internal.resource import APIResource
from .models import anythingdb as models
from .things import _ThingsMethod


@dataclass
class Category(APIResource, _ThingsMethod):
    name: str

    def get(self, **kwargs) -> models.Category:
        """
        Make a request to the server to get the Category info.

        :return: A :class:`~swx.models.anythingdb.Category` instance with
                 the Category info.
        """
        return models.Category.parse_obj(self._make_request(**kwargs).json())

    def _build_partial_path(self):
        return f"/categories/{self.name}"


@dataclass
class Categories(APIResource):

    def get(self, **kwargs) -> models.CategoryList:
        """
        Make a request to the server to list the Categories info.

        :return: A :class:`~swx.models.anythingdb.CategoryList` instance with
                 the Categories info.
        """
        return models.CategoryList.parse_obj(self._make_request(**kwargs).json())

    def _build_partial_path(self):
        return "/categories"


class _CategoriesMethod:
    """
    This class declares and implements the `categories()` method.
    """

    @overload
    def categories(self, property_name: str) -> Category:
        ...

    @overload
    def categories(self) -> Categories:
        ...

    def categories(self, property_name: str = None):
        if property_name is None:
            return Categories()._child_of(self)
        else:
            return Category(property_name)._child_of(self)
