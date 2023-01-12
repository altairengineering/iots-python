from typing import Optional, Union

from pydantic import BaseModel, typing


class IterBaseModel(BaseModel):
    """
    Extends :class:`pydantic.BaseModel` to allow accessing attributes using
    dot and square-bracket notation, even when the __root__ element is a
    dictionary or a list.
    """

    def _has_root(self, types):
        return '__root__' in self.__dict__ and isinstance(self.__root__, types)

    def __getattr__(self, attribute):
        if self._has_root(dict):
            return self.__root__.get(attribute)
        else:
            return super().__getattribute__(attribute)

    def __setattr__(self, attribute, value):
        if self._has_root(dict):
            self.__root__[attribute] = value
        else:
            super().__setattr__(attribute, value)

    def __getitem__(self, key):
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
        if self._has_root((dict, list)):
            return self.__root__
        return super(IterBaseModel, self).dict(include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none)

    def items(self):
        if self._has_root(dict):
            return self.__root__.items()
        else:
            return self.__iter__()
