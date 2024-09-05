import json
from urllib.parse import parse_qsl

import xmltodict

from ..models.basemodel import APIBaseModel


class ContentType:
    """
    Represents a Content-Type.
    """

    def __init__(self, content_type: str):
        self.content_type = content_type
        components = parse_content_type(content_type)
        self.media_type = components['media_type']
        self.type = components['type']
        self.subtype = components['subtype']
        self.suffix = components['suffix']
        self.parameters = components['parameters']

    def __eq__(self, other):
        return content_types_match(self.content_type, other.content_type)

    def __str__(self):
        return self.content_type

    def __repr__(self):
        return f"ContentType({self.content_type})"


def parse_content_type(content_type):
    """
    Parses a Content-Type into its components.

    :param content_type: The Content-Type to parse.
    :return:  A dictionary with the components of the Content-Type.
    """
    # Split the main type from the parameters
    media_type, *params = content_type.split(';')
    media_type = media_type.strip()

    # Split the base type and the suffix
    base_type, _, suffix = media_type.partition('+')

    # Split the type and subtype
    main_type, _, subtype = base_type.partition('/')

    # Parse parameters into a dictionary
    parameters = {
        key.strip(): value.strip()
        for key, value in parse_qsl(';'.join(params).replace(';', '&'))
    }

    return {
        "media_type": media_type,  # Full media type (e.g., application/json-patch+json)
        "type": main_type,  # Main type (e.g., application)
        "subtype": subtype,  # Subtype (e.g., json-patch)
        "suffix": suffix if suffix else None,  # Suffix (e.g., json), or None if not present
        "parameters": parameters  # Parameters (e.g., {'charset': 'utf-8'})
    }


def content_types_compatible(type1: str, type2: str):
    """
    Checks if two Content-Types are compatible (i.e., if they use the same
    underlying format).
    """
    parsed_type1 = parse_content_type(type1)
    parsed_type2 = parse_content_type(type2)

    if parsed_type1["type"] != parsed_type2["type"]:
        return False

    if '*' in [parsed_type1["subtype"], parsed_type2["subtype"]]:
        return True

    suffix1 = parsed_type1["suffix"] or parsed_type1["subtype"]
    suffix2 = parsed_type2["suffix"] or parsed_type2["subtype"]
    return suffix1 == suffix2


def content_types_match(type1: str, type2: str) -> bool:
    """
    Returns whether the given Content-Types match.
    """
    t1, t2 = type1.lower().split(';')[0], type2.lower().split(';')[0]
    if '*/*' in [t1, t2]:
        return True
    return t1 == t2


def to_json(obj) -> str:
    """
    Returns the JSON representation of the given object.
    Raises an exception if the object cannot be serialized to a valid JSON.
    """
    if isinstance(obj, (str, bytes)):
        json.loads(obj)
        return str(obj)
    elif isinstance(obj, (dict, list)):
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
