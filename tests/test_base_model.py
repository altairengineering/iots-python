from typing import Optional, Dict, Any, List

import pytest

from models.basemodel import IterBaseModel


class AClass(IterBaseModel):
    value: Any


def test_base_model_dict():
    """
    Tests an IterBaseModel with a dict as __root__.
    """

    class DictClass(IterBaseModel):
        __root__: Optional[Dict[str, Any]] = None

    user_info = {
        "name": "Alice",
        "age": 22,
        "info": {
            "favourite_color": "Yellow"
        },
        "lucky_numbers": [1, 2, 3]
    }

    c = DictClass.parse_obj(user_info)

    # dict
    assert c.dict() == user_info
    assert c == user_info

    c2 = DictClass.parse_obj({"foo": AClass(value=123)})
    assert repr(c2.dict()) == repr({"foo": {"value": 123}})

    # contains
    assert "name" in c
    assert "birthdate" not in c

    # get
    assert c.name == "Alice"
    assert c["name"] == "Alice"
    assert c["info"]["favourite_color"] == "Yellow"
    assert c.lucky_numbers[1] == 2
    with pytest.raises(KeyError):
        _ = c["birthdate"]

    # set
    c.name = "Brooklyn"
    assert c.name == "Brooklyn"
    c["name"] = "Chloe"
    assert c.name == "Chloe"

    # len
    assert len(c) == 4

    # delete
    del c["info"]
    assert "info" not in c

    # iter
    res = [k for k in c]
    assert res == ["name", "age", "lucky_numbers"]
    res = [(k, v) for k, v in c.items()]
    assert res == [("name", "Chloe"), ("age", 22), ("lucky_numbers", [1, 2, 3])]


def test_base_model_list():
    """
    Tests an IterBaseModel with a list as __root__.
    """

    class ListClass(IterBaseModel):
        __root__: List[Any]

    c = ListClass.parse_obj([27, 50, 9])

    # dict
    assert c.dict() == [27, 50, 9]
    assert c == [27, 50, 9]

    c2 = ListClass.parse_obj([123, AClass(value=456)])
    assert repr(c2.dict()) == repr([123, {"value": 456}])

    # contains
    assert 50 in c
    assert 1 not in c

    # get
    assert c[2] == 9
    with pytest.raises(IndexError):
        _ = c[3]

    # set
    c[1] = 51
    assert c[1] == 51

    # len
    assert len(c) == 3

    # delete
    del c[1]
    assert c.__root__ == [27, 9]

    # iter
    res = [i for i in c]
    assert res == [27, 9]
    assert not hasattr(c, 'items')


def test_base_model_obj():
    """
    Tests an IterBaseModel with a structured object.
    """

    class ObjClass(IterBaseModel):
        name: str
        age: int
        info: Any = None

    user_info = {
        "name": "Alice",
        "age": 22,
        "info": {
            "favourite_color": "Yellow"
        }
    }

    c = ObjClass.parse_obj(user_info)

    # dict
    assert c.dict() == user_info
    assert c == user_info

    # contains
    assert "name" in c
    assert "birthdate" not in c

    # get
    assert c.name == "Alice"
    assert c["name"] == "Alice"
    assert c["info"]["favourite_color"] == "Yellow"
    with pytest.raises(AttributeError):
        _ = c["birthdate"]

    # set
    c.name = "Brooklyn"
    assert c.name == "Brooklyn"
    c["name"] = "Chloe"
    assert c.name == "Chloe"

    # len
    assert len(c) == 3

    # delete
    with pytest.raises(TypeError):
        del c["name"]

    # iter
    res = [k for k in c]
    assert res == [('name', 'Chloe'), ('age', 22), ('info', {'favourite_color': 'Yellow'})]
    assert not hasattr(c, 'items')
