from dataclasses import dataclass
from typing import Union, overload

from ..internal.resource import APIResource
from ..models import models, primitives
from ..models.extensions.pagination import PaginationDescription


@dataclass
class PropertiesHistory1(APIResource):
    property: str

    def create(self, req: models.CreatePropertyHistoryValuesRequest, **kwargs) -> Union[models.PropertyHistoryValues, models.ErrorResponse]:
        """
        Adds one or more historical values for the given Thing Property.

        :param req: Request payload.
        :type req: models.CreatePropertyHistoryValuesRequest
        :return: The API response to the request.
        :rtype: Union[models.PropertyHistoryValues, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.CreatePropertyHistoryValuesRequest),
        ]

        resp = self._make_request("POST", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.PropertyHistoryValues),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (409, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def get(self, **kwargs) -> Union[models.PropertyHistoryValueList, models.ErrorResponse]:
        """
        Returns the list of historical values of the given Thing Property.

        > 🚧 **Limitations:** A maximum of 1000 values will be returned
        > per page (50 by default).

        Query parameters:
         - `at` _(str)_: This parameter can be used as a datetime or as a datetime range value.

           Using a date-time value:
            - This allows to get the Property value(s) that a Thing had with the
              date and time indicated. <br>Example: *2022-05-31T01:23:45Z*

              The result will include the last values of all the Thing Properties
              that have a timestamp equal to the `at` value.
              If there are Properties without that timestamp, the older dates closer to this one will be returned.

           Using a date-time range:
            - This allows to get the Property value(s) that a Thing had in a datetime
              range, using the `|` separator to specify start and end date-times.
              > **Example**: *2022-08-01T00:00:00Z|2022-09-01T00:00:00Z*

              Using short notation for years, months, and days is also allowed.
              > **Example**: *2022|2023* or *2022-12|2023-03* or *2023-05-15|2023-05-30*
         - `next_cursor` _(str)_: Cursor used to get the next page of results.
         - `previous_cursor` _(str)_: Cursor used to get the previous page of results.
         - `limit` _(int)_: The numbers of items to return.

        :return: The API response to the request.
        :rtype: Union[models.PropertyHistoryValueList, models.ErrorResponse]
        """
        pagination_info = PaginationDescription.parse_obj({'reuse_previous_request': True, 'method': '', 'url': '', 'modifiers': [{'op': 'set', 'param': '$request.query.next_cursor', 'value': '$response.body#/paging/next_cursor'}], 'result': 'data', 'has_more': '$response.body#/paging/next_cursor'})

        param_types = {
            'query': {
                'at': str,
                'next_cursor': str,
                'previous_cursor': str,
                'limit': int,
            },
        }

        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.PropertyHistoryValueList),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ], pagination_info=pagination_info, param_types=param_types)

    def delete(self, **kwargs) -> primitives.NoResponse:
        """
        Deletes historical values of a Thing Property.

        > 📘 **Information:** To prevent accidental deletions, the operation
        > will fail if no filters are provided.

        > ⚠️ **Warning:** This operation can remove lots of information in one go and
        > without asking for confirmation, so make sure you know what you are doing!

        Query parameters:
         - `at` _(str)_: This parameter can be used as a datetime or as a datetime range value.

           Using a date-time value:
            - This allows to delete the Property value(s) that a Thing had with the
              date and time indicated. <br>Example: *2022-05-31T01:23:45Z*

              This will delete the last values of all the Thing Properties
              that have a timestamp equal to the `at` value.
              If there are Properties without that timestamp, the older dates closer to this one will *NOT* be deleted.

           Using a date-time range:
            - This allows to delete the Property value(s) that a Thing had in a datetime
              range, using the `|` separator to specify start and end date-times.
              > **Example**: *2022-08-01T00:00:00Z|2022-09-01T00:00:00Z*

              Using short notation for years, months, and days is also allowed.
              > **Example**: *2022|2023* or *2022-12|2023-03* or *2023-05-15|2023-05-30*

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
        return f"/properties-history/{self.property}"


