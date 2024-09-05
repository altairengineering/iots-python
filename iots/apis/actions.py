from dataclasses import dataclass
from typing import Union, overload

from ..internal.resource import APIResource
from ..models import models, primitives
from ..models.extensions.pagination import PaginationDescription


@dataclass
class Actions1(APIResource):
    action_name: str
    action_id: str

    def get(self, **kwargs) -> Union[models.ActionResponse, models.ErrorResponse]:
        """
        Returns a Thing Action resource.

        :return: The API response to the request.
        :rtype: Union[models.ActionResponse, models.ErrorResponse]
        """
        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.ActionResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def update(self, req: Union[models.ActionUpdateRequest, dict], **kwargs) -> Union[models.ActionResponse, models.ErrorResponse]:
        """
        Updates a Thing Action resource.

        :param req: Request payload.
        :type req: Union[models.ActionUpdateRequest, dict]
        :return: The API response to the request.
        :rtype: Union[models.ActionResponse, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.ActionUpdateRequest),
        ]

        resp = self._make_request("PUT", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.ActionResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def delete(self, **kwargs) -> primitives.NoResponse:
        """
        Deletes a Thing Action resource.

        :return: The API response to the request.
        :rtype: primitives.NoResponse
        """
        resp = self._make_request("DELETE", **kwargs)
        return self._handle_response(resp, [
            (204, "", primitives.NoResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return f"/actions/{self.action_name}/{self.action_id}"


@dataclass
class Actions2(APIResource):
    action_name: str

    def create(self, req: Union[models.ActionCreateRequest, dict], **kwargs) -> Union[models.ActionResponse, models.ErrorResponse]:
        """
        Creates a new Action resource for the given Thing's Action.

        > 🚧 **Limitations:** A maximum of 100 Action resources will be stored.

        :param req: Request payload.
        :type req: Union[models.ActionCreateRequest, dict]
        :return: The API response to the request.
        :rtype: Union[models.ActionResponse, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.ActionCreateRequest),
        ]

        resp = self._make_request("POST", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.ActionResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def get(self, **kwargs) -> Union[models.ActionListResponse, models.ErrorResponse]:
        """
        Returns the list of Action resources of the given Thing's Action.

        > 🚧 **Limitations:** A maximum of 100 Action resources will be stored and returned
        > (50 by default per page).

        Query parameters:
         - `next_cursor` _(str)_: Cursor used to get the next page of results.
         - `previous_cursor` _(str)_: Cursor used to get the previous page of results.
         - `limit` _(int)_: The numbers of items to return.

        :return: The API response to the request.
        :rtype: Union[models.ActionListResponse, models.ErrorResponse]
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
            (200, "application/json", models.ActionListResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ], pagination_info=pagination_info, param_types=param_types)

    def _build_partial_path(self):
        return f"/actions/{self.action_name}"


@dataclass
class Actions3(APIResource):

    def get(self, **kwargs) -> Union[models.ActionListResponse, models.ErrorResponse]:
        """
        Returns the list of Action resources of the given Thing.

        > 🚧 **Limitations:** A maximum of 100 Action resources per Action will be stored and returned
        > (50 by default per page).

        Query parameters:
         - `next_cursor` _(str)_: Cursor used to get the next page of results.
         - `previous_cursor` _(str)_: Cursor used to get the previous page of results.
         - `limit` _(int)_: The numbers of items to return.

        :return: The API response to the request.
        :rtype: Union[models.ActionListResponse, models.ErrorResponse]
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
            (200, "application/json", models.ActionListResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ], pagination_info=pagination_info, param_types=param_types)

    def _build_partial_path(self):
        return "/actions"


class _ActionsMethods:
    """
    This class declares and implements the `actions()` method.
    """

    @overload
    def actions(self, action_name: str, action_id: str) -> Actions1:
        ...

    @overload
    def actions(self, action_name: str) -> Actions2:
        ...

    @overload
    def actions(self) -> Actions3:
        ...

    def actions(self, action_name: str = None, action_id: str = None):
        if action_name is not None and action_id is not None:
            return Actions1(action_name, action_id)._child_of(self)

        if action_name is not None:
            return Actions2(action_name)._child_of(self)

        if action_name is None and action_id is None:
            return Actions3()._child_of(self)

        raise ValueError("Invalid parameters")
