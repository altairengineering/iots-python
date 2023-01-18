from dataclasses import dataclass, field
from typing import List, overload

from .actions import _ActionsMethod
from .events import _EventsMethod
from .models.anythingdb import Thing as ThingModel
from .models.anythingdb import ThingList as ThingListModel
from .internal.resource import APIResource
from .properties import _PropertiesMethod


@dataclass
class Thing(APIResource, _PropertiesMethod, _ActionsMethod, _EventsMethod):
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
class Things(APIResource):
    things: List[Thing] = field(default_factory=list)

    def get(self) -> ThingListModel:
        """
        Make a request to the server to list the Things info.

        :return: A :class:`ThingListModel` with the Things info.
        """
        return ThingListModel.parse_obj(self._make_request().json())

    def _build_partial_path(self):
        return "/things"


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
