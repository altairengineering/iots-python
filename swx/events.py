from dataclasses import dataclass
from typing import Union, overload

from .internal.pagination import handle_next_pagination
from .internal.resource import APIResource
from .models.anythingdb import (EventCreateRequest, EventListResponse,
                                EventResponse)


@dataclass
class Event(APIResource):
    event_name: str

    def create(self, event: Union[EventCreateRequest, dict], **kwargs) -> EventResponse:
        """
        Make a request to the server to create a new Event value.

        :param event: The information of the new Event value
            (e.g. `{"delay": {"input": 5}}`).
        :return: A :class:`~swx.models.anythingdb.EventResponse` instance with
                 the new Event value.
        """
        payload = event
        if isinstance(event, EventCreateRequest):
            payload = event.dict()
        return EventResponse.parse_obj(self._make_request("POST", payload, **kwargs).json())

    def get(self, **kwargs) -> EventListResponse:
        """
        Make a request to the server to get the history values of the Event.

        :return: A :class:`~swx.models.anythingdb.EventListResponse` instance
                 with the value of the Event.
        """
        ret = EventListResponse.parse_obj(self._make_request(**kwargs).json())
        handle_next_pagination(self.get, ret, **kwargs)
        return ret

    def _build_partial_path(self):
        return f"/events/{self.event_name}"


@dataclass
class EventValue(APIResource):
    event_id: str

    def get(self, **kwargs) -> EventResponse:
        """
        Make a request to the server to get the value of the Event.

        :return: A :class:`~swx.models.anythingdb.EventResponse` instance with
                 the value of the Event.
        """
        return EventResponse.parse_obj(self._make_request(**kwargs).json())

    def _build_partial_path(self):
        return "/" + self.event_id


@dataclass
class Events(APIResource):

    def get(self, **kwargs) -> EventListResponse:
        """
        Make a request to the server to list the value of all the Thing
        Events.

        :return: A :class:`~swx.models.anythingdb.EventListResponse` instance
                 with the values of all the Thing Events.
        """
        ret = EventListResponse.parse_obj(self._make_request(**kwargs).json())
        handle_next_pagination(self.get, ret, **kwargs)
        return ret

    def _build_partial_path(self):
        return "/events"


class _EventsMethod:
    """
    This class declares and implements the `events()` method.
    """

    @overload
    def events(self, event_name: str, event_id: str) -> EventValue:
        ...

    @overload
    def events(self, event_name: str) -> Event:
        ...

    @overload
    def events(self) -> Events:
        ...

    def events(self, event_name: str = None, event_id: str = None):
        if event_name is not None and event_id is not None:
            event = Event(event_name)._child_of(self)
            return EventValue(event_id)._child_of(event)
        elif event_name is not None:
            return Event(event_name)._child_of(self)
        else:
            return Events()._child_of(self)
