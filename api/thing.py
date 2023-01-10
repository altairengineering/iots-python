from dataclasses import dataclass, field
from typing import List, overload

from .obj import APIObject
from .property import Property, Properties


@dataclass
class Thing(APIObject):
    thing_id: str

    @overload
    def properties(self, property_name: str) -> Property:
        ...

    @overload
    def properties(self) -> Properties:
        ...

    def properties(self, property_name: str = None):
        stack = self._stack
        stack.push(self)
        if property_name is None:
            return Properties()._with_stack(stack)
        else:
            return Property(property_name)._with_stack(stack)

    def _build_partial_path(self):
        return f"/things/{self.thing_id}"


@dataclass
class Things(APIObject):
    things: List[Thing] = field(default_factory=list)

    def _build_partial_path(self):
        return f"/things"
