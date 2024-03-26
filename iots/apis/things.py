from dataclasses import dataclass
from typing import Union, overload

from ..internal.resource import APIResource
from ..models import models, primitives
from ..models.extensions.pagination import PaginationDescription
from .actions import _ActionsMethods
from .events import _EventsMethods
from .properties import _PropertiesMethods


@dataclass
class Things1(APIResource, _ActionsMethods, _EventsMethods, _PropertiesMethods):
    thing_id: str

    def get(self, **kwargs) -> Union[models.Thing, models.ErrorResponse]:
        """
        Returns the Thing with the given ID.

        :return: The API response to the request.
        :rtype: Union[models.Thing, models.ErrorResponse]
        """
        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.Thing),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def update(self, req: models.ThingUpdate, **kwargs) -> Union[models.Thing, models.ErrorResponse]:
        """
        Updates the Thing with the given ID.

        :param req: Request payload.
        :type req: models.ThingUpdate
        :return: The API response to the request.
        :rtype: Union[models.Thing, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.ThingUpdate),
        ]

        resp = self._make_request("PUT", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.Thing),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def delete(self, **kwargs) -> primitives.NoResponse:
        """
        Deletes the Thing with the given ID and all its related information
        (Properties history, graph relationships...).

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
        return f"/things/{self.thing_id}"


