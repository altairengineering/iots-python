from dataclasses import dataclass
from typing import Union, overload

from ..internal.resource import APIResource
from ..models import models


@dataclass
class ResetSecret1(APIResource):

    def post(self, **kwargs) -> Union[models.ThingOAuth2Credentials, models.ErrorResponse]:
        """
        Resets the secret of the Thing's OAuth2 client. The client will be
        created if it does not exist yet.

        :return: The API response to the request.
        :rtype: Union[models.ThingOAuth2Credentials, models.ErrorResponse]
        """
        resp = self._make_request("POST", **kwargs)
        return self._handle_response(resp, [
            (201, "application/json", models.ThingOAuth2Credentials),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (404, "application/json", models.ErrorResponse),
            (500, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return "/reset-secret"


class _ResetSecretMethods:
    """
    This class declares and implements the `reset-secret()` method.
    """

    @overload
    def reset_secret(self) -> ResetSecret1:
        ...

    def reset_secret(self):
        return ResetSecret1()._child_of(self)

