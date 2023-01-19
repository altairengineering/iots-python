from dataclasses import dataclass
from typing import Union, overload

from .internal.resource import APIResource
from .models.anythingdb import (EventCreateRequest, EventListResponse,
                                EventResponse)


@dataclass
class Event(APIResource):
    event_name: str

    def create(self, event: Union[EventCreateRequest, dict]) -> EventResponse:
        """
        Make a request to the server to create a new Event value.

        :param event: The information of the new Event value
            (e.g. `{"delay": {"input": 5}}`).
        :return: A :class:`EventResponse` with the new Event value.
        """
        payload = event
        if isinstance(event, EventCreateRequest):
            payload = event.dict()
        return EventResponse.parse_obj(self._make_request("POST", payload).json())

    def get(self):
        """
        Make a request to the server to get the history values of the Event.

        :return: A :class:`EventListResponse` with the value of the Event.
        """
        return EventListResponse.parse_obj(self._make_request().json())

    def _build_partial_path(self):
        return f"/events/{self.event_name}"


@dataclass
class EventValue(APIResource):
    event_id: str

    def get(self) -> EventResponse:
        """
        Make a request to the server to get the value of the Event.

        :return: A :class:`EventResponse` with the value of the Event.
        """
        return EventResponse.parse_obj(self._make_request().json())

    def _build_partial_path(self):
        return "/" + self.event_id


@dataclass
class Events(APIResource):

    def get(self) -> EventListResponse:
        """
        Make a request to the server to list the value of all the Thing
        Events.

        :return: A :class:`EventListResponse` with the values of all the
            Thing Events.
        """
        return EventListResponse.parse_obj(self._make_request().json())

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