@dataclass
class Things2(APIResource):

    def create(self, req: models.ThingCreate, **kwargs) -> Union[models.Thing, models.ErrorResponse]:
        """
        Creates a new Thing inside a Space according to the
        [WoT specification](https://www.w3.org/TR/wot-thing-description/#thing).

        :param req: Request payload.
        :type req: models.ThingCreate
        :return: The API response to the request.
        :rtype: Union[models.Thing, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.ThingCreate),
        ]

        resp = self._make_request("POST", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.Thing),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def get(self, **kwargs) -> Union[models.ThingList, models.ErrorResponse]:
        """
        Returns the list of Things.

        Filters can be applied to return only the Things that match some criteria.

        > 🚧 **Limitations:** A maximum of 1000 Things will be returned
        > per page (50 by default).

        Query parameters:
         - `title` _(str)_: Filter by title.
         - `@type` _(str)_: Filter by `@type`.
         - `model` _(str)_: Filter by Model name.
         - `version` _(int)_: Filter by Version number. `model` query parameter must be also present.
         - `thingID[]` _(list)_: Filter by multiple Thing IDs.
         - `category[]` _(list)_: Filter by multiple Category names.
         - `in_category` _(bool)_: If `true`, only Things within some Category will be listed. If `false`, only Things not associated to any Category will be listed. If omitted, all Things will be listed.
         - `sort` _(list)_: Sort items by one or more fields in any order.

           For example, using `sort=uid,+title,-created` will return the results
           ordered by ascending `uid`, ascending `title` and descending `created`
           (having `uid` the highest priority and `created` the lowest).
         - `property` _(dict)_: This parameter adds a condition on the value of a Thing Property.
           Only the Things that meet this criteria will satisfy this filter.

           **Example:** given the query parameters `?property:temp=gt:20&property:dim=80`,
           a Thing will only match it if it has a `temp` Property with a value
           greater than 20 and a `dim` Property with a value equal to 80.

           The format of this query parameter is:

               property:<property_name>=<operator>:<value>

           Multiple parameters following the previous format can be used in the
           same request to set multiple conditions. Note that a Thing must meet all
           the given conditions to match.

           Supported value operators:
             * `eq`  → Equal (`==`). This is the default operator.
             * `neq` → Not equal (`!=`)
             * `gt`  → Greater than (`>`)
             * `gte` → Greater than or equal to (`>=`)
             * `lt`  → Less than (`<`)
             * `lte` → Less than or equal to (`<=`)

           Supported functions:
             * `contains` → Check whether the value is contained in the Property
               value (the Property must be an array, string or object).

               **Notes**:
                 * The string matching performed is case-sensitive.
                 * If the Property type is string, the `>`, `>=`, `<` and `<=`
                   operators will compare the values alphabetically.
                 * If the Property type is not an array, string or object, the
                   Thing will not satisfy the condition.
                 * If the Property type is an object, it will check whether an
                   attribute with the given name is present in it.
         - `links.rel` _(str)_: Filter by type of link relationship (`rel`).
         - `links.href` _(str)_: Filter by link `href`.
         - `next_cursor` _(str)_: Cursor used to get the next page of results.
         - `previous_cursor` _(str)_: Cursor used to get the previous page of results.
         - `limit` _(int)_: The numbers of items to return.

        :return: The API response to the request.
        :rtype: Union[models.ThingList, models.ErrorResponse]
        """
        pagination_info = PaginationDescription.parse_obj({'reuse_previous_request': True, 'method': '', 'url': '', 'modifiers': [{'op': 'set', 'param': '$request.query.next_cursor', 'value': '$response.body#/paging/next_cursor'}], 'result': 'data', 'has_more': '$response.body#/paging/next_cursor'})

        param_types = {
            'query': {
                'title': str,
                '@type': str,
                'model': str,
                'version': int,
                'thingID[]': list,
                'category[]': list,
                'in_category': bool,
                'sort': list,
                'property': dict,
                'links.rel': str,
                'links.href': str,
                'next_cursor': str,
                'previous_cursor': str,
                'limit': int,
            },
        }

        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.ThingList),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ], pagination_info=pagination_info, param_types=param_types)

    def delete(self, **kwargs) -> Union[models.ThingsDeleted, models.ErrorResponse]:
        """
        Deletes all the existing information (Things and history) from all the
        Things matching the given filters.

        > 📘 **Information:** To prevent accidental deletions, the operation
        > will fail if no filters are provided.

        > ⚠️ **Warning:** This operation can remove lots of Things in one go and
        > without asking for confirmation, so make sure you know what you are doing!

        Query parameters:
         - `@type` _(str)_: Filter by `@type`.
         - `thingID[]` _(list)_: Filter by multiple Thing IDs.
         - `category[]` _(list)_: Filter by multiple Category names.
         - `property` _(dict)_: This parameter adds a condition on the value of a Thing Property.
           Only the Things that meet this criteria will satisfy this filter.

           **Example:** given the query parameters `?property:temp=gt:20&property:dim=80`,
           a Thing will only match it if it has a `temp` Property with a value
           greater than 20 and a `dim` Property with a value equal to 80.

           The format of this query parameter is:

               property:<property_name>=<operator>:<value>

           Multiple parameters following the previous format can be used in the
           same request to set multiple conditions. Note that a Thing must meet all
           the given conditions to match.

           Supported value operators:
             * `eq`  → Equal (`==`). This is the default operator.
             * `neq` → Not equal (`!=`)
             * `gt`  → Greater than (`>`)
             * `gte` → Greater than or equal to (`>=`)
             * `lt`  → Less than (`<`)
             * `lte` → Less than or equal to (`<=`)

           Supported functions:
             * `contains` → Check whether the value is contained in the Property
               value (the Property must be an array, string or object).

               **Notes**:
                 * The string matching performed is case-sensitive.
                 * If the Property type is string, the `>`, `>=`, `<` and `<=`
                   operators will compare the values alphabetically.
                 * If the Property type is not an array, string or object, the
                   Thing will not satisfy the condition.
                 * If the Property type is an object, it will check whether an
                   attribute with the given name is present in it.

        :return: The API response to the request.
        :rtype: Union[models.ThingsDeleted, models.ErrorResponse]
        """
        resp = self._make_request("DELETE", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.ThingsDeleted),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return "/things"


class _ThingsMethods:
    """
    This class declares and implements the `things()` method.
    """

    @overload
    def things(self, thing_id: str) -> Things1:
        ...

    @overload
    def things(self) -> Things2:
        ...

    def things(self, thing_id: str = None):
        if thing_id is not None :
            return Things1(thing_id)._child_of(self)

        if thing_id is None:
            return Things2()._child_of(self)

        raise ValueError("Invalid parameters")
