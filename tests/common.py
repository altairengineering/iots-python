import json

from pydantic import BaseModel
from requests import Response


def make_json_response(status_code: int, body=None) -> Response:
    resp = Response()
    resp.status_code = status_code
    resp._content = json.dumps(body).encode('utf-8')
    resp.headers = {'Content-Type': 'application/json'}
    return resp


def to_dict(d) -> dict:
    if isinstance(d, dict):
        return d
    elif isinstance(d, BaseModel):
        return d.dict()
    else:
        raise ValueError("value must be a dict or a pydantic model")
