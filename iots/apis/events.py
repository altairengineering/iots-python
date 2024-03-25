from dataclasses import dataclass
from typing import Union, overload

from ..internal.resource import APIResource
from ..models import models, primitives
from ..models.extensions.pagination import PaginationDescription


@dataclass
class Events1(APIResource):
    event_name: str
    event_id: str

    def get(self, **kwargs) -> Union[models.EventResponse, models.ErrorResponse]:
        """
        Returns a Thing Event resource.

        :return: The API response to the request.
        :rtype: Union[models.EventResponse, models.ErrorResponse]
        """
        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.EventResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def delete(self, **kwargs) -> primitives.NoResponse:
        """
        Deletes a Thing Event resource.

        :return: The API response to the request.
        :rtype: primitives.NoResponse
        """
        resp = self._make_request("DELETE", **kwargs)
        return self._handle_response(resp, [
            (204, "", primitives.NoResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return f"/events/{self.event_name}/{self.event_id}"


@dataclass
class Events2(APIResource):
    event_name: str

    def create(self, req: Union[models.EventCreateRequest, dict], **kwargs) -> Union[models.EventResponse, models.ErrorResponse]:
        """
        Creates a new Event resource for the given Thing's Event.

        :param req: Request payload.
        :type req: Union[models.EventCreateRequest, dict]
        :return: The API response to the request.
        :rtype: Union[models.EventResponse, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.EventCreateRequest),
        ]

        resp = self._make_request("POST", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.EventResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def get(self, **kwargs) -> Union[models.EventListResponse, models.ErrorResponse]:
        """
        Returns the list of Event resources of the given Thing's Event.

        > 🚧 **Limitations:** A maximum of 1000 Event resources will be returned
        > per page (50 by default).

        Query parameters:
         - `next_cursor` _(str)_: Cursor used to get the next page of results.
         - `previous_cursor` _(str)_: Cursor used to get the previous page of results.
         - `limit` _(int)_: The numbers of items to return.

        :return: The API response to the request.
        :rtype: Union[models.EventListResponse, models.ErrorResponse]
        """
        pagination_info = PaginationDescription.parse_obj({'reuse_previous_request': True, 'method': '', 'url': '', 'modifiers': [{'op': 'set', 'param': '$request.query.next_cursor', 'value': '$response.body#/paging/next_cursor'}], 'result': 'data', 'has_more': '$response.body#/paging/next_cursor'})

        param_types = {
            'query': {
                'next_cursor': str,
                'previous_cursor': str,
                'limit': int,
            },
        }

        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.EventListResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ], pagination_info=pagination_info, param_types=param_types)

    def _build_partial_path(self):
        return f"/events/{self.event_name}"


@dataclass
class Events3(APIResource):

    def get(self, **kwargs) -> Union[models.EventListResponse, models.ErrorResponse]:
        """
        Returns the list of Event resources of the given Thing.

        > 🚧 **Limitations:** A maximum of 1000 Event resources will be returned
        > per page (50 by default).

        Query parameters:
         - `next_cursor` _(str)_: Cursor used to get the next page of results.
         - `previous_cursor` _(str)_: Cursor used to get the previous page of results.
         - `limit` _(int)_: The numbers of items to return.

        :return: The API response to the request.
        :rtype: Union[models.EventListResponse, models.ErrorResponse]
        """
        pagination_info = PaginationDescription.parse_obj({'reuse_previous_request': True, 'method': '', 'url': '', 'modifiers': [{'op': 'set', 'param': '$request.query.next_cursor', 'value': '$response.body#/paging/next_cursor'}], 'result': 'data', 'has_more': '$response.body#/paging/next_cursor'})

        param_types = {
            'query': {
                'next_cursor': str,
                'previous_cursor': str,
                'limit': int,
            },
        }

        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.EventListResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ], pagination_info=pagination_info, param_types=param_types)

    def _build_partial_path(self):
        return "/events"


class _EventsMethods:
    """
    This class declares and implements the `events()` method.
    """

    @overload
    def events(self, event_name: str, event_id: str) -> Events1:
        ...

    @overload
    def events(self, event_name: str) -> Events2:
        ...

    @overload
    def events(self) -> Events3:
        ...

    def events(self, event_name: str = None, event_id: str = None):
        if event_name is not None  and event_id is not None :
            return Events1(event_name, event_id)._child_of(self)

        if event_name is not None :
            return Events2(event_name)._child_of(self)

        if event_name is None and event_id is None:
            return Events3()._child_of(self)

        raise ValueError("Invalid parameters")