@dataclass
class PropertiesHistory2(APIResource):

    def create(self, req: models.CreatePropertiesHistoryValuesRequest, **kwargs) -> Union[models.PropertyHistoryValues, models.ErrorResponse]:
        """
        Adds historical values for one or more Properties of a Thing.

        :param req: Request payload.
        :type req: models.CreatePropertiesHistoryValuesRequest
        :return: The API response to the request.
        :rtype: Union[models.PropertyHistoryValues, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.CreatePropertiesHistoryValuesRequest),
        ]

        resp = self._make_request("POST", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.PropertyHistoryValues),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (409, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def get(self, **kwargs) -> Union[models.PropertyHistoryValueList, models.ErrorResponse]:
        """
        Returns the list of historical Properties values of a Thing.

        > 🚧 **Limitations:** A maximum of 1000 values will be returned
        > per page (50 by default).

        Query parameters:
         - `at` _(str)_: This parameter can be used as a datetime or as a datetime range value.

           Using a date-time value:
            - This allows to get the Property value(s) that a Thing had with the
              date and time indicated. <br>Example: *2022-05-31T01:23:45Z*

              The result will include the last values of all the Thing Properties
              that have a timestamp equal to the `at` value.
              If there are Properties without that timestamp, the older dates closer to this one will be returned.

           Using a date-time range:
            - This allows to get the Property value(s) that a Thing had in a datetime
              range, using the `|` separator to specify start and end date-times.
              > **Example**: *2022-08-01T00:00:00Z|2022-09-01T00:00:00Z*

              Using short notation for years, months, and days is also allowed.
              > **Example**: *2022|2023* or *2022-12|2023-03* or *2023-05-15|2023-05-30*
         - `group` _(bool)_: This parameter controls the format of the returned values.
           - If `false` (default), one item will be returned for each history value.
           - If `true`, the history values will be returned grouped by their timestamp.
           This means that if two or more values have the same timestamp, they will
           be returned in a single item.
         - `next_cursor` _(str)_: Cursor used to get the next page of results.
         - `previous_cursor` _(str)_: Cursor used to get the previous page of results.
         - `limit` _(int)_: The numbers of items to return.

        :return: The API response to the request.
        :rtype: Union[models.PropertyHistoryValueList, models.ErrorResponse]
        """
        pagination_info = PaginationDescription.parse_obj({'reuse_previous_request': True, 'method': '', 'url': '', 'modifiers': [{'op': 'set', 'param': '$request.query.next_cursor', 'value': '$response.body#/paging/next_cursor'}], 'result': 'data', 'has_more': '$response.body#/paging/next_cursor'})

        param_types = {
            'query': {
                'at': str,
                'group': bool,
                'next_cursor': str,
                'previous_cursor': str,
                'limit': int,
            },
        }

        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.PropertyHistoryValueList),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ], pagination_info=pagination_info, param_types=param_types)

    def delete(self, **kwargs) -> primitives.NoResponse:
        """
        Deletes historical Properties values of a Thing.

        > 📘 **Information:** To prevent accidental deletions, the operation
        > will fail if no filters are provided.

        > ⚠️ **Warning:** This operation can remove lots of information in one go and
        > without asking for confirmation, so make sure you know what you are doing!

        Query parameters:
         - `at` _(str)_: This parameter can be used as a datetime or as a datetime range value.

           Using a date-time value:
            - This allows to delete the Property value(s) that a Thing had with the
              date and time indicated. <br>Example: *2022-05-31T01:23:45Z*

              This will delete the last values of all the Thing Properties
              that have a timestamp equal to the `at` value.
              If there are Properties without that timestamp, the older dates closer to this one will *NOT* be deleted.

           Using a date-time range:
            - This allows to delete the Property value(s) that a Thing had in a datetime
              range, using the `|` separator to specify start and end date-times.
              > **Example**: *2022-08-01T00:00:00Z|2022-09-01T00:00:00Z*

              Using short notation for years, months, and days is also allowed.
              > **Example**: *2022|2023* or *2022-12|2023-03* or *2023-05-15|2023-05-30*
         - `property_name[]` _(list)_: Filter by multiple Property names.

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
        return "/properties-history"


class _PropertiesHistoryMethods:
    """
    This class declares and implements the `properties-history()` method.
    """

    @overload
    def properties_history(self, property: str) -> PropertiesHistory1:
        ...

    @overload
    def properties_history(self) -> PropertiesHistory2:
        ...

    def properties_history(self, property: str = None):
        if property is not None :
            return PropertiesHistory1(property)._child_of(self)

        if property is None:
            return PropertiesHistory2()._child_of(self)

        raise ValueError("Invalid parameters")
