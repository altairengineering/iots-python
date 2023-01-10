from dataclasses import dataclass, field


@dataclass
class Stack:
    """
    A Stack is a list used to store the objects generated during a call chain.
    This allows to access all the information needed to make an API request,
    such as building the request URL.

    Items in the stack can be:
    - One (and only one) `API` instance. This must be the first item in the
      stack.
    - A number of `APIObject` building the request.
    """
    _stack: list = field(default_factory=list)

    def push(self, obj):
        """ Inserts the given object to the end of the stack. """
        self._stack.append(obj)

    def pop(self):
        """ Removes and returns the last item in the stack. """
        return self._stack.pop()

    def build_url(self) -> str:
        """
        Builds and returns the URL using all the stack information.
        The first item must be an `API` instance, and the rest must be
        `APIObject` instances.
        """
        from api.api import API
        if len(self._stack) == 0 or not isinstance(self._stack[0], API):
            raise Exception("API instance is missing in the stack")

        return self._stack[0].host.rstrip("/") + self.build_path()

    def build_path(self) -> str:
        """
        Builds the URL path using all the `APIObject` instances in the stack.
        """
        from .obj import APIObject
        path = ""
        for obj in self._stack:
            if isinstance(obj, APIObject):
                path = path + obj._build_partial_path()

        return path
