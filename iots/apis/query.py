from dataclasses import dataclass
from typing import overload

from ..internal.resource import APIResource
from .cursor import _CursorMethods


@dataclass
class Query1(APIResource, _CursorMethods):

    def _build_partial_path(self):
        return "/query"


class _QueryMethods:
    """
    This class declares and implements the `query()` method.
    """

    @overload
    def query(self) -> Query1:
        ...

    def query(self):
        return Query1()._child_of(self)

