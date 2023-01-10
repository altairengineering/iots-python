from dataclasses import dataclass, field
from typing import List, overload

from .obj import APIObject
from models.property import PropertiesResp


@dataclass
class Property(APIObject):
    name: str

    def get(self) -> PropertiesResp:
        return PropertiesResp(self._make_request().json())

    def _build_partial_path(self):
        return f"/properties/{self.name}"


@dataclass
class Properties(APIObject):
    properties: List[Property] = field(default_factory=list)

    def get(self):
        return self.build_url()

    def _build_partial_path(self):
        return f"/properties"


class _PropertiesMethod:
    """
    This class declares and implements the `properties()` method.
    """

    @overload
    def properties(self, property_name: str) -> Property:
        ...

    @overload
    def properties(self) -> Properties:
        ...

    def properties(self, property_name: str = None):
        if property_name is None:
            return Properties()._child_of(self)
        else:
            return Property(property_name)._child_of(self)
