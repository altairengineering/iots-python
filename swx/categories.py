from dataclasses import dataclass, field
from typing import List, overload

from .models.anythingdb import Category as CategoryModel
from .models.anythingdb import CategoryList as CategoryListModel
from .obj import APIObject
from .things import _ThingsMethod


@dataclass
class Category(APIObject, _ThingsMethod):
    name: str

    def get(self) -> CategoryModel:
        """
        Make a request to the server to get the Category info.

        :return: A :class:`CategoryModel` with the Category info.
        """
        return CategoryModel.parse_obj(self._make_request().json())

    def _build_partial_path(self):
        return f"/categories/{self.name}"


@dataclass
class Categories(APIObject):
    categories: List[Category] = field(default_factory=list)

    def get(self) -> CategoryListModel:
        """
        Make a request to the server to list the Categories info.

        :return: A :class:`CategoryListModel` with the Categories info.
        """
        return CategoryListModel.parse_obj(self._make_request().json())

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
