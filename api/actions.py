from dataclasses import dataclass, field
from typing import List, overload

from models.anythingdb import ActionResponse, ActionListResponse
from .obj import APIObject


@dataclass
class Action(APIObject):
    name: str

    def get(self) -> ActionResponse:
        """
        Make a request to the server to get the value of the Action.

        :return: A :class:`ActionResponse` dict with the value of the Action.
        """
        return ActionResponse.parse_obj(self._make_request().json())

    def _build_partial_path(self):
        return f"/actions/{self.name}"


@dataclass
class Actions(APIObject):
    actions: List[Action] = field(default_factory=list)

    def get(self) -> ActionListResponse:
        """
        Make a request to the server to list the value of all the Thing
        Actions.

        :return: A :class:`ActionListResponse` dict with the values of all the
            Thing Actions.
        """
        return ActionListResponse.parse_obj(self._make_request().json())

    def _build_partial_path(self):
        return f"/actions"


class _ActionsMethod:
    """
    This class declares and implements the `actions()` method.
    """

    @overload
    def actions(self, action_name: str) -> Action:
        ...

    @overload
    def actions(self) -> Actions:
        ...

    def actions(self, action_name: str = None):
        if action_name is None:
            return Actions()._child_of(self)
        else:
            return Action(action_name)._child_of(self)
