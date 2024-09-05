import json
from dataclasses import dataclass
from typing import Union, overload

from ..internal.resource import APIResource
from ..models import models


@dataclass
class Properties1(APIResource):
    property: str

    def update(self, value, **kwargs) -> Union[models.Property, models.ErrorResponse]:
        """
        Updates the value of a Thing Property.

        Query parameters:
         - `update_history` _(bool)_: Indicates whether the values should be stored in the Properties history.

        :param value: The new value of the Property.
        :return: The API response to the request.
        :rtype: Union[models.Property, models.ErrorResponse]
        """
        req = "{\"" + str(self._path_value('property')) + "\": " + json.dumps(value) + "}"

        req_content_types = [
            ("application/json", models.Property),
        ]

        resp = self._make_request("PUT", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.Property),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def get(self, **kwargs) -> Union[models.Property, models.ErrorResponse]:
        """
        Returns the value of a Thing Property.

        :return: The API response to the request.
        :rtype: Union[models.Property, models.ErrorResponse]
        """
        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.Property),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return f"/properties/{self.property}"


@dataclass
class Properties2(APIResource):

    def update(self, req: Union[models.Properties, dict], **kwargs) -> Union[models.Properties, models.ErrorResponse]:
        """
        Updates the values of one or more Properties of a Thing.

        Query parameters:
         - `update_history` _(bool)_: Indicates whether the values should be stored in the Properties history.

        :param req: Request payload.
        :type req: Union[models.Properties, dict]
        :return: The API response to the request.
        :rtype: Union[models.Properties, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.Properties),
        ]

        resp = self._make_request("PUT", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.Properties),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def get(self, **kwargs) -> Union[models.Properties, models.ErrorResponse]:
        """
        Returns all the Property values of a Thing.

        :return: The API response to the request.
        :rtype: Union[models.Properties, models.ErrorResponse]
        """
        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.Properties),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return "/properties"


class _PropertiesMethods:
    """
    This class declares and implements the `properties()` method.
    """

    @overload
    def properties(self, property: str) -> Properties1:
        ...

    @overload
    def properties(self) -> Properties2:
        ...

    def properties(self, property: str = None):
        if property is not None:
            return Properties1(property)._child_of(self)

        if property is None:
            return Properties2()._child_of(self)

        raise ValueError("Invalid parameters")
