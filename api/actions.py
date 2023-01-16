from dataclasses import dataclass, field
from typing import List, overload, Union

from models.anythingdb import (ActionCreateRequest, ActionUpdateRequest,
                               ActionResponse, ActionListResponse)
from .obj import APIObject


@dataclass
class Action(APIObject):
    action_name: str

    def create(self, action: Union[ActionCreateRequest, dict]) -> ActionResponse:
        """
        Make a request to the server to create a new Action value.

        :param action: The information of the new Action value
            (e.g. `{"delay": {"input": 5}}`).
        :return: A :class:`ActionResponse` with the new Action value.
        """
        payload = action
        if isinstance(action, ActionCreateRequest):
            payload = action.dict()
        return ActionResponse.parse_obj(self._make_request("POST", payload).json())

    def get(self):
        """
        Make a request to the server to get the history values of the Action.

        :return: A :class:`ActionListResponse` with the value of the Action.
        """
        return ActionListResponse.parse_obj(self._make_request().json())

    def _build_partial_path(self):
        return f"/actions/{self.action_name}"


class ActionUpdateResponse:
    pass


@dataclass
class ActionValue(APIObject):
    action_id: str

    def get(self) -> ActionResponse:
        """
        Make a request to the server to get the value of the Action.

        :return: A :class:`ActionResponse` with the value of the Action.
        """
        return ActionResponse.parse_obj(self._make_request().json())

    def update(self, action: Union[ActionUpdateRequest, dict]) -> ActionResponse:
        """
        Make a request to the server to update the value of the Action.

        :param action: The information of the updated Action value
            (e.g. `{"delay": {"status": "completed"}}`).
        :return: A :class:`ActionResponse` with the returned value of the
            Action.
        """
        payload = action
        if isinstance(action, ActionUpdateRequest):
            payload = action.dict()
        return ActionResponse.parse_obj(self._make_request("PUT", payload).json())

    def delete(self):
        """
        Make a request to the server to delete the Action value.
        """
        ActionResponse.parse_obj(self._make_request("DELETE").json())

    def _build_partial_path(self):
        return "/" + self.action_id


@dataclass
class Actions(APIObject):
    actions: List[Action] = field(default_factory=list)

    def get(self) -> ActionListResponse:
        """
        Make a request to the server to list the value of all the Thing
        Actions.

        :return: A :class:`ActionListResponse` with the values of all the
            Thing Actions.
        """
        return ActionListResponse.parse_obj(self._make_request().json())

    def _build_partial_path(self):
        return "/actions"


class _ActionsMethod:
    """
    This class declares and implements the `actions()` method.
    """

    @overload
    def actions(self, action_name: str, action_id: str) -> ActionValue:
        ...

    @overload
    def actions(self, action_name: str) -> Action:
        ...

    @overload
    def actions(self) -> Actions:
        ...

    def actions(self, action_name: str = None, action_id: str = None):
        if action_name is not None and action_id is not None:
            action = Action(action_name)._child_of(self)
            return ActionValue(action_id)._child_of(action)
        elif action_name is not None:
            return Action(action_name)._child_of(self)
        else:
            return Actions()._child_of(self)
