import json

import xmltodict

from ..models.basemodel import APIBaseModel


def content_types_match(type1: str, type2: str) -> bool:
    """
    Returns whether the given Content-Types match.
    """
    t1, t2 = type1.lower().split(';')[0], type2.lower().split(';')[0]
    if '*/*' in [t1, t2]:
        return True
    return type1.lower().split(';')[0] == type2.lower().split(';')[0]


def to_json(obj) -> str:
    """
    Returns the JSON representation of the given object.
    Raises an exception if the object cannot be serialized to a valid JSON.
    """
    if isinstance(obj, (str, bytes)):
        json.loads(obj)
        return str(obj)
    elif isinstance(obj, dict):
        return json.dumps(obj)
    elif isinstance(obj, APIBaseModel):
        return obj.json()
    else:
        raise ValueError(f'Value type "{type(obj).__name__}" cannot be converted to JSON')


def to_xml(obj) -> str:
    """
    Returns the XML representation of the given object.
    Raises an exception if the object cannot be serialized to a valid XML.
    """
    if isinstance(obj, (str, bytes)):
        xmltodict.parse(obj)
        return str(obj)
    elif isinstance(obj, dict):
        obj_dict = obj
    elif isinstance(obj, APIBaseModel):
        obj_dict = obj.dict()
    else:
        raise ValueError(f'Value type "{type(obj).__name__}" cannot be converted to XML')

    obj_dict = {'root': obj_dict}
    return xmltodict.unparse(obj_dict)


SUPPORTED_REQUEST_CONTENT_TYPES = {
    'application/json': to_json,
    'application/xml': to_xml,
    'text/plain': str,
}
