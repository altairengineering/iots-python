from dataclasses import dataclass, field
from typing import List, overload

from .obj import APIObject
from .thing import Thing, Things


@dataclass
class Category(APIObject):
    name: str

    @overload
    def things(self, thing_id: str) -> Thing:
        ...

    @overload
    def things(self) -> Things:
        ...

    def things(self, thing_id: str = None):
        stack = self._stack
        stack.push(self)
        if thing_id is None:
            return Things()._with_stack(stack)
        else:
            return Thing(thing_id)._with_stack(stack)

    def _build_partial_path(self):
        return f"/categories/{self.name}"


@dataclass
class Categories(APIObject):
    categories: List[Category] = field(default_factory=list)

    def _build_partial_path(self):
        return f"/categories"
