from dataclasses import dataclass
from typing import Union, overload

from ..internal.resource import APIResource
from ..models import models


@dataclass
class Versions1(APIResource):
    version_num: int

    def get(self, **kwargs) -> Union[models.ModelVersion, models.ErrorResponse]:
        """
        Returns a Model-Version.

        :return: The API response to the request.
        :rtype: Union[models.ModelVersion, models.ErrorResponse]
        """
        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.ModelVersion),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return f"/versions/{self.version_num}"


@dataclass
class Versions2(APIResource):

    def post(self, req: models.ModelVersionCreate, **kwargs) -> Union[models.ModelVersion, models.ErrorResponse]:
        """
        Creates a new Version of a Model inside a Space.

        > 📘 **Information:** The Version identifier will be a number that
        > starts with 1 and is automatically incremented for every new Model-Version.

        > 🚧 **Limitations:** Once a Version is created, it cannot be updated or deleted.

        :param req: Request payload.
        :type req: models.ModelVersionCreate
        :return: The API response to the request.
        :rtype: Union[models.ModelVersion, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.ModelVersionCreate),
        ]

        resp = self._make_request("POST", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.ModelVersion),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def get(self, **kwargs) -> Union[models.ModelVersionList, models.ErrorResponse]:
        """
        Returns the list of Versions of a Model.

        > 🚧 **Limitations:** A maximum of 1000 Model-Versions will be returned
        > per page (50 by default).

        Query parameters:
         - `next_cursor` _(str)_: Cursor used to get the next page of results.
         - `previous_cursor` _(str)_: Cursor used to get the previous page of results.
         - `limit` _(int)_: The numbers of items to return.

        :return: The API response to the request.
        :rtype: Union[models.ModelVersionList, models.ErrorResponse]
        """
        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.ModelVersionList),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return "/versions"


class _VersionsMethods:
    """
    This class declares and implements the `versions()` method.
    """

    @overload
    def versions(self, version_num: int) -> Versions1:
        ...

    @overload
    def versions(self) -> Versions2:
        ...

    def versions(self, version_num: int = None):
        if version_num is not None :
            return Versions1(version_num)._child_of(self)

        if version_num is None:
            return Versions2()._child_of(self)

        raise ValueError("Invalid parameters")
