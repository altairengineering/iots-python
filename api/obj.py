from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from api.stack import Stack


@dataclass
class APIObject(ABC):
    """
    Abstract class to represent a part of an API call.
    This must be inherited by any class implementing an API operation.
    """
    _stack: Stack = field(default_factory=Stack, init=False)

    @abstractmethod
    def _build_partial_path(self):
        pass

    def _with_stack(self, stack: Stack):
        self._stack = stack
        return self
