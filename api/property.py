from dataclasses import dataclass, field
from typing import List

from .obj import APIObject


@dataclass
class Property(APIObject):
    name: str

    def get(self):
        stack = self._stack
        stack.push(self)
        return stack.build_url()

    def _build_partial_path(self):
        return f"/properties/{self.name}"


@dataclass
class Properties(APIObject):
    properties: List[Property] = field(default_factory=list)

    def get(self):
        stack = self._stack
        stack.push(self)
        return stack.build_url()

    def _build_partial_path(self):
        return f"/properties"
