from dataclasses import dataclass
from typing import Union, overload

from ..internal.resource import APIResource
from ..models import models, primitives


@dataclass
class Email1(APIResource):

    def send(self, req: Union[models.Email, dict], **kwargs) -> primitives.NoResponse:
        """
        Sends a new e-mail to one or more recipients.

        > 🚧 **Limitations:** Including links, styles, images and other potentially dangerous information in the message
        content is not allowed. The message will be sanitized and these items will be removed before the email is sent.

        :param req: Request payload.
        :type req: Union[models.Email, dict]
        :return: The API response to the request.
        :rtype: primitives.NoResponse
        """
        req_content_types = [
            ("application/json", models.Email),
        ]

        resp = self._make_request("POST", req, req_content_types=req_content_types, **kwargs)
        return self._handle_response(resp, [
            (202, "", primitives.NoResponse),
            (400, "application/json", models.ErrorResponse),
            (401, "application/json", models.ErrorResponse),
            (403, "application/json", models.ErrorResponse),
            (413, "application/json", models.ErrorResponse),
        ])

    def _build_partial_path(self):
        return "/email"


class _EmailMethods:
    """
    This class declares and implements the `email()` method.
    """

    @overload
    def email(self) -> Email1:
        ...

    def email(self):
        return Email1()._child_of(self)
