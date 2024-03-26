from dataclasses import dataclass
from typing import overload

from ..internal.resource import APIResource
from .categories import _CategoriesMethods
from .things import _ThingsMethods


@dataclass
class Spaces1(APIResource, _CategoriesMethods, _ThingsMethods):
    space: str

    def _build_partial_path(self):
        return f"/spaces/{self.space}"


class _SpacesMethods:
    """
    This class declares and implements the `spaces()` method.
    """

    @overload
    def spaces(self, space: str) -> Spaces1:
        ...

    def spaces(self, space: str):
        return Spaces1(space)._child_of(self)

