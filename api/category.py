from dataclasses import dataclass, field
from typing import List, overload

from .obj import APIObject
from .thing import _ThingsMethod


@dataclass
class Category(APIObject, _ThingsMethod):
    name: str

    def _build_partial_path(self):
        return f"/categories/{self.name}"


@dataclass
class Categories(APIObject):
    categories: List[Category] = field(default_factory=list)

    def _build_partial_path(self):
        return f"/categories"


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
