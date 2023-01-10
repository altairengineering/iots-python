from dataclasses import dataclass, field
from typing import List, overload

from .obj import APIObject
from .property import _PropertiesMethod

@dataclass
class Thing(APIObject, _PropertiesMethod):
    thing_id: str

    def _build_partial_path(self):
        return f"/things/{self.thing_id}"


@dataclass
class Things(APIObject):
    things: List[Thing] = field(default_factory=list)

    def _build_partial_path(self):
        return f"/things"


class _ThingsMethod:
    """
    This class declares and implements the `things()` method.
    """
    @overload
    def things(self, thing_id: str) -> Thing:
        ...

    @overload
    def things(self) -> Things:
        ...

    def things(self, thing_id: str = None):
        if thing_id is None:
            return Things()._child_of(self)
        else:
            return Thing(thing_id)._child_of(self)
