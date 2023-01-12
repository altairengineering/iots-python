from dataclasses import dataclass, field
from typing import List, overload

from models.anythingdb import (Thing as ThingModel,
                               ThingList as ThingListModel)
from .actions import _ActionsMethod
from .obj import APIObject
from .properties import _PropertiesMethod


@dataclass
class Thing(APIObject, _PropertiesMethod, _ActionsMethod):
    thing_id: str

    def get(self) -> ThingModel:
        """
        Make a request to the server to get the Thing info.

        :return: A :class:`ThingModel` with the Thing info.
        """
        return ThingModel.parse_obj(self._make_request().json())

    def _build_partial_path(self):
        return f"/things/{self.thing_id}"


@dataclass
class Things(APIObject):
    things: List[Thing] = field(default_factory=list)

    def get(self) -> ThingListModel:
        """
        Make a request to the server to list the Things info.

        :return: A :class:`ThingListModel` with the Things info.
        """
        return ThingListModel.parse_obj(self._make_request().json())

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
