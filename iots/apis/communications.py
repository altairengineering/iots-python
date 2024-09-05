from dataclasses import dataclass
from typing import overload

from ..internal.resource import APIResource
from .email import _EmailMethods


@dataclass
class Communications1(APIResource, _EmailMethods):

    def _build_partial_path(self):
        return "/communications"


class _CommunicationsMethods:
    """
    This class declares and implements the `communications()` method.
    """

    @overload
    def communications(self) -> Communications1:
        ...

    def communications(self):
        return Communications1()._child_of(self)
