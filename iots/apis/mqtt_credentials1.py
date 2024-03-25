from dataclasses import dataclass
from typing import Union, overload

from ..internal.resource import APIResource
from ..models import models, primitives


@dataclass
class MqttCredentials1(APIResource):

    def post(self, req: models.MQTTThingForm, **kwargs) -> Union[models.MQTTCategoryDocument, models.ErrorResponse]:
        """
        Creates new MQTT credentials for the given Thing.

        :param req: Request payload.
        :type req: models.MQTTThingForm
        :return: The API response to the request.
        :rtype: Union[models.MQTTCategoryDocument, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.MQTTThingForm),
        ]

        resp = self._make_request("POST", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.MQTTCategoryDocument),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
        ])

    def get(self, **kwargs) -> Union[models.MQTTThingDocument, models.ErrorResponse]:
        """
        Returns the MQTT credentials of the given Thing.

        :return: The API response to the request.
        :rtype: Union[models.MQTTThingDocument, models.ErrorResponse]
        """
        resp = self._make_request("GET", **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.MQTTThingDocument),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
        ])

    def put(self, req: models.MQTTCategoryForm, **kwargs) -> Union[models.MQTTThingDocument, models.ErrorResponse]:
        """
        Updates the existing MQTT credentials of the given Thing.

        > 📘 **Information:** Sending an empty request will generate new
        > credentials with a random password.

        :param req: Request payload.
        :type req: models.MQTTCategoryForm
        :return: The API response to the request.
        :rtype: Union[models.MQTTThingDocument, models.ErrorResponse]
        """
        req_content_types = [
            ("application/json", models.MQTTCategoryForm),
        ]

        resp = self._make_request("PUT", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (200, "application/json", models.MQTTThingDocument),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
        ])

    def delete(self, **kwargs) -> primitives.NoResponse:
        """
        Deletes the existing MQTT credentials of the given Thing.

        :return: The API response to the request.
        :rtype: primitives.NoResponse
        """
        resp = self._make_request("DELETE", **kwargs)
        return self._handle_response(resp, [
            (204, "", primitives.NoResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return "/mqtt-credentials"


class _MqttCredentials1Methods:
    """
    This class declares and implements the `mqtt-credentials()` method.
    """

    @overload
    def mqtt_credentials(self) -> MqttCredentials1:
        ...

    def mqtt_credentials(self):
        return MqttCredentials1()._child_of(self)

