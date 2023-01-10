from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from requests import Response


@dataclass
class APIObject(ABC):
    """
    Abstract class to represent a part of an API call.
    This must be inherited by any class implementing an API operation.
    """

    _stack: list = field(default_factory=list, init=False)
    """
    A list used to store the objects generated during a call chain.
    This allows to access all the information needed to make an API request,
    such as building the request URL.

    Items in the stack can be:
    - One (and only one) `API` instance. This must be the first item in the
      stack.
    - A number of `APIObject` building the request.
    """

    @abstractmethod
    def _build_partial_path(self):
        pass

    def _with_stack(self, stack: list):
        self._stack = stack
        return self

    def _child_of(self, obj):
        """
        Sets the stack of this instance to a copy of the given `APIObject`
        stack with the object itself added.
        This method is used when a new `APIObject` instance is created from
        another one.
        """
        from api.api import API
        if isinstance(obj, API):
            self._stack = [obj]
        else:
            self._stack = obj._stack.copy()
            self._stack.append(obj)
        return self

    def build_url(self) -> str:
        """
        Builds and returns the URL using all the stack information.
        The first item in the stack must be an `API` instance, and the rest
        must be `APIObject` instances.
        """
        from api.api import API
        if len(self._stack) == 0 or not isinstance(self._stack[0], API):
            raise Exception("API instance is missing in the stack")

        return self._stack[0].host.rstrip("/") + self.build_path()

    def build_path(self) -> str:
        """
        Builds the URL path using all the `APIObject` instances in the stack.
        """
        path = ""
        for obj in self._stack:
            if isinstance(obj, APIObject):
                path = path + obj._build_partial_path()

        return path + self._build_partial_path()

    def _make_request(self, method="GET", body=None) -> Response:
        from api.api import API
        if len(self._stack) == 0 or not isinstance(self._stack[0], API):
            raise Exception("API instance is missing in the stack")

        api = self._stack[0]
        return api.make_request(method, self.build_path(), body=body)
