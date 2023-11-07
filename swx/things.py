from dataclasses import dataclass
from typing import overload

from .actions import _ActionsMethod
from .events import _EventsMethod
from .internal.pagination import handle_next_pagination
from .internal.resource import APIResource
from .models import anythingdb as models
from .properties import _PropertiesMethod


@dataclass
class Thing(APIResource, _PropertiesMethod, _ActionsMethod, _EventsMethod):
    thing_id: str

    def get(self, **kwargs) -> models.Thing:
        """
        Make a request to the server to get the Thing info.

        :return: A :class:`~swx.models.anythingdb.Thing` instance with the
                 Thing info.
        """
        return models.Thing.parse_obj(self._make_request(**kwargs).json())

    def _build_partial_path(self):
        return f"/things/{self.thing_id}"


@dataclass
class Things(APIResource):

    def get(self, **kwargs) -> models.ThingList:
        """
        Make a request to the server to list the Things info.

        :return: A :class:`~swx.models.anythingdb.ThingList` instance with
                 the Things info.
        """
        ret = models.ThingList.parse_obj(self._make_request(**kwargs).json())

        # def next_func(resp, **kwargs_copy):
        #     if resp.paging.next_cursor:
        #         from copy import deepcopy
        #         kwargs2 = deepcopy(kwargs_copy)
        #         if 'params' not in kwargs2:
        #             kwargs2['params'] = {}
        #         kwargs2['params']['next_cursor'] = resp.paging.next_cursor
        #         return lambda: self.get(**kwargs2)
        #     return None
        #
        # ret._iter_func = next_func(ret, **kwargs)

        handle_next_pagination(self.get, ret, **kwargs)

        return ret

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
