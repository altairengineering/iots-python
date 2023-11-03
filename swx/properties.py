from dataclasses import dataclass
from typing import Union, overload

from .internal.resource import APIResource
from .models import anythingdb as models


@dataclass
class Property(APIResource):
    name: str

    def get(self, **kwargs) -> models.Properties:
        """
        Make a request to the server to get the value of the Property.

        :return: A :class:`~swx.models.anythingdb.Properties` instance with
                 the value of the Property.
        """
        return models.Properties.parse_obj(self._make_request(**kwargs).json())

    def update(self, value, **kwargs) -> models.Properties:
        """
        Make a request to the server to update the value of the Property.

        :param value: The value to set on the Property.
        :return: A :class:`~swx.models.anythingdb.Properties` instance with
                 the new value of the Property.
        """
        payload = {self.name: value}
        return models.Properties.parse_obj(self._make_request("PUT", payload, **kwargs).json())

    def _build_partial_path(self):
        return f"/properties/{self.name}"


@dataclass
class Properties(APIResource):

    def get(self, **kwargs) -> models.Properties:
        """
        Make a request to the server to list the value of all the Thing
        Properties.

        :return: A :class:`~swx.models.anythingdb.Properties` instance with
                 the values of all the Thing Properties.
        """
        return models.Properties.parse_obj(self._make_request(**kwargs).json())

    def update(self, values: Union[dict, models.Properties], **kwargs) -> models.Properties:
        """
        Make a request to the server to update one or multiple Property values.

        :param values: A dictionary with the Property names and values to set.
        :return:       A :class:`~swx.models.anythingdb.Properties` instance
                       with the new Property values.
        """
        return models.Properties.parse_obj(self._make_request("PUT", values, **kwargs).json())

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
