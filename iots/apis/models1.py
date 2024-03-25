from dataclasses import dataclass
from typing import Union, overload

from ..internal.resource import APIResource
from ..models import models, primitives
from .versions import _VersionsMethods


@dataclass
class Models1(APIResource, _VersionsMethods):
    model_name: str

    def get(self, **kwargs) -> Union[models.Model, models.ErrorResponse]:
        """
        Returns a Model.

        :return: The API response to the request.
        :rtype: Union[models.Model, models.ErrorResponse]
        """
        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.Model),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def put(self, req: models.ModelUpdate, **kwargs) -> Union[models.Model, models.ErrorResponse]:
        """
        Updates a Model.

        > 🚧 **Limitations:** A Model cannot be renamed.

        :param req: Request payload.
        :type req: models.ModelUpdate
        :return: The API response to the request.
        :rtype: Union[models.Model, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.ModelUpdate),
        ]

        resp = self._make_request("PUT", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.Model),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (409, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def delete(self, **kwargs) -> primitives.NoResponse:
        """
        Deletes a Model and all its Versions.

        > 🚧 **Limitations:** If a Model is being used by a Category or a Thing,
        > the Model cannot be deleted until all the associations with the Model are removed.

        :return: The API response to the request.
        :rtype: primitives.NoResponse
        """
        resp = self._make_request("DELETE", **kwargs)
        return self._handle_response(resp, [
            (204, "", primitives.NoResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.Forbidden),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return f"/models/{self.model_name}"


@dataclass
class Models2(APIResource):

    def post(self, req: models.ModelCreate, **kwargs) -> Union[models.Model, models.ErrorResponse]:
        """
        Creates a new Model inside a Space.

        > 🚧 **Limitations:** A Model cannot be renamed.

        :param req: Request payload.
        :type req: models.ModelCreate
        :return: The API response to the request.
        :rtype: Union[models.Model, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.ModelCreate),
        ]

        resp = self._make_request("POST", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.Model),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (409, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def get(self, **kwargs) -> Union[models.ModelList, models.ErrorResponse]:
        """
        Returns the list of Models.

        > 🚧 **Limitations:** A maximum of 1000 Models will be returned per
        > page (50 by default).

        Query parameters:
         - `next_cursor` _(str)_: Cursor used to get the next page of results.
         - `previous_cursor` _(str)_: Cursor used to get the previous page of results.
         - `limit` _(int)_: The numbers of items to return.

        :return: The API response to the request.
        :rtype: Union[models.ModelList, models.ErrorResponse]
        """
        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.ModelList),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return "/models"


class _Models1Methods:
    """
    This class declares and implements the `models()` method.
    """

    @overload
    def models(self, model_name: str) -> Models1:
        ...

    @overload
    def models(self) -> Models2:
        ...

    def models(self, model_name: str = None):
        if model_name is not None :
            return Models1(model_name)._child_of(self)

        if model_name is None:
            return Models2()._child_of(self)

        raise ValueError("Invalid parameters")
