from functools import reduce
from typing import Optional, Union

import requests
from pydantic import BaseModel, PrivateAttr, typing

from .pagination import Paginator, _PaginationHelper


class IterBaseModel(BaseModel):
    """
    Extends :class:`pydantic.BaseModel` to allow accessing attributes using
    dot and square-bracket notation, even when the __root__ element is a
    dictionary or a list.
    """

    def __init__(self, **data):
        super().__init__(**data)
        if self._has_root(dict):
            object.__setattr__(self, 'items', self._items)

    def _has_root(self, types):
        return '__root__' in self.__dict__ and isinstance(self.__root__, types)

    def __str__(self):
        if '__root__' in self.__dict__:
            return str(self.__root__)
        else:
            return super().__str__()

    def __repr__(self):
        if '__root__' in self.__dict__:
            return repr(self.__root__)
        else:
            return super().__repr__()

    def __getattr__(self, attribute):
        if self._has_root(dict) and not (attribute.startswith('__') and attribute.endswith('__')):
            return self.__root__[attribute]
        else:
            return super().__getattribute__(attribute)

    def __setattr__(self, attribute, value):
        if self._has_root(dict):
            self.__root__[attribute] = value
        else:
            super().__setattr__(attribute, value)

    def _nested_item(self, key: str, separator='.'):
        try:
            def get_item(a, b):
                if isinstance(a, list):
                    b = int(b)
                return a[b]

            return reduce(get_item, key.split(separator), self)
        except KeyError:
            raise KeyError(f"Key '{key}' not found")
        except IndexError:
            raise IndexError(f"Index '{key}' out of range")

    def __getitem__(self, key):
        # if isinstance(key, str) and '.' in key:
        #     return self._nested_item(key)

        if self._has_root((dict, list)):
            return self.__root__.__getitem__(key)
        else:
            return super().__getattribute__(key)

    def __setitem__(self, key, value):
        if self._has_root((dict, list)):
            return self.__root__.__setitem__(key, value)
        else:
            super().__setattr__(key, value)

    def __delitem__(self, key):
        if self._has_root((dict, list)):
            return self.__root__.__delitem__(key)
        else:
            raise TypeError("Cannot delete an object attribute")

    def __contains__(self, key):
        if self._has_root((dict, list)):
            return self.__root__.__contains__(key)
        else:
            return key in self.__dict__

    def __iter__(self):
        if self._has_root((dict, list)):
            return self.__root__.__iter__()
        else:
            return super().__iter__()

    def __len__(self):
        if self._has_root((dict, list)):
            return len(self.__root__)
        else:
            return len(self.__dict__)

    def dict(
            self,
            *,
            include: Optional[Union['typing.AbstractSetIntStr', 'typing.MappingIntStrAny']] = None,
            exclude: Optional[Union['typing.AbstractSetIntStr', 'typing.MappingIntStrAny']] = None,
            by_alias: bool = False,
            skip_defaults: Optional[bool] = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
    ) -> 'typing.DictStrAny':
        ret = super(IterBaseModel, self).dict(include=include,
                                              exclude=exclude,
                                              by_alias=by_alias,
                                              skip_defaults=skip_defaults,
                                              exclude_unset=exclude_unset,
                                              exclude_defaults=exclude_defaults,
                                              exclude_none=exclude_none)
        if self._has_root((dict, list)):
            return ret['__root__']
        else:
            return ret

    def _items(self):
        if self._has_root(dict):
            return self.__root__.items()
        else:
            return self.__iter__()


class HTTPResponseModel(BaseModel):
    """
    Extends :class:`pydantic.BaseModel` to allow embedding a requests.Response
    instance. The method http_response() returns this instance.
    """
    _http_response: requests.Response = PrivateAttr(None)

    def _set_http_response(self, response):
        object.__setattr__(self, '_http_response', response)

    def http_response(self):
        """
        Returns the HTTP response of this model instance.
        """
        return self._http_response


class PaginatorBaseModel(IterBaseModel, HTTPResponseModel, Paginator):
    """
    This class allows to paginate the results of an API response instance.
    """
    _pagination: _PaginationHelper = PrivateAttr(default_factory=_PaginationHelper)

    def _enable_pagination(self, data_attribute: str):
        self._pagination.supported = True
        self._pagination.results_attribute = data_attribute

    def __iter__(self):
        if self._pagination.supported:
            return Paginator.__iter__(self)
        else:
            return IterBaseModel.__iter__(self)

    def __next__(self):
        if self._pagination.supported:
            self._pagination.results = self[self._pagination.results_attribute]
            return Paginator.__next__(self)
        else:
            return IterBaseModel.__next__(self)


class APIBaseModel(PaginatorBaseModel):
    """
    The Pydantic base model used for API schema models.
    """
    pass
