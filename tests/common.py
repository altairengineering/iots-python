import json
from typing import Union

from requests.structures import CaseInsensitiveDict
from pydantic import BaseModel
from requests import PreparedRequest, Request, Response


def make_response(status_code: int, body=None, request: Union[PreparedRequest, Request] = None) -> Response:
    resp = Response()
    resp.status_code = status_code
    if isinstance(request, Request):
        request = request.prepare()
    resp.request = request
    if body is not None:
        if isinstance(body, (dict, BaseModel)):
            body = to_dict(body)
            resp._content = json.dumps(body).encode('utf-8')
            resp.headers = CaseInsensitiveDict({'Content-Type': 'application/json'})
        elif isinstance(body, str):
            resp._content = body.encode('utf-8')
            resp.headers = CaseInsensitiveDict({'Content-Type': 'text/plain'})
    return resp


def to_dict(d) -> dict:
    if isinstance(d, dict):
        return d
    elif isinstance(d, BaseModel):
        return json.loads(d.json())
    else:
        raise ValueError("value must be a dict or a pydantic model")


def to_json(d) -> str:
    if isinstance(d, dict):
        return json.dumps(d)
    elif isinstance(d, BaseModel):
        return d.json()
    else:
        raise ValueError("value must be a dict or a pydantic model")
