from dataclasses import dataclass, field
from typing import List, Union, overload

from .models.anythingdb import Properties as PropertiesModel
from .internal.resource import APIResource


@dataclass
class Property(APIResource):
    name: str

    def get(self) -> PropertiesModel:
        """
        Make a request to the server to get the value of the Property.

        :return: A :class:`PropertiesModel` with the value of the Property.
        """
        return PropertiesModel.parse_obj(self._make_request().json())

    def update(self, value) -> PropertiesModel:
        """
        Make a request to the server to update the value of the Property.

        :param value: The value to set on the Property.
        :return: A :class:`PropertiesModel` with the new value of the
            Property.
        """
        payload = {self.name: value}
        return PropertiesModel.parse_obj(self._make_request("POST", payload).json())

    def _build_partial_path(self):
        return f"/properties/{self.name}"


@dataclass
class Properties(APIResource):

    def get(self) -> PropertiesModel:
        """
        Make a request to the server to list the value of all the Thing
        Properties.

        :return: A :class:`PropertiesModel` with the values of all the
            Thing Properties.
        """
        return PropertiesModel.parse_obj(self._make_request().json())

    def update(self, values: Union[dict, PropertiesModel]) -> PropertiesModel:
        """
        Make a request to the server to update one or multiple Property values.

        :param values: A dictionary with the Property names and values to set.
        :return: A :class:`PropertiesModel` with the new Property values.
        """
        return PropertiesModel.parse_obj(self._make_request("POST", values).json())

    def _build_partial_path(self):
        return "/properties"


class _PropertiesMethod:
    """
    This class declares and implements the `properties()` method.
    """

    @overload
    def properties(self, property_name: str) -> Property:
        ...

    @overload
    def properties(self) -> Properties:
        ...

    def properties(self, property_name: str = None):
        if property_name is None:
            return Properties()._child_of(self)
        else:
            return Property(property_name)._child_of(self)
