from dataclasses import dataclass
from typing import Union, overload

from ..internal.resource import APIResource
from ..models import models, primitives
from ..models.extensions.pagination import PaginationDescription
from .things import _ThingsMethods


@dataclass
class Categories1(APIResource, _ThingsMethods):
    category_name: str

    def get(self, **kwargs) -> Union[models.Category, models.ErrorResponse]:
        """
        Returns the Category information.

        :return: The API response to the request.
        :rtype: Union[models.Category, models.ErrorResponse]
        """
        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.Category),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def update(self, req: models.CategoryUpdate, **kwargs) -> Union[models.Category, models.ErrorResponse]:
        """
        Updates a Category.

        > 🚧 **Limitations:** A Category cannot currently be renamed.

        :param req: Request payload.
        :type req: models.CategoryUpdate
        :return: The API response to the request.
        :rtype: Union[models.Category, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.CategoryUpdate),
        ]

        resp = self._make_request("PUT", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.Category),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (409, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def delete(self, **kwargs) -> primitives.NoResponse:
        """
        Deletes a Category.

        > 📘 **Information:** The Things inside the Category will not be removed.
        > They simply no longer belong to the deleted Category.

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
        return f"/categories/{self.category_name}"


@dataclass
class Categories2(APIResource):

    def create(self, req: models.CategoryCreate, **kwargs) -> Union[models.Category, models.ErrorResponse]:
        """
        Creates a new Category in the Space.

        > 🚧 **Limitations:** A Category cannot currently be renamed.

        :param req: Request payload.
        :type req: models.CategoryCreate
        :return: The API response to the request.
        :rtype: Union[models.Category, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.CategoryCreate),
        ]

        resp = self._make_request("POST", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.Category),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (409, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def get(self, **kwargs) -> Union[models.CategoryList, models.ErrorResponse]:
        """
        Returns the list of Categories in a Space.

        > 🚧 **Limitations:** A maximum of 1000 Categories will be returned per
        > page (50 by default).

        Query parameters:
         - `next_cursor` _(str)_: Cursor used to get the next page of results.
         - `previous_cursor` _(str)_: Cursor used to get the previous page of results.
         - `limit` _(int)_: The numbers of items to return.

        :return: The API response to the request.
        :rtype: Union[models.CategoryList, models.ErrorResponse]
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
            (200, "application/json", models.CategoryList),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ], pagination_info=pagination_info, param_types=param_types)

    def _build_partial_path(self):
        return "/categories"


class _CategoriesMethods:
    """
    This class declares and implements the `categories()` method.
    """

    @overload
    def categories(self, category_name: str) -> Categories1:
        ...

    @overload
    def categories(self) -> Categories2:
        ...

    def categories(self, category_name: str = None):
        if category_name is not None:
            return Categories1(category_name)._child_of(self)

        if category_name is None:
            return Categories2()._child_of(self)

        raise ValueError("Invalid parameters")
